CREATE DATABASE IF NOT EXISTS IsPepsiOkay;

USE IsPepsiOkay;

CREATE TABLE IF NOT EXISTS Users (
    uid INTEGER AUTO_INCREMENT,
    email CHAR(254),
    pass CHAR(32),
    uname CHAR(64),
    udob DATE,
    PRIMARY KEY (uid),
    UNIQUE (email)
);


CREATE TABLE IF NOT EXISTS Genres (
    gid INTEGER AUTO_INCREMENT,
    gname CHAR(64),
    PRIMARY KEY (gid),
    UNIQUE (gname)
);


CREATE TABLE IF NOT EXISTS People (
    pid INTEGER AUTO_INCREMENT,
    pname CHAR(64),
    pdob DATE,
    PRIMARY KEY (pid)
);

CREATE TABLE IF NOT EXISTS Movies (
    mid INTEGER AUTO_INCREMENT,
    title CHAR(255),
    mdate DATE,
    runtime INTEGER,
    languages CHAR(64),
    keywords CHAR(128),
    description VARCHAR(1024),
    tagline VARCHAR(512),
    budget REAL,
    box_office REAL,
    mrating CHAR(8),
    country CHAR(64),
    PRIMARY KEY (mid),
    UNIQUE (title, mdate)
);

CREATE TABLE IF NOT EXISTS Likes_Genre (
    uid INTEGER,
    gid INTEGER,
    glike BOOLEAN,
    FOREIGN KEY (uid) REFERENCES Users(uid),
    FOREIGN KEY (gid) REFERENCES Genres(gid),
    PRIMARY KEY (uid, gid)
);

CREATE TABLE IF NOT EXISTS Likes_Person (
    uid INTEGER,
    pid INTEGER,
    plike BOOLEAN,
    FOREIGN KEY (uid) REFERENCES Users(uid),
    FOREIGN KEY (pid) REFERENCES People(pid),
    PRIMARY KEY (uid, pid)
);

CREATE TABLE IF NOT EXISTS Is_Genre (
    mid INTEGER,
    gid INTEGER,
    FOREIGN KEY (mid) REFERENCES Movies(mid),
    FOREIGN KEY (gid) REFERENCES Genres(gid),
    PRIMARY KEY (mid, gid)
);

CREATE TABLE IF NOT EXISTS Has_Watched (
    uid INTEGER,
    mid INTEGER,
    urating REAL,
    FOREIGN KEY (uid) REFERENCES Users(uid),
    FOREIGN KEY (mid) REFERENCES Movies(mid),
    PRIMARY KEY (uid, mid)
);

CREATE TABLE IF NOT EXISTS Involved_In (
    pid INTEGER,
    mid INTEGER,
    directed BOOLEAN,
    produced BOOLEAN,
    wrote BOOLEAN,
    composed BOOLEAN,
    acted BOOLEAN,
    FOREIGN KEY (pid) REFERENCES People(pid),
    FOREIGN KEY (mid) REFERENCES Movies(mid),
    PRIMARY KEY (pid, mid)
);
