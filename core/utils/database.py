import sqlite3

class Database:
    def __init__(self, ruta_bd="data/firma_app_prevrenal.db"):
        self.ruta_bd = ruta_bd

    def conectar(self):
        return sqlite3.connect(self.ruta_bd)