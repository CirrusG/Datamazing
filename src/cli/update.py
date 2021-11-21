import psycopg2
import starbug
import read

def rename_collec(username, collectionid, new_name):
    conn = curs = result = None
    try:
        conn = starbug.connect()
        curs = conn.cursor()
        query = "update collection set name = %s where username = %s and collectionid = %s " \
                "returning *"
        curs.execute(query, (new_name, username, collectionid,))
        conn.commit()
        result = read.get_result(curs)[0]
    except (Exception, psycopg2.Error) as error:
        print("rename_collec (ERROR):", error)
    finally:
        starbug.disconnect(conn,curs)
    return result




if __name__ == '__main__':
    print(rename_collec('ly', "collection136", "Happy Friday")[0][2])
    #print("")