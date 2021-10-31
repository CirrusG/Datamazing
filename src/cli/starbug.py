# file: database.py
# demo: SSHTunnelForwarder: connect to server/host 
#       -> Psycopg2: connect to RDBMS(PostgreSQL)  
#       -> SQL: modify database
#       -> Psycopg2: fetch, commit modification to database
#       -> close curor and conenct with database
import psycopg2
from sshtunnel import SSHTunnelForwarder

conn = None
curs = None

def connect():
    # info to connect database
    username = ""
    password = ""
    dbName = "p320_10"

    try:
        # Connect to the server hosting the database by SSH
        with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                                ssh_username=username,
                                ssh_password=password,
                                remote_bind_address=('localhost', 5432)) as server:
            server.start()
            print("SSH tunnel established")

            # parameter to store information required to connect db
            params = {
                'database': dbName,
                'user': username,
                'password': password,
                'host': 'localhost',
                'port': server.local_bind_port
            }

            # connect to the db
            conn = psycopg2.connect(**params)
            print("postgreSQL:", conn.get_dsn_parameters(), "\n")

            # cursor
            curs = conn.cursor()
            print("Database connection established")

            # execute query
            curs.execute("SELECT version();")

            # fetch all/remaining rows of a query result set and returns a list
            # of tumbles. if no row, return a empty list
            # execute -> fetchall
            # ==> Here: the result of "SELECT version();"
            #rows = curs.fetchall()
            print(f"curs.fetchall(): {curs.fetchall()}")

            # make the changes to the database persistent; currently is no change(such as table creation)
            conn.commit()
    except Exception as error:
        print(f"Catch Exception: {error}")
        

def disconnect():
    if (conn):
        # close cursor
        curs.close()
        # close connect
        conn.close()
        print("PostgreSQL connection is closed")

# test
#if __name__ == "__main__":
#    connect()
#    connect()
