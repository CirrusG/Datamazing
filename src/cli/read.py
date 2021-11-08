import psycopg2
from psycopg2 import sql
import starbug

def verify_item(table, column, value):
    # check if value exists as column in the table
    # @return true if exists, otherwise false

    row = conn = curs = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        # SQL string composition: https://www.psycopg.org/docs/sql.html#sql-objects
        # ERROR <expression>, <table expression>, ALL, DISTINCT, EXCEPT, FETCH, FOR, INTERSECT, INTO, LIMIT, OFFSET,
        # ORDER, UNION or WINDOW expected, got '{'
        # NO EFFECT ON RUNNING (JUST IGNORE IT)
        query = sql.SQL('select {field} from {table} where {field} = %s').format(
            field=sql.Identifier(column), table=sql.Identifier(table))
        curs.execute(query, (value,))
        row = curs.fetchone()
    except psycopg2.Error as error:
        print("read.verify_item(ERROR)", error)
    finally:
        starbug.disconnect(conn, curs)
    # NOTE: here can return row, then in another file to check if is None,
    # if not, just get the value
    return row is not None

def get_result(curs):
    # get list of query result
    # need to be parsed for better appearance in the cli program
    # @return list of query result if has, otherwise None
    result = None
    try:
        result = []
        if curs.statusmessage is not None:
            row = curs.fetchone()
            while row is not None:
                result.append(row)
                row = curs.fetchone()
    except (Exception, psycopg2.Error) as error:
        print("read.get_result(ERROR):", error)
    return result

def verify_username(username):
    # check username if exists
    return verify_item('account', 'username', username)

def verify_email(email):
    # check email if exists
    return verify_item('account', 'email', email)

def verify_password(username, password):
    # check if password correct
    # @return True if pass password otherwise false
    result = False
    conn = curs = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        curs.execute(
            "SELECT password FROM Account WHERE username=%s", (username,))
        result = get_result(curs)[0][0] == password
    except(Exception, psycopg2.DatabaseError) as error:
        print("read.verify_password(ERROR)", error)
    finally:
        starbug.disconnect(conn, curs)
    return result

def get_user_info(key, emailOrUsername):
    # find friend by email, print username, first&last name if find
    # return user info (first_name, last_name username, email) if has, otherwise None
    conn = curs = user_info = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        if emailOrUsername:
            query = """select first_name, last_name, username, email from account where email = (%s)"""
        else:
            query = """select first_name, last_name, username, email from account where username = (%s)"""
        curs.execute(query, (key,))
        info = get_result(curs)
        if len(info) != 0:
            user_info = info
    except (Exception, psycopg2.Error) as error:
        print("read.get_user_info(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
        return user_info




def show_friend_list(username):
    # TODO: need to parse output
    conn = curs = list = None
    try:
        conn = starbug.connect(server)
        curs = conn.cursor()
        query = """select account.first_name, account.last_name, account.username 
        from account inner join follows on account.username = follows.following
        where follows.follower = %s"""
        curs.execute(query, (username, ))
        list = get_result(curs)
        # NOTE: if it is empty array, but not same as none, need to check length of this
        # just test output, the result will handle in the cli.py
        # array or none
        for row in get_result(curs):
            print(row)
    except (Exception, psycopg2.Error) as error:
        print("show_friend(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
        return list

