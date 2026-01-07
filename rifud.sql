-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 07, 2026 at 08:07 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rifud`
--

-- --------------------------------------------------------

--
-- Table structure for table `food_waste`
--

CREATE TABLE `food_waste` (
  `id` int NOT NULL,
  `name` varchar(150) NOT NULL,
  `description` varchar(255) NOT NULL,
  `foto` varchar(100) DEFAULT NULL,
  `price` int NOT NULL,
  `stock` int NOT NULL,
  `type` enum('waste','edible') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `user_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `food_waste`
--

INSERT INTO `food_waste` (`id`, `name`, `description`, `foto`, `price`, `stock`, `type`, `user_id`) VALUES
(1, 'Sayur Kangkung', 'Sayur kangkung segar sisa dari pasar pagi.', 'uploads/food_waste/e4b6a9c6ede34b24b0c32284b6156fc7.jpg', 3000, 9, 'waste', 6),
(2, 'Roti Gandum', 'Roti gandum mendekati tanggal kadaluarsa, masih layak konsumsi.', 'uploads/food_waste/e4b6a9c6ede34b24b0c32284b6156fc7.jpg', 5000, 29, 'edible', 5),
(3, 'Ayam Ungkep', 'Ayam ungkep dari catering, tidak habis terjual hari ini.', 'uploads/food_waste/6410edf4b95b4a01bfeb17625bc8f0ce.jpg', 15000, 27, 'waste', 4),
(4, 'Sambal Bakar Level 500', 'Roti gandum mendekati tanggal kadaluarsa, masih layak konsumsi.', 'uploads/food_waste/6410edf4b95b4a01bfeb17625bc8f0ce.jpg', 9000, 98, 'edible', 6),
(7, 'Burger King', 'Makanan Pagi BKing', 'uploads/food_waste/e4b6a9c6ede34b24b0c32284b6156fc7.jpg', 10000, 16, 'edible', 4),
(8, 'Bakso 1 Porsi', 'Bakso 4 Biji + Bihun + Gorengan. Catatan ini sisa bakso dari 2 hari yang lalu', 'uploads/food_waste/e4b6a9c6ede34b24b0c32284b6156fc7.jpg', 6000, 10, 'edible', 10);

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int NOT NULL,
  `qty` int NOT NULL,
  `price_total` int NOT NULL,
  `transaction_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `status` enum('pending','waiting','ready','success','declined','cancel') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT 'pending',
  `payment_type` enum('QRIS','COD') DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `food_waste_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `qty`, `price_total`, `transaction_date`, `status`, `payment_type`, `user_id`, `food_waste_id`) VALUES
(4, 2, 6000, '2025-12-10 12:51:31', 'success', 'QRIS', 9, 1),
(5, 1, 5000, '2025-12-10 12:51:31', 'waiting', 'COD', 9, 2),
(6, 3, 45000, '2025-12-10 12:51:31', 'success', 'QRIS', 11, 3),
(7, 2, 6000, '2025-12-25 16:31:56', 'success', 'QRIS', 11, 3),
(8, 5, 50000, '2025-12-25 16:42:49', 'waiting', 'QRIS', 9, 7),
(10, 2, 20000, '2025-12-28 21:08:01', 'pending', 'QRIS', 9, 8),
(28, 1, 10000, '2025-12-31 14:58:16', 'waiting', 'QRIS', 17, 7),
(29, 1, 10000, '2025-12-31 14:58:49', 'waiting', 'QRIS', 17, 7),
(30, 1, 5000, '2025-12-31 15:15:29', 'success', 'QRIS', 17, 2),
(31, 1, 10000, '2025-12-31 15:15:34', 'pending', 'QRIS', 17, 7),
(32, 2, 18000, '2026-01-07 00:54:45', 'success', 'QRIS', 11, 4),
(33, 3, 9000, '2026-01-07 00:57:02', 'success', 'QRIS', 17, 1),
(34, 3, 45000, '2026-01-07 11:12:41', 'success', 'QRIS', 18, 3),
(35, 1, 5000, '2026-01-07 11:12:59', 'success', 'QRIS', 18, 2);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `foto` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(350) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `longitude` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `latitude` varchar(150) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `open_time` time DEFAULT NULL,
  `closed_time` time DEFAULT NULL,
  `role` enum('client','resto') DEFAULT 'client'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `phone`, `foto`, `email`, `password`, `address`, `longitude`, `latitude`, `city`, `open_time`, `closed_time`, `role`) VALUES
(4, 'Budi', '029837629854', 'budi.jpg', 'budi@gmail.com', 'scrypt:32768:8:1$ary6hz7ZojRY27LB$37a1763ebbdd89738f06cbb84d4391dcf989a6b0aac8428ccb4581347473c14ab9775c66baf1e299c304739b7685fb2bc9346777aab382d3c231177f51f55521', 'Jalan Kaliurang dekat UII', ' 110.35562335280703', '-7.745519585333781', 'Yogyakarta', '07:00:00', '23:00:00', 'resto'),
(5, 'Siti Aminah', '085612341234', 'siti.png', 'siti@example.com', 'scrypt:32768:8:1$z31Gl1rqTcGNlzFo$9f946bbe402a88b9c1175807b2570120a11c01c8f9d55c77780eaeade01943efa166589f1c95e40906aba0aecd41ed4a33e5fb61870b9b00fa7bd063a4c9779f', 'Jl. Melati No. 25', '110.414937', '-7.801194', 'yogyakarta', '07:00:00', '20:00:00', 'resto'),
(6, 'Agus Saputra', '082198765432', 'agus.jpeg', 'agus@example.com', 'scrypt:32768:8:1$YosKoMSemRdGDY1H$c6b3282bb18b96f33d5d9f882965fc1984436e613eaaf203f448234aa7285ab792a366f08b0ebb29380380e18506934a840e3c0ee8c7dda35803bc924ce9dc0e', 'Jl. Kenanga No. 7', '110.3542465881601', '-7.746680095458424', 'surabaya', '08:00:00', '22:00:00', 'resto'),
(7, 'dudung resto', NULL, NULL, 'dudung@gmail.com', 'scrypt:32768:8:1$XehyFzuJRcyRIg9Q$17c6774e90b3e307f18813017fb514932ef23ac3bb93a4256b82a9769b44a1fb1e47e3ecb91eced2283e3ef29502adee69d23ef78fd5af9d0ed3396c9168e310', 'Jl Raya Ciamis', NULL, NULL, 'Ciamis', NULL, NULL, 'resto'),
(8, 'tatang resto', NULL, NULL, 'tatang@gmail.com', 'scrypt:32768:8:1$17A7xFwMewcsGkl9$6a3a752651a69f2a0dc5dff211f19268684c018db4c31979ac3a149d819b720f4ec5a65d8fa503844552bf4e6b78b8c77ae44bf0bae52a6274a7c0ade2535226', 'Jalan Raya Bandung', NULL, NULL, 'Bandung', NULL, NULL, 'resto'),
(9, 'samsuu', NULL, NULL, 'samsu@gmail.com', 'scrypt:32768:8:1$JG3Zl9vZVM4gcWtV$bf15628d0db9760c2e18a011a41a4a8033d698053bddba8f7333a7d85374f052104ef256f5326279edaa028c0db05454c14ee9dc2fa937eac7edd8f927e051d8', NULL, NULL, NULL, NULL, NULL, NULL, 'client'),
(10, 'kemal resto', NULL, NULL, 'kemal@gmail.com', 'scrypt:32768:8:1$AxvHDZDFpknaCWtv$0e82667f1cfa02ae53ed32d2e18edf276fb5465dcf74a3153460b0029e6f5ed68657198f4d395c3b904dd53f7d3e532a54f020b99dbf0cfcf993a2c7ac3d6c05', 'Jalan Raya Bandung Barat', '110.3544460886057', '-7.7453434101530565', 'Bandung', NULL, NULL, 'resto'),
(11, 'sopoooo', '083782472', 'uploads/users/1f4a97d291f44e058343f9e0d3332681.jpg', 'sopo@gmail.com', 'scrypt:32768:8:1$CqNGVEekDBZTTslN$b9e87d5104bcf566411048e4ab7df2c31c03aac514e0fc5b2ae6424305d1837627b943492b3f56df5bbbd3377959eaec6971fe5820617d89b9998ba7e0f2f8a0', 'Jalan Cianjur Utara', '-92887yds.e907.62', '-87932, -832djs', 'Cianjur', '07:00:00', '21:00:00', 'client'),
(12, 'Sesilia', '081234567890', NULL, 'sesil@gmail.com', 'scrypt:32768:8:1$0smiKKxzTvKpq6ZA$711edd805cd0d8212e15e1856d9b6ea5f315e7a85a1e3834215896f9ca38b64168192bbba73130797d86f1c3ada965a6fd4c36a2658ed4d573880f325e2d3fca', 'Jalan UGM dekat UGM', NULL, NULL, 'Yogyakarta', NULL, NULL, 'client'),
(14, 'Akmal Yunus', NULL, NULL, 'kamal@gmail.com', 'scrypt:32768:8:1$Rpq18rIbwJ8tGNFd$5434b41751ecaae7657236b46fad60b6865e1dd3f74a4872b77490c8269450b02ea0aef99ce5b94ced81815d9c661127dabe6dc6f44ea4b675554e288113fc1f', 'Jl Kronggahan Dsn Kronggahan', NULL, NULL, 'Sleman', NULL, NULL, 'resto'),
(15, 'Dadang', NULL, NULL, 'dadang@gmail.com', 'scrypt:32768:8:1$DCZYX2NwObDddhVU$062afb6abd72d3a32b60fece6a95eee6e13c2cb77a64a457928be8ee19b6213590e658514f0780adb18951178df646488aef265e56f55e9e54ffaf1d0aa774d3', 'Jl Kabupaten Sleman', NULL, NULL, 'Sleman', NULL, NULL, 'client'),
(16, 'Samsa Resto', NULL, NULL, 'samsa@gmail.com', 'scrypt:32768:8:1$v2TeCVxbge9wiAvo$4120e9326060bacd4d36e21cb099fe01abbb9023127c101a31367bb866915fe83b7ff0a178268d8d4e238cbcd6a397e69293670323b907a038b61406d1e1a02d', 'Jl Raya Sleman dekat Kronggahan', NULL, NULL, 'Sleman', NULL, NULL, 'resto'),
(17, 'Afif Murtadho', NULL, NULL, 'afif@gmail.com', 'scrypt:32768:8:1$uNkojvTWPWf4AEIP$fad27ee1fe1113577adba6bf9d32a9ce63c31fba6f7a49cf9a4c04fc177bb1588b81dcf90350714b835501f41c57b7238795bcd43281b5416a2ab653b7416a25', NULL, NULL, NULL, NULL, NULL, NULL, 'client'),
(18, 'Zidane', NULL, NULL, 'zidan@gmail.com', 'scrypt:32768:8:1$Itb2sGmER86ZZqK3$cb1a7585ca0ec3564191bded872a20d67ae121830ee4b3a59a590b3eaf1572a34491b8cc3c16bd1c0c8572022330c4634a3fbe7f7f54139a6fc3f99e0544d3d2', NULL, NULL, NULL, NULL, NULL, NULL, 'client');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `food_waste`
--
ALTER TABLE `food_waste`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_user_id` (`user_id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_user_id_in_transaction` (`user_id`),
  ADD KEY `fk_food_waste_id` (`food_waste_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `food_waste`
--
ALTER TABLE `food_waste`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `food_waste`
--
ALTER TABLE `food_waste`
  ADD CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT;

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `fk_food_waste_id` FOREIGN KEY (`food_waste_id`) REFERENCES `food_waste` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  ADD CONSTRAINT `fk_user_id_in_transaction` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
