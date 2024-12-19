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

def abrir_registro_usuario():
    ventana_registro = tk.Toplevel(ventana)
    ventana_registro.title("Registrar Usuario")
    ventana_registro.geometry("400x350")
    ventana_registro.resizable(False, False)

    # Etiqueta y entrada para el ID
    label_id = tk.Label(ventana_registro, text="ID:")
    label_id.pack(pady=5)
    entrada_id = tk.Entry(ventana_registro)
    entrada_id.pack(pady=5)

    # Etiqueta y entrada para el usuario
    label_usuario = tk.Label(ventana_registro, text="Usuario:")
    label_usuario.pack(pady=5)
    entrada_usuario = tk.Entry(ventana_registro)
    entrada_usuario.pack(pady=5)

    # Etiqueta y entrada para la contraseña
    label_contrasena = tk.Label(ventana_registro, text="Contraseña:")
    label_contrasena.pack(pady=5)
    entrada_contrasena = tk.Entry(ventana_registro, show="*")
    entrada_contrasena.pack(pady=5)

    # Selección del rol
    label_rol = tk.Label(ventana_registro, text="Seleccione su rol:")
    label_rol.pack(pady=5)
    rol_var = tk.StringVar()
    roles = ["Administrador", "Cotizante", "Banco"]
    for rol in roles:
        tk.Radiobutton(ventana_registro, text=rol, variable=rol_var, value=rol).pack(anchor=tk.W)

    # Botón para registrar usuario
    boton_registrar = tk.Button(ventana_registro, text="Registrar Usuario", command=lambda: registrar_usuario(
        entrada_id.get(), entrada_usuario.get(), entrada_contrasena.get(), rol_var.get()
    ))
    boton_registrar.pack(pady=20)

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
    
def mostrar_informacion_cotizante(usuario):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = """
            select afiliado.*, cotizante.tipo, cotizante.salario, cotizante.fecha_1_afiliacion, cotizante.ips
            from cotizante inner join afiliado on cotizante.di = afiliado.di
            where afiliado.nombres = %s
        """
        cursor.execute(query, (usuario,))
        resultado = cursor.fetchone()
        conexion.close()

        if resultado:
            ventana_cotizante = tk.Tk()
            ventana_cotizante.title("Información del Cotizante")
            ventana_cotizante.geometry("550x500")

            frame_info = tk.LabelFrame(ventana_cotizante, text="Información del Cotizante", padx=10, pady=10)
            frame_info.pack(padx=10, pady=10)

            tk.Label(frame_info, text=f"DI: {resultado[0]}").pack(pady=2)
            tk.Label(frame_info, text=f"Tipo: {resultado[1]}").pack(pady=2)
            tk.Label(frame_info, text=f"Fecha Nacimiento: {resultado[2]}").pack(pady=2)
            tk.Label(frame_info, text=f"Estado: {resultado[3]}").pack(pady=2)
            tk.Label(frame_info, text=f"Nombres: {resultado[4]}").pack(pady=2)
            tk.Label(frame_info, text=f"Apellidos: {resultado[5]}").pack(pady=2)
            tk.Label(frame_info, text=f"Género: {resultado[6]}").pack(pady=2)
            tk.Label(frame_info, text=f"Email: {resultado[7]}").pack(pady=2)
            tk.Label(frame_info, text=f"Teléfono: {resultado[8]}").pack(pady=2)
            tk.Label(frame_info, text=f"Ciudad Residencia: {resultado[9]}").pack(pady=2)
            tk.Label(frame_info, text=f"Dirección: {resultado[10]}").pack(pady=2)
            tk.Label(frame_info, text=f"Estado Actual: {resultado[11]}").pack(pady=2)
            tk.Label(frame_info, text=f"Tipo Cotizante: {resultado[12]}").pack(pady=2)
            tk.Label(frame_info, text=f"Salario: {resultado[13]}").pack(pady=2)
            tk.Label(frame_info, text=f"Fecha 1er Afiliación: {resultado[14]}").pack(pady=2)
            tk.Label(frame_info, text=f"IPS: {resultado[15]}").pack(pady=2)

            ventana_cotizante.mainloop()
        else:
            messagebox.showerror("Error", "No se encontró información para este cotizante.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener la información del cotizante: {e}")

# BANCO
def abrir_banco(parent):
    parent.destroy()  # Cierra la ventana anterior
    ventana_pagos = tk.Tk()
    ventana_pagos.title("Gestión de Pagos de BANCO")
    ventana_pagos.geometry("800x600")

    # Sección de registro
    frame_registro = tk.LabelFrame(ventana_pagos, text="Registro de Pagos", padx=10, pady=10)
    frame_registro.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_registro, text="Número Pago:").pack(pady=2)
    entrada_n_pago = tk.Entry(frame_registro)
    entrada_n_pago.pack(pady=2)

    tk.Label(frame_registro, text="Valor:").pack(pady=2)
    entrada_valor = tk.Entry(frame_registro)
    entrada_valor.pack(pady=2)

    tk.Label(frame_registro, text="Fecha (AAAA-MM-DD):").pack(pady=2)
    entrada_fecha = tk.Entry(frame_registro)
    entrada_fecha.pack(pady=2)

    boton_registrar = tk.Button(frame_registro, text="Agregar Pago", command=lambda: registrar_pago(
        entrada_n_pago.get(), entrada_valor.get(), entrada_fecha.get()
    ))
    boton_registrar.pack(pady=10)

    # Botón de regreso al dashboard
    boton_regresar = tk.Button(frame_registro, text="Regresar", command=lambda: ventana_pagos.destroy())
    boton_regresar.pack(side=tk.BOTTOM, pady=20)

    # Sección de actualización
    frame_actualizacion = tk.LabelFrame(ventana_pagos, text="Actualización de Pagos", padx=10, pady=10)
    frame_actualizacion.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_actualizacion, text="Número Pago:").pack(pady=2)
    entrada_actu_n_pago = tk.Entry(frame_actualizacion)
    entrada_actu_n_pago.pack(pady=2)

    tk.Label(frame_actualizacion, text="Valor:").pack(pady=2)
    entrada_actu_valor = tk.Entry(frame_actualizacion)
    entrada_actu_valor.pack(pady=2)

    tk.Label(frame_actualizacion, text="Fecha (AAAA-MM-DD):").pack(pady=2)
    entrada_actu_fecha = tk.Entry(frame_actualizacion)
    entrada_actu_fecha.pack(pady=2)

    boton_actualizar = tk.Button(frame_actualizacion, text="Actualizar Pago", command=lambda: actualizar_pago(
        entrada_actu_n_pago.get(), entrada_actu_valor.get(), entrada_actu_fecha.get()
    ))
    boton_actualizar.pack(pady=10)

    ventana_pagos.mainloop()


def iniciar_sesion():
    usuario = entrada_usuario.get()
    contrasena = entrada_contrasena.get()
    rol = rol_var.get()
    if not usuario or not contrasena:
        messagebox.showerror("Error", "Por favor, ingrese usuario y contraseña.")
        return

    if validar_usuario(usuario, contrasena, rol):
        messagebox.showinfo("Inicio de sesión", f"Bienvenido {rol}: {usuario}")
        if rol == "Cotizante":
            mostrar_informacion_cotizante(usuario)
        elif rol == "Banco":
            abrir_banco(ventana)
        else:
            abrir_dashboard(usuario, rol, ventana)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos o cuenta inactiva.")

def registrar_usuario(id, usuario, contrasena, rol):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO Usuario (ID, Usuario, Contrasena, Rol)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (id, usuario, contrasena, rol))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar usuario: {e}")

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
        ("Pagos", lambda: abrir_pagos(dashboard)),
        ("IPS", lambda: abrir_ips(dashboard)),
        ("Órdenes de Servicio", lambda: abrir_ordenes_servicio(dashboard))
    ]

    for texto, comando in botones:
        boton = tk.Button(frame_derecho, text=texto, width=20, height=2, command=comando)
        boton.pack(pady=5)

    dashboard.mainloop()

# Ventana de Listados
def abrir_listados(parent):
    parent.destroy()  # Cierra el dashboard principal
    ventana_listados = tk.Tk()
    ventana_listados.title("Listados")
    ventana_listados.geometry("1200x600")

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
    tabla.heading("#1", text="PK")
    tabla.heading("#2", text="Columna 2")
    tabla.heading("#3", text="Columna 3")
    tabla.heading("#4", text="Columna 4")
    tabla.heading("#5", text="Columna 5")
    tabla.heading("#6", text="Columna 6")

    # Consulta dinámica según el tipo de listado
    query_dict = {
        "Cotizantes": """SELECT Cotizante.di, nombres, apellidos, cotizante.salario, rango_salarial, ips
                            FROM Cotizante INNER JOIN AFILIADO ON AFILIADO.DI = COTIZANTE.DI
                            INNER JOIN SUELDO ON SUELDO.SALARIO = COTIZANTE.SALARIO""",
        "Beneficiarios": """SELECT Beneficiario.di, nombres, apellidos, ciudad_residencia, telefono, estado_actual 
                            FROM Beneficiario INNER JOIN AFILIADO ON AFILIADO.DI = BENEFICIARIO.DI""",
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
    tk.Label(frame_izquierdo, text="NIT:").pack(pady=2)
    entrada_nit = tk.Entry(frame_izquierdo)
    entrada_nit.pack(pady=2)

    # Botón para generar listado
    boton_generar = tk.Button(frame_izquierdo, text="Afiliados Activos", command=lambda: listar_afiliados_activos(frame_derecho, entrada_nit.get()))
    boton_generar.pack(pady=10)

    boton_generar = tk.Button(frame_izquierdo, text="Afiliados Inactivos", command=lambda: listar_afiliados_inactivos_retirados(frame_derecho))
    boton_generar.pack(pady=10)

    boton_generar = tk.Button(frame_izquierdo, text="Afiliados Independientes", command=lambda: listar_cotizantes_independientes(frame_derecho))
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

def listar_afiliados_activos(frame_derecho, nit):
    nit_string = str(nit)
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = """select afiliado.*
                    from afiliado inner join cotizante on afiliado.di = cotizante.di 
                    inner join IPS on ips.nit = cotizante.ips
                    where nit = %s and estado = 'Activo'"""
        cursor.execute(query, (nit_string,))
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

def listar_cotizantes_independientes(frame_derecho):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = """SELECT afiliado.*
                    FROM Cotizante INNER JOIN AFILIADO ON COTIZANTE.DI = AFILIADO.DI
                    WHERE Cotizante.Tipo = 'Independiente' 
                    ORDER BY estado_actual"""
        cursor.execute(query)
        resultados = cursor.fetchall()
        conexion.close()

        # Limpiar el frame_derecho antes de mostrar nuevos resultados
        for widget in frame_derecho.winfo_children():
            widget.destroy()

        label_resultado = tk.Label(frame_derecho, text="Cotizantes Independientes", font=("Arial", 14), bg="white")
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
        messagebox.showerror("Error", f"Error al listar cotizantes independientes: {e}")

def abrir_cotizantes(parent):
    parent.destroy()
    ventana_cotizantes = tk.Tk()
    ventana_cotizantes.title("Gestión de Cotizantes")
    ventana_cotizantes.geometry("800x600")

    # Sección de registro
    frame_registro = tk.LabelFrame(ventana_cotizantes, text="Registro de Cotizantes", padx=10, pady=10)
    frame_registro.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_registro, text="DI:").pack(pady=2)
    entrada_di = tk.Entry(frame_registro)
    entrada_di.pack(pady=2)

    tk.Label(frame_registro, text="Tipo:").pack(pady=2)
    opciones_tipo = ["Dependiente", "Independiente"]
    tipo_var = tk.StringVar(value=opciones_tipo[0])
    combo_tipo = ttk.Combobox(frame_registro, textvariable=tipo_var, values=opciones_tipo)
    combo_tipo.pack(pady=10)

    tk.Label(frame_registro, text="Salario:").pack(pady=2)
    entrada_salario = tk.Entry(frame_registro)
    entrada_salario.pack(pady=2)

    tk.Label(frame_registro, text="Fecha 1° Afiliación (AAAA-MM-DD):").pack(pady=2)
    entrada_fecha = tk.Entry(frame_registro)
    entrada_fecha.pack(pady=2)

    tk.Label(frame_registro, text="IPS:").pack(pady=2)
    ips = tk.Entry(frame_registro)
    ips.pack(pady=2)

    boton_registrar = tk.Button(frame_registro, text="Agregar Cotizante", command=lambda: registrar_cotizante(
        entrada_di.get(), combo_tipo.get(), entrada_salario.get(), entrada_fecha.get(), ips.get()
    ))
    boton_registrar.pack(pady=10)

    # Botón de regreso al dashboard
    boton_regresar = tk.Button(frame_registro, text="Regresar", command=lambda: abrir_dashboard("Usuario", "Administrador", ventana_cotizantes))
    boton_regresar.pack(side=tk.BOTTOM, pady=20)

    # Sección de actualización
    frame_actualizacion = tk.LabelFrame(ventana_cotizantes, text="Actualizar Cotizante", padx=10, pady=10)
    frame_actualizacion.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(frame_actualizacion, text="DI:").pack(pady=2)
    actualizar_di = tk.Entry(frame_actualizacion)
    actualizar_di.pack(pady=2)

    tk.Label(frame_actualizacion, text="Tipo:").pack(pady=2)
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

        # Calcular y registrar el rango salarial
        rango_salarial = calcular_rango_salarial(salario)
        registrar_sueldo(salario, rango_salarial)

        conexion.close()
        messagebox.showinfo("Éxito", "Cotizante registrado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar cotizante: {e}")

def calcular_rango_salarial(salario):
    salario_minimo = 1300000
    salario = float(salario)  # Convertir el salario a un valor numérico
    if salario < 2 * salario_minimo:
        return 'A'
    elif 2 * salario_minimo <= salario <= 5 * salario_minimo:
        return 'B'
    else:
        return 'C'

def registrar_sueldo(salario, rango_salarial):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO Sueldo (Salario, Rango_salarial)
            VALUES (%s, %s)
        """
        cursor.execute(query, (salario, rango_salarial))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Sueldo registrado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar sueldo: {e}")

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

        # Si se actualiza el salario, también se debe actualizar el rango salarial
        if nuevo_salario:
            rango_salarial = calcular_rango_salarial(nuevo_salario)
            registrar_sueldo(nuevo_salario, rango_salarial)

        conexion.close()
        messagebox.showinfo("Éxito", "Cotizante actualizado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar cotizante: {e}")

def abrir_in_afiliado(parent):
    parent.destroy()
    ventana_afiliado = tk.Tk()
    ventana_afiliado.title("Crear afiliado")
    ventana_afiliado.geometry("800x720")

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
    # Sección de registro
    frame_actualizacion = tk.LabelFrame(ventana_afiliado, text="Registro de afiliado", padx=10, pady=10)
    frame_actualizacion.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

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
    boton_regresar = tk.Button(ventana_afiliado, text="Regresar", command=lambda: abrir_afiliado(ventana_afiliado))
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

    tk.Label(frame_registro, text="NIT/RUT:").pack(pady=2)
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

    boton_registrar_afiliado = tk.Button(frame_registro, text="Registrar Cotizante Independiente", command=lambda: registrar_empresa(
        entrada_nit.get(), entrada_ciudad.get(), entrada_razon.get(), entrada_direccion.get(), entrada_telefono.get(), entrada_contacto.get() ))
    boton_registrar_afiliado.pack(pady=10)

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
        messagebox.showinfo("Éxito", "Empresa/Independite registrado correctamente.")
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

# CONTRATOS
def abrir_contratos(parent):
    parent.destroy()
    ventana_contratos = tk.Tk()
    ventana_contratos.title("Gestión de Contratos")
    ventana_contratos.geometry("800x650")

    # Sección de registro
    frame_registro = tk.LabelFrame(ventana_contratos, text="Registro de Contratos", padx=10, pady=10)
    frame_registro.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    # Botón de regreso al dashboard
    boton_regresar = tk.Button(frame_registro, text="Regresar", command=lambda: abrir_dashboard("Usuario", "Administrador", ventana_contratos))
    boton_regresar.pack(side=tk.BOTTOM, pady=20)

    tk.Label(frame_registro, text="#Contrato:").pack(pady=2)
    entrada_n_contrato = tk.Entry(frame_registro)
    entrada_n_contrato.pack(pady=2)

    tk.Label(frame_registro, text="#NRadicado:").pack(pady=2)
    entrada_n_radicado = tk.Entry(frame_registro)
    entrada_n_radicado.pack(pady=2)

    tk.Label(frame_registro, text="Estado:").pack(pady=2)
    opciones_estado = ["Activo", "Retirado"]
    estado_var = tk.StringVar(value=opciones_estado[0])
    combo_estados = ttk.Combobox(frame_registro, textvariable=estado_var, values=opciones_estado)
    combo_estados.pack(pady=10)

    tk.Label(frame_registro, text="Salario_base:").pack(pady=2)
    entrada_salario_base = tk.Entry(frame_registro)
    entrada_salario_base.pack(pady=2)

    tk.Label(frame_registro, text="Fecha_recibo (AAAA-MM-DD):").pack(pady=2)
    entrada_fecha_recibo = tk.Entry(frame_registro)
    entrada_fecha_recibo.pack(pady=2)

    tk.Label(frame_registro, text="Fecha_retiro (AAAA-MM-DD):").pack(pady=2)
    entrada_fecha_retiro = tk.Entry(frame_registro)
    entrada_fecha_retiro.pack(pady=2)

    tk.Label(frame_registro, text="Cotizante:").pack(pady=2)
    entrada_cotizante = tk.Entry(frame_registro)
    entrada_cotizante.pack(pady=2)

    tk.Label(frame_registro, text="Aportes:").pack(pady=2)
    entrada_aportes = tk.Entry(frame_registro)
    entrada_aportes.pack(pady=2)

    tk.Label(frame_registro, text="Empresa:").pack(pady=2)
    entrada_empresa = tk.Entry(frame_registro)
    entrada_empresa.pack(pady=2)

    boton_registrar = tk.Button(frame_registro, text="Registrar Contrato", command=lambda: registrar_contrato(
        entrada_n_contrato.get(), entrada_n_radicado.get(), combo_estados.get(), entrada_salario_base.get(),
        entrada_fecha_recibo.get(), entrada_fecha_retiro.get(), entrada_cotizante.get(), entrada_aportes.get(), entrada_empresa.get()
    ))
    boton_registrar.pack(pady=10)

    # Sección de actualización
    frame_actualizacion = tk.LabelFrame(ventana_contratos, text="Actualizar Contrato", padx=10, pady=10)
    frame_actualizacion.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(frame_actualizacion, text="#Contrato:").pack(pady=2)
    actualizar_n_contrato = tk.Entry(frame_actualizacion)
    actualizar_n_contrato.pack(pady=2)

    tk.Label(frame_actualizacion, text="#NRadicado:").pack(pady=2)
    actualizar_n_radicado = tk.Entry(frame_actualizacion)
    actualizar_n_radicado.pack(pady=2)

    tk.Label(frame_actualizacion, text="Estado:").pack(pady=2)
    actualizar_estado_var = tk.StringVar(value=opciones_estado[0])
    actualizar_combo_estados = ttk.Combobox(frame_actualizacion, textvariable=actualizar_estado_var, values=opciones_estado)
    actualizar_combo_estados.pack(pady=10)

    tk.Label(frame_actualizacion, text="Salario_base:").pack(pady=2)
    actualizar_salario_base = tk.Entry(frame_actualizacion)
    actualizar_salario_base.pack(pady=2)

    tk.Label(frame_actualizacion, text="Fecha_recibo (AAAA-MM-DD):").pack(pady=2)
    actualizar_fecha_recibo = tk.Entry(frame_actualizacion)
    actualizar_fecha_recibo.pack(pady=2)

    tk.Label(frame_actualizacion, text="Fecha_retiro (AAAA-MM-DD):").pack(pady=2)
    actualizar_fecha_retiro = tk.Entry(frame_actualizacion)
    actualizar_fecha_retiro.pack(pady=2)

    tk.Label(frame_actualizacion, text="Cotizante:").pack(pady=2)
    actualizar_cotizante = tk.Entry(frame_actualizacion)
    actualizar_cotizante.pack(pady=2)

    tk.Label(frame_actualizacion, text="Aportes:").pack(pady=2)
    actualizar_aportes = tk.Entry(frame_actualizacion)
    actualizar_aportes.pack(pady=2)

    tk.Label(frame_actualizacion, text="Empresa:").pack(pady=2)
    actualizar_empresa = tk.Entry(frame_actualizacion)
    actualizar_empresa.pack(pady=2)

    boton_actualizar = tk.Button(frame_actualizacion, text="Actualizar Contrato", command=lambda: actualizar_contrato(
        actualizar_n_contrato.get(), actualizar_n_radicado.get(), actualizar_combo_estados.get(), actualizar_salario_base.get(),
        actualizar_fecha_recibo.get(), actualizar_fecha_retiro.get(), actualizar_cotizante.get(), actualizar_aportes.get(), actualizar_empresa.get()
    ))
    boton_actualizar.pack(pady=10)

    # Sección de búsqueda
    frame_busqueda = tk.LabelFrame(ventana_contratos, text="Buscar estado de trabajador", padx=10, pady=10)
    frame_busqueda.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_busqueda, text="Número contrato:").pack(pady=2)
    num_contrato_actu = tk.Entry(frame_busqueda)
    num_contrato_actu.pack(pady=2)

    boton_buscar = tk.Button(frame_busqueda, text="Buscar estado", command=lambda: buscar_estado_cotizante(
        num_contrato_actu.get(), label_resultado_busqueda
    ))
    boton_buscar.pack(pady=10)

    label_resultado_busqueda = tk.Label(frame_busqueda, text="Estado cotizante", font=("Arial", 14), bg="white")
    label_resultado_busqueda.pack(pady=10)

    ventana_contratos.mainloop()

def buscar_estado_cotizante(n_contrato, label_resultado_busqueda):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = """
            SELECT DISTINCT Tipo
            FROM Cotizante
            INNER JOIN Contrato ON Cotizante.DI = Contrato.Cotizante
            WHERE NContrato = %s
        """
        cursor.execute(query, (n_contrato,))
        resultado = cursor.fetchone()
        conexion.close()

        if resultado:
            label_resultado_busqueda.config(text=f"Tipo de Cotizante: {resultado[0]}")
        else:
            label_resultado_busqueda.config(text="No se encontró información para este contrato.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al buscar estado del cotizante: {e}")

def registrar_contrato(n_contrato, n_radicado, estado, salario_base, fecha_recibo, fecha_retiro, cotizante, aportes, empresa):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO Contrato (NContrato, NRadicado, Estado, Salario_base, Fecha_recibo, Fecha_retiro, Cotizante, Aportes, Empresa)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (n_contrato, n_radicado, estado, salario_base, fecha_recibo, fecha_retiro, cotizante, aportes, empresa))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Contrato registrado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar contrato: {e}")

def actualizar_contrato(n_contrato, nuevo_n_radicado=None, nuevo_estado=None, nuevo_salario_base=None, nueva_fecha_recibo=None, nueva_fecha_retiro=None, nuevo_cotizante=None, nuevo_aportes=None, nueva_empresa=None):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = "UPDATE Contrato SET "
        params = []

        if nuevo_n_radicado:
            query += "NRadicado = %s, "
            params.append(nuevo_n_radicado)
        if nuevo_estado:
            query += "Estado = %s, "
            params.append(nuevo_estado)
        if nuevo_salario_base:
            query += "Salario_base = %s, "
            params.append(nuevo_salario_base)
        if nueva_fecha_recibo:
            query += "Fecha_recibo = %s, "
            params.append(nueva_fecha_recibo)
        if nueva_fecha_retiro:
            query += "Fecha_retiro = %s, "
            params.append(nueva_fecha_retiro)
        if nuevo_cotizante:
            query += "Cotizante = %s, "
            params.append(nuevo_cotizante)
        if nuevo_aportes:
            query += "Aportes = %s, "
            params.append(nuevo_aportes)
        if nueva_empresa:
            query += "Empresa = %s, "
            params.append(nueva_empresa)

        # Eliminar la última coma y espacio
        query = query.rstrip(", ")
        query += " WHERE NContrato = %s"
        params.append(n_contrato)

        cursor.execute(query, params)
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Contrato actualizado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar contrato: {e}")

# PAGOS
def abrir_pagos(parent):
    parent.destroy()  # Cierra la ventana anterior
    ventana_pagos = tk.Tk()
    ventana_pagos.title("Gestión de Pagos")
    ventana_pagos.geometry("800x600")

    # Sección de registro
    frame_registro = tk.LabelFrame(ventana_pagos, text="Registro de Pagos", padx=10, pady=10)
    frame_registro.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_registro, text="Número Pago:").pack(pady=2)
    entrada_n_pago = tk.Entry(frame_registro)
    entrada_n_pago.pack(pady=2)

    tk.Label(frame_registro, text="Valor:").pack(pady=2)
    entrada_valor = tk.Entry(frame_registro)
    entrada_valor.pack(pady=2)

    tk.Label(frame_registro, text="Fecha (AAAA-MM-DD):").pack(pady=2)
    entrada_fecha = tk.Entry(frame_registro)
    entrada_fecha.pack(pady=2)

    boton_registrar = tk.Button(frame_registro, text="Agregar Pago", command=lambda: registrar_pago(
        entrada_n_pago.get(), entrada_valor.get(), entrada_fecha.get()
    ))
    boton_registrar.pack(pady=10)

    # Botón de regreso al dashboard
    boton_regresar = tk.Button(frame_registro, text="Regresar", command=lambda: abrir_dashboard("Usuario", "Administrador", ventana_pagos))
    boton_regresar.pack(side=tk.BOTTOM, pady=20)

    # Sección de actualización
    frame_actualizacion = tk.LabelFrame(ventana_pagos, text="Actualización de Pagos", padx=10, pady=10)
    frame_actualizacion.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_actualizacion, text="Número Pago:").pack(pady=2)
    entrada_actu_n_pago = tk.Entry(frame_actualizacion)
    entrada_actu_n_pago.pack(pady=2)

    tk.Label(frame_actualizacion, text="Valor:").pack(pady=2)
    entrada_actu_valor = tk.Entry(frame_actualizacion)
    entrada_actu_valor.pack(pady=2)

    tk.Label(frame_actualizacion, text="Fecha (AAAA-MM-DD):").pack(pady=2)
    entrada_actu_fecha = tk.Entry(frame_actualizacion)
    entrada_actu_fecha.pack(pady=2)

    boton_actualizar = tk.Button(frame_actualizacion, text="Actualizar Pago", command=lambda: actualizar_pago(
        entrada_actu_n_pago.get(), entrada_actu_valor.get(), entrada_actu_fecha.get()
    ))
    boton_actualizar.pack(pady=10)

    #busqueda
    frame_busqueda = tk.LabelFrame(ventana_pagos, text="BUSCAR APORTES", padx=150, pady=10)
    frame_busqueda.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_busqueda, text="DI AFILIADO:").pack(pady=2)
    nitbusqueda = tk.Entry(frame_busqueda)
    nitbusqueda.pack(pady=2)

    tk.Label(frame_busqueda, text="Fecha 1 (AAAA-MM-DD):").pack(pady=2)
    fechabusqueda1 = tk.Entry(frame_busqueda)
    fechabusqueda1.pack(pady=2)

    tk.Label(frame_busqueda, text="Fecha 2 (AAAA-MM-DD):").pack(pady=2)
    fechabusqueda2 = tk.Entry(frame_busqueda)
    fechabusqueda2.pack(pady=2)

    boton_buscar = tk.Button(frame_busqueda, text="Buscar Pago", command=lambda: mostrar_pago(
    frame_busqueda, nitbusqueda.get(), fechabusqueda1.get(), fechabusqueda2.get())) 
    boton_buscar.pack(pady=20)

    ventana_pagos.mainloop()

def mostrar_pago(frame_derecho, di, fecha1, fecha2):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = """select pago_aportes.*
                    from pago_aportes inner join contrato on contrato.aportes = npago
                    where contrato.cotizante = %s and (fecha_pago between %s and %s)"""
        cursor.execute(query,(di, fecha1, fecha2))
        datos = cursor.fetchall()
        conexion.close()

        label_resultado = tk.Label(frame_derecho, text="Pagos", font=("Arial", 14), bg="white")
        label_resultado.pack(pady=10)

        # Configuración de columnas
        columnas = ("num_pago", "valor_pagado", "fecha_pago")
        tabla = ttk.Treeview(frame_derecho, columns=columnas, show="headings")
        tabla.heading("num_pago", text="num_pago")
        tabla.heading("valor_pagado", text="valor_pagado")
        tabla.heading("fecha_pago", text="fecha_pago")

        # Llenar la tabla con los datos obtenidos
        for fila in datos:
            tabla.insert("", tk.END, values=fila)

        tabla.pack(padx=10, pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar citas: {e}")

def registrar_pago(n_pago, valor_pagado, fecha_pago):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO Pago_aportes (NPago, Valor_pagado, Fecha_pago)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (n_pago, valor_pagado, fecha_pago))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Pago registrado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar pago: {e}")

def actualizar_pago(n_pago, nuevo_valor_pagado=None, nueva_fecha_pago=None):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = "UPDATE Pago_aportes SET "
        params = []

        if nuevo_valor_pagado:
            query += "Valor_pagado = %s, "
            params.append(nuevo_valor_pagado)
        if nueva_fecha_pago:
            query += "Fecha_pago = %s, "
            params.append(nueva_fecha_pago)

        # Eliminar la última coma y espacio
        query = query.rstrip(", ")
        query += " WHERE NPago = %s"
        params.append(n_pago)

        cursor.execute(query, params)
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Pago actualizado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar pago: {e}")

def abrir_ordenes_servicio(parent):
    parent.destroy()  # Cierra la ventana anterior
    ventana_ordenes = tk.Tk()
    ventana_ordenes.title("Gestión de Órdenes de Servicio")
    ventana_ordenes.geometry("800x600")

    # Sección de registro
    frame_registro = tk.LabelFrame(ventana_ordenes, text="Registro de Órdenes de Servicio", padx=10, pady=10)
    frame_registro.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_registro, text="Código:").pack(pady=2)
    entrada_codigo = tk.Entry(frame_registro)
    entrada_codigo.pack(pady=2)

    tk.Label(frame_registro, text="Fecha (AAAA-MM-DD):").pack(pady=2)
    entrada_fecha = tk.Entry(frame_registro)
    entrada_fecha.pack(pady=2)

    tk.Label(frame_registro, text="Nombre médico:").pack(pady=2)
    entrada_medico = tk.Entry(frame_registro)
    entrada_medico.pack(pady=2)

    tk.Label(frame_registro, text="Diagnóstico:").pack(pady=2)
    entrada_diagnostico = tk.Entry(frame_registro)
    entrada_diagnostico.pack(pady=2)

    tk.Label(frame_registro, text="IPS:").pack(pady=2)
    entrada_ips = tk.Entry(frame_registro)
    entrada_ips.pack(pady=2)

    boton_registrar = tk.Button(frame_registro, text="Agregar Orden de Servicio", command=lambda: registrar_orden_servicio(
        entrada_codigo.get(), entrada_fecha.get(), entrada_medico.get(), entrada_diagnostico.get(), entrada_ips.get()
    ))
    boton_registrar.pack(pady=10)

    # Botón de regreso al dashboard
    boton_regresar = tk.Button(frame_registro, text="Regresar", command=lambda: abrir_dashboard("Usuario", "Administrador", ventana_ordenes))
    boton_regresar.pack(side=tk.BOTTOM, pady=20)

    # Sección de actualización
    frame_actualizacion = tk.LabelFrame(ventana_ordenes, text="Actualización de Órdenes de Servicio", padx=10, pady=10)
    frame_actualizacion.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_actualizacion, text="Código:").pack(pady=2)
    entrada_actu_codigo = tk.Entry(frame_actualizacion)
    entrada_actu_codigo.pack(pady=2)

    tk.Label(frame_actualizacion, text="Fecha (AAAA-MM-DD):").pack(pady=2)
    entrada_actu_fecha = tk.Entry(frame_actualizacion)
    entrada_actu_fecha.pack(pady=2)

    tk.Label(frame_actualizacion, text="Nombre médico:").pack(pady=2)
    entrada_actu_medico = tk.Entry(frame_actualizacion)
    entrada_actu_medico.pack(pady=2)

    tk.Label(frame_actualizacion, text="Diagnóstico:").pack(pady=2)
    entrada_actu_diagnostico = tk.Entry(frame_actualizacion)
    entrada_actu_diagnostico.pack(pady=2)

    tk.Label(frame_actualizacion, text="IPS:").pack(pady=2)
    entrada_ips_actu = tk.Entry(frame_actualizacion)
    entrada_ips_actu.pack(pady=2)

    boton_actualizar = tk.Button(frame_actualizacion, text="Actualizar Orden de Servicio", command=lambda: actualizar_orden_servicio(
        entrada_actu_codigo.get(), entrada_actu_fecha.get(), entrada_actu_medico.get(), entrada_actu_diagnostico.get(), entrada_ips_actu.get()
    ))
    boton_actualizar.pack(pady=10)

    ventana_ordenes.mainloop()

def registrar_orden_servicio(codigo, fecha, nombre_medico, diagnostico, ips):
    ips_string = str(ips)
    codigo_int = int(codigo)
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO Orden_Servicio (Codigo, Fecha, Nombre_medico, Diagnostico, ips)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (codigo_int, fecha, nombre_medico, diagnostico, ips_string))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Orden de servicio registrada correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar orden de servicio: {e}")

def actualizar_orden_servicio(codigo, nueva_fecha=None, nuevo_nombre_medico=None, nuevo_diagnostico=None, ips=None):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = "UPDATE Orden_Servicio SET "
        params = []

        if nueva_fecha:
            query += "Fecha = %s, "
            params.append(nueva_fecha)
        if nuevo_nombre_medico:
            query += "Nombre_medico = %s, "
            params.append(nuevo_nombre_medico)
        if nuevo_diagnostico:
            query += "Diagnostico = %s, "
            params.append(nuevo_diagnostico)
        if ips:
            query += "ips = %s"
            params.append(ips)

        # Eliminar la última coma y espacio
        query = query.rstrip(", ")
        query += " WHERE Codigo = %s"
        params.append(codigo)

        cursor.execute(query, params)
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Orden de servicio actualizada correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar orden de servicio: {e}")

#IPS
def abrir_ips(parent):
    parent.destroy()  # Cierra la ventana anterior
    ventana_ips = tk.Tk()
    ventana_ips.title("Gestión de IPS")
    ventana_ips.geometry("800x600")

    # Sección de registro
    frame_registro = tk.LabelFrame(ventana_ips, text="Registro de IPS", padx=10, pady=10)
    frame_registro.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_registro, text="NIT:").pack(pady=2)
    entrada_nit = tk.Entry(frame_registro)
    entrada_nit.pack(pady=2)

    tk.Label(frame_registro, text="Servicio:").pack(pady=2)
    entrada_servicio = tk.Entry(frame_registro)
    entrada_servicio.pack(pady=2)

    tk.Label(frame_registro, text="Razón social:").pack(pady=2)
    entrada_razon = tk.Entry(frame_registro)
    entrada_razon.pack(pady=2)

    tk.Label(frame_registro, text="Nivel de atención:").pack(pady=2)
    entrada_atencion = tk.Entry(frame_registro)
    entrada_atencion.pack(pady=2)

    boton_registrar = tk.Button(frame_registro, text="Agregar IPS", command=lambda: registrar_ips(
        entrada_nit.get(), entrada_servicio.get(), entrada_razon.get(), entrada_atencion.get()
    ))
    boton_registrar.pack(pady=10)

    # Sección de actualización
    frame_actualizacion = tk.LabelFrame(ventana_ips, text="Actualización de IPS", padx=10, pady=10)
    frame_actualizacion.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_actualizacion, text="NIT:").pack(pady=2)
    entrada_actu_nit = tk.Entry(frame_actualizacion)
    entrada_actu_nit.pack(pady=2)

    tk.Label(frame_actualizacion, text="Servicio:").pack(pady=2)
    entrada_actu_servicio = tk.Entry(frame_actualizacion)
    entrada_actu_servicio.pack(pady=2)

    tk.Label(frame_actualizacion, text="Razón social:").pack(pady=2)
    entrada_actu_razon = tk.Entry(frame_actualizacion)
    entrada_actu_razon.pack(pady=2)

    tk.Label(frame_actualizacion, text="Nivel de atención:").pack(pady=2)
    entrada_actu_atencion = tk.Entry(frame_actualizacion)
    entrada_actu_atencion.pack(pady=2)

    boton_actualizar = tk.Button(frame_actualizacion, text="Actualizar IPS", command=lambda: actualizar_ips(
        entrada_actu_nit.get(), entrada_actu_servicio.get(), entrada_actu_razon.get(), entrada_actu_atencion.get()
    ))
    boton_actualizar.pack(pady=10)
    #busqueda
    frame_busqueda = tk.LabelFrame(ventana_ips, text="BUSCAR CITA", padx=150, pady=10)
    frame_busqueda.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_busqueda, text="NIT:").pack(pady=2)
    nitbusqueda = tk.Entry(frame_busqueda)
    nitbusqueda.pack(pady=2)

    tk.Label(frame_busqueda, text="fecha (AAAA-MM-DD):").pack(pady=2)
    fechabusqueda = tk.Entry(frame_busqueda)
    fechabusqueda.pack(pady=2)

    boton_buscar = tk.Button(frame_busqueda, text="Buscar cita", command=lambda: mostrar_cita(
        frame_busqueda, nitbusqueda.get(), fechabusqueda.get()))
    boton_buscar.pack(pady=20)

    boton_regresar = tk.Button(frame_busqueda, text="Regresar", command=lambda: abrir_dashboard("Usuario", "Administrador", ventana_ips))
    boton_regresar.pack(side=tk.BOTTOM, pady=20)

    ventana_ips.mainloop()

def mostrar_cita(frame_derecho, nit, fecha):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = """select O.*
                    from orden_servicio O inner join ips on O.ips = ips.nit
                    where ips.nit = %s and O.fecha = %s"""
        cursor.execute(query,(nit, fecha))
        datos = cursor.fetchall()
        conexion.close()

        label_resultado = tk.Label(frame_derecho, text="Citas", font=("Arial", 14), bg="white")
        label_resultado.pack(pady=10)

        # Configuración de columnas
        columnas = ("codigo", "fecha", "nombre_medico", "diagnostico", "ips")
        tabla = ttk.Treeview(frame_derecho, columns=columnas, show="headings")
        tabla.heading("codigo", text="codigo")
        tabla.heading("fecha", text="fecha")
        tabla.heading("nombre_medico", text="nombre_medico")
        tabla.heading("diagnostico", text="diagnostico")
        tabla.heading("ips", text="ips")

        # Llenar la tabla con los datos obtenidos
        for fila in datos:
            tabla.insert("", tk.END, values=fila)

        tabla.pack(padx=10, pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar citas: {e}")

def registrar_ips(nit, servicios, razon_social, nivel_atencion):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO IPS (NIT, Servicios, Razon_social, Nivel_Atencion)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (nit, servicios, razon_social, nivel_atencion))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "IPS registrada correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar IPS: {e}")

def actualizar_ips(nit, nuevos_servicios=None, nueva_razon_social=None, nuevo_nivel_atencion=None):
    conexion = conectar_db()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = "UPDATE IPS SET "
        params = []

        if nuevos_servicios:
            query += "Servicios = %s, "
            params.append(nuevos_servicios)
        if nueva_razon_social:
            query += "Razon_social = %s, "
            params.append(nueva_razon_social)
        if nuevo_nivel_atencion:
            query += "Nivel_Atencion = %s, "
            params.append(nuevo_nivel_atencion)

        # Eliminar la última coma y espacio
        query = query.rstrip(", ")
        query += " WHERE NIT = %s"
        params.append(nit)

        cursor.execute(query, params)
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "IPS actualizada correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar IPS: {e}")

# Placeholder para mostrar mensajes al hacer clic en botones
def mostrar_mensaje(seccion):
    messagebox.showinfo("Funcionalidad", f"{seccion}")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Inicio de Sesión")
ventana.geometry("400x350")
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

# Botón para registrar un nuevo usuario
boton_registrar_usuario = tk.Button(ventana, text="Registrar Nuevo Usuario", command=abrir_registro_usuario)
boton_registrar_usuario.pack(pady=10)

ventana.mainloop()
