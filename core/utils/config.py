import os
import sys

def get_database_path():
    """
    Retorna la ruta absoluta de la base de datos, compatible con ejecución como .py o como .exe (PyInstaller).
    Si no existe la carpeta 'data', la crea.
    """
    if getattr(sys, 'frozen', False):
        # Si estamos en un ejecutable (.exe) empaquetado por PyInstaller
        base_dir = os.path.dirname(sys.executable)
    else:
        # Si estamos ejecutando desde el código fuente
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    # Carpeta 'data' al lado del ejecutable o del proyecto
    db_dir = os.path.join(base_dir, 'data')
    os.makedirs(db_dir, exist_ok=True)

    return os.path.join(db_dir, 'firma_app_prevrenal.db')

# Asignamos las rutas necesarias
DB_PATH = get_database_path()