import psycopg2
from psycopg2 import sql
import starbug
import read


# create - insert

def login_user(username):
    """
    login user (add record into accessdatestimes)

    :precondition: check username, password in the cli application
    :return true if successfully login
    """

    result = False
    conn = curs = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        curs.execute(
            "insert into user_accessdatestimes(username) values (%s)", (username,))
        conn.commit()
        result = True
    except(Exception, psycopg2.DatabaseError) as error:
        print("query.pass_correct(ERROR)", error)
    finally:
        starbug.disconnect(conn, curs)
    return result


def register_user(username, password, first, last, email):
    """
    1. register new user
    since each user has unique email,
    so only need to check uname if has existed in the database
    2. insert the account into database
    :return if successful register
    """
    conn = curs = None
    result = False
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = """INSERT INTO Account VALUES (%s, %s, %s, %s, %s)"""
        curs.execute(query, (username, email, password, first, last,))
        conn.commit()
        result = True
    except (Exception, psycopg2.Error) as error:
        print("create.register_user(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result


def follow_friend(username, friend):
    """
    follow friend (user who follows friend is follower, friend is following)

    :param username: current user in the cli that want to follow friend(follower)
    :param friend: friend to follow (following)
    :return true if successfully follow otherwise false
    """
    conn = curs = result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        if read.verify_username(friend):
            query = """insert into follows (following, follower) values (%s, %s)"""
            curs.execute(query, (friend, username,))
            conn.commit()
            result = read.get_user_info(friend, False)
    except (Exception, psycopg2.Error) as error:
        print("follow_friend(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result


def create_collec(username, name):
    conn = curs = result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = """insert into collection (username, name) values (%s, %s) returning name, collectionid"""
        curs.execute(query, (username, name))
        conn.commit()
        result = read.get_result(curs)[0]
    except (Exception, psycopg2.Error) as error:
        print("create_collec(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result


def play_song(username, songid):
    conn = curs = result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = """insert into plays (username, songID) values (%s, %s)"""
        curs.execute(query, (username, songid))
        conn.commit()
        result = read.get_song_info(songid)
    except (Exception, psycopg2.Error) as error:
        print("follow_friend(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result


def add_song_collec(username, collectionid, songid):
    """
    Since adding and modifying order are different actions,
    this method is only used to automatically add songs to the end of the collection.
    """
    conn = curs = result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        collection_info = read.get_collec_info(username, collectionid)
        last_number = collection_info[-1] + 1
        query = """insert into added_to values (%s, %s, %s, %s) returning location_number"""
        curs.execute(query, (last_number, username, collectionid, songid,))
        conn.commit()
        result = read.get_result(curs)
    except (Exception, psycopg2.Error) as error:
        print("query.add_song_collec(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
        return result


def album_to_collec(username, collectionid, albumid):
    for song in read.list_album(albumid):
        add_song_collec(username, collectionid, song[1])


if __name__ == '__main__':
    # print(add_collec('ly', 'underground'))
    print(create_collec('ly', 'happy'))