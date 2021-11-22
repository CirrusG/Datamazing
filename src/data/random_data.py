"""
file: random_data.py
insert random data for phase 4 (mainly are play records)
"""
import psycopg2
from psycopg2 import sql

import sys
sys.path.insert(1, '../cli/')
import starbug
import read
import random
import time
import datetime
from datetime import timedelta
from datetime import datetime

def random_date_times():
    """
    Resource:
    https://www.w3schools.com/python/python_datetime.asp
    https://stackoverflow.com/questions/466345/converting-string-into-datetime
    """
    start = datetime.fromisoformat('2021-01-01 00:00:00')
    end = datetime.now()
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

def get_user_list():
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = """select username from account"""
        curs.execute(query,)
        result = read.get_result(curs)
    except (Exception, psycopg2.Error) as error:
        print("get_user_list(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
        return result

def random_plays_song():
    conn = curs = None
    users = get_user_list()[1]

    for user in users:
        user = user[0]
        for i in range(random.randint(300, 530)):
            try:
                conn = starbug.connect()
                curs = conn.cursor()
                query = """insert into plays (playDateTime, username, songid) values (%s, %s, %s)"""
                curs.execute(query, (random_date_times(), user, "song" + str(random.randint(1, 36273)),))
                conn.commit()
                # print(read.get_result(curs))
            except (Exception, psycopg2.Error) as error:
                print("get_user_list(ERROR):", error)
            finally:
                starbug.disconnect(conn, curs)

def get_user_collection(username):
    conn = curs = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = """select collectionid from collection where username = %s"""
        curs.execute(query, (username,))
        collecs = read.get_result(curs)
    except (Exception, psycopg2.Error) as error:
        print("get_user_list(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return collecs

def get_collec_size(collectionid):
    conn = curs = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = """select count(added_to.songid)
                from added_to join song on added_to.songid = song.songid
                where added_to.collectionid = %s"""
        curs.execute(query, (collectionid,))
        result = read.get_result(curs)[0][0]
    except (Exception, psycopg2.Error) as error:
        print("get_user_list(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result

def random_song_collection():
    conn = curs = None
    users = get_user_list()

    for user in users:
        user = user[0]
        collecs = get_user_collection(user)
        for collec in collecs:
            collec = collec[0]
            for i in range(10, 20):
                try:
                    conn = starbug.connect()
                    curs = conn.cursor()
                    max = get_collec_size(collec)
                    query = """insert into added_to (location_number, username, collectionid, songid) values (%s, %s, %s, %s)"""
                    curs.execute(query, (max, user, collec, "song" + str(random.randint(1, 36273)),))
                    conn.commit()
                    # print(read.get_result(curs))
                except (Exception, psycopg2.Error) as error:
                    print("get_user_list(ERROR):", error)
                finally:
                    starbug.disconnect(conn, curs)

def random_play_collection():
    conn = curs = None
    users = get_user_list()

    for user in users:
        user = user[0]
        collecs = get_user_collection(user)
        for collec in collecs:
            collec = collec[0]
            for i in range(1, 10):
                try:
                    conn = starbug.connect()
                    curs = conn.cursor()
                    query = """select songid from added_to where collectionid = %s"""
                    curs.execute(query, (collec, ))
                    songs = read.get_result(curs)
                    for song in songs:
                        song = song[0]
                        query = """insert into plays (playDateTime, username, songid) values (%s, %s, %s)"""
                        curs.execute(query, (random_date_times(), user, song))
                        conn.commit()
                except (Exception, psycopg2.Error) as error:
                    print("get_user_list(ERROR):", error)
                finally:
                    starbug.disconnect(conn, curs)

def main():
    return


if __name__ == '__main__':
    main()