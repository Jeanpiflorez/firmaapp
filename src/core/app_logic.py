import os
import shutil
import time
from core.utils.pdf_utils import insertar_firma_y_parentesco
from core.utils.logging_utils import configurar_logger
from core.controllers.rutas_controller import RutasController
from ui.modules.firma.index import FirmaView

logger = configurar_logger()
rutas_controller = RutasController()

def procesar_pdf(path_pdf):
    try:
        nombre = os.path.basename(path_pdf)
        logger.info(f"Procesando archivo PDF: {nombre}")

        if nombre.endswith("_CURL.pdf"):
            logger.info("El archivo requiere firma digital.")
            FirmaView(path_pdf, on_firmar_callback=mover_pdf_firmado)

        elif nombre.startswith("CertificadoAfiliacion - ") and nombre.endswith(".pdf"):
            logger.info("El archivo se moverá directamente, no requiere firma.")
            mover_pdf_directo(path_pdf)

        else:
            logger.warning(f"Archivo no reconocido y no procesado: {nombre}")

    except Exception as e:
        logger.exception(f"Error al procesar el PDF: {e}")

def mover_pdf_firmado(path_pdf, firma_path, parentesco):
    try:
        if esperar_archivo_estable(path_pdf):
            insertar_firma_y_parentesco(path_pdf, firma_path, parentesco)
            _mover_archivo(path_pdf, eliminar=firma_path)
        else:
            logger.error(f"No se pudo firmar el archivo porque no se estabilizó: {path_pdf}")
    except Exception as e:
        logger.exception(f"Error al mover el PDF firmado: {e}")

def mover_pdf_directo(path_pdf):
    try:
        if esperar_archivo_estable(path_pdf):
            _mover_archivo(path_pdf)
        else:
            logger.error(f"No se pudo mover el archivo porque no se estabilizó: {path_pdf}")
    except Exception as e:
        logger.exception(f"Error al mover el PDF sin firmar: {e}")

def _mover_archivo(path_origen, eliminar=None, reintentos=5, espera=0.5):
    ruta_destino = rutas_controller.get_ruta_destino()
    if not ruta_destino:
        logger.warning("Ruta de destino no configurada.")
        return

    os.makedirs(ruta_destino, exist_ok=True)
    nueva_ruta = os.path.join(ruta_destino, os.path.basename(path_origen))

    for intento in range(reintentos):
        try:
            # Si ya existe, lo eliminamos antes de mover
            if os.path.exists(nueva_ruta):
                os.remove(nueva_ruta)

            # Ahora sí intentamos mover
            shutil.move(path_origen, nueva_ruta)
            logger.info(f"Archivo movido a: {nueva_ruta}")
            break  # Salimos del bucle si se movió exitosamente

        except PermissionError:
            logger.warning(
                f"Intento {intento + 1}: el archivo está en uso ({path_origen}). Reintentando en {espera} segundos..."
            )
            time.sleep(espera)

        except Exception as e:
            logger.exception(f"Error inesperado al mover archivo: {path_origen}")
            return

    else:
        logger.error(f"No se pudo mover el archivo después de {reintentos} intentos: {path_origen}")
        return

    if eliminar and os.path.exists(eliminar):
        try:
            os.remove(eliminar)
            logger.info(f"Archivo temporal eliminado: {eliminar}")
        except Exception as e:
            logger.warning(f"No se pudo eliminar el archivo temporal: {eliminar} -> {e}")

def esperar_archivo_estable(path, tiempo_espera=0.5, reintentos=10):
    """ Espera hasta que el archivo deje de crecer en tamaño. """
    ultimo_tamano = -1

    for intento in range(reintentos):
        if not os.path.exists(path):
            logger.warning(f"Archivo no encontrado aún: {path}")
            time.sleep(tiempo_espera)
            continue

        tamano_actual = os.path.getsize(path)

        if tamano_actual == ultimo_tamano:
            # El tamaño no ha cambiado desde la última vez, probablemente está completo
            """ logger.info(f"El archivo parece estable: {path}") """
            return True

        logger.debug(f"Tamaño del archivo aún cambiando (intento {intento + 1}): {tamano_actual} bytes")
        ultimo_tamano = tamano_actual
        time.sleep(tiempo_espera)

    logger.error(f"El archivo no se estabilizó a tiempo: {path}")
    return False