from core.app import lanzar_aplicacion
import tkinter as tk
from tkinter import messagebox

def mostrar_mensaje_bienvenida():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    messagebox.showinfo("Firma App", "Bienvenido a Firma App.\nEl sistema se está iniciando.")
    root.destroy()
    
def mostrar_mensaje_iniciado():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    messagebox.showinfo("Firma App", "Bienvenido a Firma App.\nEl sistema está iniciado correctamente.")
    root.destroy()

if __name__ == "__main__":
    print(r"Aplicación Iniciada \(0_0)/")
    mostrar_mensaje_bienvenida() 
    lanzar_aplicacion()
    mostrar_mensaje_iniciado()