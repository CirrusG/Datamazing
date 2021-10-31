-- This script was generated by a beta version of the ERD tool in pgAdmin 4.
-- Please log an issue at https://redmine.postgresql.org/projects/pgadmin4/issues/new if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS public.account
(
    username character varying COLLATE pg_catalog."default" NOT NULL,
    email character varying COLLATE pg_catalog."default" NOT NULL,
    password character varying COLLATE pg_catalog."default" NOT NULL,
    first_name character varying COLLATE pg_catalog."default" NOT NULL,
    last_name character varying COLLATE pg_catalog."default" NOT NULL,
    creation_date timestamp with time zone DEFAULT now(),
    CONSTRAINT account_pkey PRIMARY KEY (username)
);

CREATE TABLE IF NOT EXISTS public.added_to
(
    location_number integer,
    username character varying COLLATE pg_catalog."default" NOT NULL,
    collectionid text COLLATE pg_catalog."default" NOT NULL,
    songid text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT added_to_pkey PRIMARY KEY (username, collectionid, songid)
);

CREATE TABLE IF NOT EXISTS public.alb_gen
(
    genreid text COLLATE pg_catalog."default" NOT NULL,
    albumid text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT alb_gen_pkey PRIMARY KEY (genreid, albumid)
);

CREATE TABLE IF NOT EXISTS public.album
(
    albumid text COLLATE pg_catalog."default" NOT NULL DEFAULT ('album'::text || nextval('album_seq'::regclass)),
    name character varying COLLATE pg_catalog."default" NOT NULL,
    release_date date NOT NULL,
    CONSTRAINT album_pkey PRIMARY KEY (albumid)
);

CREATE TABLE IF NOT EXISTS public.artist
(
    name character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT artist_pkey PRIMARY KEY (name)
);

CREATE TABLE IF NOT EXISTS public.collection
(
    collectionid text COLLATE pg_catalog."default" NOT NULL DEFAULT ('collection'::text || nextval('collection_seq'::regclass)),
    username character varying COLLATE pg_catalog."default" NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT collection_pkey PRIMARY KEY (collectionid, username)
);

CREATE TABLE IF NOT EXISTS public.features
(
    track_number integer,
    albumid text COLLATE pg_catalog."default" NOT NULL,
    songid text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT features_pkey PRIMARY KEY (albumid, songid)
);

CREATE TABLE IF NOT EXISTS public.follows
(
    following character varying COLLATE pg_catalog."default" NOT NULL,
    follower character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT follows_pkey PRIMARY KEY (following, follower)
);

CREATE TABLE IF NOT EXISTS public.genre
(
    genreid text COLLATE pg_catalog."default" NOT NULL DEFAULT ('genre'::text || nextval('genre_seq'::regclass)),
    name character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT genre_pkey PRIMARY KEY (genreid)
);

CREATE TABLE IF NOT EXISTS public.included_in
(
    albumid text COLLATE pg_catalog."default",
    artistname character varying COLLATE pg_catalog."default"
);

CREATE TABLE IF NOT EXISTS public.plays
(
    playdatetime timestamp with time zone NOT NULL DEFAULT now(),
    username character varying COLLATE pg_catalog."default" NOT NULL,
    songid text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT plays_pkey PRIMARY KEY (username, songid, playdatetime)
);

CREATE TABLE IF NOT EXISTS public.song
(
    songid text COLLATE pg_catalog."default" NOT NULL DEFAULT ('song'::text || nextval('song_seq'::regclass)),
    title character varying COLLATE pg_catalog."default" NOT NULL,
    length time without time zone NOT NULL,
    release_date date NOT NULL,
    genreid text COLLATE pg_catalog."default",
    artistname character varying COLLATE pg_catalog."default",
    CONSTRAINT song_pkey PRIMARY KEY (songid)
);

CREATE TABLE IF NOT EXISTS public.user_accessdatestimes
(
    username character varying COLLATE pg_catalog."default" NOT NULL,
    access_date_time timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT user_accessdatestimes_pkey PRIMARY KEY (username, access_date_time)
);

ALTER TABLE IF EXISTS public.added_to
    ADD CONSTRAINT added_to_collectionid_fkey FOREIGN KEY (collectionid)
    REFERENCES public.collection (collectionid) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.added_to
    ADD CONSTRAINT added_to_songid_fkey FOREIGN KEY (songid)
    REFERENCES public.song (songid) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.added_to
    ADD CONSTRAINT added_to_username_fkey FOREIGN KEY (username)
    REFERENCES public.account (username) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.alb_gen
    ADD CONSTRAINT alb_gen_albumid_fkey FOREIGN KEY (albumid)
    REFERENCES public.album (albumid) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.alb_gen
    ADD CONSTRAINT alb_gen_genreid_fkey FOREIGN KEY (genreid)
    REFERENCES public.genre (genreid) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.collection
    ADD CONSTRAINT collection_username_fkey FOREIGN KEY (username)
    REFERENCES public.account (username) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.features
    ADD CONSTRAINT features_albumid_fkey FOREIGN KEY (albumid)
    REFERENCES public.album (albumid) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.features
    ADD CONSTRAINT features_songid_fkey FOREIGN KEY (songid)
    REFERENCES public.song (songid) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.follows
    ADD CONSTRAINT follows_follower_fkey FOREIGN KEY (follower)
    REFERENCES public.account (username) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.follows
    ADD CONSTRAINT follows_following_fkey FOREIGN KEY (following)
    REFERENCES public.account (username) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.included_in
    ADD CONSTRAINT included_in_albumid_fkey FOREIGN KEY (albumid)
    REFERENCES public.album (albumid) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.included_in
    ADD CONSTRAINT included_in_artistname_fkey FOREIGN KEY (artistname)
    REFERENCES public.artist (name) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.plays
    ADD CONSTRAINT plays_songid_fkey FOREIGN KEY (songid)
    REFERENCES public.song (songid) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.plays
    ADD CONSTRAINT plays_username_fkey FOREIGN KEY (username)
    REFERENCES public.account (username) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.song
    ADD CONSTRAINT song_artistname_fkey FOREIGN KEY (artistname)
    REFERENCES public.artist (name) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.song
    ADD CONSTRAINT song_genreid_fkey FOREIGN KEY (genreid)
    REFERENCES public.genre (genreid) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.user_accessdatestimes
    ADD CONSTRAINT user_accessdatestimes_username_fkey FOREIGN KEY (username)
    REFERENCES public.account (username) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

END;