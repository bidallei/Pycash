import tkinter as tk
from tkinter import font

def mostrar_fuentes():
    root = tk.Tk()
    root.title("Fuentes disponibles")

    # Obtener todas las fuentes disponibles
    fuentes = font.families()

    # Crear un widget Text para mostrar las fuentes
    text_widget = tk.Text(root, height=20, width=50)
    text_widget.pack()

    # Insertar las fuentes en el widget Text
    for fuente in fuentes:
        text_widget.insert(tk.END, fuente + '\n')

    # Hacer que la ventana sea visible
    root.mainloop()

# Llamamos a la función para mostrar las fuentes
mostrar_fuentes()
