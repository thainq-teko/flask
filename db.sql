-- MySQL dump 10.13  Distrib 5.7.26, for Linux (x86_64)
--
-- Host: localhost    Database: flask_db
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.18.04.1

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
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','123456','test123@gmail.com'),(2,'user123','123456','test122@gmail.com'),(6,'abc','$2b$12$So6.DD9f.cwFTTs9rPlmruA0x.w8GIr0Bnn/gdwndynpWT9KwpiAu','test111@gmail.com'),(7,'abc','$2b$12$eOYhOD6nczFWb4yKl3DdRO2mldoRcficlV9ApPPZ1FZJxUne3n4Mq','test111@gmail.com'),(8,'abc','$2b$12$t4P2Mh5.bHDJ1Wq4oNZz1ewyB3GF4f869RFHg8Ce8lIPVUNJGt5im','test111@gmail.com'),(9,'abc','$2b$12$yc0JWWDyvPcXMghrcQZHVuKT/qLKIZUKj32BSpDUoJGuPuY6rNF96','test111@gmail.com'),(10,'abc','$2b$12$YHRQGHcQEb.CWvC7kYbgLOjj4je1qczJNw4dMQo2q/kttTWTuWtHy','test111@gmail.com'),(11,'abc','$2b$12$eexuuY6QQODGtRM/tRPoFudlcAgv6fMtEQb4JvDrguTKh/iRLuqTy','test111@gmail.com'),(12,'abc','$2b$12$LPNeKzaGNMYyEKgsNq2f3uSN1QiWWFBlUhftPBIiBUfAHpPg6vvgi','test111@gmail.com'),(13,'abc','$2b$12$ycRrVwmA5u5w9rZnPLrVYOL5gouLfFpnhdwDP6S52djXyRdcZRdzm','test111@gmail.com'),(14,'abc','$2b$12$Jsn0/87HE/kswHNADiRr9.Gr/0zE5QLYJUPCefVmIKIKWOjHhfgxa','test111@gmail.com'),(15,'abc','$2b$12$wXZK1ysjF/AgiROD/kSA1ecTFCyb0xHqjKfNL8lfgEsiDOZaRWL/u','test111@gmail.com'),(16,'abc','$2b$12$6w.yR46Re37uFY2JfZZAIO8bN0C044pk3rUlmSOdAcZVXFFO0OMp6','test111@gmail.com'),(17,'iu hnh','$2b$12$ab6JwBTW9QHPTk1SNNyVv.FShDZ/UQkoHSKUkTdrz8dAxs1wmYRxi','test111@gmail.com'),(18,'adbb','$2b$12$Qk8vVTWQnOYgjutN6emXEeOfNEPV/WVKQcAJvtaMgn8DbzFwlziqa','test111@gmail.com'),(19,'abccc','$2b$12$aObxfg7QbNzjsRSxt3GV6e3mCs9kKQDJchwFg3157BtEkajAvRMyC','test1111@gmail.com'),(20,'nhiều sản p','$2b$12$Hy0rgInutuQeBoKze2obke7/poi00/eCiL3OPs3tsz8F32vxG/xS2','test1011@gmail.com'),(21,'hệ điều hành','$2b$12$EMlXnlOENVzUPaIul.5LneQKrfXRxk41JXFWxkjPiZbRQuG2ZJ5uS','test11@gmail.com'),(22,'thainq','$2b$12$eDvYIhCHNLPVPkAvPxDw/OleZQLqK4JyPzfsDeU/C1h4LYriR0zfe','testa@gmail.com');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-05-30 13:52:32
