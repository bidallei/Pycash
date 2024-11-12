import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import backend

class FinanzasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Finanzas")
        self.root.geometry("400x300")

        # Agregar el manejador del cierre de ventana principal
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_app)

        # Título principal
        titulo_label = tk.Label(root, text="Gestión de Finanzas", font=("Arial", 18, "bold"))
        titulo_label.pack(pady=20)

        # Botón de registro de operación
        self.btn_registrar = tk.Button(root, text="Registrar operación", font=("Helvetica", 12), command=self.registrar_operacion, width = 20)
        self.btn_registrar.pack(pady=10)

        # Botón de consulta de operaciones
        self.btn_consultar = tk.Button(root, text="Consultar operaciones", font=("Helvetica", 12), command=self.consultar_operacion, width = 20)
        self.btn_consultar.pack(pady=10)

        # Botón para cerrar la aplicación
        self.btn_cerrar = tk.Button(root, text="Cerrar", font=("Helvetica", 12), command=self.cerrar_app, width = 20)
        self.btn_cerrar.pack(pady=10)

    def registrar_operacion(self):
        # Cerrar la ventana principal
        self.root.withdraw()

        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar operación")
        ventana.geometry("300x200")

        # Agregar el manejador de cierre de ventana secundaria
        def cerrar_ventana_secundaria():
            ventana.destroy()  # Cierra la ventana secundaria
            self.root.quit()  # Termina el ciclo principal si se cierra una ventana secundaria
        
        ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana_secundaria)  # Maneja el cierre con la "X"

        tk.Label(ventana, text="Fecha (YYYY-MM-DD)").grid(row=0, column=0)
        fecha_entry = tk.Entry(ventana)
        fecha_entry.grid(row=0, column=1)

        tk.Label(ventana, text="Monto").grid(row=1, column=0)
        monto_entry = tk.Entry(ventana)
        monto_entry.grid(row=1, column=1)

        tk.Label(ventana, text="Operación (ingreso/egreso)").grid(row=2, column=0)
        operacion_entry = tk.Entry(ventana)
        operacion_entry.grid(row=2, column=1)

        tk.Label(ventana, text="Descripción (pago de persona)").grid(row=3, column=0)
        descripcion_entry = tk.Entry(ventana)
        descripcion_entry.grid(row=3, column=1)

        def guardar():
            fecha = fecha_entry.get()
            monto = float(monto_entry.get())
            operacion = operacion_entry.get()
            descripcion = descripcion_entry.get()

            if operacion not in ["ingreso", "egreso"]:
                messagebox.showerror("Error", "La operación debe ser 'ingreso' o 'egreso'.")
                return

            if not fecha or not monto or not descripcion:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            backend.registrar_operacion(fecha, monto, operacion, descripcion)
            messagebox.showinfo("Éxito", "Operación registrada correctamente.")
            ventana.destroy()
            self.root.deiconify()  # Volver a mostrar la ventana principal

        # Botón para guardar la operación
        tk.Button(ventana, text="Guardar", command=guardar).grid(row=4, column=1)

        # Botón para regresar a la ventana principal
        def regresar_inicio():
            ventana.destroy()
            self.root.deiconify()  # Volver a mostrar la ventana principal

        tk.Button(ventana, text="Regresar", command=regresar_inicio).grid(row=5, column=1, pady=10)

    def consultar_operacion(self):
        # Cerrar la ventana principal
        self.root.withdraw()

        ventana = tk.Toplevel(self.root)
        ventana.title("Consultar operaciones")
        ventana.geometry("600x400")

        tk.Label(ventana, text="Buscar por (fecha/monto/descripción)").grid(row=0, column=0)
        campo_entry = tk.Entry(ventana)
        campo_entry.grid(row=0, column=1)

        tk.Label(ventana, text="Valor de búsqueda").grid(row=1, column=0)
        valor_entry = tk.Entry(ventana)
        valor_entry.grid(row=1, column=1)

        def buscar():
            campo = campo_entry.get().strip()
            valor = valor_entry.get().strip()

            # Si los campos están vacíos, mostrar todos los registros
            if not campo and not valor:
                operaciones = backend.consultar_operaciones()
            else:
                if not campo or not valor:
                    messagebox.showerror("Error", "Ambos campos son obligatorios si se desea hacer una búsqueda específica.")
                    return
                operaciones = backend.consultar_operaciones(campo, valor)

            # Crear y mostrar la tabla solo cuando se realiza la búsqueda
            if operaciones:
                # Crear la tabla solo cuando haya resultados
                tree = ttk.Treeview(ventana, columns=("Fecha", "Monto", "Operación", "Descripción", "Total"), show="headings")
                tree.grid(row=3, column=0, columnspan=2, pady=20)

                tree.heading("Fecha", text="Fecha")
                tree.heading("Monto", text="Monto")
                tree.heading("Operación", text="Operación")
                tree.heading("Descripción", text="Descripción")
                tree.heading("Total", text="Total")

                # Agregar los resultados a la tabla
                for op in operaciones:
                    tree.insert("", "end", values=(op[1], op[2], op[3], op[4], op[5]))
            else:
                messagebox.showinfo("Resultados", "No se encontraron operaciones.")

        def regresar_inicio():
            ventana.destroy()  # Cerrar la ventana secundaria
            self.root.deiconify()  # Mostrar la ventana principal
            self.root.quit()  # Terminar el ciclo principal de tkinter y cerrar la aplicación

        tk.Button(ventana, text="Buscar", command=buscar).grid(row=2, column=1)
        tk.Button(ventana, text="Regresar", command=regresar_inicio).grid(row=4, column=1, pady=10)

    def cerrar_app(self):
        self.root.quit()  # Termina el ciclo principal de tkinter y cierra la aplicación
        self.root.destroy()  # Destruye la ventana principal

if __name__ == "__main__":
    backend.crear_base_datos()
    backend.inicializar_caja()

    root = tk.Tk()
    app = FinanzasApp(root)
    root.mainloop()
