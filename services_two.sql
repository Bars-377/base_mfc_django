-- --------------------------------------------------------
-- Хост:                         127.0.0.1
-- Версия сервера:               8.0.30 - MySQL Community Server - GPL
-- Операционная система:         Win64
-- HeidiSQL Версия:              12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Дамп структуры базы данных basemfcdjango
CREATE DATABASE IF NOT EXISTS `basemfcdjango` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `basemfcdjango`;

-- Дамп структуры для таблица basemfcdjango.services_two
CREATE TABLE IF NOT EXISTS `services_two` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `id_id` text COLLATE utf8mb4_general_ci,
  `KOSGU` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `DopFC` text COLLATE utf8mb4_general_ci,
  `budget_planned` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `off_budget_planned` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `budget_concluded` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `off_budget_concluded` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `budget_remainder` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `off_budget_remainder` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `color` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Дамп данных таблицы basemfcdjango.services_two: ~21 rows (приблизительно)
INSERT INTO `services_two` (`id`, `id_id`, `KOSGU`, `DopFC`, `budget_planned`, `off_budget_planned`, `budget_concluded`, `off_budget_concluded`, `budget_remainder`, `off_budget_remainder`, `color`) VALUES
	(1, '1', '221', '0000000', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(2, '2', '222', '0000000', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(3, '3', '223', '0000021', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(4, '4', '223', '0000025', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(5, '5', '223', '0000026', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(6, '6', '223', '0000028', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(7, '7', '223', '0000029', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(8, '8', '224', '0000000', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(9, '9', '225', '0000000', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(10, '10', '226', '0000000', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(11, '11', '227', '0000000', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(12, '12', '229', '0000000', NULL, NULL, '', '', '', '', ''),
	(13, '13', '267', '0000000', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(14, '14', '244', '0000000', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(15, '15', '310', '0000000', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(16, '16', '341', '0000000', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(17, '17', '342', '0000000', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(18, '18', '343', '0000000', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(19, '19', '344', '0000000', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(20, '20', '345', '0000000', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(21, '21', '346', '0000000', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(22, '22', '349', '0000000', NULL, NULL, NULL, NULL, NULL, NULL, NULL);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
