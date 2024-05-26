import psycopg2
from config import load_config

def insert_data(username, score, level):

    sql = """INSERT INTO snake(user_name, score, level)
             VALUES(%s,%s,%s)"""
    
    config = load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement

                cur.execute(sql, (username, score, level))

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    


if  __name__ == '__main__':
    insert_data('gigi','5','0')
