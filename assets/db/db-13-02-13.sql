-- MySQL dump 10.13  Distrib 5.5.29, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: hungr
-- ------------------------------------------------------
-- Server version	5.5.29-0ubuntu0.12.10.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_425ae3c4` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_5886d21f` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_1bb8f392` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add site',6,'add_site'),(17,'Can change site',6,'change_site'),(18,'Can delete site',6,'delete_site'),(19,'Can add token',7,'add_token'),(20,'Can change token',7,'change_token'),(21,'Can delete token',7,'delete_token'),(28,'Can add restaurant',10,'add_restaurant'),(29,'Can change restaurant',10,'change_restaurant'),(30,'Can delete restaurant',10,'delete_restaurant'),(40,'Can add log entry',14,'add_logentry'),(41,'Can change log entry',14,'change_logentry'),(42,'Can delete log entry',14,'delete_logentry'),(43,'Can add restaurant category',15,'add_restaurantcategory'),(44,'Can change restaurant category',15,'change_restaurantcategory'),(45,'Can delete restaurant category',15,'delete_restaurantcategory'),(46,'Can add opening hours',16,'add_openinghours'),(47,'Can change opening hours',16,'change_openinghours'),(48,'Can delete opening hours',16,'delete_openinghours'),(49,'Can add menu section',17,'add_menusection'),(50,'Can change menu section',17,'change_menusection'),(51,'Can delete menu section',17,'delete_menusection'),(52,'Can add menu item',18,'add_menuitem'),(53,'Can change menu item',18,'change_menuitem'),(54,'Can delete menu item',18,'delete_menuitem');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'riensen','florian','','riensen@ggg.de','pbkdf2_sha256$10000$5v1NYE4O49Cx$4pJwtnFsr7Vxp2cQYXqc0KvHh2hGwrakD7st+cae+/Q=',1,1,1,'2013-02-01 11:21:41','2013-02-01 11:21:41'),(2,'collin','','','collin@tcd.ie','pbkdf2_sha256$10000$gKPWioPDqUmT$Stm01SuVhSqXIwzmqWkNd03nC/u8pKi59Z++Iw+g3Og=',0,1,0,'2013-02-01 11:38:26','2013-02-01 11:38:26'),(14,'pablo','','','pablo@tcd.ie','pbkdf2_sha256$10000$e45irqDBFj3c$98OV2RuHwkcFAMZq0e/P4zcHDu31EIuuTyJ1LfeJYpI=',0,1,0,'2013-02-01 12:55:47','2013-02-01 12:55:47'),(15,'colin','','','hardyce@tcd.ie','pbkdf2_sha256$10000$sSmQxsmDCSgo$g4XdmbYSmq2OG70vUvS5XfAEwXPjCTrv8NCFq9LKgyU=',1,1,1,'2013-02-05 16:54:12','2013-02-05 16:53:23'),(16,'pepe','pepe','pepe','pepe@pepe.com','pbkdf2_sha256$10000$XrL1NRixveIl$uk4QtjuupgF9S/8mXN/YR/H8qNOymuNs20T034ybR8E=',0,1,0,'2013-02-05 17:05:57','2013-02-05 17:05:57'),(17,'pepe2','pepe','pepe','pepe@pepe.com','pbkdf2_sha256$10000$lpzap3KqkllH$/bHs06BedgLQRQTbAsv3xQ9AttBCdd4HhciydsFqTQM=',0,1,0,'2013-02-05 17:30:58','2013-02-05 17:30:58'),(18,'pepe3','pepe','pepe','pepe@pepe.com','pbkdf2_sha256$10000$oOF1Soa8u1Hb$+SmTi/WphaJLjuumzfTYZOQKOLeHxhdKMIjIhKpFBlY=',0,1,0,'2013-02-05 17:35:14','2013-02-05 17:35:14'),(19,'Pablo2','Pablo','Porto','pablo@hotmail.com','pbkdf2_sha256$10000$GaNxEd8AKT10$bYOFqo73g/9fjBVX7CvdREYkqqrm3509E5q98Y0NRHo=',0,1,0,'2013-02-06 12:20:28','2013-02-06 12:20:28'),(20,'pepe99','Pepe','pepe','pepe@pepe.com','pbkdf2_sha256$10000$ItzFl41YIia8$vKU0FW4CRBKMrfXTJfozRQNTxTv2RHZ7UUtSHUk06n0=',0,1,0,'2013-02-06 12:24:06','2013-02-06 12:24:06'),(21,'pepe100','pepe100 ','pepe100 ','pepe100@pepe100.com','pbkdf2_sha256$10000$FmMODJarwLNU$OHA3z/U40vzbQIvGwK2BETRus594CAQg51N/0iqzNeI=',0,1,0,'2013-02-06 12:26:21','2013-02-06 12:26:21'),(22,'pepe110','pepe ','pepe ','pepe@pepe.com','pbkdf2_sha256$10000$GwEav4ClyZK3$VlwYk39F1divTMiRUPPHVgOza2pTX5ULfmgiLMnBwms=',0,1,0,'2013-02-06 12:29:53','2013-02-06 12:29:53');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_403f60f` (`user_id`),
  KEY `auth_user_groups_425ae3c4` (`group_id`),
  CONSTRAINT `group_id_refs_id_f116770` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_7ceef80f` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_403f60f` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_dfbab7d` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `user_id` int(11) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_5656ace4` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
INSERT INTO `authtoken_token` VALUES ('1c1aa2f6cae4e4e13cc74ffa6fba944f226020d6',20,'2013-02-06 12:24:06'),('23cebf20495564f435016b9097a33d0444cd932b',19,'2013-02-06 12:20:28'),('3eb7d9161ef9382b346818d08c85c9a99a2b8f0d',16,'2013-02-05 17:05:57'),('4535587778ad00f936772f4ff24cc896d008d96a',2,'2013-02-01 11:47:42'),('6f6b8e385772406984f0617e80425c29d60414cc',21,'2013-02-06 12:26:21'),('782c6cea38f9dd9783a51dcb3dfc261cc244e0fb',1,'2013-02-01 11:47:42'),('823782235d58d199e2bd4edc21cd05fc587b6aa7',22,'2013-02-06 12:29:54'),('8944bb4b1bfecfa50f55eba1e21cb5fdadaf10e6',18,'2013-02-05 17:35:14'),('d63dfb966582978e91058eb65aaa00c8d90883b4',15,'2013-02-05 16:53:23'),('d894bb24a211752ac0e419ab1d48f075230637ae',14,'2013-02-01 12:55:47'),('de468ee8d0bf32786e94d7213692d46265fc2c5e',17,'2013-02-05 17:30:58');
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_403f60f` (`user_id`),
  KEY `django_admin_log_1bb8f392` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_288599e6` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c8665aa` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (7,'2013-02-06 11:42:08',15,10,'1','pizza man (dubin 3)',2,'Changed name and postcode.'),(8,'2013-02-06 11:50:34',15,10,'1','pizza man (Pizza City,Pizza PC)',1,''),(16,'2013-02-06 12:54:03',15,10,'2','China (erere, 1234)',1,''),(18,'2013-02-12 16:38:33',15,10,'1','Toms Pizza (Dublin 6, Dublin 6)',1,''),(19,'2013-02-12 16:38:58',15,17,'1','Drinks',1,''),(20,'2013-02-12 16:39:09',15,17,'2','Hot Food',1,''),(21,'2013-02-12 16:39:20',15,16,'1','Tuesday 16:39 - 16:39',1,''),(22,'2013-02-12 16:39:29',15,16,'2','Friday 16:39 - 16:39',1,''),(23,'2013-02-12 16:39:50',15,18,'1','Cola',1,''),(24,'2013-02-12 16:40:11',15,18,'2','Pizza',1,''),(25,'2013-02-12 16:40:24',15,18,'3','Burger',1,''),(26,'2013-02-12 17:31:43',15,10,'2','Apache 3 (Dublin, Dublin)',1,'');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'site','sites','site'),(7,'token','authtoken','token'),(10,'restaurant','restaurantManagement','restaurant'),(14,'log entry','admin','logentry'),(15,'restaurant category','restaurantManagement','restaurantcategory'),(16,'opening hours','restaurantManagement','openinghours'),(17,'menu section','restaurantManagement','menusection'),(18,'menu item','restaurantManagement','menuitem');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_3da3d3d8` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('3b1e846588934a45976066488fcf6b53','Yzk4ODgyYmU3NWM5MmZkNTU2OWUwMTU5NzI3Yzc3ZjNmNzhlNDEyYzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQ91Lg==\n','2013-02-19 16:54:12'),('7bff37372a22a9b58838a41c0ab0fbb7','MTk2YzY4NGY2NTVlM2Q2OTVkOWMzZGEzMzdlZWM1ODgwNzliOWM2YTqAAn1xAS4=\n','2013-02-15 11:37:18');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restaurantManagement_menuitem`
--

DROP TABLE IF EXISTS `restaurantManagement_menuitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `restaurantManagement_menuitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `menu_category_id` int(11) NOT NULL,
  `price` decimal(6,2) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `restaurantManagement_menuitem_78f044cb` (`menu_category_id`),
  CONSTRAINT `menu_category_id_refs_id_7a6c0c2c` FOREIGN KEY (`menu_category_id`) REFERENCES `restaurantManagement_menusection` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurantManagement_menuitem`
--

LOCK TABLES `restaurantManagement_menuitem` WRITE;
/*!40000 ALTER TABLE `restaurantManagement_menuitem` DISABLE KEYS */;
INSERT INTO `restaurantManagement_menuitem` VALUES (1,1,10.00,'Cola','Tasty'),(2,2,10.00,'Pizza','Tasty Tasty'),(3,2,12.00,'Burger','mhhhh');
/*!40000 ALTER TABLE `restaurantManagement_menuitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restaurantManagement_menusection`
--

DROP TABLE IF EXISTS `restaurantManagement_menusection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `restaurantManagement_menusection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `restaurant_id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `restaurantManagement_menusection_3325d4d1` (`restaurant_id`),
  CONSTRAINT `restaurant_id_refs_id_78614255` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurantManagement_restaurant` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurantManagement_menusection`
--

LOCK TABLES `restaurantManagement_menusection` WRITE;
/*!40000 ALTER TABLE `restaurantManagement_menusection` DISABLE KEYS */;
INSERT INTO `restaurantManagement_menusection` VALUES (1,1,'Drinks'),(2,1,'Hot Food');
/*!40000 ALTER TABLE `restaurantManagement_menusection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restaurantManagement_openinghours`
--

DROP TABLE IF EXISTS `restaurantManagement_openinghours`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `restaurantManagement_openinghours` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `restaurant_id` int(11) NOT NULL,
  `day_of_week` int(11) NOT NULL,
  `time_open` time NOT NULL,
  `time_close` time NOT NULL,
  PRIMARY KEY (`id`),
  KEY `restaurantManagement_openinghours_3325d4d1` (`restaurant_id`),
  CONSTRAINT `restaurant_id_refs_id_195caf41` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurantManagement_restaurant` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurantManagement_openinghours`
--

LOCK TABLES `restaurantManagement_openinghours` WRITE;
/*!40000 ALTER TABLE `restaurantManagement_openinghours` DISABLE KEYS */;
INSERT INTO `restaurantManagement_openinghours` VALUES (1,1,1,'16:39:18','16:39:19'),(2,1,4,'16:39:27','16:39:28');
/*!40000 ALTER TABLE `restaurantManagement_openinghours` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restaurantManagement_restaurant`
--

DROP TABLE IF EXISTS `restaurantManagement_restaurant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `restaurantManagement_restaurant` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `owner_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `street1` varchar(200) NOT NULL,
  `street2` varchar(200) DEFAULT NULL,
  `postcode` varchar(50) NOT NULL,
  `city` varchar(100) NOT NULL,
  `country` varchar(100) NOT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `phone` varchar(50) NOT NULL,
  `email` varchar(75) NOT NULL,
  `preparation_time` time DEFAULT NULL,
  `delivery_minimum` decimal(5,2) NOT NULL,
  `delivery_cost` decimal(5,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone` (`phone`),
  KEY `restaurantManagement_restaurant_5d52dd10` (`owner_id`),
  CONSTRAINT `owner_id_refs_id_4f1b75f3` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurantManagement_restaurant`
--

LOCK TABLES `restaurantManagement_restaurant` WRITE;
/*!40000 ALTER TABLE `restaurantManagement_restaurant` DISABLE KEYS */;
INSERT INTO `restaurantManagement_restaurant` VALUES (1,2,'Toms Pizza','147 Rathmines Road','','Dublin 6','Dublin 6','Ireland',40.0996345,-83.1137889,'00000000000','1@1.de','00:20:00',10.00,10.00),(2,2,'Apache 3','2 Earl St N','','Dublin','Dublin','Ireland',53.4252101,-6.05255,'01000000000','r@r.de','17:31:35',1.00,1.00);
/*!40000 ALTER TABLE `restaurantManagement_restaurant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restaurantManagement_restaurantcategory`
--

DROP TABLE IF EXISTS `restaurantManagement_restaurantcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `restaurantManagement_restaurantcategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category` varchar(3) NOT NULL,
  `restaurant_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `restaurantManagement_restaurantcategory_3325d4d1` (`restaurant_id`),
  CONSTRAINT `restaurant_id_refs_id_6dbd849d` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurantManagement_restaurant` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurantManagement_restaurantcategory`
--

LOCK TABLES `restaurantManagement_restaurantcategory` WRITE;
/*!40000 ALTER TABLE `restaurantManagement_restaurantcategory` DISABLE KEYS */;
/*!40000 ALTER TABLE `restaurantManagement_restaurantcategory` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-02-13 13:01:40
