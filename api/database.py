import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="ep-young-silence-aklb1zze-pooler.c-3.us-west-2.aws.neon.tech",
        database="neondb",
        user="neondb_owner",
        password="npg_5UrNQI8inVev",
        port="5432",
        sslmode="require"
    )
    return conn