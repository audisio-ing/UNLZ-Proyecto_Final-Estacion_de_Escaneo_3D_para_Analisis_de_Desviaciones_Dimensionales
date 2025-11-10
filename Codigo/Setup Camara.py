import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json
import serial.tools.list_ports

# Archivo de configuración
CONFIG_FILE = "Setup.json"

# Variables
cam_index = 0
threshold_value = 100
arduino_port = ""

cap = None

def load_config():
    # Cargar configuración previa si existe
    global cam_index, threshold_value, arduino_port
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            cam_index = config.get("camera_index", 0)
            threshold_value = config.get("threshold", 100)
            arduino_port = config.get("arduino_port", "")
    except FileNotFoundError:
        pass

def save_config():
    config = {
        "camera_index": cam_index,
        "threshold": threshold_value,
        "arduino_port": arduino_port
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

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
        # Convertir BGR → RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    root.after(10, update_frame)  # refrescar cada 10ms

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
root.title("Setup Cámara")

# Cargar configuración antes de crear UI
load_config()
cap = cv2.VideoCapture(cam_index)

# Video
video_label = tk.Label(root)
video_label.pack()

# Cámara
tk.Label(root, text="Índice de cámara (0-3):").pack()
cam_slider = tk.Scale(root, from_=0, to=3, orient="horizontal", command=on_cam_change)
cam_slider.set(cam_index)
cam_slider.pack()

# Threshold
tk.Label(root, text="Umbral de brillo:").pack()
thresh_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", command=on_threshold_change)
thresh_slider.set(threshold_value)
thresh_slider.pack()

threshold_label = tk.Label(root, text=f"Threshold: {threshold_value}")
threshold_label.pack()

# Puertos Arduino
tk.Label(root, text="Puerto Arduino:").pack()
ports = [port.device for port in serial.tools.list_ports.comports()]
port_combo = ttk.Combobox(root, values=ports, state="readonly")
port_combo.set(arduino_port if arduino_port in ports else (ports[0] if ports else ""))
port_combo.bind("<<ComboboxSelected>>", on_port_select)
port_combo.pack()

# Loop de video
update_frame()

# Cierre seguro
def on_closing():
    if cap is not None:
        cap.release()
    save_config()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
