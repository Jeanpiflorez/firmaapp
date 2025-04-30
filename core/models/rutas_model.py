# core/models/rutas_model.py

import sqlite3
from core.utils.config import DB_PATH

class RutaModel:
    def get_ruta_by_identificador(self, identificador):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT ruta FROM rutas WHERE identificador = ?
        """, (identificador,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            return resultado[0]
        return None

    def insertar_ruta(self, ruta, descripcion, identificador):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO rutas (ruta, descripcion, identificador)
            VALUES (?, ?, ?)
        """, (ruta, descripcion, identificador))

        conn.commit()
        conn.close()