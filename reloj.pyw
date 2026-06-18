"""
Reloj de escritorio minimalista.
Se posiciona automáticamente en la esquina inferior derecha.
"""
import tkinter as tk
import time
from tkinter import TclError

# <------ Actualiza el label con la hora actual cada segundo. ---------->
def actualizar_reloj():
    hora_actual = time.strftime('%H:%M:%S')
    label.config(text=hora_actual)
    root.after(1000, actualizar_reloj)
# <------ Calcula las coordenadas para la esquina inferior derecha. ---------->
def obtener_posicion():
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    ancho_reloj = 250
    alto_reloj = 80
    margen_x = 20
    margen_y = 60
    x = ancho_pantalla - ancho_reloj - margen_x
    y = alto_pantalla - alto_reloj - margen_y
    return f"{ancho_reloj}x{alto_reloj}+{x}+{y}"
# ---------- Definimos la función que se ejecutará al cerrar ----------->
def cerrar_aplicacion():
    root.destroy()
# ----------  Función para mostrar el menú donde está el ratón ----------->
def mostrar_menu(event):
    menu_contextual.post(event.x_root, event.y_root)

# ---------- Ventana principal ----------->

root = tk.Tk()
root.title("Reloj Transparente")

# ---------- Ventana Menú ----------->
menu_contextual = tk.Menu(root, tearoff=0)
menu_contextual.add_command(label="Cerrar Reloj", command=cerrar_aplicacion)
# Vinculamos el clic derecho a la función de mostrar el menú
root.bind("<Button-3>", mostrar_menu)
# ---------- Configuración de colores ----------->
COLOR_TRANSPARENTE = "#1b1a1b"
COLOR_TEXTO = "#1dc2db"

# ---------- Configurar transparencia ----------->
try:
    root.attributes("-transparentcolor", COLOR_TRANSPARENTE)
    COLOR_FONDO = COLOR_TRANSPARENTE # Este color será invisible
except TclError:
    # Si no funciona la transparencia, usamos negro de respaldo
    root.wait_visibility(root)
    COLOR_FONDO = 'black'
    COLOR_TEXTO = 'white'

root.configure(bg=COLOR_FONDO)
root.overrideredirect(True)
root.attributes('-topmost', True)
root.geometry(obtener_posicion())

#----------- Crear el label ----------->
label = tk.Label(
    root,
    font=('calibri', 40, 'bold'),
    background=COLOR_FONDO, # Fondo transparente
    foreground=COLOR_TEXTO  
)
label.pack(anchor='center', expand=True)

#----------- Iniciamos el reloj----------->

actualizar_reloj()
root.mainloop()
