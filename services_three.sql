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


-- Дамп структуры базы данных basemfcdjango_2025
CREATE DATABASE IF NOT EXISTS `basemfcdjango_2025` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `basemfcdjango_2025`;

-- Дамп структуры для таблица basemfcdjango_2025.services_two
CREATE TABLE IF NOT EXISTS `services_three` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `id_id` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `KOSGU` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `DopFC` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `budget_planned_old` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `off_budget_planned_old` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `budget_planned` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `off_budget_planned` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `budget_concluded` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `off_budget_concluded` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `budget_remainder` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `off_budget_remainder` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `color` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Дамп данных таблицы basemfcdjango_2025.services_two: ~26 rows (приблизительно)
INSERT INTO `services_three` (`id`, `id_id`, `KOSGU`, `DopFC`, `budget_planned_old`, `off_budget_planned_old`, `budget_planned`, `off_budget_planned`, `budget_concluded`, `off_budget_concluded`, `budget_remainder`, `off_budget_remainder`, `color`) VALUES
	(1, '1', '221', '0000000', '', '', '', '', '', '', '', '', ''),
	(2, '2', '222', '0000000', '', '', '', '', '', '', '', '', ''),
	(3, '3', '223', '0000021', '', '', '', '', '', '', '', '', ''),
	(4, '4', '223', '0000025', '', '', '', '', '', '', '', '', ''),
	(5, '5', '223', '0000026', '', '', '', '', '', '', '', '', ''),
	(6, '6', '223', '0000028', '', '', '', '', '', '', '', '', ''),
	(7, '7', '223', '0000029', '', '', '', '', '', '', '', '', ''),
	(8, '8', '224', '0000000', '', '', '', '', '', '', '', '', ''),
	(9, '9', '225', '0000000', '', '', '', '', '', '', '', '', ''),
	(10, '10', '226', '0000000', '', '', '', '', '', '', '', '', ''),
	(11, '11', '227', '0000000', '', '', '', '', '', '', '', '', ''),
	(12, '12', '229', '0000000', '', '', '', '', '', '', '', '', ''),
	(13, '13', '267', '0000000', '', '', '', '', '', '', '', '', ''),
	(14, '14', '244', '0000000', '', '', '', '', '', '', '', '', ''),
	(15, '15', '310', '0000000', '', '', '', '', '', '', '', '', ''),
	(16, '16', '341', '0000000', '', '', '', '', '', '', '', '', ''),
	(17, '17', '342', '0000000', '', '', '', '', '', '', '', '', ''),
	(18, '18', '343', '0000000', '', '', '', '', '', '', '', '', ''),
	(19, '19', '344', '0000000', '', '', '', '', '', '', '', '', ''),
	(20, '20', '345', '0000000', '', '', '', '', '', '', '', '', ''),
	(21, '21', '346', '0000000', '', '', '', '', '', '', '', '', ''),
	(22, '22', '349', '0000000', '', '', '', '', '', '', '', '', ''),
	(23, '23', '221', '0000150', '', '', '', '', '', '', '', '', ''),
	(24, '24', '226', '0000150', '', '', '', '', '', '', '', '', ''),
	(25, '25', '310', '0000150', '', '', '', '', '', '', '', '', ''),
	(26, '26', '346', '0000150', '', '', '', '', '', '', '', '', ''),
	(27, '27', '225', '0000150', '', '', '', '', '', '', '', '', '');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
