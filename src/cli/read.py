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
                result.append(list(row))
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
        print("read.show_friend_list(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
        return list

def get_collec_info(username, collectionid):
    """
    Verify if the collection belongs to the user
    if successful, return the collection's information
    """
    conn = curs = None
    result = []
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = """select * from collection where collectionid = %s and username = %s"""
        curs.execute(query, (collectionid, username,))
        result = get_result(curs)
        if len(result) != 0:
            result = result[0]
            query = """select count(collectionid) from added_to where collectionid = %s"""
            curs.execute(query, (collectionid, ))
            result.extend(get_result(curs)[0])
    except (Exception, psycopg2.Error) as error:
        print("read.get_collec_info(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
        return result

def list_user_collec(username, ascOrDesc):
    conn = curs = result = None

    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = """select name, collectionid from collection where username = %s"""
        curs.execute(query, (username, ))
        result = get_result(curs)
        for each in result:
            collectionid = each[1]
            query = """select count(added_to.songid), sum(song.length)
                    from added_to join song on added_to.songid = song.songid
                    where added_to.collectionid = %s"""
            curs.execute(query, (collectionid, ))
            each.extend(get_result(curs)[0])
        if ascOrDesc:
            result.sort()
        else:
            result.sort(reverse=True)
    except (Exception, psycopg2.Error) as error:
        print("read.list_collec (ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result

def list_collec_song(username, collectionid):
    conn = curs = result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = """select location_number, songid from added_to where username = %s and collectionid = %s"""
        curs.execute(query, (username, collectionid))
        result = get_result(curs)
    except (Exception, psycopg2.Error) as error:
        print("read.show_friend_list(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
        return sorted(result)

def get_song_info(songid):
    """
    Get song info: {songid, name, length, create_date_time, genre6, artist}
    """
    conn = curs = result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = """select song.songid, song.title, song.artistName, song.length, genre.name, song.release_date 
        from song join genre on song.genreid = genre.genreid where songid = %s"""
        curs.execute(query, (songid, ))
        result = get_result(curs)[0]
    except (Exception, psycopg2.Error) as error:
        print("get_song_info (ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result

def get_album_info(albumid):
    """
    verify if the ablum exists, unless, return its information
    [album_info, [genre_list], [artist_list]]
    i.e:
    ['album1000', 'Rewind, Replay, Rebound', datetime.date(2019, 8, 28),
    ['danish metal', 'danish rock', 'alternative metal'], ['Volbeat']]
    """
    conn = curs = result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = """select * from album where albumid = %s"""
        curs.execute(query, (albumid,))
        result = get_result(curs)[0]
        query = """select name from genre join alb_gen 
        on alb_gen.genreID = genre.genreid where alb_gen.albumid = %s"""
        curs.execute(query, (albumid, ))
        genre_list = []
        for each in get_result(curs):
            genre_list.append(each[0])
        result.append(genre_list)
        query = """select artistname from included_in where albumid = %s"""
        curs.execute(query, (albumid,))
        artist_list = []
        for each in get_result(curs):
            artist_list.append(each[0])
        result.append(artist_list)
    except (Exception, psycopg2.Error) as error:
        print("read.get_album_info(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
        return result

def list_album(albumid):
    """
    return song list
    """
    conn = curs = result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = """select track_number, songid from features where albumid = %s"""
        curs.execute(query, (albumid,))
        result = get_result(curs)
    except (Exception, psycopg2.Error) as error:
        print("read.show_friend_list(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
        return sorted(result)

def get_profile(username):
    """
    1. number of collections
    2. number of followers
    3. number of following
    4. top 10 artist the user most plays
    """
    conn = curs = result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = """select count(collectionid) from collection where username = %s"""
        curs.execute(query, (username, ))
        result = get_result(curs)[0]
        query = """select count(follower) from follows where following = %s"""
        curs.execute(query, (username, ))
        result.extend(get_result(curs)[0])
        query = """select count(following) from follows where follower = %s"""
        curs.execute(query, (username,))
        result.extend(get_result(curs)[0])
        query = """select song.artistName, count(song.artistName) from plays
                join song on plays.songid = song.songid where username = %s 
                group by song.artistName order by count desc limit 10"""
        curs.execute(query, (username, ))
        result.append(get_result(curs))
    except (Exception, psycopg2.Error) as error:
        print("read.show_friend_list(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
        return result

def get_

def main():
    # print(get_collec_info('ly', 'collection136'))
    # print(get_album_info('album1000'))
    # print(list_user_collec('ly', True))
    #print(list_album('album1000'))
    print(get_profile('ly'))
    return

if __name__ == '__main__':
    main()