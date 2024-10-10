from os import getenv

pg_user = getenv("PG_USER")
pg_password = getenv("PG_PASSWORD")
pg_db = getenv("PG_DB")

def get_database_url():
    return f"postgresql://{pg_user}:{pg_password}@db:5432/{pg_db}"
