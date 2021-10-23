/*
file: table.sql
create required table for database of each user
*/

CREATE TABLE Artist(
    name VARCHAR PRIMARY KEY
);

CREATE TABLE Album(
    albumID INT PRIMARY KEY,
    name VARCHAR NOT NULL,
    release_date DATETIME(MM-DD-YYYY) NOT NULL
);

CREATE TABLE User(
    username VARCHAR PRIMARY KEY, 
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    creation_date TIMESTAMP 
);

CREATE TABLE Song(
    songID INT PRIMARY KEY,
    title VARCHAR NOT NULL, 
    length TIME (mm:ss) NOT NULL,
    release_date DATETIME(MM-DD-YYYY) NOT NULL,
    genreID INT REFERENCES Genre(genreID), 
    artistName VARCHAR REFERENCES Artist(name),

);

CREATE TABLE Collection(
    collectionID
    username
    name
);

CREATE TABLE Genre(
    genreID
    name
);


CREATE TABLE Added-To(
    collectionID
    username
    songID
    location_number
);

CREATE TABLE Alb-Gen(
    genreID
    albumID
);

CREATE TABLE Follows(
    fllowing
    follower
);

CREATE TABLE User-AccessDatesTimes(
    access_data_time
    username
);

CREATE TABLE Features(
    albumID
    songID
    track_number
);

CREATE TABLE Plays(
    username
    songID
    playDateTime
);

CREATE TABLE Included-In(){
    albumID
    artistname
}
