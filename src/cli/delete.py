import psycopg2
from psycopg2 import sql
import starbug
import read

def unfollow_friend(username, friend):
    """
    unfollow friend (delete friendship from table follows)
    :return friend info that unfollowed
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

def delete_collec(username, collectionid):

    conn = curs = result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = """delete from added_to where collectionid = %s"""
        curs.execute(query, (collectionid, ))
        conn.commit()
        query = """delete from collection where collectionid = %s and username = %s 
        returning name, collectionid"""
        curs.execute(query, (collectionid, username,))
        conn.commit()
        result = read.get_result(curs)
    except (Exception, psycopg2.Error) as error:
        print("delete_collec (ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result

if __name__ == '__main__':
    print(delete_collec('pb', 'collection111'))
