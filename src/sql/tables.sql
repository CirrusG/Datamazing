-- file: tables.sql
-- create required tables for music database

CREATE TABLE IF NOT EXISTS account(
    username VARCHAR PRIMARY KEY, 
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    creation_date TIMESTAMP WITH TIME ZONE
);

CREATE TABLE Artist(
    name VARCHAR PRIMARY KEY
);

CREATE TABLE Album(
    albumID UUID PRIMARY KEY,
    name VARCHAR NOT NULL,
    release_date DATE NOT NULL
);

/* Included-In -> Included_In */
CREATE TABLE Included_In(
    albumID UUID REFERENCES Album,
    artistname VARCHAR REFERENCES Artist
);

/* 
User is reserved name 
https://www.postgresql.org/docs/12/sql-keywords-appendix.html
user -> account
*/

CREATE TABLE Genre(
    genreID UUID PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE
);

CREATE TABLE Song(
    songID UUID PRIMARY KEY,
    title VARCHAR NOT NULL, 
    /*may be length reserved*/
    length TIME NOT NULL,
    release_date DATE NOT NULL,
    genreID UUID REFERENCES Genre,
    artistName VARCHAR REFERENCES Artist
);

CREATE TABLE Collection(
    collectionID UUID UNIQUE,
    username VARCHAR REFERENCES Account,
    name VARCHAR NOT NULL,
    PRIMARY KEY(collectionID, username)
);


/*
Added-To --> Added_To
location_number means the serial number
*/

CREATE TABLE Added_To(
    location_number SERIAL UNIQUE,
    username VARCHAR REFERENCES Account,
    songID UUID REFERENCES Song,
    collectionID UUID REFERENCES Collection(collectionID),
    PRIMARY KEY(username, songID, collectionID)
);

/*Alb-Gen -> Alb_Gen*/
CREATE TABLE Alb_Gen(
    genreID UUID REFERENCES Genre,
    albumID UUID REFERENCES Album,
    PRIMARY KEY(genreID, albumID)
);

CREATE TABLE Follows(
    following VARCHAR REFERENCES Account, 
    follower VARCHAR REFERENCES Account,
    PRIMARY KEY(following, follower)
);

/*User-AccessDatasTimes -> User_AccessDatesTimes*/
CREATE TABLE User_AccessDatesTimes(
    access_data_time TIMESTAMP WITH TIME ZONE,
    username VARCHAR REFERENCES Account,
    PRIMARY KEY(access_data_time, username)
);

CREATE TABLE Features(
    track_number SERIAL UNIQUE,
    albumID UUID REFERENCES Album,
    songID UUID REFERENCES Song,
    PRIMARY KEY(albumID, songID)
);

CREATE TABLE Plays(
    playDateTime TIMESTAMP,
    username VARCHAR REFERENCES Account,
    songID UUID REFERENCES Song,
    PRIMARY KEY(username, songID, playDateTime)
);

