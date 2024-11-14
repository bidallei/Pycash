import sqlite3

# Crear la base de datos y tablas necesarias
def crear_base_datos():
    conn = sqlite3.connect('finanzas.db')
    c = conn.cursor()
    try:
        # Crear la tabla de operaciones
        c.execute('''CREATE TABLE IF NOT EXISTS operaciones (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fecha TEXT,
                        monto REAL,
                        operacion TEXT,
                        descripcion TEXT,
                        total REAL)''')

        # Crear la tabla de personas con deuda inicial
        c.execute('''CREATE TABLE IF NOT EXISTS personas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE,
                        deuda REAL,
                        deuda_inicial REAL)''')

        # Crear la tabla de caja (solo un registro de total general)
        c.execute('''CREATE TABLE IF NOT EXISTS caja (
                        id INTEGER PRIMARY KEY CHECK (id = 1),
                        total REAL)''')
        
        # Crear la tabla de deuda_detalle para registrar cada cambio en la deuda
        c.execute('''CREATE TABLE IF NOT EXISTS deuda_detalle (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        persona_id INTEGER,
                        fecha TEXT,
                        monto REAL,
                        descripcion TEXT,
                        FOREIGN KEY (persona_id) REFERENCES personas(id))''')
    except sqlite3.Error as e:
        print(f"Error creando la base de datos: {e}")
    finally:
        c.close()
        conn.commit()
        conn.close()

# Función para inicializar la caja si está vacía
def inicializar_caja():
    conn = sqlite3.connect('finanzas.db')
    c = conn.cursor()
    try:
        c.execute('SELECT * FROM caja WHERE id=1')
        if not c.fetchone():  # Solo insertar si no existe el registro
            c.execute('INSERT INTO caja (id, total) VALUES (1, 0)')
    except sqlite3.Error as e:
        print(f"Error al inicializar la caja: {e}")
    finally:
        c.close()
        conn.commit()
        conn.close()

# Función para registrar operaciones y actualizar deudas
def registrar_operacion(fecha, monto, operacion, descripcion):
    operacion_texto = "ingreso" if operacion == "i" else "egreso" if operacion == "e" else "deuda"
    conn = sqlite3.connect('finanzas.db')
    c = conn.cursor()
    try:
        # Obtener el total actual de la caja
        c.execute('SELECT total FROM caja WHERE id=1')
        total_caja = c.fetchone()[0]

        if operacion == "i":  # Ingreso
            # Extraer el nombre de la persona desde la descripción
            try:
                nombre_persona = descripcion.split("pago de ")[1].strip()
            except IndexError:
                print("Error: La descripción no contiene el formato esperado.")
                return

            # Actualizar deuda de la persona
            c.execute('SELECT id, deuda FROM personas WHERE nombre=?', (nombre_persona,))
            persona = c.fetchone()
            if persona:
                persona_id, deuda_actual = persona
                nueva_deuda = deuda_actual - monto
                c.execute('UPDATE personas SET deuda=? WHERE id=?', (nueva_deuda, persona_id))
                
                # Registrar el pago en deuda_detalle
                c.execute('INSERT INTO deuda_detalle (persona_id, fecha, monto, descripcion) VALUES (?, ?, ?, ?)', 
                          (persona_id, fecha, -monto, f"Pago de {descripcion}"))

            else:
                # Insertar una nueva persona con deuda negativa (pagada de más)
                c.execute('INSERT INTO personas (nombre, deuda, deuda_inicial) VALUES (?, ?, ?)', 
                          (nombre_persona, -monto, 0))

            # Actualizar el total de la caja sumando el ingreso
            total_caja += monto

        elif operacion == "e":  # Egreso
            total_caja -= monto

        elif operacion == "d":  # Nueva deuda
            # Insertar nueva persona o actualizar deuda
            c.execute('SELECT id, deuda FROM personas WHERE nombre=?', (descripcion,))
            persona = c.fetchone()
            if persona:
                persona_id, deuda_actual = persona
                nueva_deuda = deuda_actual + monto
                c.execute('UPDATE personas SET deuda=? WHERE id=?', (nueva_deuda, persona_id))
                
                # Registrar la deuda en deuda_detalle
                c.execute('INSERT INTO deuda_detalle (persona_id, fecha, monto, descripcion) VALUES (?, ?, ?, ?)', 
                          (persona_id, fecha, monto, "Deuda generada"))
            else:
                # Nueva persona con deuda
                c.execute('INSERT INTO personas (nombre, deuda, deuda_inicial) VALUES (?, ?, ?)', 
                          (descripcion, monto, monto))
                
                # Obtener el ID de la nueva persona para deuda_detalle
                persona_id = c.lastrowid
                c.execute('INSERT INTO deuda_detalle (persona_id, fecha, monto, descripcion) VALUES (?, ?, ?, ?)', 
                          (persona_id, fecha, monto, "Deuda inicial"))

        # Registrar la operación con el nuevo total de la caja
        c.execute('INSERT INTO operaciones (fecha, monto, operacion, descripcion, total) VALUES (?, ?, ?, ?, ?)', 
                  (fecha, monto, operacion_texto, descripcion, total_caja))
        
        # Actualizar el total de la caja en la tabla de caja
        c.execute('UPDATE caja SET total=? WHERE id=1', (total_caja,))
    
    except sqlite3.Error as e:
        print(f"Error al registrar la operación: {e}")
    finally:
        c.close()
        conn.commit()
        conn.close()

# Función para consultar operaciones
def consultar_operaciones(fecha=None, nombre=None, operacion=None):
    conn = sqlite3.connect('finanzas.db')
    c = conn.cursor()
    try:
        # Construir la consulta SQL dinámica
        query = "SELECT * FROM operaciones WHERE 1=1"
        parameters = []
        
        if fecha:
            query += " AND fecha = ?"
            parameters.append(fecha)
        if nombre:
            query += " AND descripcion LIKE ?"
            parameters.append(f"%{nombre}%")
        if operacion:
            query += " AND operacion = ?"
            parameters.append(operacion)

        c.execute(query, parameters)
        resultados = c.fetchall()
    except sqlite3.Error as e:
        print(f"Error al consultar operaciones: {e}")
        resultados = []
    finally:
        c.close()
        conn.close()

    return resultados

# Inicializar la base de datos y la caja
crear_base_datos()
inicializar_caja()
