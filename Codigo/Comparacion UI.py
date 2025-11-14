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

# Archivo de configuración
CONFIG_FILE = "Parametros_Configuracion.json"

# Parámetros del algoritmo de alineación
angulo_paso = 45                # Ángulo grueso (grados)
iteraciones = 5                 # Número de iteraciones del refinamiento
num_muestras = 30000            # Número máximo de puntos a muestrear

# Umbral de Chamfer (fracción de la diagonal) para CÁLCULO de similitud
umbral_chamfer_frac = 0.1

# Multiplicador para la sensibilidad del GRÁFICO
FACTOR_VISUAL_GRADIENTE = 10.0

# Configuración global (se carga desde JSON)
CONFIG = {
    "piezas": {},
    "umbral_identificacion": 85.0,
    "archivo_escaneo": "Escaneo.csv"
} 


# =============================================================================
# FUNCIONES DE UTILIDAD
# =============================================================================

def center_cloud(points):
    """(NUEVA FUNCIÓN) Centra una nube de puntos restando su media (centroide)."""
    if points.size == 0:
        return points, np.array([0,0,0])
    # Calcula el centroide (la media de X, Y, Z)
    centroid = np.mean(points, axis=0)
    # Resta el centroide a todos los puntos
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
    """Convierte la distancia Chamfer en porcentaje de similitud."""
    min_coords = np.min(patron, axis=0)
    max_coords = np.max(patron, axis=0)
    diagonal_vector = max_coords - min_coords
    norm_factor = np.linalg.norm(diagonal_vector)

    if norm_factor == 0:
        return 100.0 if distancia_chamfer == 0 else 0.0

    # Umbral para el CÁLCULO
    threshold_value = max(1e-9, umbral_chamfer_frac * norm_factor)
    similarity = float(np.exp(- (distancia_chamfer / threshold_value)))
    similarity_percent = max(0.0, min(100.0, similarity * 100.0))

    return similarity_percent

def find_best_alignment(patron, comparada):
    # ... (Lógica de alineación, sin cambios) ...
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

def plot_clouds(pattern_points, compared_points, distances):
    """(MODIFICADO) Grafica la nube patrón y la alineada (con colores por similitud)."""
    plotter = pv.Plotter()
    # Patrón (negro)
    plotter.add_mesh(pv.PolyData(pattern_points), color='black', opacity=0.5, point_size=5, render_points_as_spheres=True)
    compared_cloud_pv = pv.PolyData(compared_points)
    
    # Cálculo del factor de escala para el coloreado
    min_coords = np.min(pattern_points, axis=0)
    max_coords = np.max(pattern_points, axis=0)
    diagonal = np.linalg.norm(max_coords - min_coords)
    
    # 1. Umbral base (el mismo que se usa para el cálculo de similitud)
    threshold_value = max(1e-9, umbral_chamfer_frac * diagonal)

    # 2. (NUEVO) Aplicar el multiplicador visual
    #    Se usa un valor pequeño (1e-9) para evitar división por cero si el factor es 0.
    factor_seguro = max(1e-9, FACTOR_VISUAL_GRADIENTE)
    threshold_visual = threshold_value / factor_seguro

    # 3. Similitud por punto para el coloreado (usa el umbral VISUAL)
    similitud_por_punto = np.exp(- (np.asarray(distances) / threshold_visual))
    compared_cloud_pv['similitud'] = similitud_por_punto

    # Pieza escaneada (coloreada)
    plotter.add_mesh(compared_cloud_pv, scalars='similitud', cmap='RdYlBu', point_size=6, render_points_as_spheres=True, clim=[0,1])
    plotter.add_scalar_bar(title='Similitud (local)', vertical=True)
    print("Mostrando ventana 3D (cierra la ventana para continuar)")
    plotter.show()

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
            print(f"Error en {file_patron} o escaneada: contiene valores no finitos (NaN/Inf).")
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
        print(f"⚠️ Advertencia: {fe}. Saltando comparación.")
        return 0.0, None, None, None
    except Exception as e:
        print(f"Error al comparar con {os.path.basename(file_patron)}: {e}")
        return 0.0, None, None, None


def cargar_configuracion():
    """Carga la configuración desde el archivo JSON."""
    global CONFIG
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                CONFIG = json.load(f)
            return True
        except:
            return False
    return False

def guardar_configuracion():
    """Guarda la configuración en un archivo JSON."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(CONFIG, f, indent=4)
        return True
    except:
        return False

def ejecutar_comparacion(archivo_escaneo):
    """Ejecuta el proceso de comparación completo."""
    try:
        puntos_comparada_original = _load_csv_points(archivo_escaneo)
        puntos_comparada_centrada, _ = center_cloud(puntos_comparada_original)
        
        if not np.all(np.isfinite(puntos_comparada_centrada)):
            return None, "Error: valores NaN/Infinitos en escaneado"
        
        # Ejecutar comparaciones
        comparaciones = []
        for nombre, path_patron in CONFIG["piezas"].items():
            sim, pat, comp, dists = _run_comparison(path_patron, puntos_comparada_centrada)
            comparaciones.append({
                "nombre": nombre,
                "similitud": sim,
                "patron": pat,
                "comparada": comp,
                "dists": dists
            })
        
        mejor_match = max(comparaciones, key=lambda x: x["similitud"])
        umbral = CONFIG.get("umbral_identificacion", 75.0)
        
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
                              text="Recomendado: 75% (estricto: 85%, flexible: 65%)",
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
        
        # Etiqueta de procesamiento
        label_procesando = tk.Label(self.root, text="Procesando...",
                                   font=("Segoe UI", 16), bg='#1a1a2e', fg='#00d966')
        label_procesando.pack(pady=20)
        self.root.update()
        
        # Ejecutar comparación en hilo separado
        thread = threading.Thread(target=self._ejecutar_comparacion_thread, 
                                 args=(archivo_escaneo, label_procesando))
        thread.start()
    
    def _ejecutar_comparacion_thread(self, archivo_escaneo, label_procesando):
        """Ejecuta la comparación en un hilo separado."""
        try:
            resultado, error = ejecutar_comparacion(archivo_escaneo)
            
            if error:
                self.root.after(0, lambda: self._mostrar_error_comparacion(error))
            else:
                self.root.after(0, lambda: self._pantalla_resultados(resultado, label_procesando))
        
        except Exception as e:
            self.root.after(0, lambda: self._mostrar_error_comparacion(str(e)))
    
    def _mostrar_error_comparacion(self, error):
        """Muestra error de comparación."""
        self.limpiar_ventana()
        messagebox.showerror("Error", f"Error en comparación: {error}")
        self.pantalla_principal()
    
    def _pantalla_resultados(self, resultado, label_procesando):
        """Pantalla con resultados de la comparación."""
        label_procesando.pack_forget()
        
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
        
        # Frame para gráfico 3D
        frame_grafico = tk.Frame(self.root, bg='#2d2d44', height=300, relief='sunken', bd=1)
        frame_grafico.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Mostrar gráfico en hilo separado
        thread_grafico = threading.Thread(target=self._generar_grafico,
                                        args=(resultado, frame_grafico))
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
        """Genera el gráfico 3D interactivo integrado en la ventana."""
        try:
            if resultado["patron"] is not None and resultado["comparada"] is not None:
                # Usar pyvista con plotly para interactividad (requiere plotly)
                # Si no está disponible, usar screenshot
                
                try:
                    # Intentar usar Jupyter backend que es más portable
                    import pyvista
                    
                    # Crear el plotter
                    plotter = pv.Plotter(off_screen=False, window_size=(600, 500),
                                        notebook=False)
                    
                    # Patrón (negro, semi-transparente)
                    plotter.add_mesh(pv.PolyData(resultado["patron"]), 
                                   color='black', opacity=0.4, point_size=8, 
                                   render_points_as_spheres=True, label='Patrón')
                    
                    # Nube escaneada (coloreada)
                    compared_cloud_pv = pv.PolyData(resultado["comparada"])
                    
                    # Cálculo del coloreado
                    min_coords = np.min(resultado["patron"], axis=0)
                    max_coords = np.max(resultado["patron"], axis=0)
                    diagonal = np.linalg.norm(max_coords - min_coords)
                    threshold_value = max(1e-9, umbral_chamfer_frac * diagonal)
                    factor_seguro = max(1e-9, FACTOR_VISUAL_GRADIENTE)
                    threshold_visual = threshold_value / factor_seguro
                    
                    similitud_por_punto = np.exp(- (np.asarray(resultado["dists"]) / threshold_visual))
                    compared_cloud_pv['similitud'] = similitud_por_punto
                    
                    plotter.add_mesh(compared_cloud_pv, scalars='similitud', cmap='RdYlBu',
                                   point_size=10, render_points_as_spheres=True, 
                                   clim=[0, 1], label='Escaneada')
                    
                    plotter.add_scalar_bar(title='Similitud Local', vertical=True)
                    plotter.add_legend()
                    plotter.reset_camera()
                    
                    # Mostrar en ventana interactiva
                    plotter.show()
                    
                except Exception as e:
                    print(f"No se pudo crear visualización interactiva: {e}")
                    print("Usando visualización estática...")
                    self._generar_grafico_estatico(resultado, frame_grafico)
        
        except Exception as e:
            print(f"Error al generar gráfico: {e}")
            label_error = tk.Label(frame_grafico, text="Error al generar gráfico 3D",
                                  font=("Arial", 12), bg='#ffcccc', fg='#cc0000')
            label_error.pack(fill='both', expand=True)
    
    def _generar_grafico_estatico(self, resultado, frame_grafico):
        """Genera gráfico estático como respaldo."""
        try:
            # Crear figura estática
            plotter = pv.Plotter(off_screen=True, window_size=(600, 500))
            
            # Patrón (negro)
            plotter.add_mesh(pv.PolyData(resultado["patron"]), 
                           color='black', opacity=0.5, point_size=5, 
                           render_points_as_spheres=True)
            
            # Nube escaneada (coloreada)
            compared_cloud_pv = pv.PolyData(resultado["comparada"])
            
            min_coords = np.min(resultado["patron"], axis=0)
            max_coords = np.max(resultado["patron"], axis=0)
            diagonal = np.linalg.norm(max_coords - min_coords)
            threshold_value = max(1e-9, umbral_chamfer_frac * diagonal)
            factor_seguro = max(1e-9, FACTOR_VISUAL_GRADIENTE)
            threshold_visual = threshold_value / factor_seguro
            
            similitud_por_punto = np.exp(- (np.asarray(resultado["dists"]) / threshold_visual))
            compared_cloud_pv['similitud'] = similitud_por_punto
            
            plotter.add_mesh(compared_cloud_pv, scalars='similitud', cmap='RdYlBu',
                           point_size=6, render_points_as_spheres=True, clim=[0, 1])
            
            # Guardar a imagen
            plotter.camera_position = 'xy'
            screenshot = plotter.screenshot(transparent_background=False)
            
            # Mostrar imagen en tkinter
            from PIL import Image, ImageTk
            
            img = Image.fromarray(screenshot)
            img_tk = ImageTk.PhotoImage(img)
            
            label_img = tk.Label(frame_grafico, image=img_tk, bg='white')
            label_img.image = img_tk  # Mantener referencia
            label_img.pack(fill='both', expand=True)
            
            label_nota = tk.Label(frame_grafico, 
                                 text="Gráfico estático (vista XY)",
                                 font=("Arial", 9), bg='white', fg='#999')
            label_nota.pack(pady=5)
        
        except Exception as e:
            print(f"Error al generar gráfico estático: {e}")


# =============================================================================
# PROGRAMA PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    print("🤖 Iniciando interfaz gráfica del sistema de identificación de piezas.")
    
    root = tk.Tk()
    app = AppComparacion(root)
    root.mainloop()