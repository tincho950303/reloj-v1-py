# 🕒 Reloj de escritorio minimalista

Ventana flotante, sin bordes y siempre visible para Windows, hecha con **Python + Tkinter** (solo librería estándar, sin dependencias).

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![Windows](https://img.shields.io/badge/OS-Windows-0078D6?logo=windows)
![License](https://img.shields.io/badge/License-MIT-yellow)

| 24h | 24h + aura (hover) |
|-----|--------------------|
| ![24h](assets/captura-24h.png) | ![24h aura](assets/captura-24h-aura.png) |

| 12h | 12h + aura (hover) |
|-----|--------------------|
| ![12h](assets/captura-12h.png) | ![12h aura](assets/captura-12h-aura.png) |

---

## ✨ Características

- 🪟 Flotante sin bordes, posicionado en la esquina inferior derecha
- 👻 Fondo transparente en Windows (con respaldo a negro en otros SO)
- 🖱️ Arrastrable con clic izquierdo
- ✨ Aura sutil al pasar el puntero (halo cian fijo con fundido suave)
- 📋 Menú con clic derecho: cambiar 12h/24h, activar/desactivar "siempre visible", cerrar
- ⌨️ `ESC` para cerrar
- ⚡ Tick alineado al segundo real (sin deriva)
- 📦 Cero dependencias: solo `tkinter`

## 🚀 Uso

### En Consola
```bash
# Clonar
git clone https://github.com/tincho950303/reloj-v1-py.git
cd reloj-v1-py

# Ejecutar (con consola, ideal para desarrollo)
python reloj.py
```
### En Windows

Doble clic en **`reloj.pyw`** para ejecutarlo.

## 🖱️ Controles

| Acción              | Resultado                          |
|---------------------|------------------------------------|
| Arrastrar           | Mover el reloj                     |
| Clic derecho        | Abrir menú                         |
| Menú → 12h / 24h    | Cambiar formato de hora            |
| Menú → Siempre visible | Fijar / liberar sobre otras ventanas |
| `ESC` o Menú → Cerrar | Salir                            |

## 🛠️ Tecnologías

- Python 3.8+
- Tkinter (stdlib)
- API Win32 `-transparentcolor` vía `root.attributes`

## 📁 Estructura

```text
reloj/
├── reloj.py        # App principal
├── reloj.pyw       # Lanzador sin consola (Windows)
├── requirements.txt # Vacío: solo stdlib
├── assets/         
├── docs/
│   └── SOCIAL_KIT.md # Textos listos para LinkedIn, X, Instagram y portfolio
├── LICENSE         # MIT
└── README.md
```

## 🗺️ Roadmap

- [ ] Selector de color y tamaño de fuente
- [ ] Fecha + alarma / temporizador
- [ ] Guardar posición y preferencias (`config.json`)
- [ ] Empaquetar como `.exe` con PyInstaller
- [ ] Soporte multi-monitor

## 🤝 Contribuir

¡PRs e issues bienvenidos! Ideas simples para empezar: cambiar la fuente, agregar fecha, guardar la posición.

## 👤 Autor

**tincho950303** — https://github.com/tincho950303

Si te sirve, deja una ⭐ en el repo.
