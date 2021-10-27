/*
 * file: sample_query.sql
 * \! echo not supports on the query tool on pgadmin, but could use pspl
 * usage: \i sample_query.sql
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

-- psql:src/sql/sample_query.sql:96: ERROR:  table name "alb_gen" specified more than once
\! echo "************table album, genre with alb_gen (FIXME)************"
SELECT
    album.name,
    album.release_date,
    genre.name
FROM ((alb_gen
        INNER JOIN alb_gen ON alb_gen.albumID = album.albumID)
    INNER JOIN genre ON alb_gen.genreID = genre.genreID);

