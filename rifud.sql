-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Waktu pembuatan: 28 Des 2025 pada 10.37
-- Versi server: 8.0.30
-- Versi PHP: 8.1.10

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
-- Struktur dari tabel `food_waste`
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
-- Dumping data untuk tabel `food_waste`
--

INSERT INTO `food_waste` (`id`, `name`, `description`, `foto`, `price`, `stock`, `type`, `user_id`) VALUES
(1, 'Sayur Kangkung', 'Sayur kangkung segar sisa dari pasar pagi.', 'kangkung.jpg', 3000, 12, 'waste', 6),
(2, 'Roti Gandum', 'Roti gandum mendekati tanggal kadaluarsa, masih layak konsumsi.', 'roti_gandum.jpg', 5000, 8, 'edible', 5),
(3, 'Ayam Ungkep', 'Ayam ungkep dari catering, tidak habis terjual hari ini.', 'ayam_ungkep.jpg', 15000, 5, 'waste', 4),
(4, 'Sambal Bakar Level 500', 'Roti gandum mendekati tanggal kadaluarsa, masih layak konsumsi.', 'uploads/food_waste/6410edf4b95b4a01bfeb17625bc8f0ce.jpg', 9000, 100, 'edible', 6),
(7, 'Burger King', 'Makanan Pagi BKing', 'bking.jpg', 10000, 25, 'edible', 4),
(8, 'Bakso 1 Porsi', 'Bakso 4 Biji + Bihun + Gorengan. Catatan ini sisa bakso dari 2 hari yang lalu', 'uploads/food_waste/e4b6a9c6ede34b24b0c32284b6156fc7.jpg', 6000, 10, 'edible', 10);

-- --------------------------------------------------------

--
-- Struktur dari tabel `transactions`
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
-- Dumping data untuk tabel `transactions`
--

INSERT INTO `transactions` (`id`, `qty`, `price_total`, `transaction_date`, `status`, `payment_type`, `user_id`, `food_waste_id`) VALUES
(4, 2, 6000, '2025-12-10 12:51:31', 'cancel', 'QRIS', 6, 1),
(5, 1, 5000, '2025-12-10 12:51:31', 'waiting', 'COD', 8, 2),
(6, 3, 45000, '2025-12-10 12:51:31', 'success', 'QRIS', 6, 3),
(7, 2, 6000, '2025-12-25 16:31:56', 'success', 'QRIS', 11, 3),
(8, 5, 50000, '2025-12-25 16:42:49', 'waiting', 'COD', 9, 7);

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
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
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id`, `name`, `phone`, `foto`, `email`, `password`, `address`, `longitude`, `latitude`, `city`, `open_time`, `closed_time`, `role`) VALUES
(4, 'Budi Santoso', '081234567890', 'budi.jpg', 'budi@example.com', 'scrypt:32768:8:1$ary6hz7ZojRY27LB$37a1763ebbdd89738f06cbb84d4391dcf989a6b0aac8428ccb4581347473c14ab9775c66baf1e299c304739b7685fb2bc9346777aab382d3c231177f51f55521', 'Jl. Merdeka No. 10', '106.827153', '-6.175392', 'jakarta', '07:00:00', '23:00:00', 'resto'),
(5, 'Siti Aminah', '085612341234', 'siti.png', 'siti@example.com', 'siti123', 'Jl. Melati No. 25', '110.414937', '-7.801194', 'yogyakarta', '07:00:00', '20:00:00', 'resto'),
(6, 'Agus Saputra', '082198765432', 'agus.jpeg', 'agus@example.com', 'agus123', 'Jl. Kenanga No. 7', '112.750833', '-7.250445', 'surabaya', '08:00:00', '22:00:00', 'client'),
(7, 'dudung resto', NULL, NULL, 'dudung@gmail.com', 'scrypt:32768:8:1$XehyFzuJRcyRIg9Q$17c6774e90b3e307f18813017fb514932ef23ac3bb93a4256b82a9769b44a1fb1e47e3ecb91eced2283e3ef29502adee69d23ef78fd5af9d0ed3396c9168e310', 'Jl Raya Ciamis', NULL, NULL, 'Ciamis', NULL, NULL, 'client'),
(8, 'tatang resto', NULL, NULL, 'tatang@gmail.com', 'scrypt:32768:8:1$17A7xFwMewcsGkl9$6a3a752651a69f2a0dc5dff211f19268684c018db4c31979ac3a149d819b720f4ec5a65d8fa503844552bf4e6b78b8c77ae44bf0bae52a6274a7c0ade2535226', 'Jalan Raya Bandung', NULL, NULL, 'Bandung', NULL, NULL, 'client'),
(9, NULL, NULL, NULL, 'samsu@gmail.com', 'scrypt:32768:8:1$JG3Zl9vZVM4gcWtV$bf15628d0db9760c2e18a011a41a4a8033d698053bddba8f7333a7d85374f052104ef256f5326279edaa028c0db05454c14ee9dc2fa937eac7edd8f927e051d8', NULL, NULL, NULL, NULL, NULL, NULL, 'client'),
(10, 'kemal resto', NULL, NULL, 'kemal@gmail.com', 'scrypt:32768:8:1$AxvHDZDFpknaCWtv$0e82667f1cfa02ae53ed32d2e18edf276fb5465dcf74a3153460b0029e6f5ed68657198f4d395c3b904dd53f7d3e532a54f020b99dbf0cfcf993a2c7ac3d6c05', 'Jalan Raya Bandung Barat', NULL, NULL, 'Bandung', NULL, NULL, 'resto'),
(11, 'sopoooo', '083782472', 'uploads/users/a5270d9f5f094065a3f87dc2d0329a7f.jpg', 'sopo@gmail.com', 'scrypt:32768:8:1$L9Q00UwWShGrVVYe$0dee1d99c006790ed743868293d3e439598aa6bf21b5425acbf972c114dd40e776521fac750d2d44e88b11025a028f43c987da34bcc0229d2821978741271b06', 'Jalan Cianjur Utara', '-92887yds.e907.62', '-87932, -832djs', 'Cianjur', '07:00:00', '21:00:00', 'client');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `food_waste`
--
ALTER TABLE `food_waste`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_user_id` (`user_id`);

--
-- Indeks untuk tabel `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_user_id_in_transaction` (`user_id`),
  ADD KEY `fk_food_waste_id` (`food_waste_id`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `food_waste`
--
ALTER TABLE `food_waste`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT untuk tabel `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `food_waste`
--
ALTER TABLE `food_waste`
  ADD CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT;

--
-- Ketidakleluasaan untuk tabel `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `fk_food_waste_id` FOREIGN KEY (`food_waste_id`) REFERENCES `food_waste` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  ADD CONSTRAINT `fk_user_id_in_transaction` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
