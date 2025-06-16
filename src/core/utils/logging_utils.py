import os
import sys
import logging
import traceback
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ===============================
# Funciones de logging
# ===============================

def get_logs_path():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

    logs_dir = os.path.join(base_dir, 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    return os.path.join(logs_dir, 'app.log')


def configurar_logger(nombre_logger="firma_app", nivel=logging.ERROR):
    log_path = get_logs_path()
    logger = logging.getLogger(nombre_logger)
    logger.setLevel(nivel)

    if not logger.handlers:
        archivo_handler = logging.FileHandler(log_path, encoding="utf-8")
        archivo_handler.setLevel(nivel)

        consola_handler = logging.StreamHandler()
        consola_handler.setLevel(nivel)

        formato = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        archivo_handler.setFormatter(formato)
        consola_handler.setFormatter(formato)

        logger.addHandler(archivo_handler)
        logger.addHandler(consola_handler)

    return logger

# ===============================
# Código que usa el logger
# ===============================

logger = configurar_logger(nivel=logging.INFO)

def iniciar_monitor(ruta_a_monitorear):
    """
    Intenta iniciar un monitor en la ruta indicada.
    Si la carpeta no existe, muestra un mensaje claro y registra el error.
    """
    try:
        if not os.path.exists(ruta_a_monitorear):
            raise FileNotFoundError(f"La carpeta '{ruta_a_monitorear}' no existe. Por favor, verifica la ruta.")

        event_handler = FileSystemEventHandler()  # Aquí puedes usar tu propio handler personalizado
        observer = Observer()
        observer.schedule(event_handler, path=ruta_a_monitorear, recursive=False)
        observer.start()

        logger.info(f"Monitor de carpeta iniciado en: {ruta_a_monitorear}")

    except FileNotFoundError as e:
        logger.error(str(e))  # Muestra solo el mensaje amigable
    except Exception as e:
        # Para errores inesperados, puedes decidir si mostrar el traceback completo o no
        logger.error(f"Error inesperado: {e}")
        # Si estás en modo debug, puedes hacer:
        # logger.error("Detalles:\n" + traceback.format_exc())