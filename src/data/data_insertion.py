# file: data_insertion.py
# insert required artist, genre, song, album data into database
import csv
import psycopg2
# will change to cli.starbug later
import cli.starbug as starbug
import time
# do not open csv files during inserting, otherwise throws 'OSError: [Errno 5] Input/output error
# 🎈*IMPORTANT*: overall length of run at least 25 minutes (import to starbug early)
#global variable server to make ssh connection
server = starbug.conn_server()
server.start()

def get_result(curs):
    result = []
    try:
        row = curs.fetchone()
        while row is not None:
            result.append(row)
            row = curs.fetchone()
    except (Exception, psycopg2.Error) as error:
        print("query.fetch(ERROR):", error)
    return result

def artist_insert():
    # done insert artist
    conn = curs = None
    with open('spotify-data/artists.csv', newline='') as artistfile:
        reader = csv.reader(artistfile, delimiter=',')
        # jump header
        next(reader)
        for row in reader:
            try:
                conn = starbug.connect(server)
                curs = conn.cursor()
                query = "insert into artist values (%s)"
                curs.execute(query, (row[-1],))
                conn.commit()
            except (psycopg2.DatabaseError) as error:
                print("data_insertion.py(ERROR):", error)
            finally:
                starbug.disconnect(conn, curs)


def genre_insert():
    # done insert genre
    with open('spotify-data/genres.csv', newline='') as genresfile:
        reader = csv.reader(genresfile, delimiter=',')
        # jump header
        next(reader)
        for row in reader:
            try:
                conn = starbug.connect(server)
                curs = conn.cursor()
                # print(row[-1])
                query = "insert into genre (name) values (%s)"
                curs.execute(query, (row[1],))
                conn.commit()
            except (Exception, psycopg2.Error) as error:
                print("data_insertion.py(ERROR):", error)
            finally:
                starbug.disconnect(conn, curs)


def song_album_insert():
    # table: song, album, included_in, features, alb_gen
        with open('spotify-data/tracks.csv') as tracksfile:
            reader = csv.reader(tracksfile, delimiter=',')
            # jump header
            #next(reader)

            for row in reader:
                try:
                    conn = starbug.connect(server)
                    curs = conn.cursor()
                    # name: 1, artist_name: 4, album_name: 6, track_number 7,
                    # track_duration(mm:ss): -1, track_genre: 9, track_release: 10
                    track_name = row[1]
                    artist_name = row[4]
                    track_genre = row[9]
                    curs.execute("select genreID from genre where name = %s", (track_genre,))
                    genreID = curs.fetchone()
                    if genreID is None:
                        print("song_album_insert(ERROR): genre does not exist")
                        continue
                    genreID = genreID[0]
                    track_duration = row[-1]
                    track_release = row[10]
                    album_name = row[6] # feature
                    track_number = row[7] # feature
                    # => album
                    curs.execute("select albumID from album where name = %s", (album_name,))
                    albumID = curs.fetchone()
                    if albumID is None:
                        query = "insert into album (name, release_date) values (%s, %s)"
                        curs.execute(query, (album_name, track_release))
                        conn.commit()
                        curs.execute("select albumID from album where name = %s", (album_name,))
                        albumID = curs.fetchone()
                    albumID = albumID[0]
                    # => include in
                    curs.execute("select artistname from included_in where albumID = %s", (albumID,))
                    exist = False
                    for each in get_result(curs):
                        # parse result to fit the compare
                        #print('artistname get', each[0])
                        if each[0] == artist_name:
                            exist = True
                            break
                    if not exist:
                        curs.execute("insert into included_in values (%s, %s)", (albumID, artist_name,))
                        conn.commit()
                    # => alb_gen
                    exist = False
                    curs.execute("select genreID from alb_gen where albumID = %s", (albumID,))
                    for each in get_result(curs):
                        #print('genre get', each)
                        if each[0] == genreID:
                            exist = True
                            break
                    if not exist:
                        curs.execute("insert into alb_gen values (%s, %s)", (genreID, albumID,))
                        conn.commit()
                    # => song
                    #print(name, artist_name, album_name, track_number, track_duration, track_genre, track_release)
                    query = "insert into song (title, length, release_date, genreID, artistName) values (%s, %s, %s, %s, %s)"
                    curs.execute(query, (track_name, track_duration, track_release, genreID, artist_name,))
                    conn.commit()
                    curs.execute("select songID from song where title = %s", (track_name,))
                    songID = curs.fetchone()[0]
                    # => features
                    curs.execute("select * from features where albumID = %s and songID = %s", (albumID, songID))
                    feature_res = curs.fetchone()
                    if feature_res is None:
                        query = "insert into features values (%s, %s, %s)"
                        curs.execute(query, (track_number, albumID, songID))
                        conn.commit()
                except (Exception, psycopg2.Error) as error:
                    print("data_insertion.py(ERROR):", error)
                finally:
                    starbug.disconnect(conn, curs)
                # for test
                # break
def user_insert():

def main():
    # check how long time used to import

    start = time.time()
    # -- 520.3794424533844 seconds ---
    # artist_insert()
    # -- 353.7282118797302 seconds ---
    #genre_insert()
    # -- 38019.46160531044 ---
    #song_album_insert()
    # 15 mins to 25 mins
    print("-- %s seconds ---" % (time.time() - start))
    starbug.disconn_server(server)

if __name__ == "__main__":
    main()

