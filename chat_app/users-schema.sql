-- we are using mysql database
-- log into mysql ; mysql -u <username> -p

CREATE DATABASE BookClubDB;

CREATE TABLE users(
    user_id BIGINT primary key not null auto_increment,
    user_email VARCHAR(50) not null,
    user_name VARCHAR(50) not null,
    user_password VARCHAR(45) not null
);