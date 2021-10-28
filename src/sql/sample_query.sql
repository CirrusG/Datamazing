/*
 * file: sample_query.sql
 * \! echo not supports on the query tool on pgadmin, but could use pspl
 * usage: \i sample_query.sql
 * default sorting is ascending, add desc at the ending to be descending order
 */
\! echo "***********table: account***********"
SELECT
    *
FROM
    account;

-- interval of time
-- https://popsql.com/learn-sql/postgresql/how-to-query-date-and-time-in-postgresql
\! echo "************Users created in the last three hours***********"
SELECT
    first_name,
    last_name
FROM
    account
WHERE
    creation_date BETWEEN (now() - '3 hours'::interval)
    AND now();

\! echo "************table user_accessDatesTimes************"
SELECT
    *
FROM
    user_accessdatestimes;

\! echo "************last access date time of user 'Pixie Blaese'************"
SELECT
    access_date_time
FROM
    user_accessDatesTimes
WHERE
    username LIKE 'pb'
ORDER BY
    access_date_time DESC
LIMIT 1;

\! echo "************table follows************"
SELECT
    *
FROM
    follows;

\! echo "************Pixie Blaese's follower's name************"
SELECT
    account.first_name,
    account.last_name
FROM
    account
    INNER JOIN follows ON account.username = follows.follower
WHERE
    follows.following LIKE 'pb';

\! echo "************table artist************"
SELECT
    *
FROM
    artist;

\! echo "************table genre************"
SELECT
    *
FROM
    genre;

\! echo "************table album************"
SELECT
    *
FROM
    album;

\! echo "************album released in June************"
SELECT
    name
FROM
    album
WHERE (extract(month FROM release_date) = 6);

\! echo "************table alb_gen************"
SELECT
    *
FROM
    alb_gen;

\! echo "************album info with album name, release date and genre************"
SELECT
    album.name,
    album.release_date,
    genre.name
FROM
    alb_gen
    JOIN album ON alb_gen.albumID = album.albumID
    JOIN genre ON alb_gen.genreID = genre.genreID;

\! echo "************table include_in************"
SELECT
    *
FROM
    included_in;

\! echo "************album with artist name************"
SELECT
    album.name,
    included_in.artistname
FROM
    included_in
    JOIN album ON included_in.albumID = album.albumID;

\! echo "**********talbe song***********"
SELECT
    *
FROM
    song;

-- time: minute:second:milliseconds
\! echo "**********song with length longer than 3 minutes***********"
SELECT
    title,
    length,
    release_date,
    artistname
FROM
    song
WHERE
    length > '3:00:00';

\! echo "**********sort song by length(default ascending order)*************"
SELECT
    title,
    length
FROM
    song
ORDER BY
    length;

-- FIXEME: the output will show same song multiple times based on multiple artists
\! echo "**********sort song by name artist name**********"
SELECT
    album.name,
    song.title,
    song.artistname,
    song.length,
    song.release_date
FROM
    included_in
    JOIN song ON song.artistName = included_in.artistName
    JOIN album ON album.albumID = included_in.albumID;

\! echo "***********sort song by year(earliest to latest)***********"
SELECT
    title,
    release_date
FROM
    song
ORDER BY
    date_trunc('year', release_date);

\! echo "***********sort song by genre***********"
SELECT
    song.title,
    genre.name
FROM
    song
    JOIN genre ON song.genreID = genre.genreID
ORDER BY
    genre.name;

\! echo "**********show song with listen count**********"
SELECT
    song.title AS song_name,
    count(plays.songID) AS Listen_Count
FROM
    plays
    JOIN song ON song.songID = plays.songID
GROUP BY
    song.title;

-- The resulting list of songs must show the song’s name, the artist’s name, the album,
-- the length and the listen count.
-- NOTE: since one song could appear on multiple album, the result many be multiple based on the different album
\! echo "***********song list with requirement***********"
SELECT
    song.title AS song_name,
    artist.name AS artist_name,
    album.name AS album_name,
    song.length AS song_length,
    count(plays.songID) AS listen_count
FROM
    song
    JOIN artist ON song.artistname = artist.name
    JOIN features ON song.songID = features.songID
    JOIN album ON features.albumID = album.albumID
    JOIN plays ON song.songID = plays.songID
GROUP BY
    song.songID,
    artist.name,
    album.name;

\! echo "***********table feature**********"
SELECT
    *
FROM
    features;

\! echo "***********table collection**********"
SELECT
    *
FROM
    collection;

--  Users will be to see the list of all their collections by name in ascending order.
--  The list must show the following information per collection
-- – Collection’s name
-- – Number of songs in the collection
-- – Total duration in minutes
\! echo "***********collection list with requirement(default ascending by name)**********"
SELECT
    collection.name AS collection_name,
    count(added_to.songID) AS song_count,
    sum(song.length) AS total_length
FROM
    collection
    JOIN added_to ON collection.collectionID = added_to.collectionID
    JOIN song ON added_to.songID = song.songID
GROUP BY
    collection.name;

\! echo "**********drop albums***********"
DELETE FROM alb_gen
WHERE albumID = 'album1';

DELETE FROM included_in
WHERE albumID = 'album1';

DELETE FROM features
WHERE albumID = 'album1';

DELETE FROM album
WHERE albumID = 'album1';

\! echo "**********drop collection***********"
DELETE FROM added_to
WHERE collectionID = 'collection3';

DELETE FROM collection
WHERE collectionID = 'collection3';

\! echo "**********UPDATE collection name**********"
UPDATE
    collection
SET
    name = 'Sleep Playlist'
WHERE
    collectionID = 'collection1';

SELECT
    *
FROM
    collection
WHERE
    collectionID = 'collection1';

