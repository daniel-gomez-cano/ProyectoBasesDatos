import tkinter as tk
import psycopg2 # Instalan esta libreria pip install psycopg2-binary
from tkinter import messagebox, ttk

# Función para conectar a la base de datos
def conectar_db():
    try: # Mis estimados, aquí está la duda
        conexion = psycopg2.connect(
            host="localhost",   # Esto es por defecto
            database="eps_db",  # En mi pgAdmin cree una base de datos llamada eps_db
            user="postgres",    # Este es el usuario por defecto
            password="daniel"   # Este es la contraseña que le puse a mi usuario (exposeado)
        )
        print("Conexión exitosa a la base de datos.") # Si imprime esto, es que se conectó
        return conexion
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

# Función para manejar el inicio de sesión
def validar_usuario(usuario, contrasena, rol):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return False
    try:
        cursor = conexion.cursor()
        query = """
            SELECT Usuario, Rol
            FROM Usuario
            WHERE Usuario = %s AND Contrasena = %s AND Rol = %s
        """
        cursor.execute(query, (usuario, contrasena, rol))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado is not None
    except Exception as e:
        messagebox.showerror("Error", f"Error en la consulta: {e}")
        return False

def iniciar_sesion():
    usuario = entrada_usuario.get()
    contrasena = entrada_contrasena.get()
    rol = rol_var.get()
    if not usuario or not contrasena:
        messagebox.showerror("Error", "Por favor, ingrese usuario y contraseña.")
        return

    if validar_usuario(usuario, contrasena, rol):
        messagebox.showinfo("Inicio de sesión", f"Bienvenido {rol}: {usuario}")
        abrir_dashboard(usuario, rol, ventana)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos o cuenta inactiva.")

# Función para abrir el dashboard
def abrir_dashboard(usuario, rol, screen):
    screen.destroy()

    dashboard = tk.Tk()
    dashboard.title("Dashboard")
    dashboard.geometry("800x600")

    # Panel izquierdo
    frame_izquierdo = tk.Frame(dashboard, bg="lightgray", width=200)
    frame_izquierdo.pack(side=tk.LEFT, fill=tk.Y)

    # Información del usuario
    label_usuario = tk.Label(frame_izquierdo, text=f"Usuario: {usuario}", bg="lightgray", anchor="w")
    label_usuario.pack(pady=10, padx=10, anchor="w")

    label_rol = tk.Label(frame_izquierdo, text=f"Rol: {rol}", bg="lightgray", anchor="w")
    label_rol.pack(pady=10, padx=10, anchor="w")

    # Botón de salir
    boton_salir = tk.Button(frame_izquierdo, text="Salir", command=dashboard.destroy)
    boton_salir.pack(side=tk.BOTTOM, pady=20)

    # Área del dashboard
    frame_derecho = tk.Frame(dashboard, bg="white")
    frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    label_bienvenida = tk.Label(frame_derecho, text=f"Bienvenido al panel de {rol}", font=("Arial", 16), bg="white")
    label_bienvenida.pack(pady=20)

    # Botones para funcionalidades principales
    botones = [
        ("Listados", lambda: abrir_listados(dashboard)),
        ("Afiliados", lambda: abrir_afiliado(dashboard)),
        ("Empresas", lambda: abrir_empresas(dashboard)),
        ("Contratos", lambda: abrir_contratos(dashboard)),
        ("Pagos", lambda: mostrar_mensaje("Pagos")),
        ("IPS", lambda: mostrar_mensaje("IPS")),
        ("Órdenes de Servicio", lambda: mostrar_mensaje("Órdenes de Servicio"))
    ]

    for texto, comando in botones:
        boton = tk.Button(frame_derecho, text=texto, width=20, height=2, command=comando)
        boton.pack(pady=5)

    # Información extra para llenar espacio
    label_info_extra = tk.Label(frame_derecho, text="Resumen de la jornada:\n- Afiliados activos: 256\n- Pagos procesados: 120\n- Órdenes pendientes: 34", 
                                font=("Arial", 12), bg="white", justify="left")
    label_info_extra.pack(pady=20)

    dashboard.mainloop()

# Ventana de Listados
def abrir_listados(parent):
    parent.destroy()  # Cierra el dashboard principal
    ventana_listados = tk.Tk()
    ventana_listados.title("Listados")
    ventana_listados.geometry("800x600")

    # Panel izquierdo para selección
    frame_izquierdo = tk.Frame(ventana_listados, bg="lightgray", width=200)
    frame_izquierdo.pack(side=tk.LEFT, fill=tk.Y)

    label_titulo = tk.Label(frame_izquierdo, text="Seleccionar Listado", bg="lightgray", font=("Arial", 12))
    label_titulo.pack(pady=10)

    # Lista de opciones
    opciones_listado = ["Cotizantes", "Beneficiarios", "Empresas", "Contratos", "Aportes", "IPS", "Órdenes de Servicio"]
    listado_var = tk.StringVar(value=opciones_listado[0])

    combo_listados = ttk.Combobox(frame_izquierdo, textvariable=listado_var, values=opciones_listado)
    combo_listados.pack(pady=10)

    # Botón para generar listado
    boton_generar = tk.Button(frame_izquierdo, text="Generar Listado", command=lambda: mostrar_listado(listado_var.get(), frame_derecho))
    boton_generar.pack(pady=10)

    # Botón de regreso al dashboard
    boton_regresar = tk.Button(frame_izquierdo, text="Regresar", command=lambda: abrir_dashboard("Usuario", "Administrador", ventana_listados))
    boton_regresar.pack(side=tk.BOTTOM, pady=20)

    # Área derecha para mostrar resultados
    frame_derecho = tk.Frame(ventana_listados, bg="white")
    frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    label_resultado = tk.Label(frame_derecho, text="Resultado del Listado", font=("Arial", 14), bg="white")
    label_resultado.pack(pady=10)

    ventana_listados.mainloop()

# Función para mostrar el resultado del listado
def mostrar_listado(tipo_listado, frame):
    for widget in frame.winfo_children():
        widget.destroy()  # Limpiar área de resultados

    label_titulo = tk.Label(frame, text=f"Listado de {tipo_listado}", font=("Arial", 14), bg="white")
    label_titulo.pack(pady=10)

    # Configuración de columnas de ejemplo
    columnas = ("#1", "#2", "#3", "4", "5", "6")
    tabla = ttk.Treeview(frame, columns=columnas, show="headings")
    tabla.heading("#1", text="Columna 1")
    tabla.heading("#2", text="Columna 2")
    tabla.heading("#3", text="Columna 3")
    tabla.heading("#4", text="Columna 4")
    tabla.heading("#5", text="Columna 5")
    tabla.heading("#6", text="Columna 6")

    # Consulta dinámica según el tipo de listado
    query_dict = {
        "Cotizantes": "SELECT * FROM Cotizante",
        "Beneficiarios": "SELECT * FROM Beneficiario",
        "Empresas": "SELECT * FROM Empresa",
        "Contratos": "SELECT * FROM Contrato",
        "Aportes": "SELECT * FROM Pago_aportes",
        "IPS": "SELECT * FROM IPS",
        "Órdenes de Servicio": "SELECT * FROM Orden_Servicio",
    }

    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        cursor.execute(query_dict[tipo_listado])
        datos = cursor.fetchall()
        conexion.close()

        # Llenar la tabla con los datos obtenidos
        for fila in datos:
            tabla.insert("", tk.END, values=fila)

        tabla.pack(padx=10, pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar listado: {e}")

# AFILIADOS
def abrir_afiliado(parent):
    parent.destroy()  # Cierra el dashboard principal
    ventana_afiliado = tk.Tk()
    ventana_afiliado.title("Listados")
    ventana_afiliado.geometry("800x600")

    # Panel izquierdo para selección
    frame_izquierdo = tk.Frame(ventana_afiliado, bg="lightgray", width=200)
    frame_izquierdo.pack(side=tk.LEFT, fill=tk.Y)

    # Botón para generar listado
    boton_generar = tk.Button(frame_izquierdo, text="Afiliados Activos", command=lambda: listar_afiliados_activos(frame_derecho))
    boton_generar.pack(pady=10)

    boton_generar = tk.Button(frame_izquierdo, text="Afiliados Inactivos", command=lambda: listar_afiliados_inactivos_retirados(frame_derecho))
    boton_generar.pack(pady=10)

    boton_generar = tk.Button(frame_izquierdo, text="Afiliados Independientes", command=lambda: print("Este botón todavía no se implementará"))
    boton_generar.pack(pady=10)

    boton_generar = tk.Button(frame_izquierdo, text="Cotizantes", command=lambda: abrir_cotizantes(ventana_afiliado))
    boton_generar.pack(pady=10)

    boton_generar = tk.Button(frame_izquierdo, text="Beneficiarios", command=lambda: abrir_beneficiarios(ventana_afiliado))
    boton_generar.pack(pady=10)

    boton_generar = tk.Button(frame_izquierdo, text="Registrar Afiliado", command=lambda: abrir_in_afiliado(ventana_afiliado))
    boton_generar.pack(pady=10)

    # Botón de regreso al dashboard
    boton_regresar = tk.Button(frame_izquierdo, text="Regresar", command=lambda: abrir_dashboard("Usuario", "Administrador", ventana_afiliado))
    boton_regresar.pack(side=tk.BOTTOM, pady=20)

    # Área derecha para mostrar resultados
    frame_derecho = tk.Frame(ventana_afiliado, bg="white")
    frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    label_resultado = tk.Label(frame_derecho, text="Resultado del Listado", font=("Arial", 14), bg="white")
    label_resultado.pack(pady=10)

    ventana_afiliado.mainloop()

def listar_afiliados_activos(frame_derecho):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = "SELECT * FROM Afiliado WHERE Estado_actual = 'Activo'"
        cursor.execute(query)
        resultados = cursor.fetchall()
        conexion.close()

        # Limpiar el frame_derecho antes de mostrar nuevos resultados
        for widget in frame_derecho.winfo_children():
            widget.destroy()

        label_resultado = tk.Label(frame_derecho, text="Afiliados Activos", font=("Arial", 14), bg="white")
        label_resultado.pack(pady=10)

        # Configuración de columnas
        columnas = ("DI", "Tipo", "Fecha_Nac", "Estado", "Nombres", "Apellidos", "Genero", "Correo", "Telefono", "Ciudad", "Direccion", "Estado_actual")
        tabla = ttk.Treeview(frame_derecho, columns=columnas, show="headings")
        tabla.heading("DI", text="DI")
        tabla.heading("Tipo", text="Tipo")
        tabla.heading("Fecha_Nac", text="Fecha_Nac")
        tabla.heading("Estado", text="Estado")
        tabla.heading("Nombres", text="Nombres")
        tabla.heading("Apellidos", text="Apellidos")
        tabla.heading("Genero", text="Genero")
        tabla.heading("Correo", text="Correo")
        tabla.heading("Telefono", text="Telefono")
        tabla.heading("Ciudad", text="Ciudad")
        tabla.heading("Direccion", text="Direccion")
        tabla.heading("Estado_actual", text="Estado_actual")

        # Llenar la tabla con los datos obtenidos
        for fila in resultados:
            tabla.insert("", tk.END, values=fila)

        tabla.pack(padx=10, pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar afiliados activos: {e}")

def listar_afiliados_inactivos_retirados(frame_derecho):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = "SELECT * FROM Afiliado WHERE Estado_actual IN ('Inactivo', 'Retirado')"
        cursor.execute(query)
        resultados = cursor.fetchall()
        conexion.close()

        # Limpiar el frame_derecho antes de mostrar nuevos resultados
        for widget in frame_derecho.winfo_children():
            widget.destroy()

        label_resultado = tk.Label(frame_derecho, text="Afiliados Inactivos y Retirados", font=("Arial", 14), bg="white")
        label_resultado.pack(pady=10)

        # Configuración de columnas
        columnas = ("DI", "Tipo", "Fecha_Nac", "Estado", "Nombres", "Apellidos", "Genero", "Correo", "Telefono", "Ciudad", "Direccion", "Estado_actual")
        tabla = ttk.Treeview(frame_derecho, columns=columnas, show="headings")
        tabla.heading("DI", text="DI")
        tabla.heading("Tipo", text="Tipo")
        tabla.heading("Fecha_Nac", text="Fecha_Nac")
        tabla.heading("Estado", text="Estado")
        tabla.heading("Nombres", text="Nombres")
        tabla.heading("Apellidos", text="Apellidos")
        tabla.heading("Genero", text="Genero")
        tabla.heading("Correo", text="Correo")
        tabla.heading("Telefono", text="Telefono")
        tabla.heading("Ciudad", text="Ciudad")
        tabla.heading("Direccion", text="Direccion")
        tabla.heading("Estado_actual", text="Estado_actual")

        # Llenar la tabla con los datos obtenidos
        for fila in resultados:
            tabla.insert("", tk.END, values=fila)

        tabla.pack(padx=10, pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar afiliados inactivos y retirados: {e}")

def abrir_cotizantes(parent):
    parent.destroy()
    ventana_cotizantes = tk.Tk()
    ventana_cotizantes.title("Gestión de cotizantes")
    ventana_cotizantes.geometry("800x600")

    # Sección de registro
    frame_registro = tk.LabelFrame(ventana_cotizantes, text="Registro de cotizantes", padx=10, pady=10)
    frame_registro.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_registro, text="DI:").pack(pady=2)
    entrada_di = tk.Entry(frame_registro)
    entrada_di.pack(pady=2)

    tk.Label(frame_registro, text="Tipo").pack(pady=2)
    opciones_tipo = ["Dependiente", "Independiente"]
    tipo_var = tk.StringVar(value=opciones_tipo[0])
    combo_tipo = ttk.Combobox(frame_registro, textvariable=tipo_var, values=opciones_tipo)
    combo_tipo.pack(pady=10)

    tk.Label(frame_registro, text="Salario:").pack(pady=2)
    salario = tk.Entry(frame_registro)
    salario.pack(pady=2)

    tk.Label(frame_registro, text="Fecha 1° Afiliación (AAAA-MM-DD):").pack(pady=2)
    fecha = tk.Entry(frame_registro)
    fecha.pack(pady=2)

    tk.Label(frame_registro, text="IPS:").pack(pady=2)
    ips = tk.Entry(frame_registro)
    ips.pack(pady=2)

    boton_registrar = tk.Button(frame_registro, text="Agregar Cotizante", command=lambda: registrar_cotizante(
        entrada_di.get(), combo_tipo.get(), salario.get(), fecha.get(), ips.get()
    ))
    boton_registrar.pack(pady=10)

    # Botón de regreso al dashboard
    boton_regresar = tk.Button(frame_registro, text="Regresar", command=lambda: abrir_afiliado(ventana_cotizantes))
    boton_regresar.pack(side=tk.BOTTOM, pady=20)

    # Sección de actualización
    frame_actualizacion = tk.LabelFrame(ventana_cotizantes, text="Actualizar Cotizante", padx=10, pady=10)
    frame_actualizacion.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(frame_actualizacion, text="DI:").pack(pady=2)
    actualizar_di = tk.Entry(frame_actualizacion)
    actualizar_di.pack(pady=2)

    tk.Label(frame_actualizacion, text="Tipo").pack(pady=2)
    actualizar_opciones_tipo = ["Dependiente", "Independiente"]
    actualizar_tipo_var = tk.StringVar(value=opciones_tipo[0])
    actualizar_combo_tipo = ttk.Combobox(frame_actualizacion, textvariable=actualizar_tipo_var, values=actualizar_opciones_tipo)
    actualizar_combo_tipo.pack(pady=10)

    tk.Label(frame_actualizacion, text="Salario:").pack(pady=2)
    actualizar_salario = tk.Entry(frame_actualizacion)
    actualizar_salario.pack(pady=2)

    tk.Label(frame_actualizacion, text="Fecha 1° Afiliación (AAAA-MM-DD):").pack(pady=2)
    actualizar_fecha = tk.Entry(frame_actualizacion)
    actualizar_fecha.pack(pady=2)

    tk.Label(frame_actualizacion, text="IPS:").pack(pady=2)
    actualizar_ips = tk.Entry(frame_actualizacion)
    actualizar_ips.pack(pady=2)

    boton_actualizar = tk.Button(frame_actualizacion, text="Actualizar Cotizante", command=lambda: actualizar_cotizante(
        actualizar_di.get(), actualizar_combo_tipo.get(), actualizar_salario.get(), actualizar_fecha.get(), actualizar_ips.get()
    ))
    boton_actualizar.pack(pady=10)

    ventana_cotizantes.mainloop()

def registrar_cotizante(di, tipo, salario, fecha_1_afiliacion, ips):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO Cotizante (DI, Tipo, Salario, Fecha_1_afiliacion, IPS)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (di, tipo, salario, fecha_1_afiliacion, ips))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Cotizante registrado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar cotizante: {e}")

def actualizar_cotizante(di, nuevo_tipo=None, nuevo_salario=None, nueva_fecha_1_afiliacion=None, nuevo_ips=None):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = "UPDATE Cotizante SET "
        params = []

        if nuevo_tipo:
            query += "Tipo = %s, "
            params.append(nuevo_tipo)
        if nuevo_salario:
            query += "Salario = %s, "
            params.append(nuevo_salario)
        if nueva_fecha_1_afiliacion:
            query += "Fecha_1_afiliacion = %s, "
            params.append(nueva_fecha_1_afiliacion)
        if nuevo_ips:
            query += "IPS = %s, "
            params.append(nuevo_ips)

        # Eliminar la última coma y espacio
        query = query.rstrip(", ")
        query += " WHERE DI = %s"
        params.append(di)

        cursor.execute(query, params)
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Cotizante actualizado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar cotizante: {e}")

def abrir_in_afiliado(parent):
    parent.destroy()
    ventana_afiliado = tk.Tk()
    ventana_afiliado.title("Crear afiliado")
    ventana_afiliado.geometry("800x600")

    # Sección de registro
    frame_registro = tk.LabelFrame(ventana_afiliado, text="Registro de afiliado", padx=10, pady=10)
    frame_registro.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_registro, text="#DI:").pack(pady=2)
    entrada_di = tk.Entry(frame_registro)
    entrada_di.pack(pady=2)

    tk.Label(frame_registro, text="Tipo de DI").pack(pady=2)
    opciones_tipoid = ["CC", "TI", "CE"]
    tipoid_var = tk.StringVar(value=opciones_tipoid[0])
    tipodi = ttk.Combobox(frame_registro, textvariable=tipoid_var, values=opciones_tipoid)
    tipodi.pack(pady=10)

    tk.Label(frame_registro, text="Fecha nacimiento (AAAA-MM-DD):").pack(pady=2)
    entrada_fechaN = tk.Entry(frame_registro)
    entrada_fechaN.pack(pady=2)

    tk.Label(frame_registro, text="Estado").pack(pady=2)
    entrada_estado = tk.Entry(frame_registro)
    entrada_estado.pack(pady=2)

    tk.Label(frame_registro, text="Nombres").pack(pady=2)
    entrada_nombre = tk.Entry(frame_registro)
    entrada_nombre.pack(pady=2)

    tk.Label(frame_registro, text="Apellidos").pack(pady=2)
    entrada_apellidos = tk.Entry(frame_registro)
    entrada_apellidos.pack(pady=2)

    tk.Label(frame_registro, text="Generos (M/F)").pack(pady=2)
    entrada_genero = tk.Entry(frame_registro)
    entrada_genero.pack(pady=2)

    tk.Label(frame_registro, text="Correo electronico").pack(pady=2)
    entrada_correo = tk.Entry(frame_registro)
    entrada_correo.pack(pady=2)

    tk.Label(frame_registro, text="Telefono").pack(pady=2)
    entrada_telefono = tk.Entry(frame_registro)
    entrada_telefono.pack(pady=2)

    tk.Label(frame_registro, text="Ciudad de residencia").pack(pady=2)
    entrada_ciudad = tk.Entry(frame_registro)
    entrada_ciudad.pack(pady=2)

    tk.Label(frame_registro, text="Dirección").pack(pady=2)
    entrada_direccion = tk.Entry(frame_registro)
    entrada_direccion.pack(pady=2)

    tk.Label(frame_registro, text="Estado actual").pack(pady=2)
    opciones_estado_actual = ["Activo", "Inactivo", "Retirado"]
    estado_actual_var = tk.StringVar(value=opciones_estado_actual[0])
    estadoactual = ttk.Combobox(frame_registro, textvariable=estado_actual_var, values=opciones_estado_actual)
    estadoactual.pack(pady=10)

    boton_registrar = tk.Button(frame_registro, text="Registrar Afiliado", command=lambda: registrar_afiliado(
        entrada_di.get(), tipodi.get(), entrada_fechaN.get(), entrada_estado.get(), entrada_nombre.get(),
        entrada_apellidos.get(), entrada_genero.get(), entrada_correo.get(), entrada_telefono.get(),
        entrada_ciudad.get(), entrada_direccion.get(), estadoactual.get()
    ))
    boton_registrar.pack(pady=10)

    # Sección de actualización
    frame_actualizacion = tk.LabelFrame(ventana_afiliado, text="Actualizar Afiliado", padx=10, pady=10)
    frame_actualizacion.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(frame_actualizacion, text="DI:").pack(pady=2)
    actualizar_di = tk.Entry(frame_actualizacion)
    actualizar_di.pack(pady=2)

    tk.Label(frame_actualizacion, text="Nuevo Tipo de DI").pack(pady=2)
    actualizar_tipodi = ttk.Combobox(frame_actualizacion, textvariable=tipoid_var, values=opciones_tipoid)
    actualizar_tipodi.pack(pady=10)

    tk.Label(frame_actualizacion, text="Nueva Fecha nacimiento (AAAA-MM-DD):").pack(pady=2)
    actualizar_fechaN = tk.Entry(frame_actualizacion)
    actualizar_fechaN.pack(pady=2)

    tk.Label(frame_actualizacion, text="Nuevo Estado").pack(pady=2)
    actualizar_estado = tk.Entry(frame_actualizacion)
    actualizar_estado.pack(pady=2)

    tk.Label(frame_actualizacion, text="Nuevos Nombres").pack(pady=2)
    actualizar_nombre = tk.Entry(frame_actualizacion)
    actualizar_nombre.pack(pady=2)

    tk.Label(frame_actualizacion, text="Nuevos Apellidos").pack(pady=2)
    actualizar_apellidos = tk.Entry(frame_actualizacion)
    actualizar_apellidos.pack(pady=2)

    tk.Label(frame_actualizacion, text="Nuevo Genero (M/F)").pack(pady=2)
    actualizar_genero = tk.Entry(frame_actualizacion)
    actualizar_genero.pack(pady=2)

    tk.Label(frame_actualizacion, text="Nuevo Correo electronico").pack(pady=2)
    actualizar_correo = tk.Entry(frame_actualizacion)
    actualizar_correo.pack(pady=2)

    tk.Label(frame_actualizacion, text="Nuevo Telefono").pack(pady=2)
    actualizar_telefono = tk.Entry(frame_actualizacion)
    actualizar_telefono.pack(pady=2)

    tk.Label(frame_actualizacion, text="Nueva Ciudad de residencia").pack(pady=2)
    actualizar_ciudad = tk.Entry(frame_actualizacion)
    actualizar_ciudad.pack(pady=2)

    tk.Label(frame_actualizacion, text="Nueva Dirección").pack(pady=2)
    actualizar_direccion = tk.Entry(frame_actualizacion)
    actualizar_direccion.pack(pady=2)

    tk.Label(frame_actualizacion, text="Nuevo Estado actual").pack(pady=2)
    actualizar_estado_actual = ttk.Combobox(frame_actualizacion, textvariable=estado_actual_var, values=opciones_estado_actual)
    actualizar_estado_actual.pack(pady=10)

    boton_actualizar = tk.Button(frame_actualizacion, text="Actualizar Afiliado", command=lambda: actualizar_afiliado(
        actualizar_di.get(), actualizar_tipodi.get(), actualizar_fechaN.get(), actualizar_estado.get(),
        actualizar_nombre.get(), actualizar_apellidos.get(), actualizar_genero.get(), actualizar_correo.get(),
        actualizar_telefono.get(), actualizar_ciudad.get(), actualizar_direccion.get(), actualizar_estado_actual.get()
    ))
    boton_actualizar.pack(pady=10)

    # Botón de regreso al dashboard
    boton_regresar = tk.Button(frame_registro, text="Regresar", command=lambda: abrir_afiliado(ventana_afiliado))
    boton_regresar.pack(side=tk.BOTTOM, pady=20)

    ventana_afiliado.mainloop()

def registrar_afiliado(di, tipo, fecha_nac, estado, nombres, apellidos, genero, correo, telefono, ciudad, direccion, estado_actual):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO Afiliado (DI, Tipo, Fecha_Nac, Estado, Nombres, Apellidos, Genero, Correo_electronico, Telefono, Ciudad_residencia, Direccion, Estado_actual)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (di, tipo, fecha_nac, estado, nombres, apellidos, genero, correo, telefono, ciudad, direccion, estado_actual))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Afiliado registrado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar afiliado: {e}")

def actualizar_afiliado(di, nuevo_tipo=None, nueva_fecha_nac=None, nuevo_estado=None, nuevos_nombres=None, nuevos_apellidos=None, nuevo_genero=None, nuevo_correo=None, nuevo_telefono=None, nueva_ciudad=None, nueva_direccion=None, nuevo_estado_actual=None):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = "UPDATE Afiliado SET "
        params = []

        if nuevo_tipo:
            query += "Tipo = %s, "
            params.append(nuevo_tipo)
        if nueva_fecha_nac:
            query += "Fecha_Nac = %s, "
            params.append(nueva_fecha_nac)
        if nuevo_estado:
            query += "Estado = %s, "
            params.append(nuevo_estado)
        if nuevos_nombres:
            query += "Nombres = %s, "
            params.append(nuevos_nombres)
        if nuevos_apellidos:
            query += "Apellidos = %s, "
            params.append(nuevos_apellidos)
        if nuevo_genero:
            query += "Genero = %s, "
            params.append(nuevo_genero)
        if nuevo_correo:
            query += "Correo_electronico = %s, "
            params.append(nuevo_correo)
        if nuevo_telefono:
            query += "Telefono = %s, "
            params.append(nuevo_telefono)
        if nueva_ciudad:
            query += "Ciudad_residencia = %s, "
            params.append(nueva_ciudad)
        if nueva_direccion:
            query += "Direccion = %s, "
            params.append(nueva_direccion)
        if nuevo_estado_actual:
            query += "Estado_actual = %s, "
            params.append(nuevo_estado_actual)

        # Eliminar la última coma y espacio
        query = query.rstrip(", ")
        query += " WHERE DI = %s"
        params.append(di)

        cursor.execute(query, params)
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Afiliado actualizado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar afiliado: {e}")


# Ventana de Beneficiarios
def abrir_beneficiarios(parent):
    parent.destroy()
    ventana_beneficiarios = tk.Tk()
    ventana_beneficiarios.title("Gestión de Beneficiarios")
    ventana_beneficiarios.geometry("800x600")

    # Sección de registro
    frame_registro = tk.LabelFrame(ventana_beneficiarios, text="Registro de Beneficiarios", padx=10, pady=10)
    frame_registro.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_registro, text="DI:").pack(pady=2)
    entrada_di = tk.Entry(frame_registro)
    entrada_di.pack(pady=2)

    tk.Label(frame_registro, text="Parentesco:").pack(pady=2)
    entrada_parentesco = tk.Entry(frame_registro)
    entrada_parentesco.pack(pady=2)

    tk.Label(frame_registro, text="DI Cotizante:").pack(pady=2)
    entrada_di_cotizante = tk.Entry(frame_registro)
    entrada_di_cotizante.pack(pady=2)

    boton_registrar = tk.Button(frame_registro, text="Registrar Beneficiario", 
                            command=lambda: registrar_beneficiario(entrada_di.get(), 
                                                                   entrada_parentesco.get(), 
                                                                   entrada_di_cotizante.get()))
    boton_registrar.pack(pady=10)

    # Sección de actualización
    frame_actualizacion = tk.LabelFrame(ventana_beneficiarios, text="Actualizar Beneficiarios", padx=10, pady=10)
    frame_actualizacion.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(frame_actualizacion, text="DI:").pack(pady=2)
    actualizar_di = tk.Entry(frame_actualizacion)
    actualizar_di.pack(pady=2)

    tk.Label(frame_actualizacion, text="Nuevo Parentesco:").pack(pady=2)
    actualizar_parentesco = tk.Entry(frame_actualizacion)
    actualizar_parentesco.pack(pady=2)

    boton_actualizar = tk.Button(frame_actualizacion, text="Actualizar Beneficiario", 
                             command=lambda: actualizar_beneficiario(actualizar_di.get(), 
                                                                     actualizar_parentesco.get()))
    boton_actualizar.pack(pady=10)

    boton_regresar = tk.Button(frame_registro, text="Regresar", command=lambda: abrir_afiliado(ventana_beneficiarios))
    boton_regresar.pack(side=tk.BOTTOM, pady=20)
    ventana_beneficiarios.mainloop()

def registrar_beneficiario(di, parentesco, di_cotizante):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = "INSERT INTO Beneficiario (DI, Parentesco, DI_cotizante) VALUES (%s, %s, %s)"
        cursor.execute(query, (di, parentesco, di_cotizante))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Beneficiario registrado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar beneficiario: {e}")

def actualizar_beneficiario(di, nuevo_parentesco):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = "UPDATE Beneficiario SET Parentesco = %s WHERE DI = %s"
        cursor.execute(query, (nuevo_parentesco, di))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Beneficiario actualizado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar beneficiario: {e}")

# Ventana de Empresas
def abrir_empresas(parent):
    parent.destroy()
    ventana_empresas = tk.Tk()
    ventana_empresas.title("Gestión de Empresas")
    ventana_empresas.geometry("800x600")

    # Sección de registro
    frame_registro = tk.LabelFrame(ventana_empresas, text="Registro de Empresas", padx=10, pady=10)
    frame_registro.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_registro, text="NIT:").pack(pady=2)
    entrada_nit = tk.Entry(frame_registro)
    entrada_nit.pack(pady=2)

    tk.Label(frame_registro, text="Ciudad:").pack(pady=2)
    entrada_ciudad = tk.Entry(frame_registro)
    entrada_ciudad.pack(pady=2)

    tk.Label(frame_registro, text="Razón Social:").pack(pady=2)
    entrada_razon = tk.Entry(frame_registro)
    entrada_razon.pack(pady=2)

    tk.Label(frame_registro, text="Dirección:").pack(pady=2)
    entrada_direccion = tk.Entry(frame_registro)
    entrada_direccion.pack(pady=2)

    tk.Label(frame_registro, text="Teléfono").pack(pady=2)
    entrada_telefono = tk.Entry(frame_registro)
    entrada_telefono.pack(pady=2)

    tk.Label(frame_registro, text="Contacto").pack(pady=2)
    entrada_contacto = tk.Entry(frame_registro)
    entrada_contacto.pack(pady=2)

    boton_registrar = tk.Button(frame_registro, text="Registrar Empresa", command=lambda: registrar_empresa(
        entrada_nit.get(), entrada_ciudad.get(), entrada_razon.get(), entrada_direccion.get(), entrada_telefono.get(), entrada_contacto.get() ))
    boton_registrar.pack(pady=10)

    # Sección de actualización
    frame_actualizacion = tk.LabelFrame(ventana_empresas, text="Actualizar Empresa", padx=10, pady=10)
    frame_actualizacion.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(frame_actualizacion, text="NIT:").pack(pady=2)
    actualizar_nit = tk.Entry(frame_actualizacion)
    actualizar_nit.pack(pady=2)

    tk.Label(frame_actualizacion, text="Nueva Ciudad").pack(pady=2)
    actualizar_ciudad = tk.Entry(frame_actualizacion)
    actualizar_ciudad.pack(pady=2)

    tk.Label(frame_actualizacion, text="Nueva Razón Social:").pack(pady=2)
    actualizar_razon_social = tk.Entry(frame_actualizacion)
    actualizar_razon_social.pack(pady=2)

    tk.Label(frame_actualizacion, text="Nueva Dirección:").pack(pady=2)
    actualizar_direccion = tk.Entry(frame_actualizacion)
    actualizar_direccion.pack(pady=2)

    tk.Label(frame_actualizacion, text="Nuevo Teléfono:").pack(pady=2)
    actualizar_telefono = tk.Entry(frame_actualizacion)
    actualizar_telefono.pack(pady=2)

    tk.Label(frame_actualizacion, text="Nuevo Contacto:").pack(pady=2)
    actualizar_contacto = tk.Entry(frame_actualizacion)
    actualizar_contacto.pack(pady=2)

    boton_actualizar = tk.Button(frame_actualizacion, text="Actualizar Datos Empresa", command=lambda: actualizar_empresa(
        actualizar_nit.get(), actualizar_ciudad.get(), actualizar_razon_social.get(), actualizar_direccion.get(), 
        actualizar_telefono.get(), actualizar_contacto.get() ))
    boton_actualizar.pack(pady=10)

    boton_regresar = tk.Button(frame_registro, text="Regresar", command=lambda: abrir_dashboard("Usuario", "Administrador", ventana_empresas))
    boton_regresar.pack(side=tk.BOTTOM, pady=20)
    ventana_empresas.mainloop()

def registrar_empresa(nit, ciudad ,razon_social, direccion, telefono, contacto):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = "INSERT INTO Empresa (NIT, Ciudad, Razon_social, Direccion, Telefono, Contacto) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (nit, ciudad, razon_social, direccion, telefono, contacto))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Empresa registrada correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar empresa: {e}")

def actualizar_empresa(nit, nueva_ciudad = None, nueva_razonsocial = None, nueva_direccion = None, nuevo_telefono = None, nuevo_contacto = None):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = "UPDATE Empresa SET "
        params = []

        if nueva_ciudad:
            query += "Ciudad = %s, "
            params.append(nueva_ciudad)
        
        if nueva_razonsocial:
            query += "Razon_social = %s, "
            params.append(nueva_razonsocial)
        
        if nueva_direccion:
            query += "Direccion = %s, "
            params.append(nueva_direccion)
        
        if nuevo_telefono:
            query += "Telefono = %s, "
            params.append(nuevo_telefono)
        
        if nuevo_contacto:
            query += "Contacto = %s"
            params.append(nuevo_contacto)

        query = query.rstrip(", ") + " WHERE NIT = %s"
        params.append(nit)

        cursor.execute(query, params)
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Empresa actualizada correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar empresa: {e}")

def abrir_contratos(parent):
    parent.destroy()
    ventana_contratos = tk.Tk()
    ventana_contratos.title("Gestión de Contratos")
    ventana_contratos.geometry("800x600")

    # Sección de registro
    frame_registro = tk.LabelFrame(ventana_contratos, text="Registro de Contratos", padx=10, pady=10)
    frame_registro.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    # Botón de regreso al dashboard
    boton_regresar = tk.Button(frame_registro, text="Regresar", command=lambda: abrir_dashboard("Usuario", "Administrador",ventana_contratos))
    boton_regresar.pack(side=tk.BOTTOM, pady=20)

    tk.Label(frame_registro, text="#Contrato:").pack(pady=2)
    entrada_nit = tk.Entry(frame_registro)
    entrada_nit.pack(pady=2)

    tk.Label(frame_registro, text="#NRadicado:").pack(pady=2)
    entrada_nit = tk.Entry(frame_registro)
    entrada_nit.pack(pady=2)

    tk.Label(frame_registro, text="Estado:").pack(pady=2)
    opciones_estado = ["Activo", "Retirado"]
    estado_var = tk.StringVar(value=opciones_estado[0])

    combo_estados = ttk.Combobox(frame_registro, textvariable=estado_var, values=opciones_estado)
    combo_estados.pack(pady=10)

    tk.Label(frame_registro, text="Salario_base:").pack(pady=2)
    entrada_razon = tk.Entry(frame_registro)
    entrada_razon.pack(pady=2)

    tk.Label(frame_registro, text="Fecha_retiro (AAAA-MM-DD):").pack(pady=2)
    entrada_direccion = tk.Entry(frame_registro)
    entrada_direccion.pack(pady=2)

    tk.Label(frame_registro, text="Cotizante").pack(pady=2)
    entrada_direccion = tk.Entry(frame_registro)
    entrada_direccion.pack(pady=2)

    tk.Label(frame_registro, text="Aportes").pack(pady=2)
    entrada_direccion = tk.Entry(frame_registro)
    entrada_direccion.pack(pady=2)

    tk.Label(frame_registro, text="Empresa").pack(pady=2)
    entrada_direccion = tk.Entry(frame_registro)
    entrada_direccion.pack(pady=2)

    boton_registrar = tk.Button(frame_registro, text="Registrar Contrato", command=lambda: print("Boton Registro de Contrato"))
    boton_registrar.pack(pady=10)

    # Sección de actualización
    frame_actualizacion = tk.LabelFrame(ventana_contratos, text="Actualizar Contrato", padx=10, pady=10)
    frame_actualizacion.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(frame_actualizacion, text="Estado:").pack(pady=2)
    combo_estados_actu = ttk.Combobox(frame_actualizacion, textvariable=estado_var, values=opciones_estado)
    combo_estados_actu.pack(pady=10)

    label_resultado = tk.Label(frame_actualizacion, text="Buscar estado del cotizante", font=("Arial", 14), bg="white")
    label_resultado.pack(pady=10)

    tk.Label(frame_actualizacion, text="Cotizante:").pack(pady=2)
    actualizar_direccion = tk.Entry(frame_actualizacion)
    actualizar_direccion.pack(pady=2)

    

    boton_actualizar = tk.Button(frame_actualizacion, text="Buscar estado", command=lambda: print("Boton que genera el estado del cotizante"))
    boton_actualizar.pack(pady=10)

    ventana_contratos.mainloop()

# Placeholder para mostrar mensajes al hacer clic en botones
def mostrar_mensaje(seccion):
    messagebox.showinfo("Funcionalidad", f"{seccion}")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Inicio de Sesión")
ventana.geometry("400x300")
ventana.resizable(False, False)

# Etiqueta y entrada para el usuario
label_usuario = tk.Label(ventana, text="Usuario:")
label_usuario.pack(pady=5)
entrada_usuario = tk.Entry(ventana)
entrada_usuario.pack(pady=5)

# Etiqueta y entrada para la contraseña
label_contrasena = tk.Label(ventana, text="Contraseña:")
label_contrasena.pack(pady=5)
entrada_contrasena = tk.Entry(ventana, show="*")
entrada_contrasena.pack(pady=5)

# Selección del rol
label_rol = tk.Label(ventana, text="Seleccione su rol:")
label_rol.pack(pady=5)
rol_var = tk.StringVar()
roles = ["Administrador", "Cotizante", "Banco"]
for rol in roles:
    tk.Radiobutton(ventana, text=rol, variable=rol_var, value=rol).pack(anchor=tk.W)

# Botón para iniciar sesión
boton_iniciar = tk.Button(ventana, text="Iniciar Sesión", command=iniciar_sesion)
boton_iniciar.pack(pady=20)

ventana.mainloop()
