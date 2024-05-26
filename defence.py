import psycopg2
from config import load_config

i = 0
scores = []
users = []

def get_max_min():
    sql = "SELECT * FROM snake_score"
    config  = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()

                for row in rows:
                    scores.append(row[2])
                    users.append(row[1])
                    

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    get_max_min() 
    scores = list(map(int, scores))  
    max_value = max(scores)
    min_value = min(scores)
    index_max = scores.index(max_value)
    index_min = scores.index(min_value)
    print("Max: " , users[index_max], max_value)
    print("Min: " , users[index_min], min_value)
