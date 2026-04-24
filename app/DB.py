import psycopg2
from app.model import Personaje

DATABASE_URL = "postgresql://neondb_owner:npg_NoB8mVl9bsFy@ep-floral-mud-amfzdxn6-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require"

def ConectionDB():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

if getattr(Personaje, '__table__', None) is not None:
    conn = ConectionDB()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personajes (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            color_piel VARCHAR(30),
            raza VARCHAR(30),
            fuerza INTEGER,
            agilidad INTEGER,
            magia INTEGER,
            conocimiento INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()