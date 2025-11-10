import numpy as np
import pyvista as pv # Se mantiene solo para la visualización (plot_clouds)
from scipy.spatial import KDTree
import os
import time
import sys

# Rutas de archivos PATRÓN (CSV)
FILE_PATTERN_A = "Patron-A-50.csv"
FILE_PATTERN_B = "Patron-B-50.csv"
FILE_PATTERN_C = "Patron-C-50.csv"
FILE_COMPARED = "Escaneo.csv"

# Umbral de Similitud para Identificación
UMBRAL_IDENTIFICACION = 75.0

# Parámetros del algoritmo de alineación
angulo_paso = 45                # Ángulo grueso (grados)
iteraciones = 5                 # Número de iteraciones del refinamiento
num_muestras = 30000            # Número máximo de puntos a muestrear

# Umbral de Chamfer (fracción de la diagonal) para CÁLCULO de similitud
umbral_chamfer_frac = 0.1

# (NUEVO) Multiplicador para la sensibilidad del GRÁFICO
# > 1.0 = más sensible (cambia de color más rápido)
# < 1.0 = menos sensible (colores más suaves)
FACTOR_VISUAL_GRADIENTE = 1.0 


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


def compararA(puntos_comparada_centrada):
    """Compara la pieza escaneada con la Pieza Patrón A."""
    return _run_comparison(FILE_PATTERN_A, puntos_comparada_centrada)

def compararB(puntos_comparada_centrada):
    """Compara la pieza escaneada con la Pieza Patrón B."""
    return _run_comparison(FILE_PATTERN_B, puntos_comparada_centrada)

def compararC(puntos_comparada_centrada):
    """Compara la pieza escaneada con la Pieza Patrón C."""
    return _run_comparison(FILE_PATTERN_C, puntos_comparada_centrada)


# =============================================================================
# PROGRAMA PRINCIPAL (MODIFICADO)
# =============================================================================

if __name__ == "__main__":
    print("🤖 Iniciando programa de comparación (Archivos CSV).")
    
    # Cargar la pieza escaneada UNA SOLA VEZ
    try:
        puntos_comparada_original = _load_csv_points(FILE_COMPARED)
        print(f"✅ Pieza escaneada ('{FILE_COMPARED}') cargada: {len(puntos_comparada_original)} puntos.")
    
    except Exception as e:
        print(f"❌ Error al cargar la pieza escaneada: {e}")
        sys.exit(1)

    if not np.all(np.isfinite(puntos_comparada_original)):
        print("❌ Error: La pieza escaneada contiene valores NaN o Infinitos.")
        sys.exit(1)

    # (NUEVO) Centrar la pieza escaneada UNA SOLA VEZ
    puntos_comparada_centrada, _ = center_cloud(puntos_comparada_original)
    print("✅ Pieza escaneada centrada (media en 0,0,0).")


    # 1. Ejecutar las tres comparaciones (pasando la nube ya centrada)
    print("\n--- Comparando con Patrones ---")
    
    # Comparación A
    sim_A, pat_A, comp_A, dists_A = compararA(puntos_comparada_centrada)
    print(f"Pieza A ({os.path.basename(FILE_PATTERN_A)}): Similitud = **{sim_A:.2f}%**")
    
    # Comparación B
    sim_B, pat_B, comp_B, dists_B = compararB(puntos_comparada_centrada)
    print(f"Pieza B ({os.path.basename(FILE_PATTERN_B)}): Similitud = **{sim_B:.2f}%**")

    # Comparación C
    sim_C, pat_C, comp_C, dists_C = compararC(puntos_comparada_centrada)
    print(f"Pieza C ({os.path.basename(FILE_PATTERN_C)}): Similitud = **{sim_C:.2f}%**")

    # 2. Determinar el mejor resultado
    comparaciones = [
        {"nombre": "A", "similitud": sim_A, "patron": pat_A, "comparada": comp_A, "dists": dists_A},
        {"nombre": "B", "similitud": sim_B, "patron": pat_B, "comparada": comp_B, "dists": dists_B},
        {"nombre": "C", "similitud": sim_C, "patron": pat_C, "comparada": comp_C, "dists": dists_C},
    ]
    
    mejor_match = max(comparaciones, key=lambda x: x["similitud"])
    
    print("\n--- Resultado de Identificación ---")

    if mejor_match["similitud"] >= UMBRAL_IDENTIFICACION:
        print(f"🎉 **IDENTIFICADA:** La pieza escaneada es la Pieza **{mejor_match['nombre']}**.")
        print(f"Similitud con el Patrón {mejor_match['nombre']}: {mejor_match['similitud']:.2f}% (Umbral: {UMBRAL_IDENTIFICACION:.1f}%)")
        
        # Graficar solo el mejor match que superó el umbral
        if mejor_match["patron"] is not None:
            print("\nPreparando el gráfico de la mejor coincidencia...")
            plot_clouds(
                mejor_match["patron"],      # Ya está centrado
                mejor_match["comparada"],   # Ya está centrado y rotado
                mejor_match["dists"]
            )
    else:
        print(f"⚠️ **NO IDENTIFICADA:** Ninguna pieza patrón alcanzó el umbral de {UMBRAL_IDENTIFICACION:.1f}%.")
        print(f"El mejor match fue la Pieza **{mejor_match['nombre']}** con {mejor_match['similitud']:.2f}%.")
