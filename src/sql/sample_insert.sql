-- table account insertion, creation datetime generted automatily
INSERT INTO account
    VALUES ('pb', 'pb@mail.com', 'password', 'Pixie', 'Blaese');

INSERT INTO account
    VALUES ('ta', 'ta@mail.com', 'password', 'Taya', 'Andersen');

INSERT INTO account
    VALUES ('sn', 'sn@mail.com', 'password', 'Spike', 'Noel');

-- user_accessdatetime insertion
INSERT INTO user_accessdatestimes
    VALUES ('pb');

INSERT INTO user_accessdatestimes
    VALUES ('ta');

INSERT INTO user_accessdatestimes
    VALUES ('sn');

-- follows
INSERT INTO follows
    VALUES ('pb', 'ta');

INSERT INTO follows
    VALUES ('pb', 'sn');

INSERT INTO follows
    VALUES ('ta', 'sn');

-- artist
INSERT INTO artist
    VALUES ('Stan Getz');

INSERT INTO artist
    VALUES ('Joao Gilberto');

INSERT INTO artist
    VALUES ('Antonio Carlos Jobim');

-- album
-- date with only year or year with month, need to be handled in the program
INSERT INTO album (name, release_date)
    VALUES ('The girl From Ipanema', '1/1/1989');

INSERT INTO album (name, release_date)
    VALUES ('Amoroso', '1977-1-26');

INSERT INTO album (name, release_date)
    VALUES ('Wave', 'June 15, 1967');

-- genre
INSERT INTO genre
    VALUES (DEFAULT, 'Jazz');

INSERT INTO genre
    VALUES (DEFAULT, 'Pop');

INSERT INTO genre
    VALUES (DEFAULT, 'Bossa Nova');

-- alb_gen
-- reflection: although managing genre tables with ids is more standardized (with a consistent id style),
-- the actual application requires only the name of the genre,
-- so when inserting data, a conditional function is needed to obtain the id value.
INSERT INTO alb_gen
    VALUES ('genre1', 'album1');

INSERT INTO alb_gen
    VALUES ('genre2', 'album1');

INSERT INTO alb_gen
    VALUES ('genre2', 'album2');

INSERT INTO alb_gen
    VALUES ('genre3', 'album3');

INSERT INTO alb_gen
    VALUES ('genre1', 'album3');

-- included_in
INSERT INTO included_in
    VALUES ('album1', 'Joao Gilberto');

INSERT INTO included_in
    VALUES ('album1', 'Antonio Carlos Jobim');

INSERT INTO included_in
    VALUES ('album1', 'Stan Getz');

INSERT INTO included_in
    VALUES ('album2', 'Joao Gilberto');

INSERT INTO included_in
    VALUES ('album3', 'Antonio Carlos Jobim');

-- song
-- reflection: manytimes, a song is released as a part of a album, so the release date may be same as the album
-- case-sensitivity may affect the search of song/album/artist name; need to handle in the program
INSERT INTO song
    VALUES (DEFAULT, 'Doralice', '2:44', 'May 1,1964', 'genre1', 'Joao Gilberto');

INSERT INTO song
    VALUES (DEFAULT, 'Desafinado', '5:50', '1989/1/1', 'genre1', 'Stan Getz');

INSERT INTO song
    VALUES (DEFAULT, 'Look To The Sky', '2:20', 'june 15, 1967', 'genre3', 'Antonio Carlos Jobim');

INSERT INTO song
    VALUES (DEFAULT, 'Wave', '4:41', '11/26/1977', 'genre3', 'Joao Gilberto');

-- features
-- track number need to be handled in the program
INSERT INTO features
    VALUES (1, 'album1', 'song1');

INSERT INTO features
    VALUES (1, 'album2', 'song1');

INSERT INTO features
    VALUES (1, 'album3', 'song3');

INSERT INTO features
    VALUES (2, 'album1', 'song4');

-- collection
INSERT INTO collection
    VALUES (DEFAULT, 'pb', 'My Favorite');

INSERT INTO collection
    VALUES (DEFAULT, 'ta', 'Running playlist');

INSERT INTO collection
    VALUES (DEFAULT, 'sn', 'Afternoon Tea Playlist');

-- added_to
-- collection id need to be selected by user on the CLI program
-- location_number is gotted by checking how many songs are in the collection
INSERT INTO added_to
    VALUES (1, 'pb', 'collection1', 'song1');

INSERT INTO added_to
    VALUES (2, 'ta', 'collection2', 'song3');

INSERT INTO added_to
    VALUES (1, 'sn', 'collection3', 'song1');

INSERT INTO added_to
    VALUES (2, 'sn', 'collection3', 'song2');

-- plays
INSERT INTO plays
    VALUES (DEFAULT, 'pb', 'song1');

INSERT INTO plays
    VALUES (DEFAULT, 'ta', 'song1');

INSERT INTO plays
    VALUES (DEFAULT, 'sn', 'song1');

