-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 01, 2025 at 04:58 PM
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
-- Database: `feedback_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `additional_comment`
--

CREATE TABLE `additional_comment` (
  `id` int(11) NOT NULL,
  `participant_id` varchar(11) NOT NULL,
  `additional_question` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `additional_comment`
--

INSERT INTO `additional_comment` (`id`, `participant_id`, `additional_question`) VALUES
(1, '', 'Which topic did you find useful? Why?'),
(2, '', 'Which topic did you least useful? Why?'),
(3, '', 'What part of today\'s activity/session did you like the most? Why?'),
(4, '', 'What key learning point/s have you gained from this activity/session?  '),
(5, '', 'How are you going to use the skills/knowledge/ideas/concepts gained from this activity/session?'),
(6, '', 'In a scale of 1-10 10 being the highest, how will you rate this activity/session?'),
(7, '', 'How do you think this activity/session can best be improved in the future?');

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `fullname` varchar(200) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `profile_image` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `username`, `password`, `fullname`, `email`, `phone`, `profile_image`) VALUES
(1, 'Admin', 'pbkdf2:sha256:600000$mHQTCQJSCzzeJl36$26e520aabf34dd0eca9b8c62bee854de916425bf0f25a70d2e181ac0b68c027a', 'Kyla Verona', 'emails07@gmail.com', '65236565312', '/static/uploads/friend-08.png');

-- --------------------------------------------------------

--
-- Table structure for table `assessment`
--

CREATE TABLE `assessment` (
  `id` int(11) NOT NULL,
  `question_num` int(11) NOT NULL,
  `assessment_text` text NOT NULL,
  `category` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `assessment`
--

INSERT INTO `assessment` (`id`, `question_num`, `assessment_text`, `category`) VALUES
(1, 1, 'The OBJECTIVES of the activity were clearly defined and met.', 'About the topic/s'),
(2, 2, 'The duration of the topic/s or session/s was/were adequate.', 'About the topic/s'),
(3, 3, 'The topics discussed were relevant to what I aimed to learn at the end of the session.', 'About the topic/s'),
(4, 4, 'The handouts and the other learning materials provided were appropriate for the participants and were useful.', 'About the materials'),
(5, 5, 'The quantity of the handouts and other learning materials provide were sufficient for all participants.', 'About the materials'),
(6, 6, 'The facilitator/s is/are punctual and prepared.', 'About the facilitator/s'),
(7, 7, 'The facilitator/s is/are confident and knowledgeable about the subject matter.', 'About the facilitator/s'),
(8, 8, 'The facilitator/s conducts activity in a moderate pace so that all participants are able to follow and he/she goes back to topics when nedded.', 'About the facilitator/s'),
(9, 9, 'The facilitator/s used appropriate methods to conduct the activities- performs fun, practical and relevant activities to ensure participants are engaged at all times.', 'About the facilitator/s'),
(10, 10, 'The facilitator/s explanations were clear and easy to understand.', 'About the facilitator/s'),
(11, 11, 'The facilitator/s is/are and ensures that all participants are able to follow the sessions.', 'About the facilitator/s'),
(12, 12, 'The facilitator/s is/are able to professionally deal with unforeseen challenges during facilitation at all times.', 'About the facilitator/s'),
(13, 13, 'The quality of food served is acceptable. (taste is good, cooked just right and fresh)', 'About the food and venue'),
(14, 14, 'The food servings/portions are sufficient.', 'About the food and venue'),
(15, 15, 'The food arrived before the allotted break time.', 'About the food and venue'),
(16, 16, 'The table wares (fork, spoon, plates, etc.) and/or food boxes (for packed meals) are in good condition.', 'About the food and venue'),
(17, 17, 'The food servers are well groomed and courteous.', 'About the food and venue'),
(18, 18, 'The venue is conductive to learning - clean, with sufficient space, lighting and ventilation and has other amenities such as a pantry or rest rooms to address the participants\' personal needs.', 'About the food and venue'),
(19, 19, 'Save the Children Staff monitors our training class in a regular basis', 'About Save The Children Staff Support'),
(20, 20, 'Save the Children Staff is approachable and always ready to listen to our feedback regarding the activity and other concerns.', 'About Save The Children Staff Support');

-- --------------------------------------------------------

--
-- Table structure for table `assessment_response`
--

CREATE TABLE `assessment_response` (
  `id` int(11) NOT NULL,
  `participant_id` int(11) NOT NULL,
  `assessment_number` int(11) NOT NULL,
  `response` varchar(10) NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `category` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `assessment_response`
--

INSERT INTO `assessment_response` (`id`, `participant_id`, `assessment_number`, `response`, `comment`, `category`) VALUES
(205, 16, 1, '3', ' ', 'About the topic/s'),
(206, 16, 2, '3', NULL, 'About the topic/s'),
(207, 16, 3, '3', NULL, 'About the topic/s'),
(208, 16, 4, '3', NULL, 'About the materials'),
(209, 16, 5, '3', NULL, 'About the materials'),
(210, 16, 6, '3', NULL, 'About the facilitator/s'),
(211, 16, 7, '3', NULL, 'About the facilitator/s'),
(212, 16, 8, '3', NULL, 'About the facilitator/s'),
(213, 16, 9, '3', NULL, 'About the facilitator/s'),
(214, 16, 10, '3', NULL, 'About the facilitator/s'),
(215, 16, 11, '3', NULL, 'About the facilitator/s'),
(216, 16, 12, '3', NULL, 'About the facilitator/s'),
(217, 16, 13, '3', NULL, 'About the food and venue'),
(218, 16, 14, '3', NULL, 'About the food and venue'),
(219, 16, 15, '3', NULL, 'About the food and venue'),
(220, 16, 16, '3', NULL, 'About the food and venue'),
(221, 16, 17, '3', NULL, 'About the food and venue'),
(222, 16, 18, '3', NULL, 'About the food and venue'),
(223, 16, 19, '3', NULL, 'About Save The Children Staff Support'),
(224, 16, 20, '3', NULL, 'About Save The Children Staff Support'),
(245, 18, 1, '3', NULL, 'About the topic/s'),
(246, 18, 2, '0', NULL, 'About the topic/s'),
(247, 18, 3, '1', NULL, 'About the topic/s'),
(248, 18, 4, '2', NULL, 'About the materials'),
(249, 18, 5, '2', NULL, 'About the materials'),
(250, 18, 6, '2', NULL, 'About the facilitator/s'),
(251, 18, 7, '2', NULL, 'About the facilitator/s'),
(252, 18, 9, '2', NULL, 'About the facilitator/s'),
(253, 18, 10, '3', NULL, 'About the facilitator/s'),
(254, 18, 11, '3', NULL, 'About the facilitator/s'),
(255, 18, 12, '3', NULL, 'About the facilitator/s'),
(256, 18, 13, '3', NULL, 'About the food and venue'),
(257, 18, 14, '3', NULL, 'About the food and venue'),
(258, 18, 15, '1', NULL, 'About the food and venue'),
(259, 18, 16, '3', NULL, 'About the food and venue'),
(260, 18, 17, '2', NULL, 'About the food and venue'),
(261, 18, 18, '3', NULL, 'About the food and venue'),
(262, 18, 19, '2', NULL, 'About Save The Children Staff Support'),
(263, 18, 20, '2', NULL, 'About Save The Children Staff Support'),
(284, 20, 1, '1', NULL, 'About the topic/s'),
(285, 20, 2, '2', NULL, 'About the topic/s'),
(286, 20, 3, '1', NULL, 'About the topic/s'),
(287, 20, 4, '3', NULL, 'About the materials'),
(288, 20, 5, '1', NULL, 'About the materials'),
(289, 20, 6, '2', NULL, 'About the facilitator/s'),
(290, 20, 7, '3', NULL, 'About the facilitator/s'),
(291, 20, 8, '1', NULL, 'About the facilitator/s'),
(292, 20, 9, '3', NULL, 'About the facilitator/s'),
(293, 20, 10, '2', NULL, 'About the facilitator/s'),
(294, 20, 11, '2', NULL, 'About the facilitator/s'),
(295, 20, 12, '2', NULL, 'About the facilitator/s'),
(296, 20, 13, '3', NULL, 'About the food and venue'),
(297, 20, 14, '1', NULL, 'About the food and venue'),
(298, 20, 16, '3', NULL, 'About the food and venue'),
(299, 20, 17, '2', NULL, 'About the food and venue'),
(300, 20, 18, '3', NULL, 'About the food and venue'),
(301, 20, 19, '3', NULL, 'About Save The Children Staff Support'),
(302, 20, 20, '2', NULL, 'About Save The Children Staff Support'),
(562, 27, 1, '3', 'opo', 'About the topic/s'),
(563, 27, 2, '3', 'yes po', 'About the topic/s'),
(564, 27, 3, '3', '3', 'About the topic/s'),
(565, 27, 4, '3', '4', 'About the materials'),
(566, 27, 5, '3', '5', 'About the materials'),
(567, 27, 6, '3', '6', 'About the facilitator/s'),
(568, 27, 7, '3', '7', 'About the facilitator/s'),
(569, 27, 8, '3', '8', 'About the facilitator/s'),
(570, 27, 9, '3', '9', 'About the facilitator/s'),
(571, 27, 10, '3', '10', 'About the facilitator/s'),
(572, 27, 11, '3', '11', 'About the facilitator/s'),
(573, 27, 12, '3', '12', 'About the facilitator/s'),
(574, 27, 13, '3', '13', 'About the food and venue'),
(575, 27, 14, '3', '14', 'About the food and venue'),
(576, 27, 15, '3', '15', 'About the food and venue'),
(577, 27, 16, '3', '16', 'About the food and venue'),
(578, 27, 17, '3', '17', 'About the food and venue'),
(579, 27, 18, '3', '18', 'About the food and venue'),
(580, 27, 19, '3', '19', 'About Save The Children Staff Support'),
(581, 27, 20, '3', 'yes?', 'About Save The Children Staff Support'),
(582, 45, 1, '3', 'what', 'About the topic/s'),
(583, 45, 2, '2', 'is', 'About the topic/s'),
(584, 45, 3, '3', 'it', 'About the topic/s'),
(585, 45, 4, '3', '1', 'About the materials'),
(586, 45, 5, '2', '2', 'About the materials'),
(587, 45, 6, '3', NULL, 'About the facilitator/s'),
(588, 45, 7, '3', NULL, 'About the facilitator/s'),
(589, 45, 8, '2', NULL, 'About the facilitator/s'),
(590, 45, 9, '1', NULL, 'About the facilitator/s'),
(591, 45, 10, '2', NULL, 'About the facilitator/s'),
(592, 45, 11, '3', NULL, 'About the facilitator/s'),
(593, 45, 12, '3', NULL, 'About the facilitator/s'),
(594, 45, 13, '2', NULL, 'About the food and venue'),
(595, 45, 14, '3', NULL, 'About the food and venue'),
(596, 45, 15, '2', NULL, 'About the food and venue'),
(597, 45, 16, '3', NULL, 'About the food and venue'),
(598, 45, 17, '3', NULL, 'About the food and venue'),
(599, 45, 18, '3', NULL, 'About the food and venue'),
(600, 45, 19, '3', NULL, 'About Save The Children Staff Support'),
(601, 45, 20, '2', NULL, 'About Save The Children Staff Support');

-- --------------------------------------------------------

--
-- Table structure for table `comment_response`
--

CREATE TABLE `comment_response` (
  `id` int(11) NOT NULL,
  `participant_id` int(11) NOT NULL,
  `comment_response` varchar(200) NOT NULL,
  `additional_comment_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `comment_response`
--

INSERT INTO `comment_response` (`id`, `participant_id`, `comment_response`, `additional_comment_id`) VALUES
(22, 27, 'no po', 1),
(23, 27, 'yes po', 2),
(24, 27, 'yes po', 3),
(25, 27, 'yes po', 4),
(26, 27, 'yes po', 5),
(27, 27, 'yes po', 6),
(28, 27, 'yes po', 7),
(29, 45, 'ano man', 1),
(30, 45, 'ano man', 2),
(31, 45, 'ano man', 3),
(32, 45, 'ano man', 4),
(33, 45, 'ano man', 5),
(34, 45, 'ano man', 6),
(35, 45, 'ano man', 7);

-- --------------------------------------------------------

--
-- Table structure for table `participants`
--

CREATE TABLE `participants` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `activity_name` varchar(255) DEFAULT NULL,
  `venue` varchar(200) NOT NULL,
  `school` varchar(200) NOT NULL,
  `district` varchar(200) NOT NULL,
  `facilitator_name` varchar(100) NOT NULL,
  `address` varchar(200) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `participants`
--

INSERT INTO `participants` (`id`, `name`, `activity_name`, `venue`, `school`, `district`, `facilitator_name`, `address`, `date`) VALUES
(16, 'Kyla S. Verona', 'Mathy\'s Quest: A 2D Educational Game for Mastering Fractions and Decimals', 'Tanauan 1 Central School', 'Eastern Visayas State University Tanauan', '2', 'Maeven S. Armada', 'Tanauan', '2025-03-18'),
(18, 'Simon Verona', 'Mathy\'s Quest: A 2D Educational Game ', 'Tanauan 1 Central School', 'Eastern Visayas State University Tanauan', '2', 'Maeven S. Armada', 'Tanauan', '2025-03-18'),
(20, 'Oreo Chan', 'Mathy\'s Quest', 'Tanauan 1 Central School', 'Eastern Visayas State University Tanauan', '2', 'Maeven S. Armada', 'Tanauan', '2025-03-18'),
(27, 'Ming', 'Mathys Quest: A 2D Educational Game for Mastering Fractions and Decimanls', 'Tanauan 1 Central School', 'Eastern Visayas State University Tanauan', '2', 'Maeven S. Armada', 'Tanauan', '2025-03-25'),
(45, 'Kyla', 'Mathys Quest: A 2D Educational Game for Mastering Fractions and Decimanls', 'School', 'Eastern Visayas State University ', '2', 'Cindy', 'Tanauan', '2025-03-31'),
(46, 'Kyla', 'Mathy\'s Quest: A 2D Educational Adventure for Mastering Fractions and Decimals', 'Tanauan 1 Central School', 'Evsu', '2', 'Maeven', 'Malaguicay', '2025-03-31');

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE `questions` (
  `id` int(11) NOT NULL,
  `question_text` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `questions`
--

INSERT INTO `questions` (`id`, `question_text`) VALUES
(1, '1. The OBJECTIVES of the activity were clearly defined and met.'),
(2, '2. The duration of the topic/s or session/s was/were adequate.'),
(3, '3. The topics discussed were relevant to what I aimed to learn at the end of the session.'),
(4, '1. The handouts and other learning materials provided were appropriate for the participants and were useful'),
(5, '2. The quantity of the handouts and other learning materials provided were sufficient for all participants. '),
(6, '1. The facilitator/s is/are punctual and prepared.'),
(7, '2. The facilitator/s is/area confident and knowledge about the subject matter.'),
(8, '3. The facilitator/s conducts activity in a moderate pace so that all participants are able to follow and he/she goes back to topics when needed.'),
(9, '4. The facilitator/s used appropriate methods to conduct the activities- performs fun, practical and relevenat activities to ensure participants are engaged at all times.'),
(10, '5. The facilitator/s explanations were clear and easy to understand.'),
(11, '6. The facilitator/s is/are supportive and ensures that all participants are able to follow the sessions.'),
(12, '7. The facilitator/s is/are able to professionally deal with unforeseen challenges during facilitation at all times.'),
(13, '1. The quality of food served is acceptable. (taste is good, cooked just right and fresh)'),
(14, '2. The food servings/portions are sufficient.'),
(15, '3. The food arrive before the allotted break time.'),
(16, '4. The table wares (fork, spoon, plates, etc.) are in good condition.'),
(17, '5. The food serve are well groomed and courteous.'),
(18, '6. The venue is conducive to learning - clean, with sufficient space, lighting and ventilation and has other amenities such as a pantry or rest rooms to address the participants\' personal needs.'),
(19, '1. Save the Children Staff monitors our training class in a regular basis.'),
(20, '2.Save the Children Staff is approachable and always ready to listen to our feedback regarding the activity and other concerns.');

-- --------------------------------------------------------

--
-- Table structure for table `user_response`
--

CREATE TABLE `user_response` (
  `id` int(11) NOT NULL,
  `participant_id` int(11) NOT NULL,
  `question_number` int(11) NOT NULL,
  `response` varchar(10) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `submitted_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_response`
--

INSERT INTO `user_response` (`id`, `participant_id`, `question_number`, `response`, `is_read`, `submitted_at`) VALUES
(1, 1, 1, 'No', 1, '2025-02-22 22:54:35'),
(2, 0, 1, 'No', 1, '2025-02-22 22:54:35'),
(3, 0, 1, 'Yes', 1, '2025-02-22 22:54:35'),
(4, 519, 1, 'Yes', 1, '2025-02-22 22:54:35'),
(5, 519, 2, 'Yes', 1, '2025-02-22 22:54:35'),
(6, 7, 3, 'Yes', 1, '2025-02-22 22:54:35'),
(7, 7, 4, 'Yes', 1, '2025-02-22 22:54:35'),
(8, 7, 4, 'Yes', 1, '2025-02-22 22:54:35'),
(9, 7, 5, 'No', 1, '2025-02-22 22:54:35'),
(10, 7, 6, 'No', 1, '2025-02-22 22:54:35'),
(11, 7, 7, 'Yes', 1, '2025-02-22 22:54:35'),
(12, 7, 8, 'No', 1, '2025-02-22 22:54:35'),
(13, 7, 9, 'No', 1, '2025-02-22 22:54:35'),
(14, 7, 10, 'No', 1, '2025-02-22 22:54:35'),
(15, 7, 11, 'No', 1, '2025-02-22 22:54:35'),
(16, 7, 12, 'No', 1, '2025-02-22 22:54:35'),
(17, 8, 1, 'Yes', 1, '2025-02-22 22:54:35'),
(18, 8, 2, 'No', 1, '2025-02-22 22:54:35'),
(19, 8, 3, 'No', 1, '2025-02-22 22:54:35'),
(20, 8, 4, 'No', 1, '2025-02-22 22:54:35'),
(21, 8, 5, 'No', 1, '2025-02-22 22:54:35'),
(22, 8, 6, 'Yes', 1, '2025-02-22 22:54:35'),
(23, 8, 7, 'Yes', 1, '2025-02-22 22:54:35'),
(24, 8, 8, 'No', 1, '2025-02-22 22:54:35'),
(25, 8, 9, 'No', 1, '2025-02-22 22:54:35'),
(26, 8, 10, 'No', 1, '2025-02-22 22:54:35'),
(27, 8, 11, 'No', 1, '2025-02-22 22:54:35'),
(28, 8, 12, 'No', 1, '2025-02-22 22:54:35'),
(29, 10, 1, 'Yes', 1, '2025-02-22 22:54:35'),
(30, 10, 2, 'Yes', 1, '2025-02-22 22:54:35'),
(31, 10, 3, 'No', 1, '2025-02-22 22:54:35'),
(32, 10, 4, 'No', 1, '2025-02-22 22:54:35'),
(33, 10, 5, 'No', 1, '2025-02-22 22:54:35'),
(34, 10, 6, 'Yes', 1, '2025-02-22 22:54:35'),
(35, 10, 7, 'No', 1, '2025-02-22 22:54:35'),
(36, 10, 8, 'Yes', 1, '2025-02-22 22:54:35'),
(37, 10, 9, 'No', 1, '2025-02-22 22:54:35'),
(38, 10, 10, 'No', 1, '2025-02-22 22:54:35'),
(39, 10, 11, 'No', 1, '2025-02-22 22:54:35'),
(40, 10, 12, 'No', 1, '2025-02-22 22:54:35'),
(41, 10, 12, 'No', 1, '2025-02-22 22:54:35'),
(42, 0, 1, 'No', 1, '2025-02-22 22:54:35'),
(43, 11, 1, 'No', 1, '2025-02-22 22:54:35'),
(44, 11, 2, 'Yes', 1, '2025-02-22 22:54:35'),
(45, 11, 3, 'Yes', 1, '2025-02-22 22:54:35'),
(46, 11, 4, 'No', 1, '2025-02-22 22:54:35'),
(47, 11, 5, 'No', 1, '2025-02-22 22:54:35'),
(48, 11, 6, 'No', 1, '2025-02-22 22:54:35'),
(49, 11, 7, 'No', 1, '2025-02-22 22:54:35'),
(50, 11, 8, 'Yes', 1, '2025-02-22 22:54:35'),
(51, 11, 9, 'No', 1, '2025-02-22 22:54:35'),
(52, 11, 10, 'No', 1, '2025-02-22 22:54:35'),
(53, 11, 11, 'No', 1, '2025-02-22 22:54:35'),
(54, 11, 12, 'Yes', 1, '2025-02-22 22:54:35'),
(55, 15, 1, 'Yes', 1, '2025-02-22 22:54:35'),
(56, 15, 2, 'No', 1, '2025-02-22 22:54:35'),
(57, 15, 2, 'Yes', 1, '2025-02-22 22:54:35'),
(58, 17, 1, 'Yes', 1, '2025-02-22 22:54:35'),
(59, 17, 2, 'No', 1, '2025-02-22 22:54:35'),
(60, 17, 3, 'No', 1, '2025-02-22 22:54:35'),
(61, 17, 4, 'Yes', 1, '2025-02-22 22:54:35'),
(62, 17, 5, 'Yes', 1, '2025-02-22 22:54:35'),
(63, 17, 6, 'Yes', 1, '2025-02-22 22:54:35'),
(64, 17, 7, 'No', 1, '2025-02-22 22:54:35'),
(65, 17, 8, 'Yes', 1, '2025-02-22 22:54:35'),
(66, 17, 9, 'No', 1, '2025-02-22 22:54:35'),
(67, 17, 10, 'No', 1, '2025-02-22 22:54:35'),
(68, 17, 11, 'No', 1, '2025-02-22 22:54:35'),
(69, 17, 12, 'No', 1, '2025-02-22 22:54:35'),
(70, 17, 12, 'No', 1, '2025-02-22 22:54:35'),
(71, 18, 1, 'No', 1, '2025-02-22 22:54:35'),
(72, 18, 2, 'No', 1, '2025-02-22 22:54:35'),
(73, 18, 3, 'Yes', 1, '2025-02-22 22:54:35'),
(74, 18, 4, 'Yes', 1, '2025-02-22 22:54:35'),
(75, 18, 5, 'No', 1, '2025-02-22 22:54:35'),
(76, 18, 6, 'No', 1, '2025-02-22 22:54:35'),
(77, 18, 7, 'No', 1, '2025-02-22 22:54:35'),
(78, 18, 8, 'No', 1, '2025-02-22 22:54:35'),
(79, 18, 9, 'No', 1, '2025-02-22 22:54:35'),
(80, 18, 10, 'No', 1, '2025-02-22 22:54:35'),
(81, 18, 11, 'No', 1, '2025-02-22 22:54:35'),
(82, 18, 12, 'No', 1, '2025-02-22 22:54:35'),
(83, 20, 1, 'No', 1, '2025-02-22 22:54:35'),
(84, 20, 2, 'No', 1, '2025-02-22 22:54:35'),
(85, 20, 3, 'No', 1, '2025-02-22 22:54:35'),
(86, 20, 4, 'No', 1, '2025-02-22 22:54:35'),
(87, 20, 5, 'No', 1, '2025-02-22 22:54:35'),
(88, 20, 6, 'No', 1, '2025-02-22 22:54:35'),
(89, 20, 7, 'No', 1, '2025-02-22 22:54:35'),
(90, 20, 8, 'No', 1, '2025-02-22 22:54:35'),
(91, 20, 9, 'No', 1, '2025-02-22 22:54:35'),
(92, 20, 10, 'No', 1, '2025-02-22 22:54:35'),
(93, 20, 11, 'No', 1, '2025-02-22 22:54:35'),
(94, 20, 12, 'No', 1, '2025-02-22 22:54:35'),
(95, 20, 12, 'No', 1, '2025-02-22 22:54:35'),
(96, 21, 1, 'Yes', 1, '2025-02-22 22:54:35'),
(97, 21, 2, 'Yes', 1, '2025-02-22 22:54:35'),
(98, 21, 3, 'No', 1, '2025-02-22 22:54:35'),
(99, 21, 4, 'Yes', 1, '2025-02-22 22:54:35'),
(100, 21, 5, 'No', 1, '2025-02-22 22:54:35'),
(101, 21, 6, 'No', 1, '2025-02-22 22:54:35'),
(102, 21, 7, 'No', 1, '2025-02-22 22:54:35'),
(103, 21, 8, 'Yes', 1, '2025-02-22 22:54:35'),
(104, 21, 9, 'No', 1, '2025-02-22 22:54:35'),
(105, 21, 10, 'No', 1, '2025-02-22 22:54:35'),
(106, 21, 11, 'No', 1, '2025-02-22 22:54:35'),
(107, 21, 12, 'Yes', 1, '2025-02-22 22:54:35'),
(108, 21, 12, 'Yes', 1, '2025-02-22 22:54:35'),
(109, 21, 12, 'Yes', 1, '2025-02-22 22:54:35'),
(110, 21, 12, 'No', 1, '2025-02-22 22:54:35'),
(111, 21, 12, 'Yes', 1, '2025-02-22 22:54:35'),
(112, 21, 12, 'Yes', 1, '2025-02-22 22:54:35'),
(113, 22, 12, 'Yes', 1, '2025-02-22 22:54:35'),
(114, 23, 1, 'Yes', 1, '2025-02-22 22:54:35'),
(115, 23, 2, 'No', 1, '2025-02-22 22:54:35'),
(116, 23, 3, 'Yes', 1, '2025-02-22 22:54:35'),
(117, 23, 4, 'No', 1, '2025-02-22 22:54:35'),
(118, 23, 5, 'No', 1, '2025-02-22 22:54:35'),
(119, 23, 6, 'No', 1, '2025-02-22 22:54:35'),
(120, 23, 7, 'No', 1, '2025-02-22 22:54:35'),
(121, 23, 8, 'Yes', 1, '2025-02-22 22:54:35'),
(122, 23, 9, 'No', 1, '2025-02-22 22:54:35'),
(123, 23, 10, 'No', 1, '2025-02-22 22:54:35'),
(124, 23, 11, 'No', 1, '2025-02-22 22:54:35'),
(125, 23, 12, 'Yes', 1, '2025-02-22 22:54:35'),
(126, 25, 1, 'No', 1, '2025-02-22 22:54:35'),
(127, 25, 2, 'No', 1, '2025-02-22 22:54:35'),
(128, 25, 3, 'Yes', 1, '2025-02-22 22:54:35'),
(129, 25, 4, 'No', 1, '2025-02-22 22:54:35'),
(130, 25, 4, 'No', 1, '2025-02-22 22:54:35'),
(131, 25, 5, 'No', 1, '2025-02-22 22:54:35'),
(132, 25, 6, 'No', 1, '2025-02-22 22:54:35'),
(133, 25, 7, 'No', 1, '2025-02-22 22:54:35'),
(134, 25, 8, 'Yes', 1, '2025-02-22 22:54:35'),
(135, 25, 9, 'Yes', 1, '2025-02-22 22:54:35'),
(136, 25, 10, 'No', 1, '2025-02-22 22:54:35'),
(137, 25, 11, 'No', 1, '2025-02-22 22:54:35'),
(138, 25, 12, 'Yes', 1, '2025-02-22 22:54:35'),
(139, 28, 1, 'Yes', 1, '2025-02-22 22:54:35'),
(140, 28, 1, 'Yes', 1, '2025-02-22 22:54:35'),
(141, 28, 2, 'Yes', 1, '2025-02-22 22:54:35'),
(142, 28, 3, 'Yes', 1, '2025-02-22 22:54:35'),
(143, 28, 4, 'No', 1, '2025-02-22 22:54:35'),
(144, 28, 5, 'Yes', 1, '2025-02-22 22:54:35'),
(145, 28, 6, 'No', 1, '2025-02-22 22:54:35'),
(146, 28, 7, 'Yes', 1, '2025-02-22 22:54:35'),
(147, 28, 8, 'Yes', 1, '2025-02-22 22:54:35'),
(148, 28, 9, 'No', 1, '2025-02-22 22:54:35'),
(149, 28, 10, 'Yes', 1, '2025-02-22 22:54:35'),
(150, 28, 11, 'Yes', 1, '2025-02-22 22:54:35'),
(151, 28, 12, 'Yes', 1, '2025-02-22 22:54:35'),
(152, 30, 1, 'Yes', 1, '2025-02-22 22:54:35'),
(153, 30, 2, 'Yes', 1, '2025-02-22 22:54:35'),
(154, 30, 3, 'Yes', 1, '2025-02-22 22:54:35'),
(155, 30, 4, 'Yes', 1, '2025-02-22 22:54:35'),
(156, 30, 5, 'Yes', 1, '2025-02-22 22:54:35'),
(157, 30, 6, 'Yes', 1, '2025-02-22 22:54:35'),
(158, 30, 7, 'Yes', 1, '2025-02-22 22:54:35'),
(159, 30, 8, 'Yes', 1, '2025-02-22 22:54:35'),
(160, 30, 9, 'No', 1, '2025-02-22 22:54:35'),
(161, 30, 10, 'No', 1, '2025-02-22 22:54:35'),
(162, 30, 11, 'No', 1, '2025-02-22 22:54:35'),
(163, 30, 12, 'Yes', 1, '2025-02-22 22:54:35'),
(164, 30, 12, 'Yes', 1, '2025-02-22 22:54:35'),
(165, 30, 0, 'Completed ', 1, '2025-02-22 22:54:35'),
(166, 31, 12, 'Yes', 1, '2025-02-22 22:54:35'),
(167, 31, 0, 'Completed ', 0, '2025-02-22 22:54:35'),
(168, 31, 12, 'Yes', 0, '2025-02-22 22:54:35'),
(169, 31, 0, 'Completed ', 0, '2025-02-22 22:54:35'),
(170, 32, 12, 'Yes', 0, '2025-02-22 22:54:35'),
(171, 32, 0, 'Completed ', 0, '2025-02-22 22:54:35'),
(172, 32, 12, 'Yes', 0, '2025-02-22 22:54:35'),
(173, 32, 0, 'Completed ', 0, '2025-02-22 22:54:35'),
(174, 32, 12, 'Yes', 0, '2025-02-22 22:54:35'),
(175, 32, 0, 'Completed ', 0, '2025-02-22 22:54:35'),
(176, 32, 12, 'Yes', 0, '2025-02-22 22:54:35'),
(177, 32, 0, 'Completed ', 0, '2025-02-22 22:54:35'),
(178, 32, 12, 'Yes', 0, '2025-02-22 23:00:45'),
(179, 32, 0, 'Completed ', 0, '2025-02-22 23:00:45'),
(180, 33, 1, 'Yes', 0, '2025-02-24 09:16:21'),
(181, 34, 2, 'Yes', 0, '2025-02-24 09:22:44'),
(182, 34, 3, 'Yes', 0, '2025-02-24 09:22:49'),
(183, 34, 4, 'No', 0, '2025-02-24 09:22:52'),
(184, 34, 5, 'No', 0, '2025-02-24 09:22:54'),
(185, 34, 6, 'Yes', 0, '2025-02-24 09:22:57'),
(186, 34, 7, 'Yes', 0, '2025-02-24 09:23:00'),
(187, 34, 8, 'Yes', 0, '2025-02-24 09:23:03'),
(188, 34, 9, 'Yes', 0, '2025-02-24 09:23:07'),
(189, 34, 10, 'Yes', 0, '2025-02-24 09:23:10'),
(190, 34, 11, 'No', 0, '2025-02-24 09:23:12'),
(191, 34, 12, 'Yes', 0, '2025-02-24 09:23:15'),
(192, 34, 0, 'Completed ', 0, '2025-02-24 09:23:15'),
(193, 36, 1, 'No', 0, '2025-02-24 11:39:59'),
(194, 37, 1, 'Yes', 0, '2025-02-24 14:59:49'),
(195, 37, 2, 'No', 0, '2025-02-24 14:59:51'),
(196, 37, 3, 'No', 0, '2025-02-24 14:59:54'),
(197, 37, 4, 'Yes', 0, '2025-02-24 14:59:56'),
(198, 37, 5, 'Yes', 0, '2025-02-24 14:59:59'),
(199, 37, 6, 'No', 0, '2025-02-24 15:00:03'),
(200, 37, 7, 'No', 0, '2025-02-24 15:00:06'),
(201, 37, 8, 'No', 0, '2025-02-24 15:00:09'),
(202, 37, 9, 'No', 0, '2025-02-24 15:00:11'),
(203, 37, 10, 'No', 0, '2025-02-24 15:00:14'),
(204, 37, 11, 'No', 0, '2025-02-24 15:00:17'),
(205, 37, 12, 'Yes', 0, '2025-02-24 15:00:20'),
(206, 37, 0, 'Completed ', 0, '2025-02-24 15:00:20'),
(207, 38, 1, 'Yes', 0, '2025-02-27 11:41:34'),
(208, 38, 2, 'No', 0, '2025-02-27 11:41:37'),
(209, 38, 3, 'Yes', 0, '2025-02-27 11:41:39'),
(210, 38, 4, 'No', 0, '2025-02-27 11:41:41'),
(211, 38, 5, 'Yes', 0, '2025-02-27 11:41:43'),
(212, 38, 6, 'Yes', 0, '2025-02-27 11:41:45'),
(213, 38, 7, 'Yes', 0, '2025-02-27 11:41:48'),
(214, 38, 8, 'Yes', 0, '2025-02-27 11:41:50'),
(215, 38, 9, 'Yes', 0, '2025-02-27 11:41:53'),
(216, 38, 10, 'Yes', 0, '2025-02-27 11:41:55'),
(217, 38, 11, 'Yes', 0, '2025-02-27 11:41:57'),
(218, 38, 12, 'Yes', 0, '2025-02-27 11:41:59'),
(219, 38, 0, 'Completed ', 0, '2025-02-27 11:41:59'),
(220, 39, 1, 'Yes', 0, '2025-02-27 16:52:15'),
(221, 39, 2, 'No', 0, '2025-02-27 16:52:17'),
(222, 39, 3, 'No', 0, '2025-02-27 16:52:19'),
(223, 39, 4, 'No', 0, '2025-02-27 16:52:22'),
(224, 39, 5, 'No', 0, '2025-02-27 16:52:24'),
(225, 39, 6, 'No', 0, '2025-02-27 16:52:26'),
(226, 39, 7, 'No', 0, '2025-02-27 16:52:29'),
(227, 39, 8, 'No', 0, '2025-02-27 16:52:31'),
(228, 39, 9, 'No', 0, '2025-02-27 16:52:34'),
(229, 39, 10, 'No', 0, '2025-02-27 16:52:37'),
(230, 39, 11, 'No', 0, '2025-02-27 16:52:39'),
(231, 39, 12, 'No', 0, '2025-02-27 16:52:42'),
(232, 39, 0, 'Completed ', 0, '2025-02-27 16:52:42'),
(233, 41, 12, 'Yes', 0, '2025-02-27 17:04:54'),
(234, 41, 0, 'Completed ', 0, '2025-02-27 17:04:54'),
(235, 42, 1, 'Yes', 0, '2025-02-28 09:11:27'),
(236, 42, 2, 'Yes', 0, '2025-02-28 09:11:30'),
(237, 42, 3, 'Yes', 0, '2025-02-28 09:11:32'),
(238, 42, 4, 'Yes', 0, '2025-02-28 09:11:35'),
(239, 42, 5, 'Yes', 0, '2025-02-28 09:11:38'),
(240, 42, 6, 'No', 0, '2025-02-28 09:11:42'),
(241, 42, 7, 'Yes', 0, '2025-02-28 09:11:44'),
(242, 42, 8, 'No', 0, '2025-02-28 09:11:47'),
(243, 42, 9, 'No', 0, '2025-02-28 09:11:51'),
(244, 42, 10, 'No', 0, '2025-02-28 09:11:54'),
(245, 42, 11, 'No', 0, '2025-02-28 09:11:56'),
(246, 42, 12, 'Yes', 0, '2025-02-28 09:12:01'),
(247, 42, 0, 'Completed ', 0, '2025-02-28 09:12:01'),
(248, 43, 1, 'Yes', 0, '2025-02-28 09:19:21'),
(249, 43, 2, 'No', 0, '2025-02-28 09:19:23'),
(250, 43, 3, 'No', 0, '2025-02-28 09:19:27'),
(251, 43, 4, 'No', 0, '2025-02-28 09:19:29'),
(252, 43, 5, 'No', 0, '2025-02-28 09:19:32'),
(253, 43, 6, 'No', 0, '2025-02-28 09:19:35'),
(254, 43, 7, 'No', 0, '2025-02-28 09:19:38'),
(255, 43, 8, 'No', 0, '2025-02-28 09:19:42'),
(256, 43, 9, 'No', 0, '2025-02-28 09:19:44'),
(257, 43, 10, 'No', 0, '2025-02-28 09:19:46'),
(258, 43, 11, 'No', 0, '2025-02-28 09:19:49'),
(259, 43, 12, 'No', 0, '2025-02-28 09:19:52'),
(260, 43, 0, 'Completed ', 0, '2025-02-28 09:19:52'),
(261, 44, 1, 'Yes', 0, '2025-02-28 09:27:49'),
(262, 44, 2, 'No', 0, '2025-02-28 09:27:51'),
(263, 44, 3, 'No', 0, '2025-02-28 09:27:54'),
(264, 44, 4, 'No', 0, '2025-02-28 09:27:56'),
(265, 44, 5, 'No', 0, '2025-02-28 09:27:59'),
(266, 44, 6, 'No', 0, '2025-02-28 09:28:02'),
(267, 44, 7, 'No', 0, '2025-02-28 09:28:05'),
(268, 44, 8, 'No', 0, '2025-02-28 09:28:08'),
(269, 44, 9, 'No', 0, '2025-02-28 09:28:11'),
(270, 44, 10, 'No', 0, '2025-02-28 09:28:13'),
(271, 44, 11, 'No', 0, '2025-02-28 09:28:18'),
(272, 44, 12, 'Yes', 0, '2025-02-28 09:28:21'),
(273, 44, 0, 'Completed ', 0, '2025-02-28 09:49:28'),
(274, 44, 0, 'Completed ', 0, '2025-02-28 09:59:06'),
(275, 44, 0, 'Completed ', 0, '2025-02-28 10:42:21'),
(276, 44, 0, 'Completed ', 0, '2025-02-28 10:42:31'),
(277, 45, 1, 'Yes', 0, '2025-02-28 10:53:40'),
(278, 45, 2, 'No', 0, '2025-02-28 10:53:42'),
(279, 45, 3, 'No', 0, '2025-02-28 10:53:49'),
(280, 45, 4, 'No', 0, '2025-02-28 10:53:51'),
(281, 45, 5, 'Yes', 0, '2025-02-28 10:53:53'),
(282, 45, 6, 'No', 0, '2025-02-28 10:53:55'),
(283, 45, 7, 'No', 0, '2025-02-28 10:53:57'),
(284, 45, 8, 'No', 0, '2025-02-28 10:53:59'),
(285, 45, 9, 'No', 0, '2025-02-28 10:54:00'),
(286, 45, 10, 'Yes', 0, '2025-02-28 10:54:02'),
(287, 45, 11, 'No', 0, '2025-02-28 10:54:03'),
(288, 45, 12, 'Yes', 0, '2025-02-28 10:54:05'),
(289, 45, 0, 'Completed ', 0, '2025-02-28 10:55:32'),
(290, 46, 1, 'Yes', 0, '2025-02-28 10:57:00'),
(291, 46, 2, 'Yes', 0, '2025-02-28 10:57:58'),
(292, 46, 3, 'No', 0, '2025-02-28 10:58:00'),
(293, 46, 4, 'Yes', 0, '2025-02-28 10:58:02'),
(294, 46, 5, 'No', 0, '2025-02-28 10:58:03'),
(295, 46, 6, 'No', 0, '2025-02-28 10:58:05'),
(296, 46, 7, 'No', 0, '2025-02-28 10:58:06'),
(297, 46, 8, 'No', 0, '2025-02-28 10:58:08'),
(298, 46, 9, 'No', 0, '2025-02-28 10:58:09'),
(299, 46, 10, 'No', 0, '2025-02-28 10:58:11'),
(300, 46, 11, 'No', 0, '2025-02-28 10:58:13'),
(301, 46, 12, 'No', 0, '2025-02-28 10:58:14'),
(302, 45, 0, 'Completed ', 0, '2025-02-28 11:04:18'),
(303, 45, 0, 'Completed ', 0, '2025-02-28 11:05:23'),
(304, 45, 0, 'Completed ', 0, '2025-02-28 11:06:14'),
(305, 45, 0, 'Completed ', 0, '2025-02-28 11:08:46'),
(306, 45, 0, 'Completed ', 0, '2025-02-28 11:50:48'),
(307, 47, 1, 'Yes', 0, '2025-03-01 18:35:31'),
(308, 47, 2, 'No', 0, '2025-03-01 18:35:34'),
(309, 47, 3, 'No', 0, '2025-03-01 18:35:37'),
(310, 47, 4, 'Yes', 0, '2025-03-01 18:35:39'),
(311, 47, 5, 'No', 0, '2025-03-01 18:35:42'),
(312, 47, 6, 'Yes', 0, '2025-03-01 18:35:45'),
(313, 47, 7, 'No', 0, '2025-03-01 18:35:48'),
(314, 47, 8, 'No', 0, '2025-03-01 18:35:50'),
(315, 47, 9, 'No', 0, '2025-03-01 18:35:53'),
(316, 47, 10, 'Yes', 0, '2025-03-01 18:35:55'),
(317, 47, 11, 'No', 0, '2025-03-01 18:35:57'),
(318, 47, 12, 'Yes', 0, '2025-03-01 18:36:00'),
(319, 47, 0, 'Completed ', 0, '2025-03-01 18:36:23'),
(320, 48, 1, 'Yes', 0, '2025-03-01 19:28:51'),
(321, 48, 2, 'No', 0, '2025-03-01 19:28:54'),
(322, 48, 3, 'No', 0, '2025-03-01 19:28:56'),
(323, 48, 4, 'No', 0, '2025-03-01 19:28:58'),
(324, 48, 5, 'No', 0, '2025-03-01 19:29:01'),
(325, 48, 6, 'No', 0, '2025-03-01 19:29:04'),
(326, 48, 7, 'No', 0, '2025-03-01 19:29:06'),
(327, 48, 8, 'No', 0, '2025-03-01 19:29:08'),
(328, 48, 9, 'No', 0, '2025-03-01 19:29:10'),
(329, 48, 10, 'No', 0, '2025-03-01 19:29:12'),
(330, 48, 11, 'No', 0, '2025-03-01 19:29:15'),
(331, 48, 12, 'Yes', 0, '2025-03-01 19:29:17'),
(332, 48, 0, 'Completed ', 0, '2025-03-01 19:29:20'),
(333, 49, 1, 'Yes', 0, '2025-03-04 14:08:21'),
(334, 49, 2, 'No', 0, '2025-03-04 14:08:23'),
(335, 49, 3, 'No', 0, '2025-03-04 14:08:26'),
(336, 49, 4, 'No', 0, '2025-03-04 14:08:28'),
(337, 49, 5, 'No', 0, '2025-03-04 14:08:31'),
(338, 49, 6, 'No', 0, '2025-03-04 14:08:34'),
(339, 49, 7, 'No', 0, '2025-03-04 14:08:37'),
(340, 49, 8, 'No', 0, '2025-03-04 14:08:40'),
(341, 49, 9, 'No', 0, '2025-03-04 14:08:44'),
(342, 49, 10, 'No', 0, '2025-03-04 14:08:46'),
(343, 49, 11, 'No', 0, '2025-03-04 14:08:49'),
(344, 49, 12, 'Yes', 0, '2025-03-04 14:08:51'),
(345, 49, 0, 'Completed ', 0, '2025-03-04 14:08:56');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `additional_comment`
--
ALTER TABLE `additional_comment`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `assessment`
--
ALTER TABLE `assessment`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `assessment_response`
--
ALTER TABLE `assessment_response`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `comment_response`
--
ALTER TABLE `comment_response`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_participant` (`participant_id`),
  ADD KEY `additional_comment_id` (`additional_comment_id`);

--
-- Indexes for table `participants`
--
ALTER TABLE `participants`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_response`
--
ALTER TABLE `user_response`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `additional_comment`
--
ALTER TABLE `additional_comment`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `assessment`
--
ALTER TABLE `assessment`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `assessment_response`
--
ALTER TABLE `assessment_response`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=602;

--
-- AUTO_INCREMENT for table `comment_response`
--
ALTER TABLE `comment_response`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `participants`
--
ALTER TABLE `participants`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT for table `questions`
--
ALTER TABLE `questions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `user_response`
--
ALTER TABLE `user_response`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=346;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `comment_response`
--
ALTER TABLE `comment_response`
  ADD CONSTRAINT `comment_response_ibfk_1` FOREIGN KEY (`additional_comment_id`) REFERENCES `additional_comment` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_participant` FOREIGN KEY (`participant_id`) REFERENCES `participants` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
