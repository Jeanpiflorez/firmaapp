import os
import shutil
from core.utils.pdf_utils import insertar_firma_y_parentesco
from core.utils.logging_utils import configurar_logger
from core.controllers.rutas_controller import RutasController
from ui.modules.firma.index import FirmaView

logger = configurar_logger()
rutas_controller = RutasController()

def mover_pdf_firmado(path_pdf, firma_path, parentesco):
    try:
        insertar_firma_y_parentesco(path_pdf, firma_path, parentesco)
        ruta_destino = rutas_controller.get_ruta_destino()
        if not ruta_destino:
            logger.warning("Ruta de destino no configurada.")
            return

        os.makedirs(ruta_destino, exist_ok=True)
        nueva_ruta = os.path.join(ruta_destino, os.path.basename(path_pdf))
        shutil.move(path_pdf, nueva_ruta)

        if os.path.exists(firma_path):
            os.remove(firma_path)

    except Exception as e:
        logger.exception(f"Error al mover el PDF firmado: {e}")

def procesar_pdf(path_pdf):
    try:
        FirmaView(path_pdf, on_firmar_callback=mover_pdf_firmado)
    except Exception as e:
        logger.exception(f"Error al procesar el PDF: {e}")
