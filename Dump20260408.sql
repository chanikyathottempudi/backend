-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: sample
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admincenter_compliancereport`
--

DROP TABLE IF EXISTS `admincenter_compliancereport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admincenter_compliancereport` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `generated_date` datetime(6) NOT NULL,
  `report_type` varchar(100) NOT NULL,
  `file` varchar(100) DEFAULT NULL,
  `generated_by_id` int DEFAULT NULL,
  `description` longtext,
  `title` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `admincenter_complian_generated_by_id_b6c90e7d_fk_auth_user` (`generated_by_id`),
  CONSTRAINT `admincenter_complian_generated_by_id_b6c90e7d_fk_auth_user` FOREIGN KEY (`generated_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admincenter_compliancereport`
--

LOCK TABLES `admincenter_compliancereport` WRITE;
/*!40000 ALTER TABLE `admincenter_compliancereport` DISABLE KEYS */;
/*!40000 ALTER TABLE `admincenter_compliancereport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admincenter_machine`
--

DROP TABLE IF EXISTS `admincenter_machine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admincenter_machine` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `model_number` varchar(100) NOT NULL,
  `ip_address` char(39) DEFAULT NULL,
  `status` varchar(50) NOT NULL,
  `last_calibration_date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admincenter_machine`
--

LOCK TABLES `admincenter_machine` WRITE;
/*!40000 ALTER TABLE `admincenter_machine` DISABLE KEYS */;
/*!40000 ALTER TABLE `admincenter_machine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admincenter_onboardingslide`
--

DROP TABLE IF EXISTS `admincenter_onboardingslide`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admincenter_onboardingslide` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `slide_number` int NOT NULL,
  `title` varchar(200) NOT NULL,
  `description_1` varchar(500) DEFAULT NULL,
  `description_2` varchar(500) DEFAULT NULL,
  `description_3` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slide_number` (`slide_number`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admincenter_onboardingslide`
--

LOCK TABLES `admincenter_onboardingslide` WRITE;
/*!40000 ALTER TABLE `admincenter_onboardingslide` DISABLE KEYS */;
INSERT INTO `admincenter_onboardingslide` VALUES (1,2,'Welcome to DoseStats','Empowering healthcare teams with real-time radiation dose tracking.','Enhancing patient safety through automated DRL alerts.','Optimizing clinical workflows with AI-driven insights.');
/*!40000 ALTER TABLE `admincenter_onboardingslide` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admincenter_securitysettings`
--

DROP TABLE IF EXISTS `admincenter_securitysettings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admincenter_securitysettings` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `biometric_login` tinyint(1) NOT NULL,
  `data_encryption` tinyint(1) NOT NULL,
  `automatic_logout` tinyint(1) NOT NULL,
  `hipaa_compliance` tinyint(1) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `admincenter_securitysettings_user_id_49c7bf33_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admincenter_securitysettings`
--

LOCK TABLES `admincenter_securitysettings` WRITE;
/*!40000 ALTER TABLE `admincenter_securitysettings` DISABLE KEYS */;
INSERT INTO `admincenter_securitysettings` VALUES (1,0,1,1,1,5),(7,0,1,1,1,11),(8,0,1,1,1,12),(9,0,1,1,1,13),(13,0,1,1,1,17),(16,0,1,1,1,20),(18,0,1,1,1,22),(19,0,1,1,1,23),(24,0,1,1,1,28),(26,0,1,1,1,30),(27,0,1,1,1,31),(28,0,1,1,1,32),(29,0,1,1,1,33),(35,0,1,1,1,41),(36,0,1,1,1,42),(45,0,1,1,1,51),(46,0,1,1,1,52),(47,0,1,1,1,53),(48,0,1,1,1,54),(49,0,1,1,1,55),(50,0,1,1,1,56),(51,0,1,1,1,57),(52,0,1,1,1,58),(53,0,1,1,1,59);
/*!40000 ALTER TABLE `admincenter_securitysettings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admincenter_systemlog`
--

DROP TABLE IF EXISTS `admincenter_systemlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admincenter_systemlog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `timestamp` datetime(6) NOT NULL,
  `level` varchar(20) NOT NULL,
  `message` longtext NOT NULL,
  `source` varchar(100) NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admincenter_systemlog_user_id_ad5e9030_fk_auth_user_id` (`user_id`),
  CONSTRAINT `admincenter_systemlog_user_id_ad5e9030_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admincenter_systemlog`
--

LOCK TABLES `admincenter_systemlog` WRITE;
/*!40000 ALTER TABLE `admincenter_systemlog` DISABLE KEYS */;
INSERT INTO `admincenter_systemlog` VALUES (5,'2026-03-10 07:47:26.178854','INFO','Log message 0','Auth',12),(6,'2026-03-10 07:47:26.182574','INFO','Log message 1','Auth',12),(7,'2026-03-10 07:47:26.186734','INFO','Log message 2','Auth',12),(8,'2026-03-10 07:47:26.189773','INFO','Log message 3','Auth',12),(9,'2026-03-10 07:47:26.193117','INFO','Log message 4','Auth',12),(10,'2026-03-10 07:47:26.196887','INFO','Log message 5','Auth',12),(11,'2026-03-10 07:47:26.200902','INFO','Log message 6','Auth',12),(12,'2026-03-10 07:47:26.204454','INFO','Log message 7','Auth',12),(13,'2026-03-10 07:47:26.208020','INFO','Log message 8','Auth',12),(14,'2026-03-10 07:47:26.211659','INFO','Log message 9','Auth',12),(15,'2026-03-10 07:47:26.214946','INFO','Log message 10','Auth',13),(16,'2026-03-10 07:47:26.217679','INFO','Log message 11','Auth',13),(17,'2026-03-10 07:47:26.220947','INFO','Log message 12','Auth',13),(18,'2026-03-10 07:47:26.224971','INFO','Log message 13','Auth',13),(19,'2026-03-10 07:47:26.228529','INFO','Log message 14','Auth',13),(20,'2026-03-16 06:39:34.634748','INFO','Self-signup successful: 1234567','Auth',NULL),(21,'2026-03-16 06:39:35.415394','INFO','Self-signup successful: james.wilson@hospital.com','Auth',NULL),(22,'2026-03-16 06:40:27.369729','INFO','Self-signup successful: 1234567','Auth',NULL),(23,'2026-03-16 06:40:28.197443','INFO','Self-signup successful: james.wilson@hospital.com','Auth',NULL),(24,'2026-03-16 06:40:39.651653','INFO','Self-signup successful: 1234567','Auth',NULL),(25,'2026-03-16 06:41:19.294702','INFO','Self-signup successful: 1234567','Auth',NULL),(26,'2026-03-16 06:41:20.035744','INFO','Self-signup successful: james.wilson@hospital.com','Auth',NULL),(27,'2026-03-16 06:43:24.012848','INFO','Self-signup successful: james.wilson@hospital.com','Auth',NULL),(28,'2026-03-16 07:37:25.457420','INFO','Self-signup successful: chanikya123@gmail.com','Auth',51),(29,'2026-03-16 07:40:46.455542','INFO','Self-signup successful: mani123@gmail.com','Auth',52),(30,'2026-03-17 07:36:30.618382','INFO','Self-signup successful: LV4e4279','Auth',53),(31,'2026-03-17 07:46:18.206968','INFO','Self-signup successful: brahama123@gmail.com','Auth',54),(32,'2026-03-26 06:34:02.861669','INFO','Self-signup successful: 1@gmail.com','Auth',55),(33,'2026-03-26 06:50:44.537120','INFO','Self-signup successful: ravi123@gmail.com','Auth',56),(34,'2026-03-26 06:55:32.207379','INFO','Self-signup successful: 11@gmail.com','Auth',57),(35,'2026-03-26 07:48:44.866710','INFO','Self-signup successful: srinu123@gmail.com','Auth',58),(36,'2026-03-26 08:08:05.695820','INFO','Self-signup successful: chanikyathottempudi9999@gmail.com','Auth',59);
/*!40000 ALTER TABLE `admincenter_systemlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admincenter_userprofile`
--

DROP TABLE IF EXISTS `admincenter_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admincenter_userprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `employee_id` varchar(50) NOT NULL,
  `role` varchar(100) NOT NULL,
  `profile_picture` varchar(100) DEFAULT NULL,
  `user_id` int NOT NULL,
  `permissions_summary` longtext,
  `phone_number` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `employee_id` (`employee_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `admincenter_userprofile_user_id_d864f0b8_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admincenter_userprofile`
--

LOCK TABLES `admincenter_userprofile` WRITE;
/*!40000 ALTER TABLE `admincenter_userprofile` DISABLE KEYS */;
INSERT INTO `admincenter_userprofile` VALUES (10,'LVdb8a52','CT Technician','',31,NULL,NULL),(11,'88888','Hospital Admin','',32,NULL,NULL),(12,'12345678','Hospital Admin','',33,NULL,NULL),(18,'DUP123','Radiologist','',41,NULL,NULL),(19,'FAIL999','Radiologist','',42,NULL,NULL),(28,'chanikya123','Hospital Admin','',51,NULL,NULL),(29,'mani123@gmail.com','CT Technician','',52,NULL,NULL),(30,'LV4e4279','CT Technician','',53,NULL,NULL),(31,'brahama123@gmail.com','CT Technician','',54,NULL,NULL),(32,'1@gmail.com','Radiologist','',55,NULL,NULL),(33,'ravi123@gmail.com','Hospital Admin','',56,NULL,NULL),(34,'11@gmail.com','Hospital Admin','',57,NULL,NULL),(35,'srinu123@gmail.com','Hospital Admin','',58,NULL,NULL),(36,'chanikyathottempudi9999@gmail.com','Hospital Admin','',59,NULL,NULL);
/*!40000 ALTER TABLE `admincenter_userprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admincenter_verificationcode`
--

DROP TABLE IF EXISTS `admincenter_verificationcode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admincenter_verificationcode` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `admincenter_verificationcode_user_id_a97a893b_fk_auth_user_id` (`user_id`),
  CONSTRAINT `admincenter_verificationcode_user_id_a97a893b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admincenter_verificationcode`
--

LOCK TABLES `admincenter_verificationcode` WRITE;
/*!40000 ALTER TABLE `admincenter_verificationcode` DISABLE KEYS */;
INSERT INTO `admincenter_verificationcode` VALUES (2,'040776','2026-03-10 08:03:06.150875',1,22),(3,'678103','2026-03-26 08:21:24.595953',0,59),(4,'062416','2026-03-26 08:23:11.609394',0,59),(5,'292390','2026-03-26 08:29:21.229720',0,59),(6,'014849','2026-03-26 08:34:28.356803',0,59);
/*!40000 ALTER TABLE `admincenter_verificationcode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `airisk_patientriskassessment`
--

DROP TABLE IF EXISTS `airisk_patientriskassessment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `airisk_patientriskassessment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `last_updated` datetime(6) NOT NULL,
  `confidence_level` varchar(50) NOT NULL,
  `high_risk_value` int NOT NULL,
  `high_risk_desc` varchar(200) NOT NULL,
  `pediatric_risk_value` int NOT NULL,
  `pediatric_risk_desc` varchar(200) NOT NULL,
  `protocol_deviations_value` int NOT NULL,
  `protocol_deviations_desc` varchar(200) NOT NULL,
  `patient_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `patient_id` (`patient_id`),
  CONSTRAINT `airisk_patientriskas_patient_id_f698bb03_fk_patients_` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `airisk_patientriskassessment`
--

LOCK TABLES `airisk_patientriskassessment` WRITE;
/*!40000 ALTER TABLE `airisk_patientriskassessment` DISABLE KEYS */;
INSERT INTO `airisk_patientriskassessment` VALUES (1,'2026-04-01 05:25:57.713955','High',11,'OPTIMAL STATUS (11): Minimal radiation footprint. Patient below reference thresholds.',15,'Standard adult baseline. Monitoring for cumulative exposure.',11,'AI verified machine settings at 89% alignment with Reference Levels (PRL/DRL).',37),(2,'2026-04-01 09:20:11.264961','High',19,'OPTIMAL STATUS (19): Minimal radiation footprint. Patient below reference thresholds.',24,'Standard adult baseline. Monitoring for cumulative exposure.',11,'AI verified machine settings at 89% alignment with Reference Levels (PRL/DRL).',38),(3,'2026-04-01 05:26:07.906216','High',12,'OPTIMAL STATUS (12): Minimal radiation footprint. Patient below reference thresholds.',17,'Standard adult baseline. Monitoring for cumulative exposure.',4,'AI verified machine settings at 96% alignment with Reference Levels (PRL/DRL).',39),(4,'2026-04-01 05:26:19.128181','High',21,'OPTIMAL STATUS (21): Minimal radiation footprint. Patient below reference thresholds.',16,'Standard adult baseline. Monitoring for cumulative exposure.',3,'AI verified machine settings at 97% alignment with Reference Levels (PRL/DRL).',53);
/*!40000 ALTER TABLE `airisk_patientriskassessment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add patient',8,'add_patient'),(26,'Can change patient',8,'change_patient'),(27,'Can delete patient',8,'delete_patient'),(28,'Can view patient',8,'view_patient'),(29,'Can add daily dose',7,'add_dailydose'),(30,'Can change daily dose',7,'change_dailydose'),(31,'Can delete daily dose',7,'delete_dailydose'),(32,'Can view daily dose',7,'view_dailydose'),(33,'Can add dicom scan',9,'add_dicomscan'),(34,'Can change dicom scan',9,'change_dicomscan'),(35,'Can delete dicom scan',9,'delete_dicomscan'),(36,'Can view dicom scan',9,'view_dicomscan'),(37,'Can add scan dose',11,'add_scandose'),(38,'Can change scan dose',11,'change_scandose'),(39,'Can delete scan dose',11,'delete_scandose'),(40,'Can view scan dose',11,'view_scandose'),(41,'Can add organ dose',10,'add_organdose'),(42,'Can change organ dose',10,'change_organdose'),(43,'Can delete organ dose',10,'delete_organdose'),(44,'Can view organ dose',10,'view_organdose'),(45,'Can add real time dose',12,'add_realtimedose'),(46,'Can change real time dose',12,'change_realtimedose'),(47,'Can delete real time dose',12,'delete_realtimedose'),(48,'Can view real time dose',12,'view_realtimedose'),(49,'Can add machine',14,'add_machine'),(50,'Can change machine',14,'change_machine'),(51,'Can delete machine',14,'delete_machine'),(52,'Can view machine',14,'view_machine'),(53,'Can add system log',15,'add_systemlog'),(54,'Can change system log',15,'change_systemlog'),(55,'Can delete system log',15,'delete_systemlog'),(56,'Can view system log',15,'view_systemlog'),(57,'Can add compliance report',13,'add_compliancereport'),(58,'Can change compliance report',13,'change_compliancereport'),(59,'Can delete compliance report',13,'delete_compliancereport'),(60,'Can view compliance report',13,'view_compliancereport'),(61,'Can add patient risk assessment',16,'add_patientriskassessment'),(62,'Can change patient risk assessment',16,'change_patientriskassessment'),(63,'Can delete patient risk assessment',16,'delete_patientriskassessment'),(64,'Can view patient risk assessment',16,'view_patientriskassessment'),(65,'Can add alert',17,'add_alert'),(66,'Can change alert',17,'change_alert'),(67,'Can delete alert',17,'delete_alert'),(68,'Can view alert',17,'view_alert'),(69,'Can add dose anomaly',18,'add_doseanomaly'),(70,'Can change dose anomaly',18,'change_doseanomaly'),(71,'Can delete dose anomaly',18,'delete_doseanomaly'),(72,'Can view dose anomaly',18,'view_doseanomaly'),(73,'Can add scan registration',19,'add_scanregistration'),(74,'Can change scan registration',19,'change_scanregistration'),(75,'Can delete scan registration',19,'delete_scanregistration'),(76,'Can view scan registration',19,'view_scanregistration'),(77,'Can add user profile',20,'add_userprofile'),(78,'Can change user profile',20,'change_userprofile'),(79,'Can delete user profile',20,'delete_userprofile'),(80,'Can view user profile',20,'view_userprofile'),(81,'Can add scan parameter',21,'add_scanparameter'),(82,'Can change scan parameter',21,'change_scanparameter'),(83,'Can delete scan parameter',21,'delete_scanparameter'),(84,'Can view scan parameter',21,'view_scanparameter'),(85,'Can add onboarding slide',22,'add_onboardingslide'),(86,'Can change onboarding slide',22,'change_onboardingslide'),(87,'Can delete onboarding slide',22,'delete_onboardingslide'),(88,'Can view onboarding slide',22,'view_onboardingslide'),(89,'Can add security settings',23,'add_securitysettings'),(90,'Can change security settings',23,'change_securitysettings'),(91,'Can delete security settings',23,'delete_securitysettings'),(92,'Can view security settings',23,'view_securitysettings'),(93,'Can add verification code',24,'add_verificationcode'),(94,'Can change verification code',24,'change_verificationcode'),(95,'Can delete verification code',24,'delete_verificationcode'),(96,'Can view verification code',24,'view_verificationcode');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (3,'pbkdf2_sha256$1200000$cHjhl80mkNrCQ2f2yXg84k$Kg8hAIprt/3xqk1BRyWPB4JUSUQ0FcUX8WenKsUOLQQ=',NULL,0,'asmith','Alice','Smith','asmith@example.com',0,1,'2026-03-10 04:05:38.585268'),(5,'pbkdf2_sha256$1200000$BWc73ulFYsE3wWA6J1mZol$+gfZZNeeEyyEwlpvY6+1exekeO7R8dS/L1w2Pu5y2zU=','2026-03-10 07:18:33.320070',0,'sec_test_user','','','',0,1,'2026-03-10 07:18:32.191273'),(11,'pbkdf2_sha256$1200000$POAoyXLnuNhTXwbB6JoiKh$tG/quZtt6SjtCbi55IP/d6OGRYi4Mg1fzTvn58ifCsA=',NULL,0,'reset_test_user','','','reset@test.com',0,1,'2026-03-10 07:41:33.139768'),(12,'pbkdf2_sha256$1200000$Wq0oOr5xBZHQsbBxhZbD0o$02HxgqQB4xjATgJsUgjanpXNAahPichZKjDg2SNMyh8=',NULL,0,'testloguser1','','','',0,1,'2026-03-10 07:47:24.224401'),(13,'pbkdf2_sha256$1200000$sosCZPA6QxmSDIXpD1wSPY$iDahjUiiJvxuecHSTxEgQqj2GM3Lkz2ozGePYBNTsa0=',NULL,0,'testloguser2','','','',0,1,'2026-03-10 07:47:25.235562'),(17,'pbkdf2_sha256$1200000$0thlS1PrpG0ey8H5L48G48$OOSUguABhQW+6A0oFzl7l8g3vgFgaU66O+Ta1b6CloA=',NULL,0,'detail_test_user','John','Doe','details@hospital.com',0,1,'2026-03-10 07:54:41.011722'),(20,'pbkdf2_sha256$1200000$91R0drUUdQuoxJzehGA0FR$ZPcOOjOYPOH328FpgxWOHS1s9UfmBfRjJhYFPNeO4y4=',NULL,0,'mgt_test_user1','Aris','Thorne','',0,1,'2026-03-10 07:58:21.922682'),(22,'pbkdf2_sha256$1200000$4ulCmezE1rihBZEV7OQ5na$Gjo9AvgP94Q7o4U5zU9JpU5J5BkANOogNBtNUS6QSlY=',NULL,0,'verify_test_user','','','verify@hospital.com',0,1,'2026-03-10 08:03:05.043646'),(23,'pbkdf2_sha256$1200000$o3VBr7ClAt1XC44a7t5MN1$FRTOtK8JUKhYD1rgeVH8zeqCsY/Nnrg3w+zE8/auqZ8=',NULL,0,'testuser','','','test@gmail.com',0,1,'2026-03-10 08:42:03.433661'),(28,'pbkdf2_sha256$1200000$97q4qdS0EC8fDRBIYgOxm5$l8WIP0YrHxjJFrl8SCAyW15taJq8cb8vEueDkfAcuP8=',NULL,0,'debug_user_879b0946','','','',0,1,'2026-03-11 03:30:52.102175'),(30,'pbkdf2_sha256$1200000$p5k2KOo9x6moDYPzg87ceG$0FaG82asYx0rXlDV12W2DDMHWISedZsYp4/W46ICCvg=',NULL,0,'debug_user_d16b4322','','','',0,1,'2026-03-11 03:40:01.611748'),(31,'pbkdf2_sha256$1200000$cRP3qniJxg9czI8UOEs8Ln$4wqo4vrbyjVmZHoe/gc/GMWNvGBPaiWnkjYVKLlLGvo=',NULL,0,'LVdb8a52','Dynamic','User','test_f6ae@hospital.com',0,1,'2026-03-11 04:09:38.377650'),(32,'pbkdf2_sha256$1200000$sLVay4aqF9KwE7Y6nNNyy6$hEYo05G51S2NBrvTBA0/sLfgZ83Y1LLZeTTxKLHbQ2A=',NULL,0,'88888','Secure','Admin','admin@hospital.com',0,1,'2026-03-11 05:21:24.913305'),(33,'pbkdf2_sha256$1200000$sLWklxc11BQ021iJLf7VVC$cgp5QDg5DCJo1MBxYmQdMVfpYyjiCGlaDjvDceJEpEE=',NULL,0,'12345678','chani','','chanikyathottempudi@gmail.com',0,1,'2026-03-11 06:07:07.205338'),(41,'pbkdf2_sha256$1200000$jMPwhUxpnJZxW6E4Rl0xON$t341DHnS9fTzMmCXE/NtsodaJtpGF2kyWRDLROXmz0g=',NULL,0,'DUP123','Duplicate','Test','duplicate@hospital.com',0,1,'2026-03-12 07:03:17.094622'),(42,'pbkdf2_sha256$1200000$SRfXwFj5owpjSfiKWInxce$P4NTT5ShphTJw8ZdXBqXQbtlxBLwQO6OuAYzOcUiArk=',NULL,0,'FAIL999','Test','Failure','test.failure@hospital.com',0,1,'2026-03-12 07:03:20.621102'),(51,'pbkdf2_sha256$1200000$YjoVLVHjWJTB9TIPtmC7CT$+6ZJgmAE8j7m9GsTF2ikXjzIDys9d1/oLMWqxGxCq18=',NULL,0,'chanikya123@gmail.com','chanikya','','chanikya123@gmail.com',0,1,'2026-03-16 07:37:23.290102'),(52,'pbkdf2_sha256$1200000$x0wVjtsIAuagcsYY4fciqn$XLkEhdavJkh5fyg1N5wcSO6bZqvXa3leVezsChC5vzE=',NULL,0,'mani123@gmail.com','manidhar','','mani123@gmail.com',0,1,'2026-03-16 07:40:44.365343'),(53,'pbkdf2_sha256$1200000$xk3RvT2uNT2Ka9KLiZMTXh$LKRRIfF1e3YEf/6eOzlz/m9rqUhETXjDNgOcXe4nVzE=',NULL,0,'LV4e4279','Dynamic','User','test_9d13@hospital.com',0,1,'2026-03-17 07:36:30.008187'),(54,'pbkdf2_sha256$1200000$uoWUdrOAMy0TR1bfnHGA4u$//P/sWRQqmfNLzZYWJNpo+a7WkG7tbxohuKhLYmuQSY=',NULL,0,'brahama123@gmail.com','brahamareddy','','brahama123@gmail.com',0,1,'2026-03-17 07:46:16.374397'),(55,'pbkdf2_sha256$1200000$oQ2Elkb8XnFHQnoVoMp6na$Pcc3bnSpShBCs2DC1+j7SYBAT4DnD572EAtTEcO1gaM=',NULL,0,'1@gmail.com','1','','1@gmail.com',0,1,'2026-03-26 06:34:01.416726'),(56,'pbkdf2_sha256$1200000$HNA9Zpn6yQsXt8OnxzJaa7$izGimZUy9fqsPsgFoEapQAd62dlkBJTGnOy+hK7GBMM=',NULL,0,'ravi123@gmail.com','ravi','','ravi123@gmail.com',0,1,'2026-03-26 06:50:43.268897'),(57,'pbkdf2_sha256$1200000$9sFjhNQ7JjYQ1mXKA8FMll$uoWa8V8JB6Kef+AXTMf/mNxbT82rMkG0XPasxSWhxuk=',NULL,0,'11@gmail.com','11','','11@gmail.com',0,1,'2026-03-26 06:55:30.816859'),(58,'pbkdf2_sha256$1200000$apDwWr6mYXkWamIIFJ9DmA$2vF+yncxDr65XovmbRZM+rlEnkYxmG9vRaGcyxrLPHY=',NULL,0,'srinu123@gmail.com','srinu','','srinu123@gmail.com',0,1,'2026-03-26 07:48:43.547637'),(59,'pbkdf2_sha256$1200000$4gZb4hTtfoMwdr7j2sVMpP$FULASFExiT1WaBxUaiNRlAEoQkwm0RT+OmewZQJUF4E=',NULL,0,'chanikyathottempudi9999@gmail.com','chanikya','','chanikyathottempudi9999@gmail.com',0,1,'2026-03-26 08:08:04.366369');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dicom_dicomscan`
--

DROP TABLE IF EXISTS `dicom_dicomscan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dicom_dicomscan` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `file` varchar(100) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `status` varchar(50) NOT NULL,
  `patient_id` bigint DEFAULT NULL,
  `modality` varchar(50) DEFAULT NULL,
  `protocol_name` varchar(200) DEFAULT NULL,
  `series_instance_uid` varchar(100) DEFAULT NULL,
  `study_instance_uid` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `dicom_dicomscan_patient_id_bffccc46_fk_patients_patient_id` (`patient_id`),
  CONSTRAINT `dicom_dicomscan_patient_id_bffccc46_fk_patients_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dicom_dicomscan`
--

LOCK TABLES `dicom_dicomscan` WRITE;
/*!40000 ALTER TABLE `dicom_dicomscan` DISABLE KEYS */;
/*!40000 ALTER TABLE `dicom_dicomscan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dicom_scanregistration`
--

DROP TABLE IF EXISTS `dicom_scanregistration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dicom_scanregistration` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `requesting_physician` varchar(200) NOT NULL,
  `scan_type` varchar(100) NOT NULL,
  `registered_at` datetime(6) NOT NULL,
  `status` varchar(50) NOT NULL,
  `patient_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `dicom_scanregistrati_patient_id_c4b96b63_fk_patients_` (`patient_id`),
  CONSTRAINT `dicom_scanregistrati_patient_id_c4b96b63_fk_patients_` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dicom_scanregistration`
--

LOCK TABLES `dicom_scanregistration` WRITE;
/*!40000 ALTER TABLE `dicom_scanregistration` DISABLE KEYS */;
INSERT INTO `dicom_scanregistration` VALUES (4,'Dr. Antigravity','Chest','2026-04-01 05:08:41.208294','REGISTERED',38),(5,'Dr. Antigravity','Chest','2026-04-01 05:09:44.205010','REGISTERED',38),(6,'DR.smith','Chest','2026-04-01 05:12:07.867492','REGISTERED',38),(7,'DR.smith','Neck','2026-04-01 05:26:48.515843','REGISTERED',38),(8,'DR.smith','Neck','2026-04-01 08:11:59.495818','REGISTERED',50),(9,'DR.smith','Head','2026-04-01 08:37:18.065937','REGISTERED',38),(10,'DR.smith','Head','2026-04-01 08:37:20.061754','REGISTERED',38),(11,'DR.smith','Head','2026-04-01 09:18:56.527044','REGISTERED',38),(12,'DR.smith','Head','2026-04-01 09:18:58.427023','REGISTERED',38);
/*!40000 ALTER TABLE `dicom_scanregistration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(13,'admincenter','compliancereport'),(14,'admincenter','machine'),(22,'admincenter','onboardingslide'),(23,'admincenter','securitysettings'),(15,'admincenter','systemlog'),(20,'admincenter','userprofile'),(24,'admincenter','verificationcode'),(16,'airisk','patientriskassessment'),(2,'auth','group'),(3,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(9,'dicom','dicomscan'),(19,'dicom','scanregistration'),(18,'dosestats','doseanomaly'),(10,'dosestats','organdose'),(11,'dosestats','scandose'),(21,'dosestats','scanparameter'),(17,'patients','alert'),(7,'patients','dailydose'),(8,'patients','patient'),(12,'realtimemonitor','realtimedose'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-01-28 09:25:01.156211'),(2,'auth','0001_initial','2026-01-28 09:25:01.685838'),(3,'admin','0001_initial','2026-01-28 09:25:01.814375'),(4,'admin','0002_logentry_remove_auto_add','2026-01-28 09:25:01.821182'),(5,'admin','0003_logentry_add_action_flag_choices','2026-01-28 09:25:01.829587'),(6,'contenttypes','0002_remove_content_type_name','2026-01-28 09:25:01.925568'),(7,'auth','0002_alter_permission_name_max_length','2026-01-28 09:25:01.983803'),(8,'auth','0003_alter_user_email_max_length','2026-01-28 09:25:02.009851'),(9,'auth','0004_alter_user_username_opts','2026-01-28 09:25:02.017225'),(10,'auth','0005_alter_user_last_login_null','2026-01-28 09:25:02.069976'),(11,'auth','0006_require_contenttypes_0002','2026-01-28 09:25:02.073040'),(12,'auth','0007_alter_validators_add_error_messages','2026-01-28 09:25:02.080340'),(13,'auth','0008_alter_user_username_max_length','2026-01-28 09:25:02.141605'),(14,'auth','0009_alter_user_last_name_max_length','2026-01-28 09:25:02.199754'),(15,'auth','0010_alter_group_name_max_length','2026-01-28 09:25:02.221228'),(16,'auth','0011_update_proxy_permissions','2026-01-28 09:25:02.229848'),(17,'auth','0012_alter_user_first_name_max_length','2026-01-28 09:25:02.289741'),(18,'sessions','0001_initial','2026-01-28 09:25:02.326473'),(19,'patients','0001_initial','2026-03-07 07:04:18.020598'),(20,'dicom','0001_initial','2026-03-07 07:10:20.703772'),(21,'dosestats','0001_initial','2026-03-07 07:14:01.948682'),(22,'realtimemonitor','0001_initial','2026-03-07 07:19:43.423640'),(23,'admincenter','0001_initial','2026-03-07 07:23:53.956416'),(24,'airisk','0001_initial','2026-03-07 07:26:32.317361'),(25,'patients','0002_patient_room_number','2026-03-07 07:28:44.547815'),(26,'patients','0003_alert','2026-03-07 07:31:04.118970'),(27,'dosestats','0002_doseanomaly','2026-03-07 07:36:23.337506'),(28,'admincenter','0002_compliancereport_description_compliancereport_title','2026-03-07 07:37:57.035030'),(29,'patients','0004_alert_alert_level_alert_dose_value_msv','2026-03-07 08:03:42.647484'),(30,'patients','0005_patient_age_patient_allergies_patient_clinical_notes','2026-03-07 08:08:44.940429'),(31,'dosestats','0003_scandose_facility','2026-03-07 09:17:33.349194'),(32,'dicom','0002_scanregistration','2026-03-10 04:29:28.447443'),(33,'admincenter','0003_userprofile','2026-03-10 04:37:06.908878'),(34,'patients','0006_patient_dob','2026-03-10 04:54:55.359866'),(35,'dosestats','0004_scanparameter','2026-03-10 05:26:26.878300'),(36,'admincenter','0004_onboardingslide','2026-03-10 07:07:17.516922'),(37,'admincenter','0005_securitysettings','2026-03-10 07:17:23.321382'),(38,'admincenter','0006_systemlog_user','2026-03-10 07:46:37.461981'),(39,'admincenter','0007_userprofile_permissions_summary_and_more','2026-03-10 07:50:22.280588'),(40,'admincenter','0008_verificationcode','2026-03-10 08:01:12.737601'),(41,'dicom','0003_dicomscan_modality_dicomscan_protocol_name_and_more','2026-03-16 05:51:44.494690'),(42,'patients','0007_patient_blood_group_alter_patient_allergies','2026-04-01 08:20:30.455904');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('2rf9w8gqt9aq7zihzcd32mktr4gxabvr','.eJxVjMsOwiAQRf-FtSE8prS4dO83kBkGpGogKe3K-O_apAvd3nPOfYmA21rC1tMSZhZn4cTpdyOMj1R3wHestyZjq-syk9wVedAur43T83K4fwcFe_nWaBJP3qc4UjTAGUkjKojsEkzKOz8SepUBrEYXh8zMA2mwWVkwyljx_gARWzhV:1vzrSE:8eqtRzCYCmHYytNeRIQ09IwNNHbroUgbX36QX95LLRw','2026-03-24 07:24:34.075580'),('qqsokbfo09eaxeps4toarpeoxd1zlqa4','.eJxVjEEOwiAQRe_C2hAsMIBL956BMMwgVUOT0q6MdzckXej2v_f-W8S0bzXundc4k7gIJ06_G6b85DYAPVK7LzIvbVtnlEORB-3ythC_rof7d1BTr6NWumjOqJGD8RAQ83QmYJ-Q0BObEgJBoEl7D5MrLoDNAMYqpyBbEp8vC_o4Lw:1vzrSX:ztk92I7DaPlSOqm10zgFHDbDKiPZfIxxK5O_726t80w','2026-03-24 07:24:53.781703'),('zqti7blq34ct5fy9rt8ax4l2a67inshi','.eJxVjMEOgjAQRP-lZ9OwLQutR-98Q9PuLhY1JaFwMv67kHDQ48x7M28V4rbmsFVZwsTqqlBdfrsU6SnlAPyI5T5rmsu6TEkfij5p1cPM8rqd7t9BjjXvazJgOY4IzkBCJm8FrRAb7BojLdpEnJgAoI8eqRl7b_ZArk1ioHPq8wXrOze5:1vzrMP:uBmhCh-RGPSw63GPPnPj8FlZWShUncomdWZQ0WJypRg','2026-03-24 07:18:33.326128');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dosestats_doseanomaly`
--

DROP TABLE IF EXISTS `dosestats_doseanomaly`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dosestats_doseanomaly` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `anomaly_id` varchar(50) NOT NULL,
  `area` varchar(100) NOT NULL,
  `description` varchar(255) NOT NULL,
  `dlp_value` double NOT NULL,
  `status_level` varchar(50) NOT NULL,
  `detected_at` datetime(6) NOT NULL,
  `patient_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `anomaly_id` (`anomaly_id`),
  KEY `dosestats_doseanomaly_patient_id_78cbd6b4_fk_patients_patient_id` (`patient_id`),
  CONSTRAINT `dosestats_doseanomaly_patient_id_78cbd6b4_fk_patients_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dosestats_doseanomaly`
--

LOCK TABLES `dosestats_doseanomaly` WRITE;
/*!40000 ALTER TABLE `dosestats_doseanomaly` DISABLE KEYS */;
/*!40000 ALTER TABLE `dosestats_doseanomaly` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dosestats_organdose`
--

DROP TABLE IF EXISTS `dosestats_organdose`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dosestats_organdose` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `organ_name` varchar(100) NOT NULL,
  `dose_value` double NOT NULL,
  `scan_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `dosestats_organdose_scan_id_8ed78a3d_fk_dosestats_scandose_id` (`scan_id`),
  CONSTRAINT `dosestats_organdose_scan_id_8ed78a3d_fk_dosestats_scandose_id` FOREIGN KEY (`scan_id`) REFERENCES `dosestats_scandose` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dosestats_organdose`
--

LOCK TABLES `dosestats_organdose` WRITE;
/*!40000 ALTER TABLE `dosestats_organdose` DISABLE KEYS */;
/*!40000 ALTER TABLE `dosestats_organdose` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dosestats_scandose`
--

DROP TABLE IF EXISTS `dosestats_scandose`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dosestats_scandose` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `scan_date` datetime(6) NOT NULL,
  `study_description` varchar(200) NOT NULL,
  `total_dlp` double NOT NULL,
  `avg_risk` varchar(50) NOT NULL,
  `patient_id` bigint NOT NULL,
  `facility` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `dosestats_scandose_patient_id_a9acde49_fk_patients_patient_id` (`patient_id`),
  CONSTRAINT `dosestats_scandose_patient_id_a9acde49_fk_patients_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dosestats_scandose`
--

LOCK TABLES `dosestats_scandose` WRITE;
/*!40000 ALTER TABLE `dosestats_scandose` DISABLE KEYS */;
/*!40000 ALTER TABLE `dosestats_scandose` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dosestats_scanparameter`
--

DROP TABLE IF EXISTS `dosestats_scanparameter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dosestats_scanparameter` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `kvp` double NOT NULL,
  `ma` double NOT NULL,
  `pitch` double NOT NULL,
  `scan_length` double NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `patient_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `dosestats_scanparame_patient_id_4be2349d_fk_patients_` (`patient_id`),
  CONSTRAINT `dosestats_scanparame_patient_id_4be2349d_fk_patients_` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dosestats_scanparameter`
--

LOCK TABLES `dosestats_scanparameter` WRITE;
/*!40000 ALTER TABLE `dosestats_scanparameter` DISABLE KEYS */;
INSERT INTO `dosestats_scanparameter` VALUES (1,120,250.5,1.25,500,'2026-03-10 05:26:53.667163',NULL);
/*!40000 ALTER TABLE `dosestats_scanparameter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients_alert`
--

DROP TABLE IF EXISTS `patients_alert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients_alert` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `patient_id` bigint NOT NULL,
  `alert_level` varchar(50) NOT NULL,
  `dose_value_mSv` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `patients_alert_patient_id_1697f769_fk_patients_patient_id` (`patient_id`),
  CONSTRAINT `patients_alert_patient_id_1697f769_fk_patients_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients_alert`
--

LOCK TABLES `patients_alert` WRITE;
/*!40000 ALTER TABLE `patients_alert` DISABLE KEYS */;
INSERT INTO `patients_alert` VALUES (11,'Critical Limit Reached','Dose limit exceeded',0,'2026-03-26 05:40:42.736715',51,'CRITICAL',1500);
/*!40000 ALTER TABLE `patients_alert` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients_dailydose`
--

DROP TABLE IF EXISTS `patients_dailydose`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients_dailydose` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `dose_amount` double NOT NULL,
  `patient_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `patients_dailydose_patient_id_date_a86a7604_uniq` (`patient_id`,`date`),
  CONSTRAINT `patients_dailydose_patient_id_9c33b40c_fk_patients_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients_dailydose`
--

LOCK TABLES `patients_dailydose` WRITE;
/*!40000 ALTER TABLE `patients_dailydose` DISABLE KEYS */;
INSERT INTO `patients_dailydose` VALUES (9,'2026-03-26',10,51);
/*!40000 ALTER TABLE `patients_dailydose` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients_patient`
--

DROP TABLE IF EXISTS `patients_patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients_patient` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `patient_id` varchar(50) NOT NULL,
  `name` varchar(200) NOT NULL,
  `gender` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `room_number` varchar(50) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `allergies` longtext,
  `clinical_notes` longtext,
  `dob` date DEFAULT NULL,
  `blood_group` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `patient_id` (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients_patient`
--

LOCK TABLES `patients_patient` WRITE;
/*!40000 ALTER TABLE `patients_patient` DISABLE KEYS */;
INSERT INTO `patients_patient` VALUES (37,'PT-DETAILS-001','Ethan Carter','Male','2026-03-10 05:21:50.201378',NULL,45,'None',NULL,NULL,NULL),(38,'123456789','Aarav Sharma','Male','2026-03-17 07:57:27.740676',NULL,NULL,'None',NULL,NULL,NULL),(39,'987654321','Ishani Gupta','Female','2026-03-17 07:57:27.745756',NULL,NULL,'None',NULL,NULL,NULL),(40,'456789123','Vihaan Malhotra','Male','2026-03-17 07:57:27.750389',NULL,NULL,'None',NULL,NULL,NULL),(41,'789123456','Diya Iyer','Female','2026-03-17 07:57:27.754711',NULL,NULL,'None',NULL,NULL,NULL),(42,'321654987','Advait Joshi','Male','2026-03-17 07:57:27.758804',NULL,NULL,'None',NULL,NULL,NULL),(43,'P106','Rajesh Kumar','Male','2026-03-17 07:57:27.762642',NULL,NULL,'None',NULL,NULL,NULL),(44,'P107','Priya Nair','Female','2026-03-17 07:57:27.767421',NULL,NULL,'None',NULL,NULL,NULL),(45,'P108','Arjun Singh','Male','2026-03-17 07:57:27.772076',NULL,NULL,'None',NULL,NULL,NULL),(46,'P109','Anjali Reddy','Female','2026-03-17 07:57:27.776542',NULL,NULL,'None',NULL,NULL,NULL),(47,'P110','Vikram Patil','Male','2026-03-17 07:57:27.780230',NULL,NULL,'None',NULL,NULL,NULL),(48,'P111','Sunita Deshmukh','Female','2026-03-17 07:57:27.783817',NULL,NULL,'None',NULL,NULL,NULL),(49,'P112','Suresh Pillai','Male','2026-03-17 07:57:27.788290',NULL,NULL,'None',NULL,NULL,NULL),(50,'P113','Kavita Hegde','Female','2026-03-17 07:57:27.792229',NULL,NULL,'None',NULL,NULL,NULL),(51,'TEST-001','Test Patient','Male','2026-03-26 05:40:42.720691','101',30,'None',NULL,NULL,NULL),(52,'JD-001','John Doe','Male','2026-03-31 16:36:30.167293',NULL,NULL,'None','','1990-01-01',NULL),(53,'VG-2024-111','chanikya','Male','2026-03-31 16:39:00.865636',NULL,NULL,'nil','nil','2000-01-01',NULL),(54,'9876543','lakshmi','Male','2026-04-01 08:08:12.881359',NULL,NULL,'no','Registered via App','2004-01-01',NULL),(55,'7674900','sandeep','Male','2026-04-01 08:09:00.171743',NULL,NULL,'no','Registered via App','2004-01-01',NULL),(56,'7093838','rakesh','Male','2026-04-01 08:46:57.702151',NULL,22,'no','Registered via App','2004-01-01','B+');
/*!40000 ALTER TABLE `patients_patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `realtimemonitor_realtimedose`
--

DROP TABLE IF EXISTS `realtimemonitor_realtimedose`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `realtimemonitor_realtimedose` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `timestamp` datetime(6) NOT NULL,
  `dose_rate` double NOT NULL,
  `accumulated_dose` double NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `patient_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `realtimemonitor_real_patient_id_e73ad9fb_fk_patients_` (`patient_id`),
  CONSTRAINT `realtimemonitor_real_patient_id_e73ad9fb_fk_patients_` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `realtimemonitor_realtimedose`
--

LOCK TABLES `realtimemonitor_realtimedose` WRITE;
/*!40000 ALTER TABLE `realtimemonitor_realtimedose` DISABLE KEYS */;
INSERT INTO `realtimemonitor_realtimedose` VALUES (17,'2026-03-10 05:21:50.206002',1,1,1,37),(18,'2026-03-10 05:21:50.210590',2,3,1,37),(19,'2026-03-10 05:21:50.215503',3,6,1,37),(20,'2026-03-10 05:21:50.219968',4,10,1,37),(21,'2026-03-10 05:21:50.223762',5,15,1,37),(22,'2026-03-26 05:40:42.742336',1.5,1500,0,51);
/*!40000 ALTER TABLE `realtimemonitor_realtimedose` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-08 13:31:06
