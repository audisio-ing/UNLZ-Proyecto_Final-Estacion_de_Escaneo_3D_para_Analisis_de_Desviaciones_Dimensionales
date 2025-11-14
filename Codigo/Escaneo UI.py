import cv2
import numpy as np
import math
import serial
import time
import json
import sys
import tkinter as tk
from tkinter import messagebox, ttk
import threading
from PIL import Image, ImageTk
import pyvista as pv

# Archivos de configuración
SETUP = "Setup.json"
CALIBRACION = "CalibracionZoom.npz"
PARAMETROS = "Parametros.json"
OUTPUT = "Escaneo.csv"
CONFIG_ESCANEO = "Configuracion_Escaneo.json"

# Parámetros por defecto
BAUDRATE = 115200

# Variables globales
IND_CAM, THRESHOLD, ARDUINO = None, None, None
THETA_DEG, CAM_RADIUS, CAM_HEIGHT, CAM_PITCH = (None,) * 4
OFFSET_RADIAL, OFFSET_ANGLE_DEG, OFFSET_Z, SCALE_FACTOR = (None,) * 4
XY_ASPECT_FACTOR, Z_ASPECT_FACTOR = (None,) * 2
Z_MIN, Z_MAX, MODULO_MAX = (None,) * 3

# Configuración de escaneo
ESCANEO_CONFIG = {
    "num_muestras": 10,
    "tiempo_rotacion": 40.0 # segundos
}

ser = None
escaneo_activo = False
thread_escaneo = None


# =============================================================================
# FUNCIONES DE CARGA DE PARÁMETROS
# =============================================================================

def cargar_parametros():
    """Carga todos los parámetros del sistema."""
    global IND_CAM, THRESHOLD, ARDUINO
    global THETA_DEG, CAM_RADIUS, CAM_HEIGHT, CAM_PITCH
    global OFFSET_RADIAL, OFFSET_ANGLE_DEG, OFFSET_Z, SCALE_FACTOR
    global XY_ASPECT_FACTOR, Z_ASPECT_FACTOR, Z_MIN, Z_MAX, MODULO_MAX
    
    try:
        # Cargar parámetros de escaneo
        with open(PARAMETROS, 'r') as f:
            params = json.load(f)
        
        THETA_DEG = params['THETA_DEG']
        CAM_RADIUS = params['CAM_RADIUS']
        CAM_HEIGHT = params['CAM_HEIGHT']
        CAM_PITCH = params['CAM_PITCH']
        OFFSET_RADIAL = params['OFFSET_RADIAL']
        OFFSET_ANGLE_DEG = params['OFFSET_ANGLE_DEG']
        OFFSET_Z = params['OFFSET_Z']
        SCALE_FACTOR = params['SCALE_FACTOR']
        XY_ASPECT_FACTOR = params['XY_ASPECT_FACTOR']
        Z_ASPECT_FACTOR = params['Z_ASPECT_FACTOR']
        Z_MIN = params['Z_MIN']
        Z_MAX = params['Z_MAX']
        MODULO_MAX = params['MODULO_MAX']
        
        # Cargar configuración de cámara
        with open(SETUP, 'r') as f:
            config = json.load(f)
        IND_CAM = config["camera_index"]
        THRESHOLD = config["threshold"]
        ARDUINO = config["arduino_port"]
        
        # Cargar calibración
        calib = np.load(CALIBRACION)
        K = calib["K"]
        dist = calib["dist"]
        
        return K, dist, True
    
    except Exception as e:
        print(f"Error cargando parámetros: {e}")
        return None, None, False


def cargar_config_escaneo():
    """Carga la configuración de escaneo."""
    global ESCANEO_CONFIG
    
    if not os.path.exists(CONFIG_ESCANEO):
        guardar_config_escaneo()
        return
    
    try:
        with open(CONFIG_ESCANEO, 'r') as f:
            ESCANEO_CONFIG = json.load(f)
    except:
        pass


def guardar_config_escaneo():
    """Guarda la configuración de escaneo."""
    try:
        with open(CONFIG_ESCANEO, 'w') as f:
            json.dump(ESCANEO_CONFIG, f, indent=4)
    except:
        pass


import os


# =============================================================================
# FUNCIONES DE CAPTURA Y PROCESAMIENTO
# =============================================================================

def capturar_laser_desde_frame(frame, threshold_val, k_matrix, coef_dist):
    """Captura láser desde un frame ya disponible."""
    if frame is None:
        return np.array([]), None

    # Extraer canal rojo
    red_channel = frame[:, :, 2]
    red_channel = cv2.GaussianBlur(red_channel, (15, 1), 0)

    # Detectar píxeles del láser
    laser_pixels = []
    for y, row in enumerate(red_channel):
        max_val = np.max(row)
        if max_val > threshold_val:
            x = np.argmax(row)
            laser_pixels.append([x, y])

    if not laser_pixels:
        return np.array([]), frame

    laser_pixels = np.array(laser_pixels, dtype=np.float32)
    undistorted = cv2.undistortPoints(laser_pixels.reshape(-1, 1, 2), k_matrix, coef_dist).reshape(-1, 2)
    
    rays = np.hstack([undistorted, np.ones((undistorted.shape[0], 1))])
    rays /= np.linalg.norm(rays, axis=1, keepdims=True)

    return rays, frame


def capturar_laser(threshold_val, k_matrix, coef_dist):
    """Captura un frame y detecta el láser (fallback)."""
    cap = cv2.VideoCapture(IND_CAM)
    if not cap.isOpened():
        return np.array([]), None

    time.sleep(0.1)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return np.array([]), None

    return capturar_laser_desde_frame(frame, threshold_val, k_matrix, coef_dist)


def intersectar_rayos_y_calcular_perfil(rays):
    """Intersecta rayos con el plano de láser."""
    theta_rad = np.radians(THETA_DEG)
    pitch_rad = np.radians(CAM_PITCH)
    normal_plano_mundo = np.array([np.sin(theta_rad), -np.cos(theta_rad), 0])
    T_cam_mundo = np.array([CAM_RADIUS, 0, CAM_HEIGHT])
    R_z_neg90 = np.array([[0,1,0],[-1,0,0],[0,0,1]]) 
    R_y_neg90 = np.array([[0,0,-1],[0,1,0],[1,0,0]])
    R_cam_base = R_y_neg90 @ R_z_neg90
    R_pitch = np.array([[1,0,0],[0,np.cos(pitch_rad),-np.sin(pitch_rad)],[0,np.sin(pitch_rad),np.cos(pitch_rad)]])
    R_cam_a_mundo = R_cam_base @ R_pitch
    points_2d = []

    for ray_cam in rays:
        ray_mundo = R_cam_a_mundo @ ray_cam
        denom = np.dot(normal_plano_mundo, ray_mundo)
        if abs(denom) < 1e-9:
            continue
        t = np.dot(normal_plano_mundo, T_cam_mundo) / -denom
        if t > 0:
            punto = T_cam_mundo + t * ray_mundo
            radius = np.sqrt(punto[0]**2 + punto[1]**2) * np.sign(ray_cam[0])
            points_2d.append([radius, punto[2]])
    
    return np.array(points_2d) if points_2d else np.array([])


# =============================================================================
# INTERFAZ GRÁFICA CON TKINTER
# =============================================================================

class EstacionEscaneo:
    def __init__(self, root):
        self.root = root
        self.root.title("Estación de Escaneo 3D")
        self.root.geometry("1024x768")
        self.root.configure(bg='#1a1a2e')
        
        # Variables de estado
        self.escaneo_en_curso = False
        self.frame_actual = None
        self.K_matrix = None
        self.dist_coef = None
        self.thread_escaneo = None
        self.thread_arduino = None
        
        # Conexión persistente a cámara (para evitar problemas con OBS virtual)
        self.cap = None
        self.cap_lock = threading.Lock()
        
        # Widgets para escaneo (inicializados como None)
        self.frame_progreso = None
        self.progress_bar = None
        self.label_tiempo = None
        self.label_estado = None
        self.frame_video = None
        
        # Cargar parámetros
        self.K_matrix, self.dist_coef, success = cargar_parametros()
        if not success:
            messagebox.showerror("Error", "No se pudieron cargar los parámetros del sistema")
            self.root.destroy()
            return
        
        cargar_config_escaneo()
        
        # Mostrar pantalla inicial (la conexión se hace cuando se comienza el escaneo)
        self.pantalla_inicio()
    
    def conectar_arduino(self):
        """Intenta conectar a Arduino."""
        global ser
        try:
            ser = serial.Serial(ARDUINO, BAUDRATE, timeout=2)
            time.sleep(2)
            # Limpiar buffer de entrada
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar a Arduino: {e}")
            return False
    
    def limpiar_ventana(self):
        """Limpia la ventana."""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def pantalla_inicio(self):
        """Pantalla inicial con instrucciones."""
        self.limpiar_ventana()
        
        # Título principal
        titulo = tk.Label(self.root, 
                         text="Estación de Escaneo 3D",
                         font=("Segoe UI", 32, "bold"), 
                         bg='#1a1a2e', fg='white')
        titulo.pack(pady=30)
        
        # Subtítulo
        subtitulo = tk.Label(self.root,
                            text="Análisis de Desviaciones Dimensionales",
                            font=("Segoe UI", 11),
                            bg='#1a1a2e', fg='#b0b0b0')
        subtitulo.pack(pady=5)
        
        # Separador
        sep = tk.Frame(self.root, bg='#3b24c8', height=2)
        sep.pack(fill='x', pady=20)
        
        # Instrucción
        instruccion = tk.Label(self.root,
                              text="Coloca la pieza en la cinta",
                              font=("Segoe UI", 13),
                              bg='#1a1a2e', fg='#e0e0e0')
        instruccion.pack(pady=40)
        
        # Frame para botones
        frame_botones = tk.Frame(self.root, bg='#1a1a2e')
        frame_botones.pack(pady=60, expand=True)
        
        # Botón inicio
        btn_inicio = tk.Button(frame_botones,
                              text="COMENZAR ESCANEO",
                              font=("Segoe UI", 12, "bold"),
                              width=28, height=3,
                              bg='#3b24c8', fg='white',
                              command=self.comenzar_escaneo,
                              cursor="hand2",
                              relief=tk.FLAT,
                              activebackground='#5636d3',
                              activeforeground='white')
        btn_inicio.pack(pady=20)
        
        # Frame inferior con botón de configuración
        frame_inferior = tk.Frame(self.root, bg='#1a1a2e')
        frame_inferior.pack(side='bottom', fill='x', padx=20, pady=20)
        
        btn_config = tk.Button(frame_inferior,
                              text="⚙",
                              font=("Segoe UI", 18),
                              width=3, height=1,
                              bg='white', fg='#3b24c8',
                              command=self.pantalla_configuracion,
                              cursor="hand2",
                              relief=tk.FLAT,
                              activebackground='#f0f0f0',
                              activeforeground='#3b24c8')
        btn_config.pack(anchor='se')
    
    def pantalla_configuracion(self):
        """Pantalla de configuración."""
        self.limpiar_ventana()
        
        titulo = tk.Label(self.root,
                         text="Configuración del Escaneo",
                         font=("Segoe UI", 24, "bold"),
                         bg='#1a1a2e', fg='white')
        titulo.pack(pady=20)
        
        # Separador
        sep = tk.Frame(self.root, bg='#3b24c8', height=2)
        sep.pack(fill='x', pady=10)
        
        # Frame central
        frame_config = tk.Frame(self.root, bg='#1a1a2e')
        frame_config.pack(pady=40, padx=40, fill='both', expand=True)
        
        # Número de muestras
        label_muestras = tk.Label(frame_config,
                                 text="Número de muestras:",
                                 font=("Segoe UI", 11, "bold"),
                                 bg='#1a1a2e', fg='white')
        label_muestras.pack(anchor='w', pady=15)
        
        frame_muestras = tk.Frame(frame_config, bg='#1a1a2e')
        frame_muestras.pack(anchor='w', pady=8)
        
        self.entry_muestras = tk.Entry(frame_muestras, font=("Segoe UI", 11), width=10,
                                       bg='#2d2d44', fg='white', insertbackground='#3b24c8',
                                       relief=tk.FLAT, bd=0)
        self.entry_muestras.pack(side='left', padx=5)
        self.entry_muestras.insert(0, str(ESCANEO_CONFIG["num_muestras"]))
        
        label_muestra_desc = tk.Label(frame_muestras,
                                     text="muestras",
                                     font=("Segoe UI", 10),
                                     bg='#1a1a2e', fg='#b0b0b0')
        label_muestra_desc.pack(side='left', padx=5)
        
        label_info = tk.Label(frame_config,
                             text="Tiempo estimado = muestras × 2 segundos",
                             font=("Segoe UI", 9, "italic"),
                             bg='#1a1a2e', fg='#707070')
        label_info.pack(anchor='w', pady=20)
        
        # Botones
        frame_botones = tk.Frame(self.root, bg='#1a1a2e')
        frame_botones.pack(pady=20)
        
        btn_guardar = tk.Button(frame_botones,
                               text="GUARDAR",
                               font=("Segoe UI", 10, "bold"),
                               bg='#3b24c8', fg='white',
                               command=self.guardar_configuracion,
                               cursor="hand2", width=14, height=2,
                               relief=tk.FLAT,
                               activebackground='#5636d3',
                               activeforeground='white')
        btn_guardar.pack(side='left', padx=10)
        
        btn_volver = tk.Button(frame_botones,
                              text="VOLVER",
                              font=("Segoe UI", 10, "bold"),
                              bg='#2d2d44', fg='#e0e0e0',
                              command=self.pantalla_inicio,
                              cursor="hand2", width=14, height=2,
                              relief=tk.FLAT,
                              activebackground='#3b3b54',
                              activeforeground='white')
        btn_volver.pack(side='left', padx=10)
    
    def guardar_configuracion(self):
        """Guarda la configuración."""
        try:
            num_muestras = int(self.entry_muestras.get())
            
            if num_muestras < 1:
                messagebox.showerror("Error", "Valores no válidos")
                return
            
            ESCANEO_CONFIG["num_muestras"] = num_muestras
            guardar_config_escaneo()
            
            messagebox.showinfo("Éxito", "Configuración guardada correctamente")
            self.pantalla_inicio()
        except ValueError:
            messagebox.showerror("Error", "Ingresa números válidos")
    
    def comenzar_escaneo(self):
        """Comienza el escaneo."""
        # Inicializar la cámara de forma persistente
        if not self.inicializar_camara():
            messagebox.showerror("Error", "No se pudo inicializar la cámara")
            return
        
        # Conectar a Arduino justo ahora
        if not self.conectar_arduino():
            self.liberar_camara()
            messagebox.showerror("Error", "No hay conexión con Arduino")
            return
        
        self.escaneo_en_curso = True
        self.thread_escaneo = threading.Thread(target=self._ejecutar_escaneo, daemon=True)
        self.thread_escaneo.start()
        
        # Mostrar pantalla de escaneo
        self.pantalla_escaneo_vivo()
    
    def pantalla_escaneo_vivo(self):
        """Pantalla que muestra el escaneo en vivo."""
        self.limpiar_ventana()
        
        # Frame superior para el estado (recuadro destacado)
        frame_estado = tk.Frame(self.root, bg='#3b24c8', height=60)
        frame_estado.pack(fill='x', padx=0, pady=0)
        frame_estado.pack_propagate(False)
        
        # Título con estado (grande y visible)
        self.label_estado = tk.Label(frame_estado,
                                    text="Estado: Conectando con Arduino...",
                                    font=("Segoe UI", 15, "bold"),
                                    bg='#3b24c8', fg='white')
        self.label_estado.pack(pady=12, expand=True)
        
        # Frame para video (640x480 - relación original de la cámara)
        self.frame_video = tk.Label(self.root, bg='#0a0a0f', width=640, height=480)
        self.frame_video.pack(pady=12)
        
        # Frame para progreso (inicialmente oculto)
        frame_progreso = tk.Frame(self.root, bg='#1a1a2e')
        frame_progreso.pack(fill='x', padx=20, pady=10)
        
        label_progreso = tk.Label(frame_progreso,
                                 text="Progreso del escaneo:",
                                 font=("Segoe UI", 9, "bold"),
                                 bg='#1a1a2e', fg='#3b24c8')
        label_progreso.pack(anchor='w', pady=3)
        self.label_progreso_titulo = label_progreso
        
        self.progress_bar = ttk.Progressbar(frame_progreso,
                                           length=400, mode='determinate',
                                           maximum=100)
        self.progress_bar.pack(anchor='w', pady=4, fill='x')
        self.frame_progreso = frame_progreso
        
        # Configurar estilo de la barra de progreso
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TProgressbar", background='#00d966', troughcolor='#2d2d44', 
                       bordercolor='#3b24c8', lightcolor='#00d966', darkcolor='#00d966')
        
        self.label_tiempo = tk.Label(frame_progreso,
                                    text="Tiempo restante: --:--",
                                    font=("Segoe UI", 9),
                                    bg='#1a1a2e', fg='#b0b0b0')
        self.label_tiempo.pack(anchor='w', pady=2)
        
        # Ocultar barra de progreso inicialmente
        frame_progreso.pack_forget()
        
        # Iniciar actualización de video
        self.actualizar_video_escaneo()
    
    def inicializar_camara(self):
        """Inicializa la conexión persistente a la cámara."""
        try:
            with self.cap_lock:
                if self.cap is None:
                    self.cap = cv2.VideoCapture(IND_CAM)
                    # Configurar para bajo buffer (importante para cámaras virtuales)
                    self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                    # Configurar formato y resolución
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    self.cap.set(cv2.CAP_PROP_FPS, 30)
                    # Esperar estabilización
                    for _ in range(5):
                        ret, _ = self.cap.read()
                        if not ret:
                            time.sleep(0.1)
                    return self.cap.isOpened()
        except Exception as e:
            print(f"Error inicializando cámara: {e}")
            return False
    
    def reconectar_camara(self):
        """Intenta reconectar la cámara."""
        try:
            with self.cap_lock:
                if self.cap is not None:
                    try:
                        self.cap.release()
                    except:
                        pass
                    self.cap = None
                    time.sleep(0.2)
                
                self.cap = cv2.VideoCapture(IND_CAM)
                self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                
                # Descartar primeros frames
                for _ in range(3):
                    self.cap.read()
                    time.sleep(0.05)
                
                return self.cap.isOpened()
        except Exception as e:
            print(f"Error reconectando cámara: {e}")
            return False
    
    def liberar_camara(self):
        """Libera la conexión a la cámara."""
        try:
            with self.cap_lock:
                if self.cap is not None:
                    try:
                        self.cap.release()
                    except:
                        pass
                    self.cap = None
        except:
            pass
    
    def capturar_laser_escaneo(self):
        """Captura láser usando la cámara persistente durante escaneo."""
        try:
            with self.cap_lock:
                if self.cap is None or not self.cap.isOpened():
                    return np.array([]), None
                
                # Leer frame
                ret, frame = self.cap.read()
                if not ret or frame is None:
                    return np.array([]), None
                
                # Procesar láser
                return capturar_laser_desde_frame(frame, THRESHOLD, self.K_matrix, self.dist_coef)
        except Exception as e:
            print(f"Error capturando láser: {e}")
            return np.array([]), None
    
    def actualizar_video_escaneo(self):
        """Actualiza el video en tiempo real durante escaneo."""
        if not self.escaneo_en_curso:
            return
        
        frame_exito = False
        try:
            with self.cap_lock:
                if self.cap is None or not self.cap.isOpened():
                    # Intentar reconectar
                    if not self.reconectar_camara():
                        self.root.after(33, self.actualizar_video_escaneo)
                        return
                
                # Intentar leer frame
                ret, frame = self.cap.read()
                
                if ret and frame is not None and frame.size > 0:
                    try:
                        # NO redimensionar, mantener 640x480 nativo
                        # Convertir a RGB
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        
                        # Convertir a PhotoImage (con manejo de excepción)
                        img = Image.fromarray(frame_rgb)
                        imgtk = ImageTk.PhotoImage(image=img)
                        
                        # Actualizar UI (en el thread principal)
                        if self.frame_video.winfo_exists():
                            self.frame_video.imgtk = imgtk
                            self.frame_video.config(image=imgtk)
                        frame_exito = True
                    except Exception as e:
                        print(f"Error procesando frame: {e}")
                else:
                    # Frame inválido, intentar reconectar en el próximo ciclo
                    print("Frame inválido recibido")
        
        except Exception as e:
            print(f"Error en actualizar_video_escaneo: {e}")
            # Intentar liberar y reconectar
            try:
                with self.cap_lock:
                    if self.cap is not None:
                        try:
                            self.cap.release()
                        except:
                            pass
                        self.cap = None
            except:
                pass
        
        # Actualizar cada 33ms (30 FPS) para video más fluido
        if self.escaneo_en_curso:
            self.root.after(33, self.actualizar_video_escaneo)
    
    def _ejecutar_escaneo(self):
        """Ejecuta el escaneo (en hilo separado)."""
        try:
            num_muestras = ESCANEO_CONFIG["num_muestras"]
            tiempo_rotacion = ESCANEO_CONFIG["tiempo_rotacion"]
            
            # ===== FASE 0: ESPERAR PREGUNTA DE MODO AUTOMÁTICO =====
            self.actualizar_estado("Esperando respuesta de Arduino...")
            
            tiempo_espera_modo = time.time()
            modo_recibido = False
            
            while not modo_recibido and (time.time() - tiempo_espera_modo) < 10:
                if ser.in_waiting > 0:
                    linea = ser.readline().decode('utf-8', errors='ignore').strip()
                    if linea:
                        if "modo" in linea.lower() and "automático" in linea.lower():
                            modo_recibido = True
                            break
                time.sleep(0.1)
            
            if not modo_recibido:
                self.actualizar_estado("ERROR: Arduino no envió pregunta de modo")
                self.escaneo_en_curso = False
                return
            
            # Enviar "y" para modo automático
            self.actualizar_estado("Iniciando escaneo...")
            ser.write(b"y")
            ser.flush()
            time.sleep(0.5)
            
            # ===== FASE 1: ESPERAR HOMING Y CENTRADO =====
            # Mostrar estado del Arduino sin barra de progreso
            tiempo_inicio_espera = time.time()
            muestras_preguntadas = False
            
            while not muestras_preguntadas and (time.time() - tiempo_inicio_espera) < 120:
                if not self.escaneo_en_curso:
                    self.actualizar_estado("Escaneo cancelado por usuario")
                    return
                
                try:
                    if ser.in_waiting > 0:
                        linea = ser.readline().decode('utf-8', errors='ignore').strip()
                        
                        if linea:
                            # Mostrar estado del Arduino
                            if "homing" in linea.lower():
                                self.actualizar_estado("Realizando homing...")
                            elif "centrando" in linea.lower() or "posicion" in linea.lower() or "avanzando" in linea.lower():
                                self.actualizar_estado("Centrando pieza...")
                            elif "cuantas muestras" in linea.lower() or "muestras desea" in linea.lower():
                                # Arduino pide el número de muestras
                                muestras_preguntadas = True
                            else:
                                # Mostrar cualquier otro mensaje de Arduino
                                self.actualizar_estado(linea)
                except:
                    pass
                
                time.sleep(0.2)
            
            if not muestras_preguntadas:
                self.actualizar_estado("ERROR: Timeout - Arduino no preguntó por muestras")
                self.escaneo_en_curso = False
                return
            
            # ===== FASE 2: ENVIAR NÚMERO DE MUESTRAS =====
            self.actualizar_estado(f"Enviando: {num_muestras} muestras...")
            print(f"\n[FASE 2] Enviando número de muestras: {num_muestras}")
            ser.write(f"{num_muestras}\n".encode())
            ser.flush()
            time.sleep(0.5)
            
            # Esperar confirmación de que inicia escaneo
            tiempo_espera_inicio = time.time()
            escaneo_iniciado = False
            
            while not escaneo_iniciado and (time.time() - tiempo_espera_inicio) < 10:
                if ser.in_waiting > 0:
                    linea = ser.readline().decode('utf-8', errors='ignore').strip()
                    if linea:
                        print(f"[FASE 2] Recibido: {linea}")
                        self.actualizar_estado(linea)
                        if "iniciando" in linea.lower() or "escaneo" in linea.lower():
                            escaneo_iniciado = True
                            print(f"[FASE 2] ✓ Confirmación de inicio recibida")
                time.sleep(0.2)
            
            if not escaneo_iniciado:
                print(f"[FASE 2] ⚠ Timeout, pero pasando a FASE 3 de todas formas...")
            
            # ===== FASE 3: MOSTRAR BARRA DE PROGRESO Y CAPTURAR DATOS =====
            # AHORA mostramos la barra de progreso
            print(f"\n[FASE 3] Iniciando escaneo...")
            print(f"[FASE 3] Muestras solicitadas: {num_muestras}")
            self.mostrar_barra_progreso()
            
            points_all = []
            tiempo_total_estimado = (num_muestras * 2) + tiempo_rotacion
            tiempo_inicio_progreso = time.time()
            
            muestras_recibidas = 0
            tiempo_espera_escaneo = time.time()
            
            print(f"[FASE 3] Esperando ángulos de Arduino...")
            
            # Esperar mientras Arduino envía ángulos (una muestra por ángulo)
            while muestras_recibidas < num_muestras and (time.time() - tiempo_espera_escaneo) < (tiempo_total_estimado + 30):
                if not self.escaneo_en_curso:
                    break
                
                # Leer mensajes de Arduino
                if ser.in_waiting > 0:
                    linea = ser.readline().decode('utf-8', errors='ignore').strip()
                    if linea:
                        print(f"[FASE 3] RAW: '{linea}'")
                        
                        # Intentar parsear como número (ángulo)
                        es_muestra = False
                        try:
                            angulo_valor = float(linea)
                            if 0 <= angulo_valor <= 360:
                                es_muestra = True
                                print(f"[FASE 3] ✓ Ángulo {angulo_valor:.2f}° detectado")
                        except ValueError:
                            pass
                        
                        if es_muestra:
                            muestras_recibidas += 1
                            print(f"[FASE 3] ✓ Muestra {muestras_recibidas}/{num_muestras} recibida")
                            
                            self.actualizar_estado(f"Escaneando... Muestra: {muestras_recibidas}/{num_muestras}")
                            
                            # Capturar láser (usando cámara persistente)
                            rays, frame = self.capturar_laser_escaneo()
                            
                            if rays.shape[0] > 0:
                                perfil_2d = intersectar_rayos_y_calcular_perfil(rays)
                                if perfil_2d.shape[0] > 0:
                                    # Transformar puntos
                                    radii = np.abs(perfil_2d[:, 0] + OFFSET_RADIAL)
                                    heights = -perfil_2d[:, 1]
                                    
                                    # Ángulo: se calcula basado en muestras recibidas
                                    angle_deg = ((muestras_recibidas - 1) * 360.0 / num_muestras) + OFFSET_ANGLE_DEG
                                    angle_rad = np.radians(angle_deg)
                                    
                                    puntos_transformados = np.column_stack((
                                        radii * np.cos(angle_rad),
                                        radii * np.sin(angle_rad),
                                        heights
                                    ))
                                    
                                    puntos_transformados[:, 2] += OFFSET_Z
                                    puntos_transformados *= SCALE_FACTOR
                                    puntos_transformados[:, :2] *= XY_ASPECT_FACTOR
                                    puntos_transformados[:, 2] *= Z_ASPECT_FACTOR
                                    
                                    points_all.append(puntos_transformados)
                            
                            # Actualizar barra de progreso
                            self.actualizar_progreso(muestras_recibidas, num_muestras, tiempo_total_estimado, tiempo_inicio_progreso)
                
                time.sleep(0.1)
            
            # ===== FASE 4: ESPERAR FINALIZACIÓN Y EXPULSIÓN (BARRA SIGUE VISIBLE) =====
            print(f"\n[FASE 4] Esperando finalización y expulsión...")
            
            tiempo_espera_fin = time.time()
            escaneo_completado = False
            pieza_expulsada = False
            
            # Esperar mientras Arduino confirma escaneo finalizado y pieza expulsada
            while (time.time() - tiempo_espera_fin) < 60:
                if ser.in_waiting > 0:
                    linea = ser.readline().decode('utf-8', errors='ignore').strip()
                    if linea:
                        print(f"[FASE 4] Recibido: {linea}")
                        
                        # Detectar estados
                        if "escaneo finalizado" in linea.lower():
                            escaneo_completado = True
                            print(f"[FASE 4] ✓ Escaneo finalizado")
                        
                        if "expulsando" in linea.lower():
                            self.actualizar_estado("Expulsando pieza...")
                            print(f"[FASE 4] → Expulsando pieza...")
                        
                        if "pieza expulsada" in linea.lower():
                            pieza_expulsada = True
                            print(f"[FASE 4] ✓ Pieza expulsada")
                            self.actualizar_estado("Pieza expulsada")
                            # AHORA ocultamos la barra cuando la pieza está expulsada
                            self.ocultar_barra_progreso()
                            break
                        
                        # Mostrar otros mensajes
                        if not ("expulsando" in linea.lower() or "pieza expulsada" in linea.lower() or 
                               "escaneo finalizado" in linea.lower() or "motores" in linea.lower()):
                            self.actualizar_estado(linea)
                
                time.sleep(0.2)
            
            # Si pasó el timeout sin confirmación, ocultar barra igual
            if not pieza_expulsada:
                print(f"[FASE 4] ⚠ Timeout esperando confirmación de expulsión")
                self.ocultar_barra_progreso()
                self.actualizar_estado("Timeout - procesando resultados...")
            
            # ===== FASE 5: PROCESAMIENTO Y RESULTADOS =====
            print(f"\n[FASE 5] Procesando nube de puntos...")
            if points_all:
                nube_completa = np.vstack(points_all)
                mask = (
                    (nube_completa[:, 2] >= Z_MIN) &
                    (nube_completa[:, 2] <= Z_MAX) &
                    (np.linalg.norm(nube_completa[:, :2], axis=1) <= MODULO_MAX)
                )
                nube_filtrada = nube_completa[mask]
                nube_filtrada[:, 2] -= Z_MIN
                
                # Guardar archivo
                np.savetxt(OUTPUT, nube_filtrada, delimiter=',',
                          header='X,Y,Z', comments='', fmt='%.6f')
                print(f"[FASE 5] ✓ Nube de puntos guardada: {OUTPUT}")
                
                # Mostrar resultados
                self.escaneo_en_curso = False
                self.pantalla_escaneo_completado(nube_filtrada, OUTPUT)
            else:
                self.actualizar_estado("ERROR: No se capturaron puntos")
                self.escaneo_en_curso = False
        
        except Exception as e:
            self.actualizar_estado(f"ERROR: {str(e)}")
            self.escaneo_en_curso = False
    
    def actualizar_estado(self, texto):
        """Actualiza el estado sin emojis."""
        try:
            self.label_estado.config(text=f"{texto}")
            self.root.update_idletasks()
        except:
            pass
    
    def mostrar_barra_progreso(self):
        """Muestra la barra de progreso."""
        try:
            if self.frame_progreso is None:
                print("⚠ frame_progreso es None, no se puede mostrar")
                return False
            
            # Mostrar explícitamente
            self.frame_progreso.pack(fill='x', padx=20, pady=10)
            self.root.update_idletasks()
            time.sleep(0.05)
            self.root.update_idletasks()
            print("✓ Barra de progreso MOSTRADA")
            return True
        except Exception as e:
            print(f"✗ Error mostrando barra: {e}")
            return False
    
    def ocultar_barra_progreso(self):
        """Oculta la barra de progreso."""
        try:
            if self.frame_progreso is None:
                print("⚠ frame_progreso es None, no se puede ocultar")
                return False
            
            self.frame_progreso.pack_forget()
            self.root.update_idletasks()
            print("✓ Barra de progreso OCULTA")
            return True
        except Exception as e:
            print(f"✗ Error ocultando barra: {e}")
            return False
    
    def actualizar_progreso(self, actual, total, tiempo_total, tiempo_inicio):
        """Actualiza la barra de progreso."""
        try:
            if self.progress_bar is None or self.label_tiempo is None:
                print(f"⚠ Widgets de progreso no inicializados")
                return False
            
            porcentaje = int((actual / total) * 100)
            self.progress_bar['value'] = porcentaje
            
            tiempo_transcurrido = time.time() - tiempo_inicio
            tiempo_restante = max(0, tiempo_total - tiempo_transcurrido)
            
            minutos = int(tiempo_restante // 60)
            segundos = int(tiempo_restante % 60)
            
            self.label_tiempo.config(text=f"Tiempo restante estimado: {minutos:02d}:{segundos:02d}")
            
            print(f"  → Progreso: {actual}/{total} ({porcentaje}%)")
            
            self.root.update_idletasks()
            return True
        except Exception as e:
            print(f"✗ Error actualizando progreso: {e}")
            return False
    
    def pantalla_escaneo_completado(self, nube_puntos, archivo_guardado):
        """Muestra cartel grande de escaneo completado."""
        self.limpiar_ventana()
        
        # Cartel grande con fondo degradado (oscuro a violeta)
        frame_cartel = tk.Frame(self.root, bg='#1a1a2e')
        frame_cartel.pack(fill='both', expand=True)
        
        titulo = tk.Label(frame_cartel,
                         text="ESCANEO COMPLETADO",
                         font=("Segoe UI", 42, "bold"),
                         bg='#1a1a2e', fg='#00d966')
        titulo.pack(pady=60)
        
        info_text = f"Puntos capturados: {nube_puntos.shape[0]}\nArchivo guardado correctamente"
        info = tk.Label(frame_cartel,
                       text=info_text,
                       font=("Segoe UI", 13),
                       bg='#1a1a2e', fg='#e0e0e0')
        info.pack(pady=30)
        
        # Botón para ver gráfico 3D
        btn_grafico = tk.Button(frame_cartel,
                               text="Ver Gráfico 3D",
                               font=("Segoe UI", 11, "bold"),
                               width=25, height=2,
                               bg='#3b24c8', fg='white',
                               command=lambda: self.mostrar_grafico_3d_y_volver(nube_puntos),
                               cursor="hand2",
                               relief=tk.FLAT,
                               activebackground='#5636d3',
                               activeforeground='white')
        btn_grafico.pack(pady=20)
        
        # Auto-mostrar gráfico después de 2 segundos
        self.root.after(2000, lambda: self.mostrar_grafico_3d_y_volver(nube_puntos))
    
    def mostrar_grafico_3d(self, nube_puntos):
        """Muestra el gráfico 3D."""
        try:
            plotter = pv.Plotter(window_size=(1024, 768))
            plotter.set_background('white')
            plotter.add_mesh(pv.PolyData(nube_puntos), color='red',
                           point_size=8, render_points_as_spheres=True)
            plotter.add_scalar_bar()
            plotter.show_grid()
            plotter.show_axes()
            plotter.view_isometric()
            plotter.show()
        except Exception as e:
            messagebox.showerror("Error", f"Error mostrando gráfico: {e}")
    
    def mostrar_grafico_3d_y_volver(self, nube_puntos):
        """Muestra el gráfico 3D y luego vuelve al inicio."""
        try:
            # Detener escaneo y liberar recursos
            self.escaneo_en_curso = False
            self.liberar_camara()
            self.mostrar_grafico_3d(nube_puntos)
        except:
            pass
        finally:
            self.pantalla_inicio()
    
    def pantalla_expulsion(self):
        """Pantalla de expulsión de pieza."""
        self.limpiar_ventana()
        
        titulo = tk.Label(self.root,
                         text="Pieza Expulsada",
                         font=("Arial", 24, "bold"),
                         bg='white', fg='#333')
        titulo.pack(pady=40)
        
        mensaje = tk.Label(self.root,
                          text="El escaneo ha sido completado\nPuede retirar la pieza",
                          font=("Arial", 14),
                          bg='white', fg='#666')
        mensaje.pack(pady=40)
        
        # Botón para volver
        btn_volver = tk.Button(self.root,
                              text="Volver al Inicio",
                              font=("Arial", 12, "bold"),
                              width=20, height=2,
                              bg='#4CAF50', fg='white',
                              command=self.pantalla_inicio,
                              cursor="hand2")
        btn_volver.pack(pady=40)


# =============================================================================
# PROGRAMA PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = EstacionEscaneo(root)
    root.mainloop()
