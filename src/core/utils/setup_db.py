# core/setup_db.py

import sqlite3
import os
from core.utils.config import DB_PATH

def crear_base_de_datos():
    # Asegúrate de que la carpeta que contiene la BD exista
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rutas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ruta TEXT NOT NULL,
            descripcion TEXT,
            identificador TEXT UNIQUE NOT NULL
        )
    """)

    conn.commit()
    conn.close()