-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Май 10 2020 г., 20:34
-- Версия сервера: 8.0.20
-- Версия PHP: 7.2.24-0ubuntu0.18.04.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `scpbot`
--

-- --------------------------------------------------------

--
-- Структура таблицы `Currency`
--

CREATE TABLE `Currency` (
  `id` int NOT NULL,
  `code_name` text,
  `for_once` int DEFAULT NULL,
  `full_name` text,
  `price` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Currency`
--

INSERT INTO `Currency` (`id`, `code_name`, `for_once`, `full_name`, `price`) VALUES
(1, 'AUD', 1, 'Австралийский доллар', 48.0984),
(2, 'GBP', 1, 'Фунт стерлингов Соединенного королевства', 91.5059),
(3, 'BYN', 1, 'Белорусский рубль', 30.2607),
(4, 'DKK', 1, 'Датская крона', 10.7191),
(5, 'USD', 1, 'Доллар США', 73.8725),
(6, 'EUR', 1, 'Евро', 80.0039),
(7, 'KZT', 100, 'Казахстанских тенге', 17.507),
(8, 'CAD', 1, 'Канадский доллар', 52.9248),
(9, 'CNY', 1, 'Китайский юань', 10.4346),
(10, 'NOK', 10, 'Норвежских крон', 72.0237),
(11, 'XDR', 1, 'СДР (специальные права заимствования)', 100.544),
(12, 'SGD', 1, 'Сингапурский доллар', 52.2547),
(13, 'TRY', 1, 'Турецкая лира', 10.3937),
(14, 'UAH', 10, 'Украинских гривен', 27.5448),
(15, 'SEK', 10, 'Шведских крон', 75.3724),
(16, 'CHF', 1, 'Швейцарский франк', 75.938),
(17, 'JPY', 100, 'Японских иен', 69.4813),
(18, 'AZN', 1, 'Азербайджанский манат', 43.5441),
(19, 'AMD', 100, 'Армянских драмов', 15.2377),
(20, 'BGN', 1, 'Болгарский лев', 40.8836),
(21, 'BRL', 1, 'Бразильский реал', 12.6659),
(22, 'HUF', 100, 'Венгерских форинтов', 22.8842),
(23, 'INR', 100, 'Индийских рупий', 97.7829),
(24, 'KGS', 100, 'Киргизских сомов', 93.5934),
(25, 'MDL', 10, 'Молдавских леев', 41.4316),
(26, 'PLN', 1, 'Польский злотый', 17.5598),
(27, 'RON', 1, 'Румынский лей', 16.5652),
(28, 'TJS', 10, 'Таджикских сомони', 71.9654),
(29, 'TMT', 1, 'Новый туркменский манат', 21.1366),
(30, 'UZS', 10000, 'Узбекских сумов', 72.8238),
(31, 'CZK', 10, 'Чешских крон', 29.3424),
(32, 'ZAR', 10, 'Южноафриканских рэндов', 39.9535),
(33, 'KRW', 1000, 'Вон Республики Корея', 60.5314);

-- --------------------------------------------------------

--
-- Структура таблицы `Sources`
--

CREATE TABLE `Sources` (
  `Name` tinytext NOT NULL,
  `URL` tinytext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Sources`
--

INSERT INTO `Sources` (`Name`, `URL`) VALUES
('RU', 'http://scpfoundation.net/'),
('ENG', 'http://scp-wiki.net/');

-- --------------------------------------------------------

--
-- Структура таблицы `Users`
--

CREATE TABLE `Users` (
  `id` int NOT NULL,
  `chat_id` int NOT NULL,
  `source` text NOT NULL,
  `last_finding` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `favorite` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `special_functions` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Users`
--

INSERT INTO `Users` (`id`, `chat_id`, `source`, `last_finding`, `favorite`, `special_functions`) VALUES
(1, 666314796, 'ENG', 'None', 'None', 1),
(2, 500268815, 'ENG', NULL, 'None,876,682', 0),
(3, 830099659, 'RU', NULL, 'None,456', 0),
(4, 971875675, 'ENG', NULL, NULL, 0),
(5, 1035500953, 'ENG', NULL, 'None,173', 0),
(6, 618225990, 'RU', NULL, NULL, 0),
(7, 998456737, 'RU', NULL, 'None,079', 0),
(8, 1183228906, 'ENG', NULL, 'None,096', 0);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `Currency`
--
ALTER TABLE `Currency`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `Currency`
--
ALTER TABLE `Currency`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT для таблицы `Users`
--
ALTER TABLE `Users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
