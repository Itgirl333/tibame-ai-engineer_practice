SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- --------------------------------------------------------

--
-- 資料表結構 `member`
--

CREATE TABLE `member` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `birthday` date NOT NULL DEFAULT '0000-00-00',
  `address` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 傾印資料表的資料 `member`
--

INSERT INTO `member` (`id`, `name`, `birthday`, `address`) VALUES
(1, '陳文在', '1993-11-01', '台北市中山區'),
(2, '蕭宇殷', '1990-05-22', '新北市板橋區'),
(3, '藍天晴', '1997-02-10', '桃園市中壢區'),
(4, '林致世', '1992-10-10', '新竹縣竹東鎮'),
(5, '呂來來', '1997-03-01', '新北市萬里區'),
(10, '蔡杉智', '1993-07-05', '台北市大安區'),
(11, '姚文武', '1995-07-11', '台北市北投區'),
(12, '關自如', '1996-10-21', '新北市永和區'),
(20, '周怡敏', '1988-12-11', '新北市三重區'),
(21, '白依依', '1985-01-05', '新北市新店區'),
(22, '鄭芷茵', '1993-02-10', '新北市林口區');

-- --------------------------------------------------------

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `member`
--
ALTER TABLE `member`
  ADD PRIMARY KEY (`id`);


--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `member`
--
ALTER TABLE `member`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
