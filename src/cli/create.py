import psycopg2
from psycopg2 import sql
import starbug
import read

def login_user(username):
    # login user (add record into accessdatestimes)
    # @precondition: check username, password in the cli application
    # @return true if successfully login
    result = False
    conn = curs = None
    try:
        conn = starbug.connect(server)
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
    # register new user
    # since each user has unique email,
    # so only need to check uname if has existed in the database
    # insert account into database
    # @return if successful register
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