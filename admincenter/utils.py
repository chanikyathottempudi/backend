from .models import SystemLog

def log_audit_activity(level, message, source, user=None):
    """
    Utility function to log system and audit activities.
    """
    SystemLog.objects.create(
        level=level,
        message=message,
        source=source,
        user=user
    )
    print(f"AUDIT LOG [{level}] {source}: {message}")
