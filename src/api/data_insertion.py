import csv
import psycopg2
import sys
sys.path.append('../cli/')
import local as starbug
# will change to cli.starbug later

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
    return row

def artist_insert():
    # done insert artist
    try:
        with open('spotify-data/artists.csv', newline='') as artistfile:
            conn = starbug.connect()
            curs = conn.cursor()
            reader = csv.reader(artistfile, delimiter=',')
            # jump header
            next(reader)
            for row in reader:
                print(row[-1])
                sql = "insert into artist values (%s)"
                curs.execute(sql, (row[-1],))
                conn.commit()
            starbug.disconnect(conn, curs)
    except (Exception, psycopg2.Error) as error:
        print("data_insertion.py(ERROR):", error)


def genre_insert():
    try:
        # done insert genre
        with open('spotify-data/genres.csv', newline='') as genresfile:
            conn = starbug.connect()
            curs = conn.cursor()
            reader = csv.reader(genresfile, delimiter=',')
            # jump header
            next(reader)
            for row in reader:
                # print(row[-1])
                sql = "insert into genre (name) values (%s)"
                curs.execute(sql, (row[1],))
                conn.commit()
            starbug.disconnect(conn, curs)
    except (Exception, psycopg2.Error) as error:
        print("data_insertion.py(ERROR):", error)


def song_album_insert():
    # table: song, album, included_in, features, alb_gen
    try:
        with open('spotify-data/tracks.csv') as tracksfile:
            conn = starbug.connect()
            curs = conn.cursor()
            reader = csv.reader(tracksfile, delimiter=',')
            # jump header
            next(reader)
            for row in reader:
                # name: 1, artist_name: 4, album_name: 6, track_number 7, 
                # track_duration(mm:ss): -1, track_genre: 9, track_release: 10
                name = row[1]
                artist_name = row[4]
                track_genre = row[9]
                track_duration = row[-1]
                track_release = row[10]
                album_name = row[6] # feature
                track_number = row[7] # feature
                # table: album
                result = if_exist('album', 'name', album_name)
                if result == None:
                    sql = "insert into album (name, release_date) values (%s, %s)"
                    curs.execute(sql, (album_name, track_release))
                    curs.commit()
                curs.excute("select albumID from album where name = %s", (album_name))
                albumID = curs.fetchone()
                # include: 
                # TODO get albumID, genreID
                sql = "insert into features"
                #sql = "select albumID from album where album_name = %s"
                #print(name, artist_name, album_name, track_number, track_duration, track_genre, track_release)
                sql = "insert into song (title, length, release_data, genreID, artistName) values (%s, %s, %s, %s, %s)"
                curs.execute(sql, (name, track_duration, track_release, track_genre,artist_name, ))
                conn.commit()
                break # test first record
            starbug.disconnect(conn, curs)
    except (Exception, psycopg2.Error) as error:
        print("data_insertion.py(ERROR):", error)
    
def album_insert():
    return



# artist_insert()
#genre_insert()

song_insert()