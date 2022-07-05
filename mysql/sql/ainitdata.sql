DROP DATABASE IF EXISTS share_course_plan;
CREATE DATABASE share_course_plan;

USE share_course_plan;

/* 1. ユーザ情報 */
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    user_id     CHAR(32)                PRIMARY KEY,
    email       CHAR(128)   NOT NULL    UNIQUE,
    `name`      VARCHAR(64) NOT NULL,
    is_admin    BOOLEAN     NOT NULL    DEFAULT 0
);

/* 2. ユーザ認証情報 */
DROP TABLE IF EXISTS users_auth;
CREATE TABLE users_auth (
    user_id     CHAR(32)    NOT NULL    UNIQUE,
    hashed_pw   CHAR(64)    NOT NULL,
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

/* 3. ユーザ設定 */
DROP TABLE IF EXISTS users_settings;
CREATE TABLE users_settings (
    user_id                     CHAR(32)    NOT NULL    UNIQUE,
    taking_class_is_public      BOOLEAN     NOT NULL    DEFAULT 0,
    complete_class_is_public    BOOLEAN     NOT NULL    DEFAULT 0,
    grade_is_public             BOOLEAN     NOT NULL    DEFAULT 0,
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

/* 4. 科目 */
DROP TABLE IF EXISTS classes;
CREATE TABLE classes (
    class_id    CHAR(16)                PRIMARY KEY,
    `name`      CHAR(32)    NOT NULL,
    credits     FLOAT       NOT NULL
);

/* 5. 履修&成績管理 */
DROP TABLE IF EXISTS users_classes;
CREATE TABLE users_classes (
    user_id     CHAR(32),
    class_id    CHAR(16),
    grade       CHAR(2)     DEFAULT NULL,
    PRIMARY KEY (user_id, class_id),
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (class_id)
        REFERENCES classes(class_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

/* 6. 投稿 */
DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
    post_id     CHAR(32)                PRIMARY KEY,
    user_id     CHAR(32)    NOT NULL,
    post_on     DATETIME    NOT NULL,
    `text`      VARCHAR(64) NOT NULL,
    reply_to    CHAR(32),
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (reply_to)
        REFERENCES posts(post_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
