CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    birthday DATE
);

SET GLOBAL innodb_flush_log_at_trx_commit = 2;

TRUNCATE TABLE users;