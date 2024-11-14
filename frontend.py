import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import backend

class FinanzasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Finanzas")
        self.root.geometry("400x180")
        self.centrar_ventana(self.root, 400, 300)
        self.root.configure(bg="#3B322C")

        # Agregar el manejador del cierre de ventana principal
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_app)

        # Título principal
        titulo_label = tk.Label(root, text="Gestión de Finanzas", font=("Arial", 17, "bold"), bg="#5E8C61", fg="white", width = 20)
        titulo_label.pack(pady=20)

        # Botón de registro de operación
        self.btn_registrar = tk.Button(root, text="Registrar operación", font=("Helvetica", 12), bg="#5E8C61", fg="white", command=self.registrar_operacion, width = 20)
        self.btn_registrar.pack(pady=10)

        # Botón de consulta de operaciones
        self.btn_consultar = tk.Button(root, text="Consultar operaciones", font=("Helvetica", 12), bg="#5E8C61", fg="white", command=self.consultar_operacion, width = 20)
        self.btn_consultar.pack(pady=10)

        # Botón para cerrar la aplicación
        self.btn_cerrar = tk.Button(root, text="Cerrar", font=("Helvetica", 12), bg="#5E8C61", fg="white", command=self.cerrar_app, width = 20)
        self.btn_cerrar.pack(pady=10)

    def centrar_ventana(self, ventana, ancho=400, alto=300):
        pantalla_ancho = ventana.winfo_screenwidth()
        pantalla_alto = ventana.winfo_screenheight()
        
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def registrar_operacion(self):
        # Cerrar la ventana principal
        self.root.withdraw()

        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar operación")
        self.centrar_ventana(ventana, 350, 300)
        ventana.configure(bg="#3B322C")

        tk.Label(ventana, text="Fecha (YYYY-MM-DD)").grid(row=0, column=0)
        fecha_entry = tk.Entry(ventana)
        fecha_entry.grid(row=0, column=1)

        tk.Label(ventana, text="Monto").grid(row=1, column=0)
        monto_entry = tk.Entry(ventana)
        monto_entry.grid(row=1, column=1)

        tk.Label(ventana, text="Egreso: e, Ingreso: i, Deuda: d").grid(row=2, column=0)
        operacion_entry = tk.Entry(ventana)
        operacion_entry.grid(row=2, column=1)

        tk.Label(ventana, text="Descripción").grid(row=3, column=0)
        descripcion_entry = tk.Entry(ventana)
        descripcion_entry.grid(row=3, column=1)

        def guardar():
            fecha = fecha_entry.get().strip()
            monto = float(monto_entry.get().strip())
            operacion = operacion_entry.get().strip().lower()
            descripcion = descripcion_entry.get().strip()

            if operacion not in ["i", "e", "d"]:
                tk.messagebox.showerror("Error", "El tipo de operación debe ser 'i' para ingreso, 'e' para egreso, o 'd' para deuda.")
                return

            if not fecha or not monto or not descripcion:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            backend.registrar_operacion(fecha, monto, operacion, descripcion)
            messagebox.showinfo("Éxito", "Operación registrada correctamente.")
            ventana.destroy()
            self.root.deiconify()  # Volver a mostrar la ventana principal

        # Botón para guardar la operación
        tk.Button(ventana, text="Guardar", command=guardar, bg="#5E8C61", fg="white").grid(row=4, column=0, columnspan=2, pady=5, padx=5, sticky="nsew")

        # Botón para regresar a la ventana principal
        def regresar_inicio():
            ventana.destroy()
            self.root.deiconify()  # Volver a mostrar la ventana principal

        tk.Button(ventana, text="Regresar", command=regresar_inicio, bg="#5E8C61", fg="white").grid(row=5, column=0, columnspan=2, pady=5, padx=5, sticky="ew")

        # Botón para cerrar la ventana
        tk.Button(ventana, text="Cerrar", command=self.root.destroy, bg="#5E8C61", fg="white").grid(row=6, column=0, columnspan=2, pady=5, padx=5, sticky="ew")

    def consultar_operacion(self):
        # Cerrar la ventana principal
        self.root.withdraw()

        # Crear la ventana secundaria para consulta de operaciones
        ventana = tk.Toplevel(self.root)
        ventana.title("Consultar operaciones")
        self.centrar_ventana(ventana, 600, 280)
        self.root.configure(bg="#3B322C")

        # Campo de entrada para Fecha
        tk.Label(ventana, text="Fecha (YYYY-MM-DD)").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        fecha_entry = tk.Entry(ventana)
        fecha_entry.grid(row=0, column=1, pady=5, padx=5)

        # Campo de entrada para Nombre
        tk.Label(ventana, text="Nombre").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        nombre_entry = tk.Entry(ventana)
        nombre_entry.grid(row=1, column=1, pady=5, padx=5)

        # Campo de entrada para Tipo de Operación
        tk.Label(ventana, text="Egreso: e o Ingreso: i").grid(row=2, column=0, pady=5, padx=5, sticky="e")
        operacion_entry = tk.Entry(ventana)
        operacion_entry.grid(row=2, column=1, pady=5, padx=5)

        def buscar():
            fecha = fecha_entry.get().strip()
            nombre = nombre_entry.get().strip()
            operacion = operacion_entry.get().strip()

            # Verificar que al menos un campo esté lleno para hacer la búsqueda
            if not fecha and not nombre and not operacion:
                operaciones = backend.consultar_operaciones()  # Consulta todos los registros
            else:
                # Llamar al backend con los filtros proporcionados
                operaciones = backend.consultar_operaciones(fecha, nombre, operacion)

            # Mostrar los resultados en una tabla
            if operaciones:
                tree = ttk.Treeview(ventana, columns=("Fecha", "Monto", "Operación", "Descripción", "Total"), show="headings")
                tree.grid(row=7, column=0, columnspan=2, pady=20)

                tree.heading("Fecha", text="Fecha")
                tree.heading("Monto", text="Monto")
                tree.heading("Operación", text="Operación")
                tree.heading("Descripción", text="Descripción")
                tree.heading("Total", text="Total")

                # Agregar las filas de resultado
                for op in operaciones:
                    tree.insert("", "end", values=(op[1], op[2], op[3], op[4], op[5]))
            else:
                messagebox.showinfo("Resultados", "No se encontraron operaciones.")
        
        # Botón para ejecutar la búsqueda
        tk.Button(ventana, text="Buscar", command=buscar, bg="#5E8C61", fg="white").grid(row=3, column=0, columnspan=2, pady=5, padx=5, sticky="ew")

        # Botón para regresar a la ventana principal
        tk.Button(ventana, text="Regresar", command=lambda: (ventana.destroy(), self.root.deiconify()), bg="#5E8C61", fg="white").grid(row=5, column=0, columnspan=2, pady=5, padx=5, sticky="ew")

        # Botón para cerrar toda la aplicación
        tk.Button(ventana, text="Cerrar", command=self.root.destroy, bg="#5E8C61", fg="white").grid(row=6, column=0, columnspan=2, pady=5, padx=5, sticky="ew")

    def cerrar_app(self):
        self.root.quit()  # Termina el ciclo principal de tkinter y cierra la aplicación
        self.root.destroy()  # Destruye la ventana principal

if __name__ == "__main__":
    backend.crear_base_datos()
    backend.inicializar_caja()

    root = tk.Tk()
    app = FinanzasApp(root)
    root.mainloop()
