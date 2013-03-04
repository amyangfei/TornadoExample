CREATE DATABASE  IF NOT EXISTS `yuedu` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `yuedu`;
-- MySQL dump 10.13  Distrib 5.5.16, for osx10.5 (i386)
--
-- Host: localhost    Database: yuedu
-- ------------------------------------------------------
-- Server version	5.5.23

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
-- Table structure for table `y_users`
--

DROP TABLE IF EXISTS `y_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `y_users` (
  `u_id` int(11) NOT NULL AUTO_INCREMENT,
  `u_email` varchar(45) NOT NULL,
  `u_name` varchar(45) DEFAULT 'Reader',
  `u_password` varchar(45) NOT NULL,
  PRIMARY KEY (`u_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `y_users`
--

LOCK TABLES `y_users` WRITE;
/*!40000 ALTER TABLE `y_users` DISABLE KEYS */;
INSERT INTO `y_users` VALUES (1,'admin@gmail.com','hello','a7ea773036a99a6130e41e8c0b65a1b0e3616def');
/*!40000 ALTER TABLE `y_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `y_articles`
--

DROP TABLE IF EXISTS `y_articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `y_articles` (
  `a_id` int(11) NOT NULL AUTO_INCREMENT,
  `a_url` varchar(45) NOT NULL,
  `a_title` varchar(45) NOT NULL,
  `a_author` varchar(45) DEFAULT NULL,
  `a_content` text,
  PRIMARY KEY (`a_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `y_articles`
--

LOCK TABLES `y_articles` WRITE;
/*!40000 ALTER TABLE `y_articles` DISABLE KEYS */;
INSERT INTO `y_articles` VALUES (1,'jfbkok417','hello','a','aaa'),(2,'83rh1s','world','b','我不记得和他一起走进电影院 \n在那个傍晚。可我听到古老的 \n印度人在喊：不要相信 \n马，也不要相信现代性'),(3,'utdq0sxpqj','hurt','c','纽约/十一月/第五大街 \n太阳是一个粉碎的金属盘 \n孤离在阴影中，我问自己： \n这是巴别还是索多玛？');
/*!40000 ALTER TABLE `y_articles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-03-04 17:31:29
