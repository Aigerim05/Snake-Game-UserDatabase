import psycopg2
from config import load_config

def delete_data():

    sql = """ DELETE FROM snake;"""
    

    config = load_config()
    
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                
                cur.execute(sql, ())

            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    



if __name__ == '__main__':
    delete_data()
