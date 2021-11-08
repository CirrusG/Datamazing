# file: database.py
# author: Datamazing (group 8)
# demo: SSHTunnelForwarder: connect to server/host 
#       -> Psycopg2: connect to RDBMS(PostgreSQL)  
#       -> SQL: modify database
#       -> Psycopg2: fetch, commit modification to database
#       -> close cursor and connect with database
# docs: https://sshtunnel.readthedocs.io/en/latest/
from datetime import datetime
import psycopg2
import sshtunnel
from sshtunnel import SSHTunnelForwarder


def get_db_name():
    # group database name
    # DON'T FORGET TO REMOVE THIS
    dbName = "p320_10"
    return dbName


def get_password():
    # ssh/database password
    # DON'T FORGET TO REMOVE THIS
    password = ""
    return password


def get_username():
    # ssh/database username
    # DON'T FORGET TO REMOVE THIS
    username = ""
    return username


def conn_server():
    # connect to starbug server
    # @return server pointer
    server = None
    try:
        server = SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                                    ssh_username=get_username(),
                                    ssh_password=get_password(),
                                    remote_bind_address=('localhost', 5432))
        server.start()
        #print(datetime.now(), "SSH tunnel established")
    except sshtunnel.BaseSSHTunnelForwarderError as error:
        print("starbug.conn_server(Exception):", error)
    return server


def disconn_server(server):
    # close starbug server
    server.close()
    #print(datetime.now(), "SSH tunnel closed")


def connect():
    # connect database
    # @return database connect pointer
    global server
    server = conn_server()
    conn = None
    try:
        params = {
            'database': get_db_name(),
            'user': get_username(),
            'password': get_password(),
            'host': 'localhost',
            'port': server.local_bind_port
        }

        conn = psycopg2.connect(**params)
        #print(datetime.now(), "Database connection established")
    except psycopg2.Error as error:
        print(f"starbug.connect(Exception): {error}")
    return conn


def disconnect(conn, curs):
    try:
        if (conn is not None) and (curs is not None):
            # close cursor
            curs.close()
            # close connect
            conn.close()
            # print("Database connection is closed")
    except (Exception, psycopg2.Error) as error:
        print(f"starbug.disconnect(Exception): {error}")
    finally:
        disconn_server(server)
        #print(f"{datetime.now()} Datebase connection broken")
