import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import serial.tools.list_ports

# Archivo de configuración
CONFIG_FILE = "Configuracion.json"

# Paleta de colores - Tema Oscuro
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

# Variables
cam_index = 0
threshold_value = 100
arduino_port = ""

cap = None

def load_config():
    # Cargar configuración
    global cam_index, threshold_value, arduino_port
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            setup = config.get("setup_camara", {})
            cam_index = setup.get("camera_index")
            threshold_value = setup.get("threshold")
            arduino_port = setup.get("arduino_port")
    except FileNotFoundError:
        pass

def save_config():
    # Cargar configuración completa
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        # Crear estructura por defecto si no existe
        config = {
            "version": "1.0",
            "descripcion": "Archivo de configuración unificado",
            "setup_camara": {},
            "parametros_calibracion": {},
            "parametros_comparacion": {},
            "configuracion_escaneo": {}
        }
    
    # Actualizar solo la sección setup_camara
    config["setup_camara"] = {
        "camera_index": cam_index,
        "threshold": threshold_value,
        "arduino_port": arduino_port
    }
    
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
    
    messagebox.showinfo("Éxito", "Configuración guardada correctamente")

def update_camera(index):
    global cap, cam_index
    cam_index = index
    if cap is not None:
        cap.release()
    cap = cv2.VideoCapture(cam_index)

def process_frame():
    global cap, threshold_value

    if cap is None or not cap.isOpened():
        return None

    ret, frame = cap.read()
    if not ret:
        return None

    # Extraer canal rojo
    red_channel = frame[:, :, 2]

    # Aplicar suavizado gaussiano horizontal
    red_channel = cv2.GaussianBlur(red_channel, (15, 1), 0)

    # Máscara para la línea
    laser_mask = np.zeros_like(red_channel)
    height, width = red_channel.shape

    for y in range(height):
        row = red_channel[y]
        max_val = np.max(row)
        if max_val > threshold_value:
            x = np.argmax(row)
            laser_mask[y, x] = 255

    # Crear overlay rojo solo con los puntos detectados
    laser_overlay = cv2.merge([
        laser_mask,
        laser_mask,
        np.zeros_like(laser_mask)
    ])

    # Combinar la cámara original + línea detectada
    output = cv2.addWeighted(frame, 0.5, laser_overlay, 1.0, 0)

    return output

# Procesado del video y threshold
def update_frame():
    frame = process_frame()
    if frame is not None:
        # SIN redimensionar - usar dimensiones reales 640x480
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    root.after(33, update_frame)  # refrescar cada 33ms (~30 FPS)

def on_cam_change(val):
    update_camera(int(val))

def on_threshold_change(val):
    global threshold_value
    threshold_value = int(val)
    threshold_label.config(text=f"Threshold: {threshold_value}")

def on_port_select(event):
    global arduino_port
    arduino_port = port_combo.get()

# Interfaz Tkinter
root = tk.Tk()
root.title("Setup Cámara y Arduino")
root.geometry("1024x768")
root.resizable(False, False)
root.configure(bg=COLORS['bg_principal'])

# Aplicar tema oscuro a ttk
style = ttk.Style()
style.theme_use('clam')
style.configure('TCombobox', fieldbackground=COLORS['bg_input'], background=COLORS['bg_input'])
style.configure('TScale', background=COLORS['bg_principal'])

# Cargar configuración antes de crear UI
load_config()
cap = cv2.VideoCapture(cam_index)

# === TÍTULO ===
titulo_frame = tk.Frame(root, bg=COLORS['bg_principal'])
titulo_frame.pack(fill='x', padx=12, pady=5)

titulo = tk.Label(titulo_frame, text="CONFIGURACIÓN",
                 font=("Segoe UI", 14, "bold"), bg=COLORS['bg_principal'], 
                 fg=COLORS['texto_principal'])
titulo.pack(anchor='w')

separador = tk.Frame(root, bg=COLORS['acento_primario'], height=1)
separador.pack(fill='x', padx=0)

# === ÁREA DE VIDEO (640x480 - FIJO, SIN ESCALAR) ===
video_frame = tk.Frame(root, bg=COLORS['bg_secundario'])
video_frame.pack(pady=5, padx=12, fill='both', expand=False)

video_label_titulo = tk.Label(video_frame, text="Vista Previa Cámara",
                             font=("Segoe UI", 9, "bold"), 
                             bg=COLORS['bg_secundario'], fg=COLORS['texto_principal'])
video_label_titulo.pack(pady=3)

# Label EXACTAMENTE 640x480 - SIN REDIMENSIONAR
video_label = tk.Label(video_frame, bg='#000000', width=640, height=480)
video_label.pack()

# === CONTROLES - LAYOUT HORIZONTAL COMPACTO ===
controles_frame_main = tk.Frame(root, bg=COLORS['bg_principal'])
controles_frame_main.pack(fill='x', padx=12, pady=4)

# COLUMNA IZQUIERDA: Sliders verticales
col_izquierda = tk.Frame(controles_frame_main, bg=COLORS['bg_principal'])
col_izquierda.pack(side='left', fill='both', expand=True, padx=(0, 8))

# --- Sección 1: Cámara ---
camara_frame = tk.LabelFrame(col_izquierda, text="Cámara",
                             font=("Segoe UI", 9, "bold"), 
                             bg=COLORS['bg_secundario'], fg=COLORS['texto_principal'],
                             padx=8, pady=6, relief='flat', bd=1)
camara_frame.pack(fill='x', pady=3)

cam_label = tk.Label(camara_frame, text="Índice (0-3):",
                    font=("Segoe UI", 8), bg=COLORS['bg_secundario'], 
                    fg=COLORS['texto_secundario'])
cam_label.pack(anchor='w', pady=(0, 3))

cam_slider = tk.Scale(camara_frame, from_=0, to=3, orient="horizontal", 
                     command=on_cam_change, bg=COLORS['bg_principal'],
                     fg=COLORS['texto_principal'], troughcolor=COLORS['bg_secundario'],
                     highlightthickness=0, relief='flat', activebackground=COLORS['acento_primario'],
                     length=150)
cam_slider.set(cam_index)
cam_slider.pack(fill='x', padx=3)

# --- Sección 2: Threshold ---
threshold_frame = tk.LabelFrame(col_izquierda, text="Threshold",
                               font=("Segoe UI", 9, "bold"),
                               bg=COLORS['bg_secundario'], fg=COLORS['texto_principal'],
                               padx=8, pady=6, relief='flat', bd=1)
threshold_frame.pack(fill='x', pady=3)

thresh_label = tk.Label(threshold_frame, text="Brillo (0-255):",
                       font=("Segoe UI", 8), bg=COLORS['bg_secundario'],
                       fg=COLORS['texto_secundario'])
thresh_label.pack(anchor='w', pady=(0, 3))

thresh_slider = tk.Scale(threshold_frame, from_=0, to=255, orient="horizontal",
                        command=on_threshold_change, bg=COLORS['bg_principal'],
                        fg=COLORS['texto_principal'], troughcolor=COLORS['bg_secundario'],
                        highlightthickness=0, relief='flat', activebackground=COLORS['acento_primario'],
                        length=150)
thresh_slider.set(threshold_value)
thresh_slider.pack(fill='x', padx=3)

threshold_label = tk.Label(threshold_frame, text=f"Valor: {threshold_value}",
                          font=("Segoe UI", 8, "bold"), bg=COLORS['bg_secundario'],
                          fg=COLORS['exito'])
threshold_label.pack(anchor='w', padx=3, pady=(3, 0))

# COLUMNA DERECHA: Arduino
col_derecha = tk.Frame(controles_frame_main, bg=COLORS['bg_principal'])
col_derecha.pack(side='right', fill='both', expand=True, padx=(8, 0))

# --- Sección 3: Puerto Arduino ---
arduino_frame = tk.LabelFrame(col_derecha, text="Arduino",
                             font=("Segoe UI", 9, "bold"),
                             bg=COLORS['bg_secundario'], fg=COLORS['texto_principal'],
                             padx=8, pady=6, relief='flat', bd=1)
arduino_frame.pack(fill='x', pady=3)

port_label = tk.Label(arduino_frame, text="Puerto Serial:",
                     font=("Segoe UI", 8), bg=COLORS['bg_secundario'],
                     fg=COLORS['texto_secundario'])
port_label.pack(anchor='w', pady=(0, 3))

ports = [port.device for port in serial.tools.list_ports.comports()]
port_combo = ttk.Combobox(arduino_frame, values=ports, state="readonly",
                         font=("Segoe UI", 8), width=12)
port_combo.set(arduino_port if arduino_port in ports else (ports[0] if ports else ""))
port_combo.bind("<<ComboboxSelected>>", on_port_select)
port_combo.pack(fill='x', pady=(0, 3), padx=3)

# Información de puertos
if ports:
    port_info = tk.Label(arduino_frame, text=f"Disponibles: {', '.join(ports)}",
                        font=("Segoe UI", 7, "italic"), bg=COLORS['bg_secundario'],
                        fg=COLORS['texto_secundario'], justify='left', wraplength=120)
else:
    port_info = tk.Label(arduino_frame, text="⚠️ No detectados",
                        font=("Segoe UI", 7, "italic"), bg=COLORS['bg_secundario'],
                        fg=COLORS['error'])
port_info.pack(anchor='w', padx=3, pady=(2, 0), fill='x')

# --- Sección 4: Botones Arduino (Grid 2x2) ---
botones_arduino_frame = tk.Frame(col_derecha, bg=COLORS['bg_secundario'])
botones_arduino_frame.pack(fill='x', pady=3, padx=3)

def crear_boton_mejorado(parent, text, command, bg_color, fg_color, 
                         hover_bg, active_bg, font_size=9):
    """Crea un botón con estilo mejorado y efectos hover"""
    btn = tk.Button(parent, text=text, command=command,
                   font=("Segoe UI", font_size, "bold"),
                   bg=bg_color, fg=fg_color,
                   activebackground=active_bg, activeforeground=fg_color,
                   relief='flat', bd=0, padx=12, pady=6,
                   cursor="hand2", highlightthickness=0)
    
    # Efectos hover
    def on_enter(event):
        btn.config(bg=hover_bg)
    
    def on_leave(event):
        btn.config(bg=bg_color)
    
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    return btn

btn_guardar_config = crear_boton_mejorado(botones_arduino_frame, "💾 GUARDAR",
                                         save_config,
                                         COLORS['exito'], COLORS['bg_principal'],
                                         '#00ff7a', '#00e060',
                                         font_size=9)
btn_guardar_config.pack(side='left', padx=3, fill='both', expand=True)

btn_cancelar = crear_boton_mejorado(botones_arduino_frame, "❌ CANCELAR",
                                   root.quit,
                                   COLORS['error'], COLORS['texto_principal'],
                                   '#ff6b6b', '#e53935',
                                   font_size=9)
btn_cancelar.pack(side='left', padx=3, fill='both', expand=True)

# Loop de video
update_frame()

# Cierre seguro
def on_closing():
    if cap is not None:
        cap.release()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
