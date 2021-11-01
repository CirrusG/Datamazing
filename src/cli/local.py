
import psycopg2


def connect():
    # info to connect database
    conn = None
    username = "postgres"
    password = "changeme"
    dbName = "test"
    try:
        # parameter to store information required to connect
        params = {
            'database': dbName,
            'user': username,
            'password': password,
            'host': 'localhost',
            'port': 5432
        }
        conn = psycopg2.connect(**params)
        print("Database connection established")
    except (Exception, psycopg2.Error) as error:
        print(f"Catch Exception: {error}")
    return conn


def disconnect(conn, curs):
    try:
        if conn is not None:
            # close cursor
            curs.close()
            # close connect
            conn.close()
            print("Database connection is closed")
    except (Exception, psycopg2.Error) as error:
       print(f"Catch Exception: {error}") 



# test
#if __name__ == "__main__":
#    connect()
#    disconnect()
