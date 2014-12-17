DROP DATABASE IF EXISTS IsPepsiOkay;
CREATE DATABASE IsPepsiOkay;

USE IsPepsiOkay;

SET collation_connection = 'utf8_general_ci';
ALTER DATABASE IsPepsiOkay CHARACTER SET utf8 COLLATE utf8_general_ci;


CREATE TABLE IF NOT EXISTS Users (
    uid INTEGER AUTO_INCREMENT,
    email CHAR(254),
    pass CHAR(32),
    uname CHAR(64),
    udob DATE,
    PRIMARY KEY (uid),
    UNIQUE (email)
);
ALTER TABLE Users CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE IF NOT EXISTS Genres (
    gid INTEGER AUTO_INCREMENT,
    gname CHAR(64),
    PRIMARY KEY (gid),
    UNIQUE (gname)
);
ALTER TABLE Genres CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE IF NOT EXISTS People (
    pid INTEGER AUTO_INCREMENT,
    pname CHAR(64),
    pdob DATE,
    PRIMARY KEY (pid)
);
ALTER TABLE People CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE IF NOT EXISTS Movies (
    mid CHAR(32),
    title CHAR(255),
    mdate DATE,
    runtime INTEGER,
    languages CHAR(64),
    description VARCHAR(4096),
    budget INTEGER,
    box_office INTEGER,
    country CHAR(64),
    PRIMARY KEY (mid),
    UNIQUE (title, mdate)
);
ALTER TABLE Movies CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE IF NOT EXISTS Likes_Genre (
    uid INTEGER,
    gid INTEGER,
    glike BOOLEAN,
    FOREIGN KEY (uid) REFERENCES Users(uid),
    FOREIGN KEY (gid) REFERENCES Genres(gid),
    PRIMARY KEY (uid, gid)
);
ALTER TABLE Likes_Genre CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE IF NOT EXISTS Likes_Person (
    uid INTEGER,
    pid INTEGER,
    plike BOOLEAN,
    FOREIGN KEY (uid) REFERENCES Users(uid),
    FOREIGN KEY (pid) REFERENCES People(pid),
    PRIMARY KEY (uid, pid)
);
ALTER TABLE Likes_Person CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE IF NOT EXISTS Is_Genre (
    mid CHAR(32),
    gid INTEGER,
    FOREIGN KEY (mid) REFERENCES Movies(mid),
    FOREIGN KEY (gid) REFERENCES Genres(gid),
    PRIMARY KEY (mid, gid)
);
ALTER TABLE Is_Genre CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE IF NOT EXISTS Has_Watched (
    uid INTEGER,
    mid CHAR(32),
    urating REAL,
    FOREIGN KEY (uid) REFERENCES Users(uid),
    FOREIGN KEY (mid) REFERENCES Movies(mid),
    PRIMARY KEY (uid, mid)
);
ALTER TABLE Has_Watched CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE IF NOT EXISTS Involved_In (
    pid INTEGER,
    mid CHAR(32),
    directed BOOLEAN,
    produced BOOLEAN,
    wrote BOOLEAN,
    composed BOOLEAN,
    acted BOOLEAN,
    FOREIGN KEY (pid) REFERENCES People(pid),
    FOREIGN KEY (mid) REFERENCES Movies(mid),
    PRIMARY KEY (pid, mid)
);
ALTER TABLE Involved_In CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
