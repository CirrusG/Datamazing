import psycopg2
from psycopg2 import sql
import starbug
import read

def unfollow_friend(username, friend):
    """
    unfollow friend (delete friendship from table follows)
    :return
    """

    conn = curs = result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        if read.verify_username(friend):
            query = """DELETE FROM follows where following = %s and follower = %s"""
            curs.execute(query, (friend, username, ))
            conn.commit()
            result = read.get_user_info(friend, False)
            # TODO may need double check
    except (Exception, psycopg2.Error) as error:
        print("unfollow_friend(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result
