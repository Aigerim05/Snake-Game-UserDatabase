import psycopg2
from config import load_config

def update_data(username, score, level):

    sql = """ UPDATE snake
                SET score = %s, level = %s
                WHERE user_name = %s"""
    

    config = load_config()
    
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
            
                cur.execute(sql, (score, level, username))

            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    


if __name__ == '__main__':
    update_data('aiko', '200', "23")
