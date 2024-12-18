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

# Los INSERT que utilicé en la base de datos:
"""INSERT INTO Afiliado (DI, Tipo, Fecha_Nac, Estado, Nombres, Apellidos, Genero, Correo_electronico, Telefono, Ciudad_residencia, Direccion, Estado_actual)
VALUES (101, 'CC', '2000-01-01', 'Activo', 'Juan', 'Perez', 'M', 'juan.perez@mail.com', '1234567', 'Medellin', 'Calle 123', 'Activo');

-- Datos de ejemplo para Cotizante
INSERT INTO Cotizante (DI, Tipo, Salario, Fecha_1_afiliacion, IPS)
VALUES (101, 'Dependiente', 2500.00, '2023-01-01', NULL);
//  
-- Datos de ejemplo para Empresa
INSERT INTO Empresa (NIT, Ciudad, Razon_social, Direccion, Telefono, Contacto)
VALUES (555001, 'Bogota', 'Empresa X', 'Calle Falsa 123', '9876543', 'Maria Gonzalez');"""

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
        abrir_dashboard(usuario, rol)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos o cuenta inactiva.")

# Función para abrir el dashboard
def abrir_dashboard(usuario, rol):
    ventana.destroy()

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
        ("Afiliados", lambda: abrir_beneficiarios(dashboard)),
        ("Empresas", lambda: abrir_empresas(dashboard)),
        ("Contratos", lambda: mostrar_mensaje("Contratos")),
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
    boton_regresar = tk.Button(frame_izquierdo, text="Regresar", command=lambda: abrir_dashboard("Usuario", "Administrador"))
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
    columnas = ("#1", "#2", "#3")
    tabla = ttk.Treeview(frame, columns=columnas, show="headings")
    tabla.heading("#1", text="Columna 1")
    tabla.heading("#2", text="Columna 2")
    tabla.heading("#3", text="Columna 3")

    # Consulta dinámica según el tipo de listado
    query_dict = {
        "Cotizantes": "SELECT DI, Tipo, Salario FROM Cotizante",
        "Beneficiarios": "SELECT DI, Parentesco, DI_cotizante FROM Beneficiario",
        "Empresas": "SELECT NIT, Ciudad, Razon_social FROM Empresa",
        "Contratos": "SELECT NContrato, Estado, Salario_base FROM Contrato",
        "Aportes": "SELECT NPago, Valor_pagado, Fecha_pago FROM Pago_aportes",
        "IPS": "SELECT NIT, Servicios, Razon_social FROM IPS",
        "Órdenes de Servicio": "SELECT Codigo, Fecha, Nombre_medico FROM Orden_Servicio",
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

    tk.Label(frame_registro, text="Razón Social:").pack(pady=2)
    entrada_razon = tk.Entry(frame_registro)
    entrada_razon.pack(pady=2)

    tk.Label(frame_registro, text="Dirección:").pack(pady=2)
    entrada_direccion = tk.Entry(frame_registro)
    entrada_direccion.pack(pady=2)

    boton_registrar = tk.Button(frame_registro, text="Registrar Empresa", command=lambda: mostrar_mensaje("Empresa registrada"))
    boton_registrar.pack(pady=10)

    # Sección de actualización
    frame_actualizacion = tk.LabelFrame(ventana_empresas, text="Actualizar Empresa", padx=10, pady=10)
    frame_actualizacion.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(frame_actualizacion, text="NIT:").pack(pady=2)
    actualizar_nit = tk.Entry(frame_actualizacion)
    actualizar_nit.pack(pady=2)

    tk.Label(frame_actualizacion, text="Nueva Dirección:").pack(pady=2)
    actualizar_direccion = tk.Entry(frame_actualizacion)
    actualizar_direccion.pack(pady=2)

    boton_actualizar = tk.Button(frame_actualizacion, text="Actualizar Empresa", command=lambda: mostrar_mensaje("Empresa actualizada"))
    boton_actualizar.pack(pady=10)

    ventana_empresas.mainloop()

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
