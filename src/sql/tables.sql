/* 
 * file: tables.sql
 * create required tables for music database value of talbes account
 * 
 * Since we don't define schema, the following sql statements will be inserted into the public schema by default.
 * The table name will become lowercase after inserting into the database
 * pspl usage: \i tables.sql
 */
-- default postgres time zone is `Etc/UTC`, change it to new york time
-- note: The time zone is already set in the starbug database, 
-- this is set for test database, but repeated the setting will not affect starbug database. 
set timezone='America/New_York';

-- account
-- email should be unique for searching friends (avoid multiple results)
CREATE TABLE Account (
    username varchar PRIMARY KEY,
    email varchar NOT NULL UNIQUE,
    password VARCHAR NOT NULL,
    first_name varchar NOT NULL,
    last_name varchar NOT NULL,
    creation_date timestamp with time zone DEFAULT now() -- auto generate creation_date
);

-- User_AccessDatesTimes
-- User-AccessDatesTimes -> User_AccessDatesTimes
CREATE TABLE User_AccessDatesTimes (
    username varchar REFERENCES Account,
    access_date_time timestamp with time zone NOT NULL DEFAULT now(),
    PRIMARY KEY (username, access_date_time)
);

-- Follows
CREATE TABLE Follows (
    following VARCHAR REFERENCES Account,
    follower varchar REFERENCES Account,
    PRIMARY KEY (FOLLOWING, follower)
);

-- Artist
CREATE TABLE Artist (
    name varchar PRIMARY KEY
);

-- Genre
CREATE SEQUENCE genre_seq
    START 1;

CREATE TABLE Genre (
    genreID text NOT NULL DEFAULT ('genre' || nextval('genre_seq')) PRIMARY KEY,
    name varchar NOT NULL UNIQUE
);

ALTER SEQUENCE genre_seq OWNED BY Genre.genreID;

-- Album
-- id's prefix is the name of table
-- Note: Although the ID is used as the main key, it is not directly related to the other attributes of the table.
-- When the user needs to use one or more other attributes to obtain possible results, the user finally selects the target album by choosing the id.
CREATE SEQUENCE album_seq
    START 1;

CREATE TABLE Album (
    albumID text NOT NULL DEFAULT ('album' || nextval('album_seq')) PRIMARY KEY,
    name varchar NOT NULL,
    -- date not support insert 'only year'
    -- if met invalid date, may parse into 01/01/'year
    -- supported example: https://www.postgresql.org/docs/12/datatype-datetime.html#DATATYPE-DATETIME-DATE-TABLE
    release_date date NOT NULL
);

ALTER SEQUENCE album_seq OWNED BY Album.albumID;

-- Alb_Gen
-- Alb-Gen -> Alb_Gen
CREATE TABLE Alb_Gen (
    genreID text REFERENCES Genre,
    albumID text REFERENCES Album,
    PRIMARY KEY (genreID, albumID)
);

-- Included_In
-- Included-In -> Included_In
CREATE TABLE Included_In (
    albumID text REFERENCES Album,
    artistname varchar REFERENCES Artist
);

-- Song
CREATE SEQUENCE song_seq
    START 1;

CREATE TABLE Song (
    songID text NOT NULL DEFAULT ('song' || nextval('song_seq')) PRIMARY KEY,
    title varchar NOT NULL,
    -- time: minute:second:milliseconds
    length time NOT NULL,
    release_date date NOT NULL,
    genreID text REFERENCES Genre,
    artistName varchar REFERENCES Artist
);

ALTER SEQUENCE song_seq OWNED BY Song.songID;

-- Features (link between song and album)
-- the track_number need to handle by number of album appearances
-- may need to query to get the count, then add 1 to this for track_number of new insertion
CREATE TABLE Features (
    track_number int,
    albumID text REFERENCES Album,
    songID text REFERENCES Song,
    PRIMARY KEY (albumID, songID)
);

-- Collection
-- User is reserved name
-- https://www.postgresql.org/docs/12/sql-keywords-appendix.html
-- user -> account
CREATE SEQUENCE collection_seq
    START 1;

CREATE TABLE Collection (
    collectionID text NOT NULL DEFAULT ('collection' || nextval('collection_seq')) UNIQUE,
    username varchar REFERENCES Account,
    name varchar NOT NULL,
    PRIMARY KEY (collectionID, username)
);

ALTER SEQUENCE collection_seq OWNED BY Collection.collectionID;

-- Added_To
-- Added-To --> Added_To
-- location_number means the serial number
CREATE TABLE Added_To (
    location_number int,
    username varchar REFERENCES Account,
    collectionID text REFERENCES Collection (collectionID),
    songID text REFERENCES Song,
    PRIMARY KEY (username, collectionID, songID)
);

-- plays
CREATE TABLE Plays (
    playDateTime timestamp with time zone DEFAULT now(),
    username varchar REFERENCES Account,
    songID text REFERENCES Song,
    PRIMARY KEY (username, songID, playDateTime)
);

