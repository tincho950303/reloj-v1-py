# AGENTS.md — Reloj de escritorio minimalista

Guía para agentes de IA que trabajen en este repo. Proyecto pequeño: preferir
cambios mínimos y verificados antes que refactors grandes.

## Stack y archivos

- Python 3.8+ con **solo librería estándar** (`tkinter`, `time`, `ctypes`).
  No agregar dependencias sin pedirlo antes.
- `reloj.py` — app principal (clase `RelojFlotante` + `main()`). Lógica completa aquí.
- `reloj.pyw` — lanzador sin consola para Windows. Solo importa `main` de
  `reloj.py`; **no duplicar lógica** en este archivo.
- `requirements.txt` — intencionalmente vacío (stdlib). Solo tocar si se agrega
  una dependencia real.
- `assets/` — capturas (`captura.png` es la principal que muestra el README).
- `docs/SOCIAL_KIT.md` — textos para redes/portfolio.

## Cómo ejecutar y verificar

```powershell
python reloj.py          # con consola (desarrollo)
python -m py_compile reloj.py reloj.pyw   # verificación rápida de sintaxis
```

- Tras cada cambio de código: `py_compile` obligatorio y borrar `__pycache__`.
- Si hay display disponible, prueba funcional mínima: instanciar `RelojFlotante`,
  `update_idletasks()`, simular `_hover_on/_hover_off` y `destroy()`.
- No abrir la app con `mainloop()` bloqueante desde el agente.

## Convenciones de código

- Todo el estado de la ventana vive en `RelojFlotante`; nada de código a nivel
  módulo salvo constantes, helpers (`_a_rgb`, `_mezclar`) y `main()`.
- El fondo transparente usa el color clave `COLOR_TRANSPARENTE` (`-transparentcolor`
  en Windows). **Nunca** usar ese color para texto o aura: se volvería invisible.
- El aura se dibuja con 16 textos desplazados en un `Canvas` (+ texto principal).
  Es fija y sutil, con fundido (~260 ms) entre apagada/encendida. No reintroducir
  parpadeo ni pulso sin que lo pidan.
- El cursor debe quedar por defecto (sin `cursor=` en el canvas).
- Ventana de tamaño fijo (`ANCHO_RELOJ x ALTO_RELOJ`): verificar que formatos
  largos como `12:59:59 PM` no se recorten al cambiar fuentes o tamaños.
- El fix de borde blanco de Win11 (`_quitar_borde_win11`, API DWM) va envuelto en
  `try/except`: mantenerlo tolerante a fallos.
- Docstrings en español, código y nombres en el estilo existente.

## Commits

- Commits en español, formato: `Área: descripción breve` (ej: `Aura: suavizar fundido`).
- No commitear ni pushear sin que lo pidan explícitamente.
- Nunca commitear `venv/`, `__pycache__/` ni capturas con nombres por defecto
  (`Captura de pantalla ...`): renombrar a `captura-*.png` descriptivos.
