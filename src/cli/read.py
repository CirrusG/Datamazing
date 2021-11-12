import psycopg2
from psycopg2 import sql
import starbug


def verify_item(table, column, value):
    """
    check if value/row exists on column of the table
    :param table the table to look up
    :param column the column of the table to look up
    :param value the row on the column of the table to look up
    :return true if exists, otherwise false
    """

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
    return row is not None


def get_result(curs):
    """
    get list of query result
    need to be parsed for better appearance in the cli program
    :param curs cursor of database for fetching and commit query
    :return list of query result if has, otherwise None
    """
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
    """
    check username if exists
    :return True if username exists in account table otherwise false
    """
    return verify_item('account', 'username', username)


def verify_email(email):
    """
    check email if exists
    :return True if email exists in account table otherwise false
    """
    return verify_item('account', 'email', email)


def verify_password(username, password):
    """
    check if password correct by username
    :param username
    :param password
    :return True if pass password verification otherwise false
    """
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
    """
     find friend by email or username
     :param key value of email or username
     :param emailOrUsername boolean control to define the type of key; email is True, username is False
     :return user info (first_name, last_name username, email) if has, otherwise None
    """
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
            user_info = info[0]
    except (Exception, psycopg2.Error) as error:
        print("read.get_user_info(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
        return user_info


def show_friend_list(username):
    """
    get array list of friend
    need to parse output

    :param username username of user to look up friend
    :return friend list {firstname, lastname, email, username}
    """
    conn = curs = list = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = """select account.first_name, account.last_name, account.email, account.username 
        from account inner join follows on account.username = follows.following
        where follows.follower = %s"""
        curs.execute(query, (username,))
        list = get_result(curs)
    except (Exception, psycopg2.Error) as error:
        print("show_friend(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
        return list

def main():
   print(get_user_info('bc', False))

if __name__ == '__main__':
    main()