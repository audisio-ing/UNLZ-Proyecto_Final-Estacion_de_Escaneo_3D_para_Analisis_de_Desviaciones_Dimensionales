import numpy as np
import pyvista as pv
from scipy.spatial import KDTree
import os
import time
import sys
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import threading

# Archivo de configuración unificado
CONFIG_FILE = "Configuracion.json"

# Directorio para escaneos (carpeta raíz, no Datos)
# El script se ejecuta desde Datos, así que subimos un nivel con parent
SCANS_DIR = Path.cwd().parent / 'Escaneos'
SCANS_DIR.mkdir(exist_ok=True)

# Parámetros del algoritmo de alineación
angulo_paso = 45                # Ángulo grueso (grados)
iteraciones = 5                 # Número de iteraciones del refinamiento
num_muestras = 30000            # Número máximo de puntos a muestrear

# Umbral de Chamfer (fracción de la diagonal) para CÁLCULO de similitud
umbral_chamfer_frac = 0.25

# Multiplicador para la sensibilidad del GRÁFICO
FACTOR_VISUAL_GRADIENTE = 12.5

# Variable global para configuración
CONFIG = {
    "piezas": {},
    "umbral_identificacion": 85.0,
    "archivo_escaneo": ""
}


def load_config():
    """Carga la configuración de comparación desde el archivo unificado."""
    global CONFIG
    try:
        if not os.path.exists(CONFIG_FILE):
            print(f"Archivo de configuración no encontrado: {CONFIG_FILE}")
            return False
            
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        
        comparacion = config.get('parametros_comparacion', {})
        CONFIG = {
            "piezas": comparacion.get("piezas", {}),
            "umbral_identificacion": comparacion.get("umbral_identificacion", 85.0),
            "archivo_escaneo": str(SCANS_DIR / "Escaneo.csv")
        }
        return True
    except Exception as e:
        print(f"Error cargando configuración: {e}")
        return False


def save_config():
    """Guarda la configuración de comparación en el archivo unificado."""
    global CONFIG
    try:
        # Cargar configuración completa existente
        if not os.path.exists(CONFIG_FILE):
            print(f"Archivo de configuración no existe: {CONFIG_FILE}")
            return False
            
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        
        # Actualizar solo la sección parametros_comparacion
        config['parametros_comparacion'] = {
            "piezas": CONFIG.get("piezas", {}),
            "umbral_identificacion": CONFIG.get("umbral_identificacion", 85.0)
        }
        
        # Guardar de vuelta
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print(f"Error guardando configuración: {e}")
        return False



# Cargar configuración al iniciar
load_config()


# =============================================================================
# FUNCIONES DE UTILIDAD
# =============================================================================

# Centra la nube de puntos
def center_cloud(points):
    if points.size == 0:
        return points, np.array([0,0,0])
    # Calcula el centroide solo en X e Y
    centroid = np.array([np.mean(points[:, 0]), np.mean(points[:, 1]), 0])
    # Resta el centroide a todos los puntos (pero Z permanece igual)
    return points - centroid, centroid

def rotate_z(points, angle_deg):
    angle_rad = np.radians(angle_deg)
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)
    rotation_matrix = np.array([
        [cos_a, -sin_a, 0],
        [sin_a,  cos_a, 0],
        [0,      0,     1]
    ])
    return points @ rotation_matrix.T

def get_chamfer_and_dists(patron, comparada):
    """Calcula la distancia Chamfer."""
    arbol_patron = KDTree(patron)
    arbol_comparada = KDTree(comparada)

    dists_comparada_a_patron, _ = arbol_patron.query(comparada, k=1)
    dists_patron_a_comparada, _ = arbol_comparada.query(patron, k=1)

    distancia_chamfer = np.mean(dists_comparada_a_patron) + np.mean(dists_patron_a_comparada)
    return distancia_chamfer, dists_comparada_a_patron

def get_similarity_percent(patron, distancia_chamfer):
    """Convierte la distancia Chamfer en porcentaje de similitud (función lineal)."""
    min_coords = np.min(patron, axis=0)
    max_coords = np.max(patron, axis=0)
    diagonal_vector = max_coords - min_coords
    norm_factor = np.linalg.norm(diagonal_vector)

    if norm_factor == 0:
        return 100.0 if distancia_chamfer == 0 else 0.0

    # Umbral para el CÁLCULO
    threshold_value = max(1e-9, umbral_chamfer_frac * norm_factor)
    # Normalización lineal: 100% cuando distancia=0, 0% cuando distancia=threshold
    similarity_percent = max(0.0, min(100.0, (1.0 - distancia_chamfer / threshold_value) * 100.0))

    return similarity_percent

# Rota la pieza para encontrar la mejor alineación
def find_best_alignment(patron, comparada):
    paso = int(angulo_paso) if angulo_paso >= 1 else 5
    lista_angulos = np.arange(0, 360, paso)

    mejor_angulo = 0.0
    mejor_distancia = np.inf
    mejores_distancias_por_punto = None
    mejor_nube_rotada = comparada

    # Búsqueda gruesa
    for ang in lista_angulos:
        rotada = rotate_z(comparada, ang)
        dist_chamfer, dists_puntos = get_chamfer_and_dists(patron, rotada)
        if dist_chamfer < mejor_distancia:
            mejor_distancia = dist_chamfer
            mejor_angulo = ang
            mejores_distancias_por_punto = dists_puntos
            mejor_nube_rotada = rotada

    # Refinamiento fino
    intervalo = float(angulo_paso / 2)
    for i in range(int(iteraciones)):
        mitad = intervalo / 2.0
        candidatos = np.mod([mejor_angulo - mitad, mejor_angulo + mitad], 360)
        for ang in candidatos:
            rotada = rotate_z(comparada, ang)
            dist_chamfer, dists_puntos = get_chamfer_and_dists(patron, rotada)
            if dist_chamfer < mejor_distancia:
                mejor_distancia = dist_chamfer
                mejor_angulo = float(ang)
                mejores_distancias_por_punto = dists_puntos
                mejor_nube_rotada = rotada
        intervalo = mitad

    return float(mejor_angulo % 360), mejor_distancia, mejores_distancias_por_punto, mejor_nube_rotada

def downsample_cloud(points, max_points):
    """Reduce el número de puntos de una nube si es demasiado grande."""
    if len(points) > max_points:
        indices = np.random.choice(len(points), max_points, replace=False)
        return points[indices]
    return points


# =============================================================================
# FUNCIONES DE CARGA Y COMPARACIÓN
# =============================================================================

def _load_csv_points(filepath):
    """Carga puntos desde un archivo .csv (X,Y,Z), saltando la primera fila (cabecera)."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Archivo no encontrado: '{filepath}'")
    try:
        points = np.loadtxt(filepath, delimiter=',', skiprows=1, dtype=np.float64)
        if points.ndim != 2 or points.shape[1] < 3:
            raise ValueError("El archivo CSV no tiene el formato esperado (min. 3 columnas).")
        return points[:, :3]
    except Exception as e:
        raise IOError(f"Error al leer/procesar el CSV '{filepath}': {e}")


def _run_comparison(file_patron, puntos_comparada_centrada):
    """(MODIFICADO) Función auxiliar que ejecuta todo el flujo de comparación."""
    try:
        # Cargar patrón (con la nueva función CSV)
        puntos_patron_original = _load_csv_points(file_patron)
        
        # (NUEVO) Centrar el patrón
        puntos_patron_centrado, _ = center_cloud(puntos_patron_original)
        
        # Validar puntos (Patrón y Escaneada)
        if not np.all(np.isfinite(puntos_patron_centrado)) or not np.all(np.isfinite(puntos_comparada_centrada)):
            return 0.0, None, None, None
        
        # Downsampling (usando las nubes centradas)
        puntos_patron_down = downsample_cloud(puntos_patron_centrado, num_muestras)
        puntos_comparada_down = downsample_cloud(puntos_comparada_centrada, num_muestras)
        
        # Alineación (usando las nubes centradas y reducidas)
        mejor_angulo, mejor_distancia, _, nube_alineada_down = find_best_alignment(
            puntos_patron_down, puntos_comparada_down
        )
        
        # Similitud (calculada sobre las nubes reducidas)
        similarity = get_similarity_percent(puntos_patron_down, mejor_distancia)
        
        # Resultados finales (usando nubes completas y centradas para graficar)
        # Rota la nube comparada (completa y centrada)
        final_rotated_centrada = rotate_z(puntos_comparada_centrada, mejor_angulo)
        # Calcula las distancias finales entre el patrón (completo, centrado) y la nube rotada
        _, final_dists_original = get_chamfer_and_dists(puntos_patron_centrado, final_rotated_centrada)
        
        # Devuelve el porcentaje, la nube patrón (centrada) y la nube alineada (centrada)
        return similarity, puntos_patron_centrado, final_rotated_centrada, final_dists_original
    
    except FileNotFoundError as fe:
        return 0.0, None, None, None
    except Exception as e:
        return 0.0, None, None, None


def cargar_configuracion():
    """Carga la configuración desde el archivo JSON."""
    global CONFIG
    load_config()  # Usar la función load_config() que ya está optimizada
    return os.path.exists(CONFIG_FILE)

def guardar_configuracion():
    """Guarda la configuración en un archivo JSON."""
    save_config()  # Usar la función save_config() que ya está optimizada

def ejecutar_comparacion(archivo_escaneo, callback=None):
    """Ejecuta el proceso de comparación completo."""
    try:
        def mostrar_mensaje(msg):
            print(msg)
            if callback:
                callback(msg)
        
        mostrar_mensaje("1. Cargando archivo de escaneo...")
        puntos_comparada_original = _load_csv_points(archivo_escaneo)
        mostrar_mensaje(f"   ✓ Puntos cargados: {len(puntos_comparada_original)}")
        
        mostrar_mensaje("2. Centrando nube de puntos...")
        puntos_comparada_centrada, _ = center_cloud(puntos_comparada_original)
        mostrar_mensaje("   ✓ Nube centrada")
        
        if not np.all(np.isfinite(puntos_comparada_centrada)):
            return None, "Error: valores NaN/Infinitos en escaneado"
        
        mostrar_mensaje("3. Ejecutando comparaciones...")
        
        # Ejecutar comparaciones
        comparaciones = []
        piezas_list = list(CONFIG["piezas"].items())
        mostrar_mensaje(f"   Comparando con {len(piezas_list)} piezas patrón")
        
        for idx, (nombre, path_patron) in enumerate(piezas_list):
            mostrar_mensaje(f"   - Comparando con {nombre}...")
            sim, pat, comp, dists = _run_comparison(path_patron, puntos_comparada_centrada)
            mostrar_mensaje(f"     ✓ Similitud: {sim:.2f}%")
            comparaciones.append({
                "nombre": nombre,
                "similitud": sim,
                "patron": pat,
                "comparada": comp,
                "dists": dists
            })
        
        mostrar_mensaje("4. Seleccionando mejor coincidencia...")
        mejor_match = max(comparaciones, key=lambda x: x["similitud"])
        umbral = CONFIG.get("umbral_identificacion", 75.0)
        
        mostrar_mensaje(f"5. ✓ Pieza: {mejor_match['nombre']} ({mejor_match['similitud']:.2f}%)")
        mostrar_mensaje("Preparando resultado...")
        
        return {
            "aprobada": mejor_match["similitud"] >= umbral,
            "pieza": mejor_match["nombre"],
            "similitud": mejor_match["similitud"],
            "umbral": umbral,
            "patron": mejor_match["patron"],
            "comparada": mejor_match["comparada"],
            "dists": mejor_match["dists"],
            "comparaciones": comparaciones
        }, None
        
    except Exception as e:
        print(f"ERROR en ejecutar_comparacion: {e}")
        import traceback
        traceback.print_exc()
        return None, f"Error: {str(e)}"


# =============================================================================
# INTERFAZ GRÁFICA CON TKINTER
# =============================================================================

class AppComparacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Identificación de Piezas")
        self.root.geometry("1024x768")
        self.root.configure(bg='#1a1a2e')
        
        # Cargar configuración existente
        cargar_configuracion()
        
        self.pantalla_principal()
    
    def limpiar_ventana(self):
        """Limpia todos los widgets de la ventana."""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def pantalla_principal(self):
        """Pantalla inicial con dos opciones."""
        self.limpiar_ventana()
        
        # Título
        titulo = tk.Label(self.root, text="Sistema de Identificación de Piezas",
                         font=("Segoe UI", 32, "bold"), bg='#1a1a2e', fg='white')
        titulo.pack(pady=40)
        
        # Subtítulo
        subtitulo = tk.Label(self.root, text="Análisis de Desviaciones Dimensionales",
                            font=("Segoe UI", 11), bg='#1a1a2e', fg='#b0b0b0')
        subtitulo.pack(pady=5)
        
        # Separador
        sep = tk.Frame(self.root, bg='#3b24c8', height=2)
        sep.pack(fill='x', pady=20)
        
        # Marco para botones
        marco_botones = tk.Frame(self.root, bg='#1a1a2e')
        marco_botones.pack(pady=80, expand=True)
        
        # Botón Comparación (principal)
        btn_comparar = tk.Button(marco_botones, text="COMPARACIÓN",
                                font=("Segoe UI", 12, "bold"),
                                width=28, height=3,
                                bg='#3b24c8', fg='white',
                                command=self.pantalla_comparacion,
                                cursor="hand2",
                                relief=tk.FLAT,
                                activebackground='#5636d3',
                                activeforeground='white')
        btn_comparar.pack(pady=20)
        
        # Frame inferior con botón de configuración
        frame_inferior = tk.Frame(self.root, bg='#1a1a2e')
        frame_inferior.pack(side='bottom', fill='x', padx=20, pady=20)
        
        btn_config = tk.Button(frame_inferior, text="⚙",
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
        """Pantalla de configuración de piezas y umbral."""
        self.limpiar_ventana()
        
        # Título
        titulo = tk.Label(self.root, text="CONFIGURACIÓN",
                         font=("Segoe UI", 24, "bold"), bg='#1a1a2e', fg='white')
        titulo.pack(pady=20)
        
        # Frame scrollable
        canvas = tk.Canvas(self.root, bg='#1a1a2e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1a1a2e')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Variables para almacenar rutas
        self.rutas_piezas = {}
        self.entries_rutas = {}
        
        # Cargar rutas existentes
        for nombre in ["Pieza 1", "Pieza 2", "Pieza 3"]:
            if nombre in CONFIG["piezas"]:
                self.rutas_piezas[nombre] = CONFIG["piezas"][nombre]
        
        # Seleccionar archivos de patrón
        for i, nombre in enumerate(["Pieza 1", "Pieza 2", "Pieza 3"]):
            frame_pieza = tk.LabelFrame(scrollable_frame, text=nombre, font=("Segoe UI", 11, "bold"),
                                        bg='#2d2d44', fg='white', padx=10, pady=10)
            frame_pieza.pack(fill='x', padx=20, pady=10)
            
            # Frame para la ruta y botones
            frame_contenido = tk.Frame(frame_pieza, bg='#2d2d44')
            frame_contenido.pack(fill='x')
            
            # Label mostrando archivo seleccionado
            label_archivo = tk.Label(frame_contenido, text="Archivo: No seleccionado",
                                    font=("Segoe UI", 10), bg='#2d2d44', fg='#b0b0b0',
                                    wraplength=300, justify='left')
            label_archivo.pack(anchor='w', pady=5)
            self.entries_rutas[nombre] = label_archivo
            
            # Actualizar label si hay ruta previa
            if nombre in self.rutas_piezas:
                archivo = os.path.basename(self.rutas_piezas[nombre])
                label_archivo.config(text=f"Archivo: {archivo}")
            
            # Botones
            frame_botones = tk.Frame(frame_contenido, bg='#2d2d44')
            frame_botones.pack(fill='x', pady=5)
            
            btn_seleccionar = tk.Button(frame_botones, text="📁 Seleccionar Archivo",
                                       font=("Segoe UI", 10, "bold"), bg='#3b24c8', fg='white',
                                       command=lambda n=nombre, lbl=label_archivo: self.seleccionar_archivo_patron(n, lbl),
                                       cursor="hand2", relief=tk.FLAT,
                                       activebackground='#5636d3', activeforeground='white')
            btn_seleccionar.pack(side='left', padx=5)
            
            if nombre in self.rutas_piezas:
                btn_limpiar = tk.Button(frame_botones, text="🗑️ Limpiar",
                                       font=("Segoe UI", 9), bg='#f44336', fg='white',
                                       command=lambda n=nombre, lbl=label_archivo: self.limpiar_archivo_patron(n, lbl),
                                       cursor="hand2", relief=tk.FLAT,
                                       activebackground='#ff5555', activeforeground='white')
                btn_limpiar.pack(side='left', padx=2)
        
        # Separador
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', padx=20, pady=20)
        
        # Umbral de tolerancia
        frame_umbral = tk.LabelFrame(scrollable_frame, text="Umbral de Aceptación",
                                    font=("Segoe UI", 11, "bold"), bg='#2d2d44',
                                    fg='white', padx=10, pady=10)
        frame_umbral.pack(fill='x', padx=20, pady=10)
        
        label_umbral_desc = tk.Label(frame_umbral, 
                                    text="Porcentaje mínimo de similitud para aprobar (0-100%):",
                                    font=("Segoe UI", 10), bg='#2d2d44', fg='#b0b0b0')
        label_umbral_desc.pack(anchor='w', pady=5)
        
        frame_input_umbral = tk.Frame(frame_umbral, bg='#2d2d44')
        frame_input_umbral.pack(anchor='w', pady=5)
        
        self.entry_umbral = tk.Entry(frame_input_umbral, font=("Segoe UI", 12), width=8,
                                     bg='#3b3b5c', fg='white', insertbackground='white')
        self.entry_umbral.pack(side='left', padx=5)
        self.entry_umbral.insert(0, str(CONFIG.get("umbral_identificacion", 75.0)))
        
        label_porcento = tk.Label(frame_input_umbral, text="%", font=("Segoe UI", 12, "bold"),
                                 bg='#2d2d44', fg='white')
        label_porcento.pack(side='left', padx=5)
        
        # Recomendación
        label_recom = tk.Label(frame_umbral,
                              text="Recomendado: 85% (Estricto: 90%, Flexible: 80%)",
                              font=("Segoe UI", 9, "italic"), bg='#2d2d44', fg='#808080')
        label_recom.pack(anchor='w', pady=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botones de acción
        frame_acciones = tk.Frame(self.root, bg='#1a1a2e')
        frame_acciones.pack(pady=20)
        
        btn_guardar = tk.Button(frame_acciones, text="GUARDAR",
                               font=("Segoe UI", 12, "bold"),
                               bg='#00d966', fg='#1a1a2e',
                               command=self.guardar_config,
                               cursor="hand2", relief=tk.FLAT,
                               activebackground='#00ff7a', activeforeground='#1a1a2e',
                               padx=20, pady=10)
        btn_guardar.pack(side='left', padx=10)
        
        btn_cancelar = tk.Button(frame_acciones, text="CANCELAR",
                                font=("Segoe UI", 12, "bold"),
                                bg='#3b24c8', fg='white',
                                command=self.pantalla_principal,
                                cursor="hand2", relief=tk.FLAT,
                                activebackground='#5636d3', activeforeground='white',
                                padx=20, pady=10)
        btn_cancelar.pack(side='left', padx=10)
    
    def seleccionar_archivo_patron(self, nombre_pieza, label_widget):
        """Abre diálogo para seleccionar archivo patrón."""
        archivo = filedialog.askopenfilename(
            title=f"Seleccionar archivo patrón para {nombre_pieza}",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if archivo:
            self.rutas_piezas[nombre_pieza] = archivo
            nombre_archivo = os.path.basename(archivo)
            label_widget.config(text=f"Archivo: {nombre_archivo}")
    
    def limpiar_archivo_patron(self, nombre_pieza, label_widget):
        """Limpia el archivo seleccionado para una pieza."""
        if nombre_pieza in self.rutas_piezas:
            del self.rutas_piezas[nombre_pieza]
        label_widget.config(text="Archivo: No seleccionado")
    
    def guardar_config(self):
        """Guarda la configuración."""
        try:
            # Validar que se hayan ingresado archivos
            piezas_ingresadas = 0
            for nombre in ["Pieza 1", "Pieza 2", "Pieza 3"]:
                if nombre in self.rutas_piezas and self.rutas_piezas[nombre]:
                    piezas_ingresadas += 1
            
            if piezas_ingresadas == 0:
                messagebox.showerror("Error", "Debe seleccionar al menos una pieza patrón.")
                return
            
            # Actualizar configuración
            CONFIG["piezas"] = {}
            for nombre in ["Pieza 1", "Pieza 2", "Pieza 3"]:
                if nombre in self.rutas_piezas and self.rutas_piezas[nombre]:
                    CONFIG["piezas"][nombre] = self.rutas_piezas[nombre]
            
            try:
                umbral = float(self.entry_umbral.get())
                if umbral < 0 or umbral > 100:
                    raise ValueError("El umbral debe estar entre 0 y 100.")
                CONFIG["umbral_identificacion"] = umbral
            except ValueError as e:
                messagebox.showerror("Error", f"Umbral inválido: {e}")
                return
            
            # Guardar a archivo
            guardar_configuracion()
            messagebox.showinfo("Éxito", "Configuración guardada correctamente.")
            self.pantalla_principal()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")
    
    def pantalla_comparacion(self):
        """Pantalla de comparación con resultados."""
        self.limpiar_ventana()
        
        # Validar que esté configurado
        if not CONFIG["piezas"]:
            messagebox.showerror("Error", "Debe configurar las piezas patrón primero.")
            self.pantalla_principal()
            return
        
        # Seleccionar archivo de escaneo
        archivo_escaneo = filedialog.askopenfilename(
            title="Seleccionar archivo de escaneo (CSV)",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not archivo_escaneo:
            self.pantalla_principal()
            return
        
        # Pantalla de procesamiento mejorada
        frame_procesamiento = tk.Frame(self.root, bg='#1a1a2e')
        frame_procesamiento.pack(fill='both', expand=True)
        
        # Espaciador superior
        tk.Frame(frame_procesamiento, bg='#1a1a2e').pack(fill='both', expand=True)
        
        # Frame con borde y contenido
        frame_interior = tk.Frame(frame_procesamiento, bg='#2d2d44', relief='raised', bd=3)
        frame_interior.pack(expand=True, padx=40, pady=40, ipadx=30, ipady=30)
        
        # Texto de procesamiento
        label_procesando = tk.Label(frame_interior, text="⏳ PROCESANDO...",
                                   font=("Segoe UI", 32, "bold"), 
                                   bg='#2d2d44', fg='#00d966')
        label_procesando.pack(pady=20)
        
        # Subtexto dinámico (label_progreso)
        self.label_progreso = tk.Label(frame_interior, text="Analizando nube de puntos",
                                       font=("Segoe UI", 12), 
                                       bg='#2d2d44', fg='#b0b0b0',
                                       wraplength=400, justify='left')
        self.label_progreso.pack(pady=10)
        
        # Espaciador inferior
        tk.Frame(frame_procesamiento, bg='#1a1a2e').pack(fill='both', expand=True)
        
        self.root.update()
        
        # Ejecutar comparación en hilo separado
        thread = threading.Thread(target=self._ejecutar_comparacion_thread, 
                                 args=(archivo_escaneo,),
                                 daemon=False)
        thread.start()
    
    def _ejecutar_comparacion_thread(self, archivo_escaneo):
        """Ejecuta la comparación en un hilo separado."""
        try:
            self._actualizar_progreso("Cargando archivo de escaneo...")
            resultado, error = ejecutar_comparacion(archivo_escaneo, self._actualizar_progreso)
            
            if error:
                self.root.after(0, lambda: self._mostrar_error_comparacion(error))
            else:
                self.root.after(0, lambda: self._pantalla_resultados(resultado))
        
        except Exception as e:
            print(f"Excepción en hilo de comparación: {e}")
            import traceback
            traceback.print_exc()
            self.root.after(0, lambda: self._mostrar_error_comparacion(str(e)))
    
    def _actualizar_progreso(self, mensaje):
        """Actualiza el label de progreso en la GUI."""
        if hasattr(self, 'label_progreso'):
            self.root.after(0, lambda: self.label_progreso.config(text=mensaje))
    
    def _mostrar_error_comparacion(self, error):
        """Muestra error de comparación."""
        self.limpiar_ventana()
        messagebox.showerror("Error", f"Error en comparación: {error}")
        self.pantalla_principal()
    
    def _pantalla_resultados(self, resultado):
        """Pantalla con resultados de la comparación."""
        # Limpiar ventana
        self.limpiar_ventana()
        
        # Frame superior con resultado (Aprobada/Desaprobada)
        color_fondo = '#00d966' if resultado["aprobada"] else '#f44336'
        frame_resultado = tk.Frame(self.root, bg=color_fondo, height=150)
        frame_resultado.pack(fill='x', padx=0, pady=0)
        frame_resultado.pack_propagate(False)
        
        # Texto de resultado
        texto_resultado = "✓ APROBADA" if resultado["aprobada"] else "✗ DESAPROBADA"
        label_resultado = tk.Label(frame_resultado, text=texto_resultado,
                                  font=("Segoe UI", 48, "bold"),
                                  bg=color_fondo,
                                  fg='white')
        label_resultado.pack(expand=True)
        
        # Frame con información
        frame_info = tk.Frame(self.root, bg='#1a1a2e')
        frame_info.pack(fill='x', padx=20, pady=20)
        
        # Pieza detectada
        label_pieza = tk.Label(frame_info, text=f"Pieza Detectada: {resultado['pieza']}",
                              font=("Segoe UI", 18, "bold"), bg='#1a1a2e', fg='white')
        label_pieza.pack(anchor='w', pady=5)
        
        # Similitud
        label_similitud = tk.Label(frame_info, 
                                  text=f"Similitud: {resultado['similitud']:.1f}% (Umbral: {resultado['umbral']:.1f}%)",
                                  font=("Segoe UI", 14), bg='#1a1a2e', fg='#b0b0b0')
        label_similitud.pack(anchor='w', pady=5)
        
        # Aviso de gráfico en nueva ventana
        frame_aviso = tk.Frame(self.root, bg='#3b3b5c', relief='solid', bd=1, padx=15, pady=15)
        frame_aviso.pack(fill='x', padx=20, pady=15)
        
        label_aviso_icon = tk.Label(frame_aviso, text="ℹ️", font=("Segoe UI", 20),
                                   bg='#3b3b5c', fg='#3b24c8')
        label_aviso_icon.pack(side='left', padx=10)
        
        frame_texto_aviso = tk.Frame(frame_aviso, bg='#3b3b5c')
        frame_texto_aviso.pack(side='left', fill='both', expand=True)
        
        label_aviso_titulo = tk.Label(frame_texto_aviso, text="Gráfico 3D Interactivo",
                                     font=("Segoe UI", 12, "bold"),
                                     bg='#3b3b5c', fg='white', justify='left')
        label_aviso_titulo.pack(anchor='w')
        
        label_aviso_texto = tk.Label(frame_texto_aviso, 
                                    text="Se abrirá una ventana externa con el gráfico 3D interactivo.\nPuedes rotar, zoom y explorar la comparación. Cierra la ventana para continuar.",
                                    font=("Segoe UI", 10),
                                    bg='#3b3b5c', fg='#b0b0b0', justify='left')
        label_aviso_texto.pack(anchor='w', pady=5)
        
        # Mostrar gráfico en hilo separado
        thread_grafico = threading.Thread(target=self._generar_grafico,
                                        args=(resultado, None),
                                        daemon=True)
        thread_grafico.start()
        
        # Botones de acción
        frame_botones = tk.Frame(self.root, bg='#1a1a2e')
        frame_botones.pack(pady=15)
        
        btn_nueva = tk.Button(frame_botones, text="NUEVA COMPARACIÓN",
                             font=("Segoe UI", 12, "bold"),
                             bg='#3b24c8', fg='white',
                             command=self.pantalla_principal,
                             cursor="hand2", relief=tk.FLAT,
                             activebackground='#5636d3', activeforeground='white',
                             padx=15, pady=10)
        btn_nueva.pack(side='left', padx=10)
    
    def _generar_grafico(self, resultado, frame_grafico):
        """Genera el gráfico 3D interactivo en una ventana separada."""
        try:
            if resultado["patron"] is not None and resultado["comparada"] is not None:
                # Crear el plotter
                plotter = pv.Plotter(off_screen=False, window_size=(800, 600),
                                    notebook=False)
                
                # Patrón (negro, semi-transparente)
                plotter.add_mesh(pv.PolyData(resultado["patron"]), 
                               color='black', opacity=0.25, point_size=4, 
                               render_points_as_spheres=True, label='Patrón')
                
                # Nube escaneada (coloreada)
                compared_cloud_pv = pv.PolyData(resultado["comparada"])
                
                # Cálculo del coloreado (normalización lineal)
                min_coords = np.min(resultado["patron"], axis=0)
                max_coords = np.max(resultado["patron"], axis=0)
                diagonal = np.linalg.norm(max_coords - min_coords)
                threshold_value = max(1e-9, umbral_chamfer_frac * diagonal)
                factor_seguro = max(1e-9, FACTOR_VISUAL_GRADIENTE)
                threshold_visual = threshold_value / factor_seguro
                
                similitud_por_punto = np.maximum(0.0, 1.0 - (np.asarray(resultado["dists"]) / threshold_visual))
                compared_cloud_pv['Similitud'] = similitud_por_punto
                
                plotter.add_mesh(compared_cloud_pv, scalars='Similitud', cmap='RdYlBu',
                               point_size=5, render_points_as_spheres=True, 
                               clim=[0, 1], label='Escaneada')
                
                plotter.add_legend()
                plotter.reset_camera()
                
                # Mostrar en ventana interactiva
                plotter.show()
        
        except Exception as e:
            print(f"Error al generar gráfico: {e}")
            messagebox.showerror("Error", f"Error al generar gráfico 3D: {e}")


# =============================================================================
# PROGRAMA PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = AppComparacion(root)
    root.mainloop()
