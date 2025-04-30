import os
import shutil
import customtkinter as ctk
import sqlite3

from core.utils.setup_db import crear_base_de_datos
from core.utils.monitor import MonitorCarpeta
from core.controllers.rutas_controller import RutasController
from core.utils.config import DB_PATH
from ui.modules.firma.index import FirmaView
from ui.modules.rutasconfig.index import RutasSetupView
from core.utils.pdf_utils import insertar_firma_y_parentesco
from core.utils.logging_utils import configurar_logger

# Inicializamos el logger global
logger = configurar_logger()
rutas_controller = RutasController()


def mover_pdf_firmado(path_pdf, firma_path, parentesco):
    try:
        logger.info(f"Iniciando proceso de firma para: {path_pdf}")
        insertar_firma_y_parentesco(path_pdf, firma_path, parentesco)

        ruta_destino = rutas_controller.get_ruta_destino()
        if not ruta_destino:
            logger.warning("Ruta de destino no configurada.")
            return

        os.makedirs(ruta_destino, exist_ok=True)
        nombre_pdf = os.path.basename(path_pdf)
        nueva_ruta = os.path.join(ruta_destino, nombre_pdf)

        shutil.move(path_pdf, nueva_ruta)
        logger.info(f"PDF firmado movido a: {nueva_ruta}")

        if os.path.exists(firma_path):
            os.remove(firma_path)
            logger.info(f"Firma temporal eliminada: {firma_path}")

    except Exception as e:
        logger.exception(f"Error al mover el PDF firmado: {e}")


def procesar_pdf(path_pdf):
    logger.info(f"Procesando PDF detectado: {path_pdf}")
    try:
        FirmaView(path_pdf, on_firmar_callback=mover_pdf_firmado)
    except Exception as e:
        logger.exception(f"Error al procesar el PDF: {e}")


def crear_y_configurar_db():
    if not os.path.exists(DB_PATH):
        logger.info("Base de datos no encontrada. Creando nueva...")
        crear_base_de_datos()
    else:
        logger.info("Base de datos detectada correctamente.")


def verificar_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.close()
        logger.info("Conexión a la base de datos verificada.")
    except sqlite3.OperationalError as e:
        logger.error("Error de conexión con la base de datos.")
        logger.exception(e)
        exit(1)


def hay_rutas_configuradas():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM rutas")
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    except sqlite3.Error as e:
        logger.exception(f"Error al verificar rutas configuradas: {e}")
        return False


def obtener_ruta_origen():
    ruta = rutas_controller.get_ruta_origen()
    if not ruta:
        logger.warning("No se encontró ruta de origen configurada.")
        return None
    return ruta


def iniciar_monitor(ruta):
    try:
        logger.info(f"Iniciando monitor en la ruta: {ruta}")
        monitor = MonitorCarpeta(ruta, procesar_pdf)
        monitor.iniciar()
    except Exception as e:
        logger.exception(f"Error al iniciar el monitor: {e}")


def mostrar_ventana_configuracion():
    def continuar_app():
        ruta = obtener_ruta_origen()
        if ruta:
            app.after(500, lambda: iniciar_monitor(ruta))

    logger.info("Mostrando ventana de configuración de rutas.")
    setup_view = RutasSetupView(on_guardar_callback=continuar_app)
    setup_view.grab_set()
    app.mainloop()


# ---------- INICIO DEL PROGRAMA ----------
if __name__ == "__main__":
    logger.info("Aplicación iniciada.")
    crear_y_configurar_db()
    verificar_db()

    app = ctk.CTk()
    app.withdraw()

    if not hay_rutas_configuradas():
        mostrar_ventana_configuracion()
    else:
        ruta_a_escuchar = obtener_ruta_origen()
        if ruta_a_escuchar:
            lanzar_monitor = lambda: iniciar_monitor(ruta_a_escuchar)
            lanzar_monitor()
            app.mainloop()
