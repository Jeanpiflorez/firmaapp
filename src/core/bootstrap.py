# src/core/bootstrap.py

import os
import sqlite3
from core.utils.config import DB_PATH
from core.utils.setup_db import crear_base_de_datos

def crear_y_configurar_db():
    """
    Si no existe la base de datos, la crea usando el método del módulo setup_db.
    """
    if not os.path.exists(DB_PATH):
        crear_base_de_datos()

def verificar_db():
    """
    Verifica si la base de datos es accesible (sqlite3 se puede conectar).
    Lanza excepción si falla.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.close()
    except sqlite3.OperationalError as e:
        raise RuntimeError("Error de conexión con la base de datos") from e

def hay_rutas_configuradas():
    """
    Revisa si existe al menos una ruta configurada en la base de datos.
    Retorna True si hay, False si no hay o si hay error.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM rutas")
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    except sqlite3.Error as e:
        print(f"Error al verificar rutas configuradas: {e}")
        return False
