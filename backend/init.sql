-- Active: 1678143755910@@127.0.0.1@3306@leaderboard
-- CREATE TABLE users (
--   id INT AUTO_INCREMENT PRIMARY KEY,
--   first_name VARCHAR(50) NOT NULL,
--   last_name VARCHAR(50) NOT NULL,
--   username VARCHAR(25) NOT NULL UNIQUE,
--   student_id CHAR(8) NOT NULL,
--   email VARCHAR(50) NOT NULL UNIQUE,
--   hashed_password VARCHAR(100) NOT NULL
-- );

-- CREATE TABLE comments (
--           id INT AUTO_INCREMENT PRIMARY KEY,
--           username VARCHAR(50) NOT NULL,
--           comment VARCHAR(500) NOT NULL,
--           comment_id VARCHAR(50) NOT NULL,
--           date VARCHAR(50) NOT NULL,


--         );
-- show TABLES;

-- drop table users; 

-- INSERT INTO users (username, first_name, last_name, email, student_id, hashed_password)
-- VALUES ('johndoe', 'John', 'Doe', 'johndoe@example.com', '12345678', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW');


SELECT * FROM users;
SELECT * FROM comments;


SELECT users.username FROM users WHERE users.email="johndoe@example.com";



SELECT username, first_name, last_name, email, student_id, hashed_password FROM users WHERE username="johndoe";