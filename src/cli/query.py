# file: query.py
# this file is interface between cli and database
# @author Datamazing
# resource:
# SQL string composition https://www.psycopg.org/docs/sql.html#sql-objects

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


# def collec_exists(name):
#     return if_exist('collection', 'name', name)

# TODO
def collc_list(username, collc):
    return


def song_list(criteria, table, value):
    # select criteria from table where criteria like value
    return


def main():
    # test connect and query
    #print(register_user('st', 'st@mail.com', 'Siana', 'Tucker', 'knockdoor'))
    #print(pass_correct('pb', '3password'))
    print(email_exists('pb@mail.com'))


if __name__ == "__main__":
    main()
