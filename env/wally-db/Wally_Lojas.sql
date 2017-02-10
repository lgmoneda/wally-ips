CREATE DATABASE  IF NOT EXISTS `Wally` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `Wally`;
-- MySQL dump 10.13  Distrib 5.5.53, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: Wally
-- ------------------------------------------------------
-- Server version	5.5.53-0+deb8u1

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
-- Table structure for table `Lojas`
--

DROP TABLE IF EXISTS `Lojas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Lojas` (
  `LojasId` int(11) NOT NULL,
  `placeId` int(11) DEFAULT NULL,
  `categoria` varchar(45) DEFAULT NULL,
  `nome` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`LojasId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Lojas`
--

LOCK TABLES `Lojas` WRITE;
/*!40000 ALTER TABLE `Lojas` DISABLE KEYS */;
INSERT INTO `Lojas` VALUES (1,1,'Roupas','Calvin Klein'),(2,2,'Alimentação','Praça de Alimentação'),(3,3,'Roupas','Lacoste'),(4,4,'Alimentação','Rascal'),(5,5,'Roupas','Hering'),(6,6,'Alimentação','Viena'),(7,7,'Roupas','Arezzo'),(8,8,'Varejo','Carrefour'),(9,9,'Corpo & Saúde','Bodytech'),(10,10,'Livraria','Saraiva'),(11,11,'Entretenimento','Cinemark'),(12,12,'Roupas','C&A'),(13,13,'Roupas','Lilica & Tigor'),(14,14,'Varejo','City Lar Eletrodomésticos'),(15,15,'Roupas','Havaianas'),(16,16,'Corpo & Saúde','Drogasil'),(17,17,'Corpo & Saúde','Bayard'),(18,18,'Entretenimento','Hot Zone'),(19,19,'Roupas','Ralph Lauren'),(20,20,'Corpo & Saúde','Centauro');
/*!40000 ALTER TABLE `Lojas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-12-09 10:08:58
