# file: query.py
# this file is interface between cli and database
# @author Datamazing
# resource:
# Basic module usage: https://www.psycopg.org/docs/usage.html (query params, adaptation of python values to sql types, etcs)
# SQL string composition: https://www.psycopg.org/docs/sql.html#sql-objects
# 

import psycopg2
# just for ease of changing the database(local -> starbug)
from psycopg2 import sql

import local as starbug


def if_exist(table, column, value):
    # check if value exists as column in the table
    # 🎉 PASS TEST
    # reference
    row = conn = curs = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        # ERROR <expression>, <table expression>, ALL, DISTINCT, EXCEPT, FETCH, FOR, INTERSECT, INTO, LIMIT, OFFSET,
        # ORDER, UNION or WINDOW expected, got '{'
        # NO EFFECT ON RUNNING (JUST IGNORE IT)
        query = sql.SQL('select {field} from {table} where {field} = %s').format(
            field=sql.Identifier(column), table=sql.Identifier(table))
        curs.execute(query, (value,))
        row = curs.fetchone()
    except(Exception, psycopg2.Error) as error:
        print("query.check_exist(ERROR)", error)
    finally:
        starbug.disconnect(conn, curs)
    # NOTE: here can return row, then in another file to check if is None, if not, just get the value
    return row is not None


def get_result(curs):
    # get array of query result, need to parse in the cli program
    # 🎉 PASS TEST
    result = None
    try:
        result = []
        row = curs.fetchone()
        while row is not None:
            result.append(row)
            print(row)
            row = curs.fetchone()
            # psycopg2.RaiseException
    except (Exception, psycopg2.Error) as error:
        print("query.fetch(ERROR):", error)
    return result


def user_exists(username):
    # check username if exists
    # 🎉 PASS TEST
    return if_exist('account', 'username', username)


def email_exists(email):
    # check email if exists
    # 🎉 PASS TEST
    return if_exist('account', 'email', email)


def pass_correct(username, password):
    # check if password correct
    # since the user pass login check, no require to check if password is None
    # 🎉 PASS TEST
    conn = curs = result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        curs.execute(
            "SELECT password FROM Account WHERE username=%s", (username,))
        row = curs.fetchone()
        result = (row == password)
    except(Exception, psycopg2.DatabaseError) as error:
        print("query.pass_correct(ERROR)", error)
    finally:
        starbug.disconnect(conn, curs)
    return result


def register_user(uname, password, first, last, email):
    # insert account into database
    # since each user has unique email, so only need to check uname
    # 🎉 PASS TEST
    conn = curs = None
    if not user_exists(uname):
        try:
            conn = starbug.connect()
            curs = conn.cursor()
            query = "INSERT INTO Account VALUES (%s, %s, %s, %s, %s)"
            curs.execute(query, (uname, password, first, last, email,))
            conn.commit()
        except (Exception, psycopg2.Error) as error:
            print("query.register_user(ERROR):", error)
        finally:
            starbug.disconnect(conn, curs)
    else:
        print(f"user {uname} already exists")


def collec_exists(user, c_name):
    # check if collection exist based on username, and collection name
    # 🎉 PASS TEST
    conn = curs = row = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        # collection(collectionID,username, name(aka. c_name))
        query = "SELECT * FROM Collection WHERE username = %s AND name = %s"
        curs.execute(query, (user, c_name,))
        row = curs.fetchone()
    except(Exception, psycopg2.Error) as error:
        print("query.check_exist(ERROR)", error)
    finally:
        starbug.disconnect(conn, curs)
    return row is not None


def add_collec(username, name):
    # add a new collection
    # 🎉 PASS TEST
    conn = curs = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = "insert into collection (username, name) values (%s, %s)"
        curs.execute(query, (username, name,))
        conn.commit()
    except(Exception, psycopg2.Error) as error:
        print("add_collec(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)


def list_collec(username):
    # returns list of collecs belonging to users username
    # 🎉 PASS TEST
    conn = curs = result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = "SELECT name FROM Collection where username = %s"
        curs.execute(query, (username,))
        result = get_result(curs)
    except (Exception, psycopg2.Error) as error:
        print("query.register_user(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result


def rename_collec(username, collec, collec_new):
    # renames collection
    # 🎉 PASS TEST
    result = conn = curs = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = "UPDATE Collection SET name = %s WHERE name = %s AND username = %s"
        curs.execute(query, (collec_new, collec, username,))
        conn.commit()
        result = get_result(curs)
    except (Exception, psycopg2.Error) as error:
        print("query.register_user(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    # should check if successfully rename
    return result


def delete_collec(username, collec):
    # deletes collection
    # 🎉 PASS TEST
    result = conn = curs = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = "DELETE FROM Collection WHERE name = %s AND username = %s"
        curs.execute(query, (collec, username,))
        conn.commit()
        result = get_result(curs)
    except (Exception, psycopg2.Error) as error:
        print("query.register_user(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result


def show_collec(username, collec):
    # show song list in the collection
    # 🎉 PASS TEST
    result = conn = curs = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = """select title from song where songid in 
        (select songid from added_to where collectionid = %s and username = %s)"""
        curs.execute(query, (collec, username,))
        result = get_result(curs)
    except (Exception, psycopg2.Error) as error:
        print("query.register_user(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result


# def song_list(criteria, value, username):
#     # select criteria from table where criteria like value
#     result = None
#     try:
#         conn = starbug.connect()
#         curs = conn.cursor()
#         # FIXME function song_list_helper
#         #query = song_list_helper(criteria)
#         last_search_sql = (query, value)
#         curs.execute(query, (value,))
#         result = get_result(curs)
#     except (Exception, psycopg2.Error) as error:
#         print("query.register_user(ERROR):", error)
#     finally:
#         starbug.disconnect(conn, curs)
#     return result

# FIXME
#last_search_sql = None


# def song_list_helper(criteria):
#     # FIXME fix it by "GROUP BY clause"
#     # ERROR Column's.title, s.artistName, a.name, a.length' is invalid in the select list
#     # because it is not contained in either an aggregate function or the GROUP BY clause
#     # QUESTION: what is its logic to work on criteria

#     start = """SELECT s.title, s.artistName, a.name, a.length, COUNT(p.songID)
#                 FROM Song as s, Features as f, Album as a,
#                     Plays as p, Genre as g, Alb_gen as ag
#                 WHERE s.songID = f.songID, a.albumID = f.albumID, g.genreID = ag.genreID,
#                     s.songID = p.songID,  ag.albumID = a.albumID"""
#     return {
#         'song': start + """s.title = %s""",
#         'artist': start + """s.artistName = %s""",
#         'album': start + """a.name = %s""",
#         'genre': start + """ag.name = %s"""
#     }.get(criteria, start + """s.title = %s""")


# def song_list_sort(criteria, order):
#     result = None
#     try:
#         conn = starbug.connect()
#         curs = conn.cursor()
#         query = song_list_sort_helper(criteria)
#         curs.execute(query, (last_search_sql[1], order,))
#         result = get_result(curs)
#     except (Exception, psycopg2.Error) as error:
#         print("query.register_user(ERROR):", error)
#     finally:
#         starbug.disconnect(conn, curs)
#     return result


# def song_list_sort_helper(criteria):
#     start = last_search_sql[0] + """ORDER BY """
#     return {
#         'song': start + "s.title + %s",
#         'artist': start + "s.artistName + %s",
#         'genre': start + "g.name + %s",
#         'released': start + "s.release_date + %s"
#     }.get(criteria, start + "s.title + %s")


# FIXME
# def album_to_add(value):
#     # returns a list of (artistName, releaseDate) for all albums matching value
#     result = conn = curs = None
#     try:
#         conn = starbug.connect()
#         curs = conn.cursor()
#         query = """SELECT i.artistName, a.release_date
#                 From Included_in AS i, Album as a
#                 WHERE i.albumID = a.albumID and a.name = %s"""
#         curs.execute(query, (value,))
#     except (Exception, psycopg2.Error) as error:
#         print("query.register_user(ERROR):", error)
#     finally:
#         starbug.disconnect(conn, curs)

# FIXME
# def songs_to_add(value):
#     # returns a list of (artistName, albumName, releaseDate) for all songs matching value
#     result = None
#     try:
#         conn = starbug.connect()
#         curs = conn.cursor()
#         query = """SELECT s.artistName, a.name, s.release_date
#                 FROM Song as s, Album as a, Features as f
#                 WHERE s.songID = f.SongID and a.AlbumID = f.AlbumID
#                     and s.title = %s"""
#         curs.execute(query, (value,))
#     except (Exception, psycopg2.Error) as error:
#         print("query.register_user(ERROR):", error)
#     finally:
#         starbug.disconnect(conn, curs)


def main():
    # test connect and query
    #print(collec_exists('pb', 'My Favorite'))
    #print(if_exist("account", "password", "password"))
    # rename_collec('pb', 'One night', 'Halloween')
    #add_collec('pb', 'wow')
    #list_collec('pb')
    #delete_collec('pb', 'wow')
    #list_collec('pb')
    #show_collec('pb', 'collection')
    return


if __name__ == "__main__":
    main()
