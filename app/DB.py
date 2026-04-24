import sqlite3
from app.model import Personaje

def ConectionDB():
    conn = sqlite3.connect('personajes.db')
    return conn

if getattr(Personaje, '__table__', None) is not None:
    conn = ConectionDB()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            color_piel TEXT,
            raza TEXT,
            fuerza INTEGER,
            agilidad INTEGER,
            magia INTEGER,
            conocimiento INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()