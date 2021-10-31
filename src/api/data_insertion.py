# file: data_insertion.py
# insert required artist, genre, song, album data into database
import csv
import psycopg2
from psycopg2 import sql
# will change to cli.starbug later
import cli.local as starbug
# do not open csv files during inserting, otherwise throws 'OSError: [Errno 5] Input/output error
# 🎈*IMPORTANT*: overall length of run at least 25 minutes (import to starbug early)

def get_result(curs):
    result = []
    try:
        row = curs.fetchone()
        while row is not None:
            result.append(row)
            print(row)
            row = curs.fetchone()
    except (Exception, psycopg2.Error) as error:
        print("query.fetch(ERROR):", error)
    return result

def artist_insert():
    # done insert artist
    with open('spotify-data/artists.csv', newline='') as artistfile:
        reader = csv.reader(artistfile, delimiter=',')
        # jump header
        next(reader)
        for row in reader:
            try:
                conn = starbug.connect()
                curs = conn.cursor()
                sql = "insert into artist values (%s)"
                curs.execute(sql, (row[-1],))
                conn.commit()
            except (Exception, psycopg2.Error) as error:
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
                conn = starbug.connect()
                curs = conn.cursor()
                # print(row[-1])
                sql = "insert into genre (name) values (%s)"
                curs.execute(sql, (row[1],))
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
            next(reader)
            for row in reader:
                try:
                    conn = starbug.connect()
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
                    track_duration = row[-1]
                    track_release = row[10]
                    album_name = row[6] # feature
                    track_number = row[7] # feature
                    # => album
                    curs.execute("select albumID from album where name = %s", (album_name,))
                    albumID = curs.fetchone()
                    if albumID is None:
                        sql = "insert into album (name, release_date) values (%s, %s)"
                        curs.execute(sql, (album_name, track_release))
                        conn.commit()
                        curs.execute("select albumID from album where name = %s", (album_name,))
                        albumID = curs.fetchone()
                    # => include in
                    curs.execute("select artistname from included_in where albumID = %s", (albumID,))
                    exist = False
                    for each in get_result(curs):
                       if each == artist_name:
                            exist = True
                    if not exist:
                        curs.execute("insert into included_in values (%s, %s)", (albumID, artist_name,))
                        conn.commit()
                    # => alb_gen
                    exist = False
                    curs.execute("select genreID from alb_gen where albumID = %s", (albumID,))
                    for each in get_result(curs):
                        if each == genreID:
                            exist = True
                    if not exist:
                        curs.execute("insert into alb_gen values (%s, %s)", (genreID, albumID,))
                        conn.commit()
                    # => song
                    #print(name, artist_name, album_name, track_number, track_duration, track_genre, track_release)
                    sql = "insert into song (title, length, release_date, genreID, artistName) values (%s, %s, %s, %s, %s)"
                    curs.execute(sql, (track_name, track_duration, track_release, genreID, artist_name,))
                    conn.commit()
                    curs.execute("select songID from song where title = %s", (track_name,))
                    songID = curs.fetchone()
                    # => features
                    curs.execute("select * from features where albumID = %s and songID = %s", (albumID, songID))
                    if curs.fetchone is None:
                        sql = "insert into features values (%s, %s, %s)"
                        curs.execute(sql, (track_number, albumID, songID))
                        conn.commit()
                    starbug.disconnect(conn, curs)
                except (Exception, psycopg2.Error) as error:
                    print("data_insertion.py(ERROR):", error)

# better to run one by one
#artist_insert()
#genre_insert()
#song_album_insert()