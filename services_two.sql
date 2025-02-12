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

-- Дамп структуры для таблица basemfcdjango.services_vault
CREATE TABLE IF NOT EXISTS `services_two` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `id_id` text COLLATE utf8mb4_general_ci,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `KOSGU` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `DopFC` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `budget_limit` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `off_budget_limit` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `budget_planned` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `off_budget_planned` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `budget_bargaining` text COLLATE utf8mb4_general_ci,
  `off_budget_bargaining` text COLLATE utf8mb4_general_ci,
  `budget_concluded` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `off_budget_concluded` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `budget_completed` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `off_budget_completed` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `budget_execution` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `off_budget_execution` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `budget_remainder` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `off_budget_remainder` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `budget_plans` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `off_budget_plans` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `color` text COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Дамп данных таблицы basemfcdjango.services_vault: ~22 rows (приблизительно)
INSERT INTO `services_two` (`id`, `id_id`, `name`, `KOSGU`, `DopFC`, `budget_limit`, `off_budget_limit`, `budget_planned`, `off_budget_planned`, `budget_bargaining`, `off_budget_bargaining`, `budget_concluded`, `off_budget_concluded`, `budget_completed`, `off_budget_completed`, `budget_execution`, `off_budget_execution`, `budget_remainder`, `off_budget_remainder`, `budget_plans`, `off_budget_plans`, `color`) VALUES
	(1, '1', 'Связь', '221', '0000000', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
	(2, '2', 'Транспортные расходы', '222', '0000000', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
	(3, '3', 'ТКО', '223', '0000021', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
	(4, '4', 'Тепло', '223', '0000025', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
	(6, '6', 'Газ', '223', '0000026', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
	(8, '8', 'Э/э', '223', '0000028', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
	(10, '10', 'Вода', '223', '0000029', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
	(11, '11', 'Аренда', '224', '0000000', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
	(12, '12', 'Содержание', '225', '0000000', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
	(13, '13', 'Прочие', '226', '0000000', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
	(14, '14', 'Страхование', '227', '0000000', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
	(15, '15', 'Аренда ЗУ', '229', '0000000', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
	(16, '16', 'Санаторно-курортное лечение', '267', '0000000', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
	(17, '17', 'Штрафы', '244', '0000000', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
	(18, '18', 'ОС', '310', '0000000', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
	(19, '19', 'Лекарственные препараты и материалы', '341', '0000000', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
	(20, '20', 'Продукты питания', '342', '0000000', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
	(21, '21', 'ГСМ', '343', '0000000', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
	(23, '23', 'Строительные материалы', '344', '0000000', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
	(24, '24', 'Спецодежда', '345', '0000000', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
	(25, '25', 'Прочие материалы', '346', '0000000', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
	(26, '26', 'Прочие материалы однократного применения', '349', '0000000', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
  (27, '27', 'Связь', '221', '0000150', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
  (28, '28', 'Прочие', '226', '0000150', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
  (29, '29', 'ОС', '310', '0000150', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
  (30, '30', 'Прочие материалы', '346', '0000150', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
  (31, '31', 'Содержание', '225', '0000150', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
