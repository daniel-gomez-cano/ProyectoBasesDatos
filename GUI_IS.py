import tkinter as tk
from tkinter import messagebox

# Función para manejar el inicio de sesión
def iniciar_sesion():
    usuario = entrada_usuario.get()
    contrasena = entrada_contrasena.get()
    rol = rol_var.get()

    if not usuario or not contrasena:
        messagebox.showerror("Error", "Por favor, ingrese usuario y contraseña.")
        return

    # Aquí se validará la combinación de usuario, contraseña y rol.
    # Por ahora es un placeholder para simplificar.
    if rol == "Administrador":
        messagebox.showinfo("Inicio de sesión", f"Bienvenido Administrador: {usuario}")
        # Redirige a la interfaz de gestión de afiliados, empresas, etc.
        abrir_interfaz_administrador()
    elif rol == "Cotizante":
        messagebox.showinfo("Inicio de sesión", f"Bienvenido Cotizante: {usuario}")
        # Redirige a la interfaz de consulta de información propia
        abrir_interfaz_cotizante()
    elif rol == "Banco":
        messagebox.showinfo("Inicio de sesión", f"Bienvenido Banco: {usuario}")
        # Redirige a la interfaz de carga de pagos
        abrir_interfaz_banco()
    else:
        messagebox.showerror("Error", "Seleccione un rol válido.")

# Funciones para abrir las interfaces específicas (placeholders por ahora)
def abrir_interfaz_administrador():
    messagebox.showinfo("Interfaz", "Aquí se cargará la interfaz de Administrador.")

def abrir_interfaz_cotizante():
    messagebox.showinfo("Interfaz", "Aquí se cargará la interfaz de Cotizante.")

def abrir_interfaz_banco():
    messagebox.showinfo("Interfaz", "Aquí se cargará la interfaz del Banco.")

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
"""Cambios para el hpta commit"""