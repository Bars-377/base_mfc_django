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

-- Дамп структуры для таблица basemfcdjango.auth_user
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Дамп данных таблицы basemfcdjango.auth_user: ~10 rows (приблизительно)
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
	(4, 'pbkdf2_sha256$870000$Hbab3vIXks3P91BjPO38nA$IT98nqTCP/5c4TP/BXgAUQv2LkaYjllZTvOngO1eLCI=', '2025-02-13 07:49:17.584795', 1, 'bars_377', '', '', 'rollerkrick@gmail.com', 1, 1, '2024-10-24 08:00:42.000000'),
	(13, 'pbkdf2_sha256$870000$ingYWJFsqgkloR5kSa4LPO$+98XFAQL7tYArfhY0on7w5HRJBj9uz7t9OJMmeygKCA=', NULL, 0, 'gavrilov', '', '', 'gavrilov@mail.ru', 0, 1, '2025-02-13 07:39:22.000000'),
	(14, 'pbkdf2_sha256$870000$oVZ5A5NVqV2IALTJzGrm35$P3+astxXI0CgFDltlTlYkbC5ZZfjaFli30gMftkUgO4=', NULL, 0, 'rusanova', '', '', 'rusanova@mail.ru', 0, 1, '2025-02-13 07:39:36.000000'),
	(15, 'pbkdf2_sha256$870000$hvLbLRF6hOOCZ5VWm17KEM$PKMgS28luwkn+MdjBRz6sNn4uW5nsAZMoOfDjkwGKTE=', NULL, 0, 'zaharko', '', '', 'zaharko@mail.ru', 0, 1, '2025-02-13 07:39:52.000000'),
	(16, 'pbkdf2_sha256$870000$BfWKgHOi32Wrq9seSSeeRJ$WOKKW7nRr1KTjg6ZA3HgBszsDNDjGpU3Z4ZoL9uNUOM=', NULL, 0, 'dorjieva', '', '', 'dorjieva@mail.ru', 0, 1, '2025-02-13 07:40:04.000000'),
	(17, 'pbkdf2_sha256$870000$fiAYdDdlXZr8p5uJTaeFH1$3+/1o5bVJc8v9eXjp+AKnMZfVLhWSW4wxtm3pIquXfE=', NULL, 0, 'safronova', '', '', 'safronova@mail.ru', 0, 1, '2025-02-13 07:40:16.000000'),
	(18, 'pbkdf2_sha256$870000$pkbpA40W8qfiRL5nSvOwwx$GdzrHsZxCMMcCX8dR1+nBLFr2syKNnjNFzEbtIt8ggA=', '2025-02-13 07:56:07.339585', 0, 'schastniy', '', '', 'schastniy@mail.ru', 0, 1, '2025-02-13 07:40:26.000000'),
	(19, 'pbkdf2_sha256$870000$m1RrWjU1Qfl91if7jaO8U3$UiG7ZYZ0lu1cFiSX1K5tSF2CCpw67g5Mx4+GH0R3LTI=', NULL, 0, 'goremiko', '', '', 'goremiko@mail.ru', 0, 1, '2025-02-13 07:40:36.000000'),
	(20, 'pbkdf2_sha256$870000$fbR6vNMdN2s41z55jHnTFV$39t7YangpPhKbJvm43OXnk9YD4UVpCFo4OqCLtNpO/A=', '2025-02-13 07:50:53.539008', 0, 'stepankova', '', '', 'stepankova@mail.ru', 0, 1, '2025-02-13 07:40:47.000000'),
	(21, 'pbkdf2_sha256$870000$AN70xdrZzfK5HQX76UbnjS$K/1bAZD9fgaSKvFKNLlKZuQ7HLFaJh1IS4v7igQay1U=', NULL, 0, 'girnova', '', '', 'girnova@mail.ru', 0, 1, '2025-02-13 07:41:00.000000');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
