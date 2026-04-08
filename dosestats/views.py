from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Avg
from django.db.models.functions import TruncMonth
from datetime import timedelta
from django.utils import timezone
from .models import ScanDose, OrganDose, DoseAnomaly, ScanParameter
from patients.models import Alert
from .serializers import ScanDoseSerializer, OrganDoseSerializer, DoseAnomalySerializer, ScanParameterSerializer

class ScanDoseViewSet(viewsets.ModelViewSet):
    queryset = ScanDose.objects.all()
    serializer_class = ScanDoseSerializer

    # Action to get aggregated scan doses for a patient
    @action(detail=False, methods=['get'])
    def by_patient(self, request):
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response({"error": "patient_id is required"}, status=400)
        
        scans = self.queryset.filter(patient_id=patient_id)
        serializer = self.get_serializer(scans, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def average_dlp(self, request):
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response({"error": "patient_id is required"}, status=400)
        
        avg_dlp = self.queryset.filter(patient_id=patient_id).aggregate(Avg('total_dlp'))['total_dlp__avg']
        # Default to 0 if they have no scans yet
        avg_dlp = round(avg_dlp, 2) if avg_dlp else 0.0
        
        return Response({"average_dlp": avg_dlp})

    # Example aggregation (monthly)
    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response({"error": "patient_id is required"}, status=400)
        
        # Get daily cumulative dose for the last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        daily_doses = self.queryset.filter(
            patient_id=patient_id, 
            scan_date__gte=thirty_days_ago
        ).annotate(date=TruncDate('scan_date')).values('date').annotate(daily_total=Sum('total_dlp')).order_by('date')
        
        return Response(daily_doses)

    @action(detail=False, methods=['get'])
    def monthly_heatmap(self, request):
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response({"error": "patient_id required"}, status=400)
        
        # Aggregate total DLP per month for heatmap/bar chart
        monthly_doses = self.queryset.filter(
            patient_id=patient_id
        ).annotate(month=TruncMonth('scan_date')).values('month').annotate(monthly_total=Sum('total_dlp')).order_by('month')
        
        return Response(monthly_doses)

    @action(detail=False, methods=['get'])
    def cumulative_trend(self, request):
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response({"error": "patient_id required"}, status=400)
            
        patient_scans = self.queryset.filter(patient_id=patient_id).order_by('scan_date')
        
        if not patient_scans.exists():
             return Response({
                 "patient_name": "Unknown",
                 "lifetime_total_dlp": 0.0,
                 "trend_data": []
             })
             
        # Get patient name from the first record
        patient_name = patient_scans.first().patient.name
        
        # Calculate total lifetime dose
        lifetime_total = patient_scans.aggregate(Sum('total_dlp'))['total_dlp__sum']
        
        # Format trend data
        trend_data = [
            {
                "scan_date": scan.scan_date,
                "total_dlp": scan.total_dlp
            } for scan in patient_scans
        ]
        
        return Response({
            "patient_name": f"Patient: {patient_name}",
            "lifetime_total_dlp": round(lifetime_total, 2) if lifetime_total else 0.0,
            "trend_data": trend_data
        })

    @action(detail=False, methods=['get'])
    def latest_organ_doses(self, request):
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response({"error": "patient_id required"}, status=400)
            
        latest_scan = self.queryset.filter(patient_id=patient_id).order_by('-scan_date').first()
        
        if not latest_scan:
            return Response({
                "patient_name": "Unknown",
                "ai_prediction_status": "No scans found",
                "doses": {
                    "Head": 0.0, "Chest": 0.0, "Pelvis": 0.0,
                    "Abdomen": 0.0, "Legs": 0.0, "Arms": 0.0
                }
            })
            
        patient_name = latest_scan.patient.name
        
        # Build dictionary of all associated organ doses
        organ_doses = latest_scan.organ_doses.all()
        doses_dict = {
            "Head": 0.0, "Chest": 0.0, "Pelvis": 0.0,
            "Abdomen": 0.0, "Legs": 0.0, "Arms": 0.0
        }
        
        for organ in organ_doses:
             # Just map to existing keys if available, else add it
             doses_dict[organ.organ_name] = round(organ.dose_value, 2)
             
        return Response({
             "patient_name": f"Patient: {patient_name}",
             "ai_prediction_status": "Processing complete",
             "doses": doses_dict
        })

    @action(detail=False, methods=['post'])
    def predict_dose(self, request):
        data = request.data
        
        # Extract parameters 
        body_part = data.get('body_part', 'Unknown')
        
        try:
            age = int(data.get('age', 0))
            weight = float(data.get('weight', 0.0))
            kvp = int(data.get('kvp', 120))
            mas = int(data.get('mas', 250))
        except ValueError:
            return Response({"error": "Invalid numeric parameters provided."}, status=400)
            
        # --- Simulated AI Logic ---
        # Base DLP depends heavily on body part and mAs
        base_dlp_factor = 1.0
        if "head" in body_part.lower():
            base_dlp_factor = 2.5
        elif "abdomen" in body_part.lower() or "pelvis" in body_part.lower():
            base_dlp_factor = 4.0
        elif "chest" in body_part.lower():
            base_dlp_factor = 3.0
            
        # Simplified physics approximation: Dose ~ kVp^2 * mAs
        kvp_ratio = (kvp / 120.0) ** 2
        mas_ratio = mas / 100.0
        
        predicted_dlp = 100 * base_dlp_factor * kvp_ratio * mas_ratio
        
        # Effective dose estimation (roughly DLP * conversion factor k)
        # Using a generalized k factor for simplicity
        k_factor = 0.015
        effective_dose = predicted_dlp * k_factor
        
        # Risk thresholds
        if effective_dose > 15.0:
            risk_status = "HIGH RISK"
            protocol_tip = "Dose is significantly high. Consider drastically reducing mAs or evaluating alternative imaging modalities."
        elif effective_dose > 8.0:
            risk_status = "MODERATE RISK"
            protocol_tip = "Dose is elevated. Suggest optimizing kVp and utilizing automatic exposure control."
        else:
            risk_status = "LOW RISK"
            protocol_tip = "Parameters are optimal for this patient profile and diagnostic requirement."
            
        return Response({
            "risk_status": risk_status,
            "predicted_dlp": round(predicted_dlp, 1),
            "effective_dose": round(effective_dose, 1),
            "protocol_tip": protocol_tip
        })

    @action(detail=False, methods=['get'])
    def daily_trend(self, request):
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response({"success": False, "error": "patient_id required"}, status=400)
        
        # Last 7 days daily total
        seven_days_ago = timezone.now() - timedelta(days=7)
        from django.db.models.functions import TruncDate
        daily_doses = self.queryset.filter(
            patient__patient_id=patient_id, 
            scan_date__gte=seven_days_ago
        ).annotate(date=TruncDate('scan_date')).values('date').annotate(daily_total=Sum('total_dlp')).order_by('date')
        
        return Response({"success": True, "data": daily_doses})

    @action(detail=False, methods=['get'])
    def monthly_trend(self, request):
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response({"success": False, "error": "patient_id required"}, status=400)
        
        # Last 6 months
        six_months_ago = timezone.now() - timedelta(days=180)
        from django.db.models.functions import TruncMonth
        monthly_doses = self.queryset.filter(
            patient__patient_id=patient_id,
            scan_date__gte=six_months_ago
        ).annotate(month=TruncMonth('scan_date')).values('month').annotate(monthly_total=Sum('total_dlp')).order_by('month')
        
        return Response({"success": True, "data": monthly_doses})

    @action(detail=False, methods=['get'])
    def dose_statistics(self, request):
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response({"success": False, "error": "patient_id required"}, status=400)
            
        stats = self.queryset.filter(patient__patient_id=patient_id).aggregate(
            average=Avg('total_dlp'),
            high=models.Max('total_dlp'),
            low=models.Min('total_dlp')
        )
        
        return Response({
            "success": True, 
            "data": {
                "average": round(stats['average'] or 0, 2),
                "high": round(stats['high'] or 0, 2),
                "low": round(stats['low'] or 0, 2)
            }
        })

    @action(detail=False, methods=['post'])
    def detect_anomalies(self, request):
        patient_id = request.data.get('patient_id')
        if not patient_id:
            return Response({"success": False, "error": "patient_id required"}, status=400)
        
        # Logic to identify abnormal parameters (highly simplified)
        from patients.models import Patient
        try:
            patient = Patient.objects.get(patient_id=patient_id)
        except Patient.DoesNotExist:
            return Response({"success": False, "error": "Patient not found"}, status=404)

        anomalies = []
        recent_scans = ScanDose.objects.filter(patient=patient).order_by('-scan_date')[:5]
        for scan in recent_scans:
            if scan.total_dlp > 1000: # Threshold for anomaly
                anomaly, created = DoseAnomaly.objects.get_or_create(
                    patient=patient,
                    anomaly_id=f"PX-{scan.id}",
                    defaults={
                        "area": scan.study_description,
                        "description": "Unusually high Dose Length Product detected.",
                        "dlp_value": scan.total_dlp,
                        "status_level": "CRITICAL"
                    }
                )
                anomalies.append(DoseAnomalySerializer(anomaly).data)
        
        return Response({"success": True, "anomalies": anomalies})

class OrganDoseViewSet(viewsets.ModelViewSet):
    queryset = OrganDose.objects.all()
    serializer_class = OrganDoseSerializer

class DoseAnomalyViewSet(viewsets.ModelViewSet):
    queryset = DoseAnomaly.objects.all()
    serializer_class = DoseAnomalySerializer
    
    def get_queryset(self):
        queryset = DoseAnomaly.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        if patient_id is not None:
            queryset = queryset.filter(patient__patient_id=patient_id)
        return queryset

class DashboardViewSet(viewsets.ViewSet):
    def list(self, request):
        today = timezone.now().date()
        total_scans_today = ScanDose.objects.filter(scan_date__date=today).count()
        active_alerts_count = Alert.objects.filter(is_active=True).count()
        anomalies_today = DoseAnomaly.objects.filter(detected_at__date=today).count()
        compliance_rate = max(0, 100 - (anomalies_today * 5))
        
        return Response({
            "success": True,
            "data": {
                "total_scans_today": total_scans_today,
                "active_alerts_count": active_alerts_count,
                "safety_compliance_percentage": compliance_rate
            }
        })

class ScanParameterViewSet(viewsets.ModelViewSet):
    queryset = ScanParameter.objects.all()
    serializer_class = ScanParameterSerializer
