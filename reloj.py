"""
Reloj de escritorio minimalista para Windows.

- Ventana flotante sin bordes, siempre visible.
- Fondo transparente (con respaldo a negro si no es soportado).
- Arrastrable con clic izquierdo, menú con clic derecho.
- Formato 24h / 12h, atajo ESC para cerrar.

Ejecución:
    python reloj.py        # con consola (recomendado para desarrollo)
    start reloj.pyw        # sin consola en Windows
"""

import time
import tkinter as tk
from tkinter import TclError

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------
# Ancho único amplio: evita que el formato 12h ("12:59:59 PM") quede recortado
# como se veía en las capturas. Si igual se recorta en tu DPI, sube este valor.
ANCHO_RELOJ = 390
ALTO_RELOJ = 100
MARGEN_X = 25
MARGEN_Y = 65

COLOR_TRANSPARENTE = "#1b1a1b"  # Este color se vuelve invisible en Windows
COLOR_TEXTO = "#15a6b6"
COLOR_TEXTO_RESPALDO = "white"
COLOR_FONDO_RESPALDO = "black"

# Aura sutil al pasar el puntero: halo cian tenue + texto aclarado.
# Sin parpadeo: aparece/desaparece con una transición (fundido) fija.
COLOR_AURA_EXTERIOR = "#0d5561"
COLOR_AURA_INTERIOR = "#1899ad"
COLOR_TEXTO_HOVER = "#c9f3f9"
AURA_INTERVALO_MS = 20    # cada cuántos ms avanza la transición
AURA_DURACION_MS = 260    # duración total del fundido
AURA_PASO = AURA_INTERVALO_MS / AURA_DURACION_MS

FUENTE_24H = ("Segoe UI", 44, "bold")  # "15:25:15" (8 caracteres, entra holgado)
FUENTE_12H = ("Segoe UI", 34, "bold")  # "3:25:35 PM" (más largo, fuente menor)
FORMATO_24H = "%H:%M:%S"
FORMATO_12H = "%I:%M:%S %p"


def _a_rgb(color_hex: str) -> tuple:
    """Convierte '#rrggbb' a tupla (r, g, b)."""
    color_hex = color_hex.lstrip("#")
    return tuple(int(color_hex[i:i + 2], 16) for i in (0, 2, 4))


def _mezclar(origen: str, destino: str, t: float) -> str:
    """Interpola dos colores hex. t=0 → origen, t=1 → destino."""
    t = max(0.0, min(1.0, t))
    ro, go, bo = _a_rgb(origen)
    rd, gd, bd = _a_rgb(destino)
    return "#%02x%02x%02x" % (
        round(ro + (rd - ro) * t),
        round(go + (gd - go) * t),
        round(bo + (bd - bo) * t),
    )


class RelojFlotante:
    """Ventana de reloj sin bordes, arrastrable y siempre visible."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.usar_24h = True
        self.siempre_visible = True
        self._drag_x = 0
        self._drag_y = 0

        self.color_fondo = self._configurar_transparencia()

        self.root.configure(bg=self.color_fondo, bd=0, highlightthickness=0)
        self.root.overrideredirect(True)  # Sin barra de título ni bordes
        self.root.attributes("-topmost", True)
        self._quitar_borde_win11()  # Evita el borde blanco / esquina redondeada
        self.root.geometry(self._posicion_inicial())

        self.color_texto_base = (
            COLOR_TEXTO
            if self.color_fondo == COLOR_TRANSPARENTE
            else COLOR_TEXTO_RESPALDO
        )
        self._hover = False
        self._aura_t = 0.0        # 0 = apagada, 1 = encendida al completo
        self._aura_objetivo = 0   # hacia dónde va la transición (0 o 1)
        self._aura_job = None     # id del after() en curso, si lo hay

        # Canvas en vez de Label: permite dibujar el texto varias veces
        # desplazado para simular el halo/aura alrededor de la hora.
        self.canvas = tk.Canvas(
            self.root,
            width=ANCHO_RELOJ,
            height=ALTO_RELOJ,
            background=self.color_fondo,
            highlightthickness=0,
            bd=0,
            cursor="fleur",
        )
        self.canvas.pack(anchor="center", expand=True)

        cx, cy = ANCHO_RELOJ // 2, ALTO_RELOJ // 2
        # Halo exterior (desplazamientos grandes, tono tenue y sutil)
        self._aura_items = []
        for dx, dy in ((-4, 0), (4, 0), (0, -4), (0, 4),
                       (-3, -3), (3, -3), (-3, 3), (3, 3)):
            self._aura_items.append(
                self.canvas.create_text(
                    cx + dx, cy + dy,
                    text="", font=FUENTE_24H, fill=COLOR_AURA_EXTERIOR,
                    state="hidden",
                )
            )
        # Halo interior (desplazamientos cortos, tono medio, no chillón)
        for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2),
                       (-1, -1), (1, -1), (-1, 1), (1, 1)):
            self._aura_items.append(
                self.canvas.create_text(
                    cx + dx, cy + dy,
                    text="", font=FUENTE_24H, fill=COLOR_AURA_INTERIOR,
                    state="hidden",
                )
            )
        self._texto_id = self.canvas.create_text(
            cx, cy, text="", font=FUENTE_24H, fill=self.color_texto_base
        )

        self.menu = self._crear_menu()
        self._vincular_eventos()
        self.actualizar()

    # -- configuración -----------------------------------------------------
    def _configurar_transparencia(self) -> str:
        """Activa fondo transparente en Windows, con respaldo si falla."""
        try:
            self.root.attributes("-transparentcolor", COLOR_TRANSPARENTE)
            return COLOR_TRANSPARENTE
        except TclError:
            # Linux / macOS u otros casos: fondo negro opaco
            return COLOR_FONDO_RESPALDO

    def _posicion_inicial(self) -> str:
        """Esquina inferior derecha de la pantalla principal."""
        ancho = self.root.winfo_screenwidth()
        alto = self.root.winfo_screenheight()
        x = ancho - ANCHO_RELOJ - MARGEN_X
        y = alto - ALTO_RELOJ - MARGEN_Y
        return f"{ANCHO_RELOJ}x{ALTO_RELOJ}+{x}+{y}"

    def _quitar_borde_win11(self) -> None:
        """Quita el borde blanco y las esquinas redondeadas de Windows 11.

        En Win11 las ventanas sin bordes igual muestran un filo claro
        (se veía en tu captura). Se desactiva por API DWM; si falla,
        se ignora sin romper la app.
        """
        try:
            import ctypes

            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            # DWMWA_WINDOW_CORNER_PREFERENCE = 33, DWMWCP_DONOTROUND = 1
            preferencia = ctypes.c_int(1)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, 33, ctypes.byref(preferencia), ctypes.sizeof(preferencia)
            )
        except Exception:
            pass

    def _crear_menu(self) -> tk.Menu:
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Cambiar a 12h / 24h", command=self.alternar_formato)
        menu.add_command(
            label="Siempre visible: ON", command=self.alternar_siempre_visible
        )
        menu.add_separator()
        menu.add_command(label="Cerrar  (ESC)", command=self.root.destroy)
        return menu

    def _vincular_eventos(self) -> None:
        # Arrastrar con botón izquierdo
        self.canvas.bind("<ButtonPress-1>", self._iniciar_arrastre)
        self.canvas.bind("<B1-Motion>", self._arrastrar)
        # Aura estilo PS2 al pasar el puntero
        self.canvas.bind("<Enter>", self._hover_on)
        self.canvas.bind("<Leave>", self._hover_off)
        # Menú con botón derecho (Button-2 para macOS con un botón)
        self.root.bind("<Button-3>", self._mostrar_menu)
        self.root.bind("<Button-2>", self._mostrar_menu)
        self.root.bind("<Escape>", lambda _e: self.root.destroy())

    # -- comportamiento ----------------------------------------------------
    def actualizar(self) -> None:
        """Refresca la hora cada segundo, alineado al cambio de segundo."""
        if self.usar_24h:
            texto = time.strftime(FORMATO_24H)
            fuente = FUENTE_24H
        else:
            # %I deja "03:.. PM" con cero inicial; lo limpiamos a "3:.. PM"
            texto = time.strftime(FORMATO_12H).lstrip("0")
            fuente = FUENTE_12H
        color_principal = _mezclar(self.color_texto_base, COLOR_TEXTO_HOVER, self._aura_t)
        self.canvas.itemconfig(self._texto_id, text=texto, font=fuente, fill=color_principal)
        for item in self._aura_items:
            self.canvas.itemconfig(item, text=texto, font=fuente)
        # 1000 - ms actuales => el tick cae justo al cambiar el segundo
        resto = 1000 - int(time.time() * 1000) % 1000
        self.root.after(max(50, resto), self.actualizar)

    def alternar_formato(self) -> None:
        self.usar_24h = not self.usar_24h
        self.actualizar()

    def alternar_siempre_visible(self) -> None:
        self.siempre_visible = not self.siempre_visible
        self.root.attributes("-topmost", self.siempre_visible)
        estado = "ON" if self.siempre_visible else "OFF"
        self.menu.entryconfig(1, label=f"Siempre visible: {estado}")

    def _hover_on(self, _event: tk.Event) -> None:
        """Inicia el fundido de aparición del aura (sutil y fija)."""
        self._hover = True
        self._aura_objetivo = 1
        self._animar_aura()

    def _hover_off(self, _event: tk.Event) -> None:
        """Inicia el fundido de desaparición del aura."""
        self._hover = False
        self._aura_objetivo = 0
        self._animar_aura()

    def _animar_aura(self) -> None:
        """Avanza la transición del aura un paso hacia su objetivo.

        Si el puntero entra/sale a mitad del fundido, la animación
        simplemente invierte la dirección: transición continua del
        punto A al punto B, sin parpadeo.
        """
        if self._aura_job is not None:
            try:
                self.root.after_cancel(self._aura_job)
            except tk.TclError:
                pass
            self._aura_job = None

        if self._aura_t < self._aura_objetivo:
            self._aura_t = min(self._aura_objetivo, self._aura_t + AURA_PASO)
        elif self._aura_t > self._aura_objetivo:
            self._aura_t = max(self._aura_objetivo, self._aura_t - AURA_PASO)

        self._aplicar_aura(self._aura_t)

        if self._aura_t != self._aura_objetivo:
            self._aura_job = self.root.after(AURA_INTERVALO_MS, self._animar_aura)

    def _aplicar_aura(self, t: float) -> None:
        """Dibuja el estado intermedio del fundido (t=0 apagada, t=1 plena)."""
        self.canvas.itemconfig(
            self._texto_id,
            fill=_mezclar(self.color_texto_base, COLOR_TEXTO_HOVER, t),
        )
        if t <= 0:
            for item in self._aura_items:
                self.canvas.itemconfig(item, state="hidden")
            return
        for i, item in enumerate(self._aura_items):
            destino = COLOR_AURA_EXTERIOR if i < 8 else COLOR_AURA_INTERIOR
            self.canvas.itemconfig(
                item, state="normal",
                fill=_mezclar(self.color_fondo, destino, t),
            )

    def _mostrar_menu(self, event: tk.Event) -> None:
        try:
            self.menu.post(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def _iniciar_arrastre(self, event: tk.Event) -> None:
        self._drag_x = event.x
        self._drag_y = event.y

    def _arrastrar(self, event: tk.Event) -> None:
        self.root.geometry(f"+{event.x_root - self._drag_x}+{event.y_root - self._drag_y}")


def main() -> None:
    root = tk.Tk()
    root.title("Reloj Transparente")
    RelojFlotante(root)
    root.mainloop()


if __name__ == "__main__":
    main()
