from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import time
import os

from core.utils.logging_utils import configurar_logger

logger = configurar_logger()

class MonitorCarpeta:
    def __init__(self, ruta_directorio, callback_pdf_detectado):
        self.ruta = ruta_directorio
        self.callback = callback_pdf_detectado
        self.observer = Observer()

    def iniciar(self):
        try:
            event_handler = self._crear_event_handler()
            self.observer.schedule(event_handler, self.ruta, recursive=False)
            self.observer.start()

            logger.info(f"Monitor de carpeta activado en: {self.ruta}")

            hilo = threading.Thread(target=self._ejecutar)
            hilo.daemon = True
            hilo.start()

        except Exception as e:
            logger.exception(f"Error al iniciar el monitor de carpeta en {self.ruta}: {e}")

    def _crear_event_handler(self):
        monitor = self

        class Handler(FileSystemEventHandler):
            def on_created(self, event):
                try:
                    if not event.is_directory and event.src_path.endswith(".pdf"):
                        logger.info(f"Archivo PDF detectado: {event.src_path}")
                        monitor.callback(event.src_path)
                except Exception as e:
                    logger.exception(f"Error al procesar archivo creado: {event.src_path}")

        return Handler()

    def _ejecutar(self):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Deteniendo el monitor de carpeta (KeyboardInterrupt)...")
            self.observer.stop()
        except Exception as e:
            logger.exception("Error inesperado durante la ejecución del monitor")
            self.observer.stop()

        self.observer.join()
        logger.info("Monitor de carpeta detenido correctamente.")
