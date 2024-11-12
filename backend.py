import sqlite3

# Crear la base de datos y tablas necesarias
def crear_base_datos():
    conn = sqlite3.connect('finanzas.db')
    c = conn.cursor()

    # Crear la tabla de operaciones
    c.execute('''CREATE TABLE IF NOT EXISTS operaciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT,
                    monto REAL,
                    operacion TEXT,
                    descripcion TEXT,
                    total REAL)''')

    # Crear la tabla de personas
    c.execute('''CREATE TABLE IF NOT EXISTS personas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE,
                    deuda REAL)''')

    # Crear la tabla de caja (solo un registro de total general)
    c.execute('''CREATE TABLE IF NOT EXISTS caja (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    total REAL)''')

    conn.commit()
    conn.close()

# Función para inicializar la caja si está vacía
def inicializar_caja():
    conn = sqlite3.connect('finanzas.db')
    c = conn.cursor()
    c.execute('SELECT * FROM caja WHERE id=1')
    if not c.fetchone():  # Solo insertar si no existe el registro
        c.execute('INSERT INTO caja (id, total) VALUES (1, 0)')
    conn.commit()
    conn.close()

# Función para registrar operaciones
def registrar_operacion(fecha, monto, operacion, descripcion):
    
    conn = sqlite3.connect('finanzas.db')
    c = conn.cursor()
    
    # Obtener el total actual de la caja
    c.execute('SELECT total FROM caja WHERE id=1')
    total_caja = c.fetchone()[0]

    # Registrar la operación
    if operacion == "ingreso":
        # Identificar el nombre de la persona desde la descripción
        nombre_persona = descripcion.split("pago de ")[1].strip()
        
        # Actualizar deuda o agregar nueva persona si no existe
        c.execute('SELECT deuda FROM personas WHERE nombre=?', (nombre_persona,))
        deuda_persona = c.fetchone()
        if deuda_persona is not None:
            nueva_deuda = deuda_persona[0] - monto
            c.execute('UPDATE personas SET deuda=? WHERE nombre=?', (nueva_deuda, nombre_persona))
        else:
            c.execute('INSERT INTO personas (nombre, deuda) VALUES (?, ?)', (nombre_persona, -monto))

        # Actualizar el total de la caja sumando el ingreso
        total_caja += monto

    elif operacion == "egreso":
        # Restar el monto de la caja
        total_caja -= monto

    # Registrar la operación con el nuevo total de la caja
    c.execute('INSERT INTO operaciones (fecha, monto, operacion, descripcion, total) VALUES (?, ?, ?, ?, ?)', 
              (fecha, monto, operacion, descripcion, total_caja))
    
    # Actualizar el total de la caja en la tabla de caja
    c.execute('UPDATE caja SET total=? WHERE id=1', (total_caja,))
    
    conn.commit()
    conn.close()

# Función para consultar operaciones
def consultar_operaciones(campo=None, valor=None):
    conn = sqlite3.connect('finanzas.db')
    c = conn.cursor()

    # Verificar si se requiere una búsqueda específica o mostrar todos los registros
    if campo and valor:
        query = f"SELECT * FROM operaciones WHERE {campo} LIKE ?"
        c.execute(query, ('%' + valor + '%',))
    else:
        # Mostrar todas las operaciones si no se especifica ningún campo o valor
        query = "SELECT * FROM operaciones"
        c.execute(query)

    operaciones = c.fetchall()
    conn.close()
    return operaciones

# Inicializar la base de datos y la caja
crear_base_datos()
inicializar_caja()
