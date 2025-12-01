import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import subprocess
import sys
import os
from pathlib import Path
import json
import importlib.util

# PALETA DE COLORES - Tema Oscuro
COLORS = {
    'bg_principal': '#1a1a2e',      # Negro profundo
    'bg_secundario': '#2d2d44',     # Gris oscuro
    'bg_input': '#3b3b5c',          # Gris más oscuro
    'acento_primario': '#3b24c8',   # Púrpura
    'acento_hover': '#5636d3',      # Púrpura claro
    'exito': '#00d966',             # Verde neon
    'error': '#f44336',             # Rojo
    'texto_principal': 'white',       # Blanco
    'texto_secundario': '#b0b0b0'   # Gris claro
}

# Directorio raíz del proyecto
# Cuando se ejecuta como Python, usar la carpeta actual (Datos/)
if getattr(sys, 'frozen', False):
    # Ejecutado como .exe: el .exe está en Escaner3D/dist/
    EXE_DIR = Path(sys.executable).parent  # dist/
    ESCANER3D_DIR = EXE_DIR.parent  # Escaner3D/
    ROOT_DIR = ESCANER3D_DIR / 'Datos'
else:
    # Ejecutado como script Python: estamos en Datos/
    ROOT_DIR = Path(__file__).parent
    ESCANER3D_DIR = ROOT_DIR.parent

# Validar que ROOT_DIR existe
if not ROOT_DIR.exists():
    ROOT_DIR = Path.cwd()
    ESCANER3D_DIR = ROOT_DIR.parent

# Directorio FINAL: en Escaner3D/ (no en Datos/)
SCANS_DIR = ESCANER3D_DIR / 'Escaneos'

# Las rutas de los programas están en Datos/
PROGRAMS = {
    'setup': {
        'path': ROOT_DIR / 'Setup Camara UI.py',
        'name': 'Configurar Cámara',
        'icon': '⚙️',
        'description': 'Configura la cámara, ajusta el threshold\nde detección del láser y selecciona\nel puerto Arduino.'
    },
    'escaneo': {
        'path': ROOT_DIR / 'Escaneo UI.py',
        'name': 'Realizar Escaneo',
        'icon': '📸',
        'description': 'Inicia un nuevo escaneo 3D\n y guarda los resultados.'
    },
    'comparacion': {
        'path': ROOT_DIR / 'Comparacion UI.py',
        'name': 'Comparación',
        'icon': '📊',
        'description': 'Compara escaneos 3D y determina\nla similitud entre piezas.'
    }
}


# ========================================================================================
# FUNCIONES DE UTILIDAD
# ========================================================================================

def crear_imagen_placeholder(width=120, height=120, text="LOGO"):
    """
    Crea una imagen placeholder para el logo.
    Esto será reemplazado cuando se proporcione el logo real.
    """
    img = Image.new('RGB', (width, height), color=COLORS['bg_secundario'])
    draw = ImageDraw.Draw(img)
    
    # Dibujar un círculo de borde
    border_width = 3
    draw.ellipse(
        [border_width, border_width, width - border_width, height - border_width],
        outline=COLORS['acento_primario'],
        width=border_width
    )
    
    # Añadir texto (será reemplazado con imagen real)
    text_bbox = draw.textbbox((0, 0), text)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    draw.text((text_x, text_y), text, fill=COLORS['acento_primario'])
    
    return img


def cargar_logo():
    """
    Intenta cargar el logo desde el archivo especificado.
    Si no existe, usa un placeholder.
    
    Busca el logo en:
    1. Logo.png en la carpeta del ejecutable (para desarrollo)
    2. Logo.png empaquetado en el .exe (para distribución)
    
    Si no encuentra nada, genera un placeholder automáticamente.
    """
    logo_path = ROOT_DIR / 'Logo.png'
    
    # Intentar cargar desde archivo externo (modo desarrollo)
    if logo_path.exists():
        try:
            img = Image.open(logo_path)
            # Redimensionar si es necesario (máximo 120x120)
            img.thumbnail((120, 120), Image.Resampling.LANCZOS)
            return img
        except Exception as e:
            print(f"Error al cargar el logo: {e}")
            return crear_imagen_placeholder()
    
    # Si no existe archivo, usar placeholder
    # (En distribución .exe, el logo está empaquetado)
    return crear_imagen_placeholder()


def ejecutar_programa(program_key):
    """
    Ejecuta el programa especificado.
    En desarrollo: como subproceso
    En .exe compilado: importa y ejecuta directamente
    """
    try:
        program_info = PROGRAMS[program_key]
        program_path = program_info['path']
        
        # Si está compilado como .exe (sys.frozen), importar y ejecutar directamente
        if getattr(sys, 'frozen', False):
            # Ejecutado como .exe
            ejecutar_programa_compilado(program_key, program_path)
        else:
            # Desarrollo: ejecutar como subproceso desde ROOT_DIR (Datos/)
            if not program_path.exists():
                messagebox.showerror("Error", f"No se encontró: {program_path}")
                return
            
            subprocess.Popen(
                [sys.executable, str(program_path)],
                cwd=str(ROOT_DIR)  # Ejecutar desde Datos/ para que encuentre Configuracion.json
            )
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al ejecutar: {str(e)}")
        import traceback
        traceback.print_exc()


def ejecutar_programa_compilado(program_key, program_path):
    """
    Ejecuta un programa cuando está compilado como .exe.
    Importa el módulo y ejecuta su función principal.
    """
    import importlib.util
    import os
    
    try:
        # Cambiar directorio de trabajo a ROOT_DIR (Datos/) donde está la configuración
        os.chdir(str(ROOT_DIR))
        
        # Agregar la ruta actual (Datos/) al sys.path
        if str(ROOT_DIR) not in sys.path:
            sys.path.insert(0, str(ROOT_DIR))
        
        print(f"Cargando módulo: {program_path}")
        print(f"Directorio de trabajo: {os.getcwd()}")
        
        # Cargar el módulo desde el archivo
        spec = importlib.util.spec_from_file_location(
            program_path.stem,
            str(program_path)
        )
        
        if spec is None or spec.loader is None:
            raise ImportError(f"No se pudo crear especificación para {program_path}")
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[program_path.stem] = module
        
        print(f"Ejecutando módulo: {program_path.stem}")
        spec.loader.exec_module(module)
        
    except Exception as e:
        print(f"Error ejecutando módulo compilado: {e}")
        import traceback
        traceback.print_exc()
        messagebox.showerror("Error", f"Error: {str(e)}")


def crear_boton_programa(parent, program_key, row, col):
    """
    Crea un botón estilizado para un programa.
    """
    program_info = PROGRAMS[program_key]
    
    # Frame del botón
    btn_frame = tk.Frame(parent, bg=COLORS['bg_secundario'], highlightthickness=2,
                        highlightbackground=COLORS['bg_input'], highlightcolor=COLORS['acento_primario'])
    btn_frame.grid(row=row, column=col, padx=12, pady=12, sticky='nsew')
    
    # Hacer el frame expandible
    parent.grid_rowconfigure(row, weight=1)
    parent.grid_columnconfigure(col, weight=1)
    
    # Variable para controlar el estado
    estado = {'hover': False}
    
    # Función para cambiar color al pasar el mouse
    def on_enter(event):
        estado['hover'] = True
        btn_frame.config(bg=COLORS['bg_input'], highlightbackground=COLORS['acento_primario'])
        icon_label.config(fg=COLORS['acento_hover'])
    
    def on_leave(event):
        estado['hover'] = False
        btn_frame.config(bg=COLORS['bg_secundario'], highlightbackground=COLORS['bg_input'])
        icon_label.config(fg=COLORS['acento_primario'])
    
    def on_click(event=None):
        ejecutar_programa(program_key)
    
    btn_frame.bind('<Enter>', on_enter)
    btn_frame.bind('<Leave>', on_leave)
    btn_frame.bind('<Button-1>', on_click)
    btn_frame.bind('<Return>', on_click)
    
    # Ícono grande
    icon_label = tk.Label(
        btn_frame,
        text=program_info['icon'],
        font=('Arial', 48),
        bg=COLORS['bg_secundario'],
        fg=COLORS['acento_primario'],
        cursor='hand2'
    )
    icon_label.pack(pady=(15, 5))
    icon_label.bind('<Enter>', on_enter)
    icon_label.bind('<Leave>', on_leave)
    icon_label.bind('<Button-1>', on_click)
    
    # Nombre del programa
    name_label = tk.Label(
        btn_frame,
        text=program_info['name'],
        font=('Segoe UI', 12, 'bold'),
        bg=COLORS['bg_secundario'],
        fg=COLORS['texto_principal'],
        cursor='hand2'
    )
    name_label.pack(pady=(0, 8))
    name_label.bind('<Enter>', on_enter)
    name_label.bind('<Leave>', on_leave)
    name_label.bind('<Button-1>', on_click)
    
    # Descripción del programa
    desc_label = tk.Label(
        btn_frame,
        text=program_info['description'],
        font=('Segoe UI', 9),
        bg=COLORS['bg_secundario'],
        fg=COLORS['texto_secundario'],
        wraplength=200,
        justify='center',
        cursor='hand2'
    )
    desc_label.pack(padx=10, pady=(0, 15))
    desc_label.bind('<Enter>', on_enter)
    desc_label.bind('<Leave>', on_leave)
    desc_label.bind('<Button-1>', on_click)
    
    return btn_frame


# ========================================================================================
# FUNCIÓN PRINCIPAL
# ========================================================================================

def main():
    """
    Crea la ventana principal del launcher.
    """
    # Crear estructura de carpetas
    try:
        ESCANER3D_DIR.mkdir(exist_ok=True)
        SCANS_DIR.mkdir(exist_ok=True)
    except:
        pass
    
    # Crear ventana raíz
    root = tk.Tk()
    root.title("Escaner 3D - Centro de Control")
    root.geometry("1024x768")
    root.resizable(False, False)
    
    # Establecer color de fondo
    root.config(bg=COLORS['bg_principal'])
    
    # ==================== Header con Logo ====================
    header_frame = tk.Frame(root, bg=COLORS['bg_principal'], height=160)
    header_frame.pack(fill='x', padx=0, pady=0)
    header_frame.pack_propagate(False)
    
    # Contenedor del header con márgenes
    header_content = tk.Frame(header_frame, bg=COLORS['bg_principal'])
    header_content.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Logo en la esquina superior izquierda
    logo_img = cargar_logo()
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(header_content, image=logo_photo, bg=COLORS['bg_principal'])
    logo_label.image = logo_photo  # Guardar referencia
    logo_label.pack(side='left', padx=(0, 20))
    
    # Título y descripción
    title_frame = tk.Frame(header_content, bg=COLORS['bg_principal'])
    title_frame.pack(side='left', fill='both', expand=True)
    
    title_label = tk.Label(
        title_frame,
        text="Escaner 3D",
        font=('Segoe UI', 24, 'bold'),
        bg=COLORS['bg_principal'],
        fg=COLORS['texto_principal']
    )
    title_label.pack(anchor='w')
    
    subtitle_label = tk.Label(
        title_frame,
        text="Centro de Control - Selecciona una opción para comenzar",
        font=('Segoe UI', 11),
        bg=COLORS['bg_principal'],
        fg=COLORS['texto_secundario']
    )
    subtitle_label.pack(anchor='w', pady=(5, 0))
    
    # ==================== Separador ====================
    separator = tk.Frame(root, bg=COLORS['bg_secundario'], height=2)
    separator.pack(fill='x')
    
    # ==================== Contenedor de programas ====================
    content_frame = tk.Frame(root, bg=COLORS['bg_principal'])
    content_frame.pack(fill='both', expand=True, padx=40, pady=40)
    
    # Grid de programas (3 columnas)
    for idx, program_key in enumerate(PROGRAMS.keys()):
        crear_boton_programa(content_frame, program_key, 0, idx)
    
    # ==================== Footer ====================
    footer_frame = tk.Frame(root, bg=COLORS['bg_secundario'], height=60)
    footer_frame.pack(fill='x', side='bottom')
    footer_frame.pack_propagate(False)
    
    footer_label = tk.Label(
        footer_frame,
        text="Proyecto Final - Estacion de Escaneo 3D para Analisis de Desviaciones Dimensionales - F.I.U.N.L.Z.",
        font=('Segoe UI', 10),
        bg=COLORS['bg_secundario'],
        fg=COLORS['texto_secundario']
    )
    footer_label.pack(pady=15)
    
    # Centrar ventana en la pantalla
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == '__main__':
    main()
