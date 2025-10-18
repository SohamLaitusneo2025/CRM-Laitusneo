-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 23, 2025 at 11:57 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `crm_laitusneo`
--

-- --------------------------------------------------------

--
-- Table structure for table `deals`
--

CREATE TABLE `deals` (
  `id` int(11) NOT NULL,
  `client_name` varchar(100) NOT NULL,
  `mobile` varchar(20) NOT NULL,
  `email` varchar(120) NOT NULL,
  `product_name` varchar(200) NOT NULL,
  `price` varchar(50) NOT NULL,
  `last_activity` date NOT NULL,
  `status` enum('New','Qualifying','Demo Scheduled','Pending Commitment','In Negotiation','WON','LOST') DEFAULT NULL,
  `previous_status` enum('New','Qualifying','Demo Scheduled','Pending Commitment','In Negotiation','WON','LOST') DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `salesman_id` int(11) NOT NULL,
  `source_lead_id` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `deals`
--

INSERT INTO `deals` (`id`, `client_name`, `mobile`, `email`, `product_name`, `price`, `last_activity`, `status`, `previous_status`, `created_at`, `updated_at`, `salesman_id`, `source_lead_id`) VALUES
(1, 'Enhanced Test Client', '+1234567890', 'enhanced.client@example.com', 'Enhanced Test Product', '₹2,00,000', '2025-09-22', 'WON', 'Qualifying', '2025-09-22 09:56:08', '2025-09-22 09:56:16', 3, NULL),
(2, 'Enhanced Test Client', '+1234567890', 'enhanced.client@example.com', 'Enhanced Test Product', '₹2,00,000', '2025-09-22', 'WON', 'Qualifying', '2025-09-22 09:57:36', '2025-09-22 09:57:44', 4, NULL),
(3, 'Second Test Client', '+1234567891', 'second.client@example.com', 'Second Test Product', '₹1,50,000', '2025-09-22', 'Pending Commitment', 'In Negotiation', '2025-09-22 09:57:46', '2025-09-22 09:57:57', 4, NULL),
(4, 'Laitusneo Technologies', '8900569341', 'soham@gmail.com', 'E-School', '₹10,000', '2025-09-22', 'WON', 'LOST', '2025-09-22 10:49:34', '2025-09-22 10:57:32', 6, NULL),
(10, 'Test Lead', '1234567890', 'test@example.com', 'Test Product', '₹1,000', '2025-09-22', 'New', NULL, '2025-09-22 12:29:32', '2025-09-22 12:29:32', 3, 'L004'),
(11, 'Test Client', '+1234567890', 'client1758602702@test.com', 'Test Product', '₹10,000', '2025-09-23', 'WON', 'New', '2025-09-23 04:45:12', '2025-09-23 04:45:16', 12, 'L007'),
(13, 'XYZ Company', '1234567890', 'xyz@gmail.com', 'E-School', '₹1,000', '2025-09-23', 'WON', 'Pending Commitment', '2025-09-23 07:18:51', '2025-09-23 09:17:55', 7, 'L009');

-- --------------------------------------------------------

--
-- Table structure for table `leads`
--

CREATE TABLE `leads` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(120) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `product_name` varchar(200) NOT NULL,
  `status` enum('New','Contacted','Qualified','Accepted','Rejected','Won','Lost','Pipelined') DEFAULT 'New',
  `value` float DEFAULT NULL,
  `last_contact` date DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `salesman_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `leads`
--

INSERT INTO `leads` (`id`, `name`, `email`, `contact_number`, `product_name`, `status`, `value`, `last_contact`, `created_at`, `updated_at`, `salesman_id`) VALUES
(4, 'Test Lead', 'test@example.com', '1234567890', 'Test Product', 'Pipelined', 1000, NULL, '2025-09-22 12:29:22', '2025-09-22 12:29:32', 3),
(5, 'API Test Lead', 'apitest@example.com', '9876543210', 'API Product', 'New', 2000, NULL, '2025-09-22 12:31:03', '2025-09-22 12:31:03', 8),
(6, 'Test Client', 'client@test.com', '+1234567890', 'Test Product', 'Accepted', 10000, NULL, '2025-09-23 04:44:06', '2025-09-23 04:44:08', 10),
(7, 'Test Client', 'client1758602702@test.com', '+1234567890', 'Test Product', 'Won', 10000, NULL, '2025-09-23 04:45:10', '2025-09-23 04:45:16', 12),
(9, 'XYZ Company', 'xyz@gmail.com', '1234567890', 'E-School', 'Won', 1000, NULL, '2025-09-23 07:03:01', '2025-09-23 09:17:55', 7);

-- --------------------------------------------------------

--
-- Table structure for table `meetings`
--

CREATE TABLE `meetings` (
  `id` int(11) NOT NULL,
  `type` enum('offline','online') NOT NULL,
  `client_name` varchar(100) NOT NULL,
  `mobile_number` varchar(20) NOT NULL,
  `email` varchar(120) NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `venue` varchar(200) DEFAULT NULL,
  `platform` varchar(50) DEFAULT NULL,
  `status` enum('Scheduled','Completed','Cancelled','Postponed') NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `salesman_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `meetings`
--

INSERT INTO `meetings` (`id`, `type`, `client_name`, `mobile_number`, `email`, `date`, `time`, `venue`, `platform`, `status`, `created_at`, `updated_at`, `salesman_id`) VALUES
(2, 'offline', 'Soham Karmakar', '8900569341', 'soham@gmail.com', '2025-09-23', '14:36:00', 'Etawah, Uttar Pradesh', '', 'Scheduled', '2025-09-23 09:06:26', '2025-09-23 09:06:26', 7);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `price` varchar(50) DEFAULT NULL,
  `delivery_timeline` varchar(100) DEFAULT NULL,
  `technologies` varchar(200) DEFAULT NULL,
  `github_link` varchar(200) DEFAULT NULL,
  `preview_link` varchar(200) DEFAULT NULL,
  `ppt_link` varchar(200) DEFAULT NULL,
  `demo_video_link` varchar(200) DEFAULT NULL,
  `admin_name` varchar(100) DEFAULT NULL,
  `conversation_flow_link` varchar(200) DEFAULT NULL,
  `status` enum('working','under_maintenance','rejected') DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `main_user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `description`, `price`, `delivery_timeline`, `technologies`, `github_link`, `preview_link`, `ppt_link`, `demo_video_link`, `admin_name`, `conversation_flow_link`, `status`, `created_at`, `updated_at`, `main_user_id`) VALUES
(1, 'E-School', 'E-Learning Software', '20000', '2-3 Weeks', 'React, SQL', 'https://www.youtube.com/', 'https://www.youtube.com/', 'https://www.youtube.com/', 'https://www.youtube.com/', 'Soham Karmakar', 'https://www.youtube.com/', 'working', '2025-09-22 10:12:38', '2025-09-22 10:12:38', 5),
(2, 'CRM Software', 'CRM Software to track deals', '15000', '2 Weeks', 'React, Python', 'https://www.youtube.com/', 'https://www.youtube.com/', 'https://www.youtube.com/', 'https://www.youtube.com/', 'Soham Karmakar', 'https://www.youtube.com/', 'working', '2025-09-22 10:13:23', '2025-09-22 10:13:23', 5);

-- --------------------------------------------------------

--
-- Table structure for table `salesmen`
--

CREATE TABLE `salesmen` (
  `id` int(11) NOT NULL,
  `salesman_id` varchar(20) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `main_user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `salesmen`
--

INSERT INTO `salesmen` (`id`, `salesman_id`, `email`, `password_hash`, `first_name`, `last_name`, `contact_number`, `is_active`, `created_at`, `updated_at`, `main_user_id`) VALUES
(1, 'SM1001', 'soham123@gmail.com', '$2b$12$tXq0SVMcwczdT5Kd2SYchuC0AQHp2eCisTcmp8K0bFKIeYhv3xmM2', 'Soham', 'Karmakar', '8900569341', 1, '2025-09-19 11:58:40', '2025-09-19 11:59:19', 3);

-- --------------------------------------------------------

--
-- Table structure for table `tasks`
--

CREATE TABLE `tasks` (
  `id` int(11) NOT NULL,
  `task_id` varchar(20) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` text DEFAULT NULL,
  `target_quantity` int(11) DEFAULT NULL,
  `current_quantity` int(11) DEFAULT NULL,
  `due_date` date NOT NULL,
  `priority` enum('low','medium','high') DEFAULT NULL,
  `status` enum('pending','in_progress','completed','overdue') DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `salesman_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `assigned_by_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tasks`
--

INSERT INTO `tasks` (`id`, `task_id`, `title`, `description`, `target_quantity`, `current_quantity`, `due_date`, `priority`, `status`, `created_at`, `updated_at`, `salesman_id`, `product_id`, `assigned_by_id`) VALUES
(1, 'T001', 'CRM Software', 'Properly sale the items', 10, 0, '2025-09-22', 'medium', 'overdue', '2025-09-22 10:19:01', '2025-09-23 05:03:15', 7, 2, 5),
(2, 'T002', 'E-School', 'Do it properly', 10, 10, '2025-09-23', 'medium', 'completed', '2025-09-22 10:26:52', '2025-09-22 10:39:52', 6, 1, 5),
(3, 'T003', 'CRM Software', 'Do the task properly', 10, 10, '2025-09-22', 'medium', 'completed', '2025-09-22 11:02:00', '2025-09-22 11:02:40', 7, 2, 5);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `user_type` enum('main','sub') NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `main_user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `password_hash`, `first_name`, `last_name`, `username`, `contact_number`, `user_type`, `is_active`, `created_at`, `updated_at`, `main_user_id`) VALUES
(1, 'admin@crm.com', '$2b$12$Mr/Sc19AhUl2o1pdr29HDe5HJ9PXadJ4JlbX8ljOAZtShjEtzILJ2', 'Admin', 'User', NULL, NULL, 'main', 1, '2025-09-22 09:55:34', '2025-09-22 09:55:34', NULL),
(2, 'test@example.com', '$2b$12$0EqsrJP3ywlBit7uRXwjeeSlbChWmZZDwumx5lgi9pfcZkqw.KMya', 'Test', 'User', NULL, NULL, 'main', 1, '2025-09-22 09:56:01', '2025-09-22 09:56:01', NULL),
(3, 'test.enhanced@example.com', '$2b$12$1GzVe6tTdWd6cuvXz32mMef4M.nr9MT0UX.PLjvIs1mDoA21RLiLK', 'Test', 'Salesman Enhanced', 'SM6588', '+1234567890', 'sub', 1, '2025-09-22 09:56:03', '2025-09-22 09:56:03', 2),
(4, 'test.enhanced2@example.com', '$2b$12$X8Gjqe0rz2qeYRcDAJIVdOQThtRMlAhD7ojDRH5q2qM8qpuTZFEge', 'Test', 'Salesman Enhanced 2', 'SM7916', '+1234567890', 'sub', 1, '2025-09-22 09:57:32', '2025-09-22 09:57:32', 2),
(5, 'soham.karmakar@laitusneo.com', '$2b$12$zFKFuf9WffhhQVdhr6mHae2xzSzOqIapGWCpocadSjD.r29LA3kOC', 'Soham', 'Karmakar', NULL, NULL, 'main', 1, '2025-09-22 09:58:57', '2025-09-22 09:58:57', NULL),
(6, 'soham@gmail.com', '$2b$12$C102HOc7s5fCZpkxjKWCcOZrocvHzq3Gb2/NMnNgJM0oBCHi4rUJG', 'Abhi', '', 'SM6476', '8900569341', 'sub', 0, '2025-09-22 10:10:10', '2025-09-23 05:57:18', 5),
(7, 'adi@gmail.com', '$2b$12$anR8Pgho4u0.k.H8XGpS5e4/HTFzpm5/NNzO3fsKcfnssCYYmvVsu', 'Aditya', '', 'SM6501', '89005695454', 'sub', 1, '2025-09-22 10:11:19', '2025-09-23 07:02:14', 5),
(8, 'test@sub.com', '$2b$12$WMOwiIhEBK6dYDAU4QaTeupJoO10vFXXDe0JMPxm8e3nu.p7K.SSe', 'Test', 'Sub', NULL, NULL, 'sub', 1, '2025-09-22 12:30:55', '2025-09-22 12:30:55', NULL),
(9, 'main@test.com', '$2b$12$eUBc6hQxtitFxfwos0ElZO/33Nof/zbr7AzWQPfPMdmVarNCKQQKS', 'Main', 'User', NULL, NULL, 'main', 1, '2025-09-23 04:43:59', '2025-09-23 04:43:59', NULL),
(10, 'john@test.com', '$2b$12$sYzOJLNQTgbH1o/GjojpDeurwWfVLXYkVacpDB/anzdqCnj14Q782', 'John', 'Salesman', 'SM5797', '+1234567890', 'sub', 1, '2025-09-23 04:44:01', '2025-09-23 04:44:01', 9),
(11, 'main1758602702@test.com', '$2b$12$Mn0mXE2jWONNU.pM.7v/rOKqa9a7nhTZ6dkf80qBK5VNR0DGqvI/e', 'Main', 'User', NULL, NULL, 'main', 1, '2025-09-23 04:45:04', '2025-09-23 04:45:04', NULL),
(12, 'john1758602702@test.com', '$2b$12$P1BElEvT2GOI0EbyrRe2ruSOhGJalWkY2n2NGu.niQASuPDtEHie2', 'John', 'Salesman', 'SM8516', '+1234567890', 'sub', 1, '2025-09-23 04:45:06', '2025-09-23 04:45:06', 11),
(13, 'soha@gmail.com', '$2b$12$Dk/VwnKxzFsLRJ3rGNk5n.YoSAMNbEpNPcHc8Z9IbV7XxsOKRftSi', 'Soha', '', 'SM5937', '8900569341', 'sub', 1, '2025-09-23 06:00:32', '2025-09-23 07:17:13', 5);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `deals`
--
ALTER TABLE `deals`
  ADD PRIMARY KEY (`id`),
  ADD KEY `salesman_id` (`salesman_id`);

--
-- Indexes for table `leads`
--
ALTER TABLE `leads`
  ADD PRIMARY KEY (`id`),
  ADD KEY `salesman_id` (`salesman_id`);

--
-- Indexes for table `meetings`
--
ALTER TABLE `meetings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `salesman_id` (`salesman_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_user_id` (`main_user_id`);

--
-- Indexes for table `salesmen`
--
ALTER TABLE `salesmen`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_salesmen_salesman_id` (`salesman_id`),
  ADD UNIQUE KEY `ix_salesmen_email` (`email`),
  ADD KEY `main_user_id` (`main_user_id`);

--
-- Indexes for table `tasks`
--
ALTER TABLE `tasks`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `task_id` (`task_id`),
  ADD KEY `salesman_id` (`salesman_id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `assigned_by_id` (`assigned_by_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_users_email` (`email`),
  ADD UNIQUE KEY `ix_users_username` (`username`),
  ADD KEY `main_user_id` (`main_user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `deals`
--
ALTER TABLE `deals`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `leads`
--
ALTER TABLE `leads`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `meetings`
--
ALTER TABLE `meetings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `salesmen`
--
ALTER TABLE `salesmen`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `tasks`
--
ALTER TABLE `tasks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `deals`
--
ALTER TABLE `deals`
  ADD CONSTRAINT `deals_ibfk_1` FOREIGN KEY (`salesman_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `leads`
--
ALTER TABLE `leads`
  ADD CONSTRAINT `leads_ibfk_1` FOREIGN KEY (`salesman_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `meetings`
--
ALTER TABLE `meetings`
  ADD CONSTRAINT `meetings_ibfk_1` FOREIGN KEY (`salesman_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`main_user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `salesmen`
--
ALTER TABLE `salesmen`
  ADD CONSTRAINT `salesmen_ibfk_1` FOREIGN KEY (`main_user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `tasks`
--
ALTER TABLE `tasks`
  ADD CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`salesman_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `tasks_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  ADD CONSTRAINT `tasks_ibfk_3` FOREIGN KEY (`assigned_by_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`main_user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
