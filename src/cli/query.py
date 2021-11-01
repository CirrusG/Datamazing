# file: query.py
# this file is interface between cli and database
# @author Datamazing
# resource:
# Basic module usage: https://www.psycopg.org/docs/usage.html (query params, adaptation of python values to sql types, etcs)
# SQL string composition: https://www.psycopg.org/docs/sql.html#sql-objects
# TODO list:
# - search song by criteria

import psycopg2
# just for ease of changing the database(local -> starbug)
from psycopg2 import sql

import starbug as starbug

server = starbug.conn_server()
server.start()

def if_exist(table, column, value):
    # check if value exists as column in the table
    # 🎉 PASS TEST
    # reference
    row = conn = curs = None
    try:
        conn = starbug.connect(server)
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
    result = None
    try:
        result = []
        # output of fetch is a array, else it is None
        # the array contains one or more values, do not use row[0], check length firstly
        if curs.statusmessage is not None:
            row = curs.fetchone()
            while row is not None:
                result.append(row)
                row = curs.fetchone()
            # psycopg2.RaiseException
    except (Exception, psycopg2.Error) as error:
        print("query.get_result(ERROR):", error)
    return result

def register_user(uname, password, first, last, email):
    # insert account into database
    # since each user has unique email, so only need to check uname
    conn = curs = None
    if not user_exists(uname):
        try:
            conn = starbug.connect(server)
            curs = conn.cursor()
            query = "INSERT INTO Account VALUES (%s, %s, %s, %s, %s)"
            curs.execute(query, (uname, email, password, first, last,))
            conn.commit()
        except (Exception, psycopg2.Error) as error:
            print("query.register_user(ERROR):", error)
        finally:
            starbug.disconnect(conn, curs)
    else:
        print(f"user {uname} already exists")

def user_exists(username):
    # check username if exists
    return if_exist('account', 'username', username)

def email_exists(email):
    # check email if exists
    return if_exist('account', 'email', email)

def pass_correct(username, password):
    # check if password correct
    # since it need to compare if password correct, check if none does not work
    # since the user pass login check, no require to check if password is None
    conn = curs = result = None
    try:
        conn = starbug.connect(server)
        curs = conn.cursor()
        curs.execute(
            "SELECT password FROM Account WHERE username=%s", (username,))
        row = curs.fetchone()
        # print(row) #it is a array
        if row is not None:
            row = row[0]
            # only row is not None, comparasion is meaningful
            result = (row == password)
    except(Exception, psycopg2.DatabaseError) as error:
        print("query.pass_correct(ERROR)", error)
    finally:
        starbug.disconnect(conn, curs)
    return result

def login_user(username, password):
    if pass_correct(username, password):
        conn = curs = None
        try:
            conn = starbug.connect(server)
            curs = conn.cursor()
            curs.execute(
                "insert into user_accessdatestimes(username) values (%s)", (username,))
            conn.commit()
        except(Exception, psycopg2.DatabaseError) as error:
            print("query.pass_correct(ERROR)", error)
        finally:
            starbug.disconnect(conn, curs)

def add_collec(username, name):
    # add a new collection
    conn = curs = None
    try:
        conn = starbug.connect(server)
        curs = conn.cursor()
        query = "insert into collection (username, name) values (%s, %s)"
        curs.execute(query, (username, name,))
        conn.commit()
    except(Exception, psycopg2.Error) as error:
        print("add_collec(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)

def collec_exists(user, c_name):
    # check if collection exist based on username, and collection name
    # in the query, has condition to check by collection name
    # just check if None or not to know the existence
    conn = curs = row = None
    try:
        conn = starbug.connect(server)
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

def list_collec(username):
    # returns list of collecs belonging to users username
    # need to handle array message returned
    conn = curs = result = None
    try:
        conn = starbug.connect(server)
        curs = conn.cursor()
        query = "SELECT name FROM Collection where username = %s"
        curs.execute(query, (username,))
        result = get_result(curs)
    except (Exception, psycopg2.Error) as error:
        print("query.list_collec(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result

def rename_collec(username, collecid, collec_new):
    # renames collection
    result = conn = curs = None
    try:
        conn = starbug.connect(server)
        curs = conn.cursor()
        query = "UPDATE Collection SET name = %s WHERE collectionid = %s AND username = %s"
        curs.execute(query, (collec_new, collecid, username,))
        conn.commit()
        result = get_result(curs)
    except (Exception, psycopg2.Error) as error:
        print("query.rename_collec(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    # should check if successfully rename
    return result

def delete_collec(username, collecid):
    # deletes collection
    result = conn = curs = None
    try:
        conn = starbug.connect(server)
        curs = conn.cursor()
        query = "delete from added_to where collectionid = %s"
        curs.execute(query, (collecid, ))
        conn.commit()
        query = "DELETE FROM Collection WHERE collectionid = %s AND username = %s"
        curs.execute(query, (collecid, username,))
        conn.commit()
        result = get_result(curs)
    except (Exception, psycopg2.Error) as error:
        print("query.delete_collec(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result

def show_collec(username, collecid):
    # show song list in the collection
    result = conn = curs = None
    try:
        conn = starbug.connect(server)
        curs = conn.cursor()
        query = """select title from song where songid in 
        (select songid from added_to where collectionid = %s and username = %s)"""
        curs.execute(query, (collecid, username,))
        result = get_result(curs)
    except (Exception, psycopg2.Error) as error:
        print("query.show_collec(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result

def add_song_collec(local_number, username, collecid, songid):
    conn = curs = None
    try:
        conn = starbug.connect(server)
        curs = conn.cursor()
        query = """insert into added_to values (%s, %s, %s, %s)"""
        curs.execute(query, (local_number, username, collecid, songid,))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("query.add_song_collec(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
# ============= search song function --------------
# criteria
#1.
def song_list(criteria, value, username):
    # select criteria from table where criteria like value
    result = None
    try:
        conn = starbug.connect(server)
        curs = conn.cursor()
        query = song_list_helper(criteria)
        value = '%' + value + '%'
        global last_search_sql
        last_search_sql = (query, value)
        query += "ORDER BY s.title"
        curs.execute(query, (value,))
        result = get_result(curs)
    except (Exception, psycopg2.Error) as error:
        print("query.song_list(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result

#FIXME
last_search_sql = None


def song_list_helper(criteria):
    # FIXME fix it by "GROUP BY clause"
    # ERROR Column's.title, s.artistName, a.name, a.length' is invalid in the select list
    # because it is not contained in either an aggregate function or the GROUP BY clause
    # QUESTION: what is its logic to work on criteria

    start = """SELECT s.title, s.artistName, a.name, s.length
                FROM Song as s
                INNER JOIN Features as f
                    ON s.songID = f.songID
                INNER JOIN Album as a
                    ON a.albumID = f.albumID
                INNER JOIN Alb_gen as ag
                    ON ag.albumID = a.albumID
                INNER JOIN Genre as g
                    ON g.genreID = ag.genreID
                WHERE """
    end = ""#  "GROUP BY a.name "
    return {
        'song': start + """s.title LIKE %s """ + end,
        'artist': start + """s.artistName LIKE %s """+ end,
        'album': start + """a.name LIKE %s """+ end,
        'genre': start + """ag.name LIKE %s """+ end
    }.get(criteria, start + """s.title LIKE %s """+ end)


def song_list_sort(criteria, order):
    result = None
    try:
        conn = starbug.connect(server)
        curs = conn.cursor()
        query = song_list_sort_helper(criteria)
        curs.execute(query, (last_search_sql[1],))
        result = get_result(curs)
    except (Exception, psycopg2.Error) as error:
        print("query.song_list_sort(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result


def song_list_sort_helper(criteria):
    global last_search_sql
    start = last_search_sql[0] + "ORDER BY "
    return {
        'song': start + "s.title",
        'artist': start + "s.artistName",
        'genre': start + "g.name",
        'released': start + "s.release_date"
    }.get(criteria, start + "s.title")


#FIXME
def album_to_add(value):
    # returns a list of (artistName, releaseDate) for all albums matching value
    result = conn = curs = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = """SELECT i.artistName, a.release_date
                From Included_in AS i, Album as a
                WHERE i.albumID = a.albumID and a.name = %s"""
        curs.execute(query, (value,))
    except (Exception, psycopg2.Error) as error:
        print("query.album_to_add(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)

#FIXME
def songs_to_add(value):
    # returns a list of (artistName, albumName, releaseDate) for all songs matching value
    result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = """SELECT s.artistName, a.name, s.release_date
                FROM Song as s, Album as a, Features as f
                WHERE s.songID = f.SongID and a.AlbumID = f.AlbumID
                    and s.title = %s"""
        curs.execute(query, (value,))
    except (Exception, psycopg2.Error) as error:
        print("query.song_to_add(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)

# friend: find friend by email -> output info if find -> add friend by select username
def find_friend_e(email):
    # find friend by email, print username, first&last name if find
    # return username if has, otherwise None
    # when the return is not None, cli could query if want to add this friend
    conn = curs = friend = None
    try:
        conn = starbug.connect(server)
        curs = conn.cursor()
        query = """select username, first_name, last_name from account where email = %s"""
        curs.execute(query, (email,))
        result = get_result(curs)
        # email is unique, so the output only be [1][1]
        # example output: [('ta', 'Taya', 'Andersen')]
        # if no result: []
        # print(result)
        if len(result) == 1 and len(result[0]) == 3:
            friend = result[0][0]
    except (Exception, psycopg2.Error) as error:
        print("find_friend_u(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
        return friend

def find_friend(username):
    # repurposed find_friend function to be used w username instead of email
    conn = curs = friend = None
    try:
        conn = starbug.connect(server)
        curs = conn.cursor()
        query = """select username, first_name, last_name from account where username = %s"""
        curs.execute(query, (username,))
        result = get_result(curs)
        # email is unique, so the output only be [1][1]
        # example output: [('ta', 'Taya', 'Andersen')]
        # if no result: []
        # print(result)
        if len(result) == 1 and len(result[0]) == 3:
            friend = result[0][0]
    except (Exception, psycopg2.Error) as error:
        print("find_friend(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
        return friend

def follow_friend(friend, username):
    # @parm friend: friend to follow (following)
    # @param username: current user in the cli that want to follow friend(follower)
    # do not need to check user username since entered application
    # but need to record 'username' as global value in the cli since it need to use many times
    conn = curs = result = None
    try:
        conn = starbug.connect(server)
        curs = conn.cursor()
        if (if_exist('account', 'username', friend)):
            query = """insert into follows (following, follower) values (%s, %s)"""
            curs.execute(query, (friend, username, ))
            conn.commit()
            result = True
            # TODO may need double check
    except (Exception, psycopg2.Error) as error:
        print("follow_friend(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result

def unfollow_friend(friend, username):
    # copied the follow_friend code and changed INSERT to DELETE, may need some tweaking
    conn = curs = result = None
    try:
        conn = starbug.connect(server)
        curs = conn.cursor()
        if (if_exist('account', 'username', friend)):
            query = """DELETE FROM follows where following = %s and follower = %s"""
            curs.execute(query, (friend, username, ))
            conn.commit()
            result = True
            # TODO may need double check
    except (Exception, psycopg2.Error) as error:
        print("unfollow_friend(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
    return result

def show_friend_list(username):
    # TODO: need to parse output
    conn = curs = list = None
    try:
        conn = starbug.connect(server)
        curs = conn.cursor()
        query = """select account.first_name, account.last_name 
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

def play_song(username, songID):
    # play song by username, songID (after looking up song, select the id to play)
    # return song info
    # add play record
    conn = curs = song = None
    try:
        conn = starbug.connect(server)
        curs = conn.cursor()
        query = """select * from song where songID = %s"""
        curs.execute(query, (songID, ))
        list = get_result(curs)
        if (len(list[0]) > 0):
            song = list[0]
            query = """insert into plays(username, songID) values (%s, %s)"""
            curs.execute(query, (username, songID,))
            conn.commit()
            # test record in plays
            # NOTE: datatime need to be handled by extracting to get day, month, year and time
            curs.execute(
                "select playDateTime from plays where username = %s and songID = %s", (username, songID,))
            for each in get_result(curs):
                print(each)
    except (Exception, psycopg2.Error) as error:
        print("play_song(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)
        return song

def play_album(username, albumID):
    # call play_song to get a list of song info
    conn = curs = None
    try:
        conn = starbug.connect(server)
        curs = conn.cursor()
        query = """select song.songID from song 
                join features on song.songID = features.songID
                where features.albumID = %s"""
        curs.execute(query, (albumID,))
        list = get_result(curs)
        for each in list:
            if len(each) == 1:
                play_song(username, each[0])
    except (Exception, psycopg2.Error) as error:
        print("play_album(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)

def play_collec(username, collecID):
    conn = curs = None
    try:
        conn = starbug.connect(server)
        curs = conn.cursor()
        query = """select song.songID from song 
                join added_to on song.songID = added_to.songID
                where added_to.collectionID = %s"""
        curs.execute(query, (collecID,))
        list = get_result(curs)
        for each in list:
            if len(each) == 1:
               play_song(username, each[0])
    except (Exception, psycopg2.Error) as error:
        print("play_collec(ERROR):", error)
    finally:
        starbug.disconnect(conn, curs)

def main():
    # test connect and query
    # uncomment to see, some insertions has done, need to modify
    # print(if_exist("song", "songid", "song3500"))
    # register_user('ly', '1234', 'Lee', 'Yun', 'ly@mail.com')
    # register_user('pb', '2345', 'Pixie', 'Blaese', 'pb@mail.com')
    # print(user_exists('ly'))
    # print(email_exists('ly@mail.com'))
    # print(pass_correct('ly', '1234'))
    # print(pass_correct('ly', '12df4')) #false
    # add_collec('ly', 'hello world')
    # print(collec_exists('ly', 'hello world'))
    # print(list_collec('ly'))
    # print(rename_collec('ly', 'collection1', 'happy day'))
    # print(list_collec('ly'))
    # print(show_collec('ly', 'collection1'))
    # add_song_collec('1', 'ly', 'collection1', 'song103')
    # add_song_collec('1', 'ly', 'collection1', 'song300')
    # add_song_collec('1', 'ly', 'collection1', 'song120')
    # add_song_collec('1', 'ly', 'collection1', 'song230')
    # add_song_collec('1', 'ly', 'collection1', 'song500')
    # print(show_collec('ly', 'collection1'))
    #print(find_friend_e('pb@mail.com'))
    #print(find_friend('pb'))
    #print(follow_friend('pb', 'ly'))
    #show_friend_list('ly')
    #print(unfollow_friend('pb', 'ly'))
    #play_song('ly', 'song3434')
    #play_album('ly', 'album300')
    #play_collec('ly', 'collection1')
    #delete_collec('ly', 'collection1')
    login_user('ly', '1234')
    starbug.disconn_server(server)


if __name__ == "__main__":
    main()
