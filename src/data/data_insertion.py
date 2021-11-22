# file: data_insertion.py
# insert required artist, genre, song, album data into database
# random data insertion for phrase 3 (music, artist, album, collections)
import csv
from random import randint

import psycopg2
# will change to cli.starbug later
from psycopg2 import sql

import cli.starbug as starbug
import cli.query as query

import time

from src.cli.query import login_user
# do not open csv files during inserting, otherwise throws 'OSError: [Errno 5] Input/output error
# 🎈*IMPORTANT*: overall length of run at least 25 minutes (import to starbug early)
#global variable server to make ssh connection
server = starbug.conn_server()
server.start()


def artist_insert():
    # done insert artist
    conn = curs = None
    with open('spotify-data/artists.csv', newline='') as artistfile:
        reader = csv.reader(artistfile, delimiter=',')
        # jump header
        next(reader)
        for row in reader:
            try:
                conn = starbug.connect(server)
                curs = conn.cursor()
                query = "insert into artist values (%s)"
                curs.execute(query, (row[-1],))
                conn.commit()
            except (psycopg2.DatabaseError) as error:
                print("artist_insert(ERROR):", error)
            finally:
                starbug.disconnect(conn, curs)

def genre_insert():
    # done insert genre
    with open('spotify-data/genres.csv', newline='') as genresfile:
        reader = csv.reader(genresfile, delimiter=',')
        # jump header
        next(reader)
        for row in reader:
            try:
                conn = starbug.connect(server)
                curs = conn.cursor()
                # print(row[-1])
                query = "insert into genre (name) values (%s)"
                curs.execute(query, (row[1],))
                conn.commit()
            except (Exception, psycopg2.Error) as error:
                print("genre_insert(ERROR):", error)
            finally:
                starbug.disconnect(conn, curs)

def song_album_insert():
    # table: song, album, included_in, features, alb_gen
        with open('spotify-data/tracks.csv') as tracksfile:
            reader = csv.reader(tracksfile, delimiter=',')
            # jump header
            #next(reader)

            for row in reader:
                try:
                    conn = starbug.connect(server)
                    curs = conn.cursor()
                    # name: 1, artist_name: 4, album_name: 6, track_number 7,
                    # track_duration(mm:ss): -1, track_genre: 9, track_release: 10
                    track_name = row[1]
                    artist_name = row[4]
                    track_genre = row[9]
                    curs.execute("select genreID from genre where name = %s", (track_genre,))
                    genreID = curs.fetchone()
                    if genreID is None:
                        print("song_album_insert(ERROR): genre does not exist")
                        continue
                    genreID = genreID[0]
                    track_duration = row[-1]
                    track_release = row[10]
                    album_name = row[6] # feature
                    track_number = row[7] # feature
                    # => album
                    curs.execute("select albumID from album where name = %s", (album_name,))
                    albumID = curs.fetchone()
                    if albumID is None:
                        query = "insert into album (name, release_date) values (%s, %s)"
                        curs.execute(query, (album_name, track_release))
                        conn.commit()
                        curs.execute("select albumID from album where name = %s", (album_name,))
                        albumID = curs.fetchone()
                    albumID = albumID[0]
                    # => include in
                    curs.execute("select artistname from included_in where albumID = %s", (albumID,))
                    exist = False
                    for each in query.get_result(curs):
                        # parse result to fit the compare
                        #print('artistname get', each[0])
                        if each[0] == artist_name:
                            exist = True
                            break
                    if not exist:
                        curs.execute("insert into included_in values (%s, %s)", (albumID, artist_name,))
                        conn.commit()
                    # => alb_gen
                    exist = False
                    curs.execute("select genreID from alb_gen where albumID = %s", (albumID,))
                    for each in query.get_result(curs):
                        #print('genre get', each)
                        if each[0] == genreID:
                            exist = True
                            break
                    if not exist:
                        curs.execute("insert into alb_gen values (%s, %s)", (genreID, albumID,))
                        conn.commit()
                    # => song
                    #print(name, artist_name, album_name, track_number, track_duration, track_genre, track_release)
                    query = "insert into song (title, length, release_date, genreID, artistName) values (%s, %s, %s, %s, %s)"
                    curs.execute(query, (track_name, track_duration, track_release, genreID, artist_name,))
                    conn.commit()
                    curs.execute("select songID from song where title = %s", (track_name,))
                    songID = curs.fetchone()[0]
                    # => features
                    curs.execute("select * from features where albumID = %s and songID = %s", (albumID, songID))
                    feature_res = curs.fetchone()
                    if feature_res is None:
                        query = "insert into features values (%s, %s, %s)"
                        curs.execute(query, (track_number, albumID, songID))
                        conn.commit()
                except (Exception, psycopg2.Error) as error:
                    print("song_album_insert(ERROR):", error)
                finally:
                    starbug.disconnect(conn, curs)
                # for test
                # break

def user_insert():
    with open ('user-data/users.csv', newline='') as userfile:
        reader = csv.reader(userfile, delimiter=',')
        next(reader)
        for row in reader:
            #print(row)
            username = row[0]
            email = row[1]
            password = row[2]
            first = row[3]
            last = row[4]
            query.register_user(username, password, first, last, email)

def get_username_list():
    try:
        conn = starbug.connect(server)
        curs = conn.cursor()
        curs.execute("select username from account")
        result = query.get_result(curs)
    except (Exception, psycopg2.Error) as error:
        print("user_login(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result

def user_login_insert():
    for each in get_username_list():
        login_user(each[0])
    

def collection_insert():
    # add collection of random user until all collection assigned
    # collection -> added_to
    with open('user-data/collection.csv', newline='') as collecfile:
        reader = csv.reader(collecfile, delimiter=',')
        next(reader)
        for row in reader:
            try:
                conn = starbug.connect(server)
                curs = conn.cursor()
                curs.execute("select username from account")
                result = query.get_result(curs)
                username = result[randint(0, len(result))][0]
                #print(username)
                query.add_collec(username, row[0])

            except (Exception, psycopg2.Error) as error:
                print("collection_insert(ERROR):", error)
            finally:
                starbug.disconnect(conn, curs)

def get_table_size(table):
    conn = curs =  None
    result = []
    try:
        conn = starbug.connect(server)
        curs = conn.cursor()
        one_query = sql.SQL("select count(*) from {table};").format(table = sql.Identifier(table))
        curs.execute(one_query)
        result = query.get_result(curs)
    except (Exception, psycopg2.Error) as error:
        print("get_table_size(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result[0][0]

def get_collec_size(collecid):
    try:
        conn = starbug.connect(server)
        curs = conn.cursor()
        curs.execute("select count(*) from added_to where collectionid = %s", (collecid,))
        num = query.get_result(curs)[0][0]
    except (Exception, psycopg2.Error) as error:
        print("insert_song_collec(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return num

def insert_song_collec():
    conn = curs = None
    #user_num = get_table_size("account")
    song_num = get_table_size("song")
    collec_num = get_table_size("collection")
    for num in range(1, 2000):
        try:
            conn = starbug.connect(server)
            curs = conn.cursor()
            collecid = "collection" + str(randint(1, collec_num))
            curs.execute("select username from collection where collectionid = %s", (collecid,))
            username = query.get_result(curs)[0][0]
            songid = "song" + str(randint(1, song_num))
            curs.execute("insert into added_to values(%s, %s, %s, %s)", (get_collec_size(collecid)+1, username, collecid, songid,))
            #print(collecid)
            conn.commit()
        except (Exception, psycopg2.Error) as error:
            print("insert_song_collec(ERROR):", error)
        finally:
            starbug.disconnect(conn, curs)

def random_plays():
    # for easier to insert, play album
    conn = curs = None
    user_num = get_table_size("account")
    album_num = get_table_size("album")
    user_list = get_username_list()
    #print(get_username_list())
    #collec_num = get_table_size("collection")
    for num in range(1, 100):
        try:
            albumid = 'album' + str(randint(1, album_num))
            username = user_list[randint(1, user_num) - 1][0]
            print(query.play_album(username, albumid))
        except (Exception, psycopg2.Error) as error:
            print("insert_song_collec(ERROR):", error)
        finally:
            starbug.disconnect(conn, curs)
        #break

def main():
    return

if __name__ == "__main__":
    main()

