import os
import sys
import logging

def get_logs_path():
    """
    Retorna la ruta absoluta del archivo de logs, asegurando que exista la carpeta 'logs'.
    Compatible con ejecución desde PyInstaller o como script.
    """
    if getattr(sys, 'frozen', False):
        # Ejecutable compilado (.exe)
        base_dir = os.path.dirname(sys.executable)
    else:
        # Código fuente
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

    logs_dir = os.path.join(base_dir, 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    return os.path.join(logs_dir, 'app.log')


def configurar_logger(nombre_logger="firma_app", nivel=logging.ERROR):
    """
    Configura y retorna un logger estándar para la aplicación.
    - Escribe en logs/app.log
    - También imprime en consola
    """
    log_path = get_logs_path()

    logger = logging.getLogger(nombre_logger)
    logger.setLevel(nivel)

    # Evitar agregar múltiples handlers si ya están configurados
    if not logger.handlers:
        # Handler para archivo
        archivo_handler = logging.FileHandler(log_path, encoding="utf-8")
        archivo_handler.setLevel(nivel)

        # Handler para consola
        consola_handler = logging.StreamHandler()
        consola_handler.setLevel(nivel)

        # Formato común
        formato = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        archivo_handler.setFormatter(formato)
        consola_handler.setFormatter(formato)

        # Agregar handlers
        logger.addHandler(archivo_handler)
        logger.addHandler(consola_handler)

    return logger
