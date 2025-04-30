# core/controllers/rutas_controller.py
from core.models.rutas_model import RutaModel

class RutasController:
    def __init__(self):
        self.model = RutaModel()

    def get_ruta_origen(self):
        return self.model.get_ruta_by_identificador("origen")

    def get_ruta_destino(self):
        return self.model.get_ruta_by_identificador("destino")

    def insertar_ruta(self, ruta, descripcion, identificador):
        self.model.insertar_ruta(ruta, descripcion, identificador)
