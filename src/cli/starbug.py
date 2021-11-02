# file: database.py
# demo: SSHTunnelForwarder: connect to server/host 
#       -> Psycopg2: connect to RDBMS(PostgreSQL)  
#       -> SQL: modify database
#       -> Psycopg2: fetch, commit modification to database
#       -> close curor and conenct with database
import psycopg2


username = ""
password = ""
dbName = "p320_10"
from sshtunnel import SSHTunnelForwarder

def conn_server():
    server = SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                            ssh_username=username,
                            ssh_password=password,
                            remote_bind_address=('localhost', 5432))
        #server.start()
    #print("SSH tunnel established")
    return server

def disconn_server(server):
    server.close()


def connect(server):
    # info to connect database
    conn = None

    try:
        #Connect to the server hosting the database by SSH

            # parameter to store information required to connect db
            params = {
                'database': dbName,
                'user': username,
                'password': password,
                'host': 'localhost',
                'port': server.local_bind_port
                #'port': 5432
            }

            # connect to the db
            conn = psycopg2.connect(**params)
            #print("Database connection established")
                #print("postgreSQL:", conn.get_dsn_parameters(), "\n")

                # cursor
                #curs = conn.cursor()

                # execute query
                #curs.execute("SELECT version();")

                # fetch all/remaining rows of a query result set and returns a list
                # of tumbles. if no row, return a empty list
                # execute -> fetchall
                # ==> Here: the result of "SELECT version();"
                #rows = curs.fetchall()
                #print(f"curs.fetchall(): {curs.fetchall()}")

                # make the changes to the database persistent; currently is no change(such as table creation)
                #conn.commit()
    except (Exception, psycopg2) as error:
        print(f"starbug.py(Exception): {error}")
    return conn
        

def disconnect(conn, curs):
    try:
        if conn is not None:
            # close cursor
            curs.close()
            # close connect
            conn.close()
            #print("Database connection is closed")
    except (Exception, psycopg2.Error) as error:
       print(f"Catch Exception: {error}")

# test
# server = conn_server()
# server.start()
# conn = connect()
# curs = conn.cursor()
# #curs.execute("select usename, count(*) as count from pg_stat_activity where datname like 'p320\__' group by usename order by count desc")
# curs.execute("select version();")
# print(query.get_result(curs))
# disconnect(conn, curs)
# server.stop()
