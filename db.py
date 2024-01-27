import psycopg2

DATABASE_URL = "postgresql://postgres:Episodio1@localhost:5432/Inventario"

def connect_db():
    return psycopg2.connect(DATABASE_URL)
