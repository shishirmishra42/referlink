import psycopg2
def get_connection():
    conn = psycopg2.connect(
        dbname="referlink",
        user="postgres",
        password="914Shift@",
        host="localhost",
        port="5432"
    )
    return conn
