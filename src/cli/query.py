# file: query.py
# this file is interface between cli and database
# @author Datamazing
# resource:
# Basic module usage: https://www.psycopg.org/docs/usage.html (query params, adaptation of python values to sql types, etcs)
# SQL string composition: https://www.psycopg.org/docs/sql.html#sql-objects
# 

import psycopg2
from psycopg2 import sql
# just for ease of changing the database(local -> starbug)
import local as starbug


def if_exist(table, column, value):
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = sql.SQL('select {field} from {table} where {field} = %s').format(
            field=sql.Identifier(column), table=sql.Identifier(table))
        curs.execute(query, (value,))
        row = curs.fetchone()
    except(Exception, psycopg2.Error) as error:
        print("query.check_exist(ERROR)", error)
    finally:
        starbug.disconnect(conn, curs)
    # NOTE: here can return row, then in another file to check if is None, if not, just get the value
    return (row is not None)


def get_result(curs):
    try:
        result = []
        row = curs.fetchone()
        while row is not None:
            result.append(row)
            print(row)
            row = curs.fetchone()
            psycopg2.RaiseException
    except (Exception, psycopg2.Error) as error:
        print("query.fetch(ERROR):", error)
    return result


def user_exists(username):
    return if_exist('account', 'username', username)


def email_exists(email):
    return if_exist('account', 'email', email)


def pass_correct(username, password):
    # since the user pass login check, no require to check if password is None
    result = None
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
    if (not (user_exists(uname, email))):
        try:
            conn = starbug.connect()
            curs = conn.cursor()
            sql = "INSERT INTO Account VALUES (%s, %s, %s, %s, %s)"
            curs.execute(sql, (uname, password, first, last, email,))
            # curs.execute("INSERT INTO account VALUES ")
            conn.commit()
        except (Exception, psycopg2.Error) as error:
            print("query.register_user(ERROR):", error)
        finally:
            starbug.disconnect(conn, curs)


def collec_exists(user, c_name):
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = "SELECT name FROM Collection WHERE username =%s AND c_name=%s"
        curs.execute(query, (user, c_name,))
        row = curs.fetchone()
    except(Exception, psycopg2.Error) as error:
        print("query.check_exist(ERROR)", error)
    finally:
        starbug.disconnect(conn, curs)
    return (row is not None)


def list_collec(username):
    #returns list of collecs belonging to users username
    result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        sql = "SELECT name FROM Collection where username=%s"
        curs.execute(sql, (username,))
        result = get_result(curs)
    except (Exception, psycopg2.Error) as error:
            print("query.register_user(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result


def rename_collec(username, collec, collec_new):
    # renames collection
    result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        sql = "UPDATE Collection SET name=%s WHERE name=%s AND username=%s"
        curs.execute(sql, (collec_new, collec, username,))
        conn.commit()
        result = get_result(curs)
    except (Exception, psycopg2.Error) as error:
            print("query.register_user(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result


def delete_collec(username, collec):
    # deletes collection
    result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        sql = "DELETE FROM Collection WHERE name=%s AND username=%s"
        curs.execute(sql, (collec, username,))
        conn.commit()
        result = get_result(curs)
    except (Exception, psycopg2.Error) as error:
            print("query.register_user(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result


def show_collec(username, collec):
    result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        sql = """SELECT title FROM Song 
                WHERE songID IN (
                    SELECT a.songID 
                    FROM Added_to AS a, Collection AS c
                    WHERE a.collectionID = c.collectionID,
                        c.name = %s, a.username = %s)"""
        curs.execute(sql,(collec,username,))
        result = get_result(curs)
    except (Exception, psycopg2.Error) as error:
            print("query.register_user(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result


def song_list(criteria, value, username):
    # select criteria from table where criteria like value
    result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        sql = song_list_helper(criteria)
        last_search_sql = (sql, value)
        curs.execute(sql, (value,))
        result = get_result(curs)
    except (Exception, psycopg2.Error) as error:
            print("query.register_user(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result

last_search_sql = None

def song_list_helper(criteria):
    start = """SELECT s.title, s.artistName, a.name, s.length, COUNT(p.songID) 
                FROM Song as s, Features as f, Album as a, 
                    Plays as p, Genre as g, Alb_gen as ag 
                WHERE s.songID = f.songID, a.albumID = f.albumID, g.genreID = ag.genreID,
                    s.songID = p.songID,  ag.albumID = a.albumID,"""
    return {
        'song': start + """s.title = %s""",
        'artist': start + """s.artistName = %s""",
        'album': start + """a.name = %s""",
        'genre': start + """ag.name = %s""" 
    }.get(criteria, start + """s.title = %s""")

def song_list_sort(criteria, order):
    result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        sql = song_list_sort_helper(criteria)
        curs.execute(sql, (last_search_sql[1],order,))
        result = get_result(curs)
    except (Exception, psycopg2.Error) as error:
            print("query.register_user(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result

def song_list_sort_helper(criteria):
    start = last_search_sql[0] + """ORDER BY """
    return {
        'song' : start + "s.title + %s",
        'artist' : start + "s.artistName + %s",
        'genre' : start + "g.name + %s",
        'released' : start + "s.release_date + %s"
    }.get(criteria, start + "s.title + %s")

def album_to_add(value):
    #returns a list of (artistName, releaseDate) for all albums matching value 
    result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        sql = """SELECT i.artistName, a.release_date
                From Included_in AS i, Album as a
                WHERE i.albumID = a.albumID, a.name = %s"""
        curs.execute(sql, (value,))
        result = get_result(curs)
    except (Exception, psycopg2.Error) as error:
            print("query.register_user(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result

def songs_to_add(value):
    #returns a list of (artistName, albumName, relaseDate) for all songs matching value 
    result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        sql = """SELECT s.artistName, a.name, s.release_date
                FROM Song as s, Album as a, Features as f
                WHERE s.songID = f.SongID, a.AlbumID = f.AlbumID
                    s.title = %s"""
        curs.execute(sql, (value,))
        result = get_result(curs)
    except (Exception, psycopg2.Error) as error:
            print("query.register_user(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result

def main():
    # test connect and query
    #print(register_user('st', 'st@mail.com', 'Siana', 'Tucker', 'knockdoor'))
    #print(pass_correct('pb', '3password'))
    print(email_exists('pb@mail.com'))


if __name__ == "__main__":
    main()
