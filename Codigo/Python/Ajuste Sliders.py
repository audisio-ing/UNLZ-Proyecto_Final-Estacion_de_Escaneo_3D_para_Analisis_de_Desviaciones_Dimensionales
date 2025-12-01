import cv2
import numpy as np
import math
import json
import sys
import time
import os
import pyvista as pv

# --- SECCIÓN DE PARÁMETROS INICIALES ---
CONFIG_FILE = "Setup.json"
CALIB_FILE = "CalibracionZoom.npz"
OBJ_FILE_PATH = "Pieza.obj"
NUM_SIMULATED_SAMPLES = 2
SAVED_PARAMS_FILE = "Parametros.json" # Archivo para cargar y guardar ajustes

# Parámetro Fijo para el OBJ
OBJ_SCALE_FACTOR = 10.0
# ----------------------------------------------------

# --- NUEVA FUNCIÓN PARA CARGAR PARÁMETROS O USAR DEFAULTS ---
def load_or_create_params(filename):
    """
    Intenta cargar los parámetros desde un archivo JSON. Si no existe o falla,
    devuelve un diccionario con valores por defecto.
    """
    # Define los valores iniciales por defecto
    initial_offset_x = (-7.2) - 15.62
    initial_offset_y = (-4.3) - 9.027
    default_params = {
        'THETA_DEG': 30.0,
        'CAM_RADIUS': 226.0,
        'CAM_HEIGHT': 100.0,
        'CAM_PITCH': -10.0,
        'OFFSET_RADIAL': np.sqrt(initial_offset_x**2 + initial_offset_y**2),
        'OFFSET_ANGLE_DEG': np.degrees(np.arctan2(initial_offset_y, initial_offset_x)),
        'OFFSET_Z': 240.0,
        'SCALE_FACTOR': 1.0,
        'XY_ASPECT_FACTOR': 1.0,
        'Z_ASPECT_FACTOR': 1.0,
        'Z_MIN': 0.0,
        'Z_MAX': 110.0,
        'MODULO_MAX': 100.0,
    }

    try:
        with open(filename, 'r') as f:
            print(f"Cargando parámetros desde '{filename}'...")
            loaded_params = json.load(f)
            final_params = default_params.copy()
            final_params.update(loaded_params)
            print("Parámetros cargados exitosamente.")
            return final_params
    except FileNotFoundError:
        print(f"'{filename}' no encontrado. Usando parámetros por defecto.")
        return default_params
    except Exception as e:
        print(f"Error al cargar '{filename}': {e}. Usando parámetros por defecto.")
        return default_params

# --- DICCIONARIO DE PARÁMETROS INTERACTIVOS (ahora se carga dinámicamente) ---
params = load_or_create_params(SAVED_PARAMS_FILE)

# --- CARGA DE CONFIGURACIÓN Y CALIBRACIÓN ---
print("\nScanner Interactivo con PyVista\n")
try:
    with open(CONFIG_FILE, 'r') as f: config = json.load(f)
    IND_CAM, THRESHOLD = config.get("camera_index", 3), config.get("threshold", 120)
    print(f"Configuración cargada: Cámara={IND_CAM}, Umbral={THRESHOLD}")
except Exception as e: print(f"Error cargando configuración: {e}"); sys.exit(1)

try:
    data = np.load(CALIB_FILE)
    K, dist = data["K"], data["dist"]
    print(f"Calibración cargada de {CALIB_FILE}")
except Exception as e: print(f"Error cargando calibración: {e}"); sys.exit(1)

def capturar_rayos(IND_CAM, threshold_val, k_matrix, dist_coeffs_val):
    cap = cv2.VideoCapture(IND_CAM)
    if not cap.isOpened(): print(f"Error: No se pudo abrir la cámara {IND_CAM}"); return np.array([])
    time.sleep(1); ret, frame = cap.read(); cap.release()
    if not ret: print("Error: no se pudo capturar un frame."); return np.array([])
    cv2.imwrite("captura_verificacion.png", frame); print("Frame guardado como 'captura_verificacion.png'")
    red_channel = frame[:, :, 2]
    laser_pixels = [[np.argmax(row), y] for y, row in enumerate(red_channel) if np.max(row) > threshold_val]
    if not laser_pixels: return np.array([])
    laser_pixels = np.array(laser_pixels, dtype=np.float32)
    undistorted = cv2.undistortPoints(laser_pixels.reshape(-1, 1, 2), k_matrix, dist_coeffs_val).reshape(-1, 2)
    rays = np.hstack([undistorted, np.ones((undistorted.shape[0], 1))]); rays /= np.linalg.norm(rays, axis=1, keepdims=True)
    return rays

def save_params(state):
    """Guarda el diccionario de parámetros actual en un archivo JSON."""
    with open(SAVED_PARAMS_FILE, 'w') as f:
        json.dump(params, f, indent=4)
    print(f"\n¡Parámetros guardados exitosamente en '{SAVED_PARAMS_FILE}'!\n")

def update_scan(param_name, value):
    params[param_name] = value
    
    theta_rad, pitch_rad = np.radians(params['THETA_DEG']), np.radians(params['CAM_PITCH'])
    normal_plano_mundo = np.array([np.sin(theta_rad), -np.cos(theta_rad), 0])
    T_cam_mundo = np.array([params['CAM_RADIUS'], 0, params['CAM_HEIGHT']])
    R_z_neg90, R_y_neg90 = np.array([[0,1,0],[-1,0,0],[0,0,1]]), np.array([[0,0,-1],[0,1,0],[1,0,0]])
    R_cam_base = R_y_neg90 @ R_z_neg90
    R_pitch = np.array([[1,0,0],[0,np.cos(pitch_rad),-np.sin(pitch_rad)],[0,np.sin(pitch_rad),np.cos(pitch_rad)]])
    R_cam_a_mundo = R_cam_base @ R_pitch
    puntos_intersectados = []
    for ray_cam in initial_rays:
        ray_mundo = R_cam_a_mundo @ ray_cam
        denom = np.dot(normal_plano_mundo, ray_mundo)
        if abs(denom) < 1e-9: continue
        t = np.dot(normal_plano_mundo, T_cam_mundo) / -denom
        if t > 0: puntos_intersectados.append(T_cam_mundo + t * ray_mundo)
    
    if not puntos_intersectados: plotter.add_mesh(pv.PolyData(), name='scan'); return

    angle_rad = np.radians(params['OFFSET_ANGLE_DEG'])
    offset_x = params['OFFSET_RADIAL'] * np.cos(angle_rad)
    offset_y = params['OFFSET_RADIAL'] * np.sin(angle_rad)

    nube_de_puntos = np.array(puntos_intersectados)
    nube_de_puntos[:, 2] *= -1
    nube_de_puntos += [offset_x, offset_y, params['OFFSET_Z']]
    nube_de_puntos *= params['SCALE_FACTOR']
    nube_de_puntos[:, :2] *= params['XY_ASPECT_FACTOR']
    nube_de_puntos[:, 2] *= params['Z_ASPECT_FACTOR']
    
    mask = (
        (nube_de_puntos[:, 2] >= params['Z_MIN']) &
        (nube_de_puntos[:, 2] <= params['Z_MAX']) &
        (np.linalg.norm(nube_de_puntos[:, :2], axis=1) <= params['MODULO_MAX'])  # Filtrar por módulo
    )
    base_profile = nube_de_puntos[mask]

    if base_profile.shape[0] == 0: plotter.add_mesh(pv.PolyData(), name='scan'); return

    angles = np.linspace(0, 2*np.pi, NUM_SIMULATED_SAMPLES, endpoint=False)
    all_rotated_clouds = []
    for angle in angles:
        c, s = np.cos(angle), np.sin(angle)
        rotation_matrix = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
        all_rotated_clouds.append(base_profile @ rotation_matrix.T)
    full_simulated_cloud = np.vstack(all_rotated_clouds)

    cloud = pv.PolyData(full_simulated_cloud)
    plotter.add_mesh(cloud, name='scan', color='red', point_size=5, render_points_as_spheres=True)

    combined_bounds = np.array(cloud.bounds)
    if 'reference_obj' in plotter.actors:
        obj_bounds = plotter.actors['reference_obj'].bounds
        combined_bounds = np.array([min(combined_bounds[0], obj_bounds[0]), max(combined_bounds[1], obj_bounds[1]),
                                     min(combined_bounds[2], obj_bounds[2]), max(combined_bounds[3], obj_bounds[3]),
                                     min(combined_bounds[4], obj_bounds[4]), max(combined_bounds[5], obj_bounds[5])])
    x_r, y_r, z_r = combined_bounds[1]-combined_bounds[0], combined_bounds[3]-combined_bounds[2], combined_bounds[5]-combined_bounds[4]
    max_r = max(x_r, y_r, z_r) if max(x_r, y_r, z_r) > 0 else 1
    center = np.array([(combined_bounds[0]+combined_bounds[1])/2, (combined_bounds[2]+combined_bounds[3])/2, (combined_bounds[4]+combined_bounds[5])/2])
    cubic_bounds = [center[0]-max_r/2, center[0]+max_r/2, center[1]-max_r/2, center[1]+max_r/2, center[2]-max_r/2, center[2]+max_r/2]
    plotter.add_mesh(pv.Box(bounds=cubic_bounds), name='bounding_box', style='wireframe', opacity=0.0)

# --- CAPTURA INICIAL Y CONFIGURACIÓN DEL PLOTTER ---
print("\nCapturando perfil láser inicial...")
initial_rays = capturar_rayos(IND_CAM, THRESHOLD, K, dist)

if initial_rays.shape[0] > 0:
    plotter = pv.Plotter(window_size=[1600, 1000])
    plotter.set_background('white')

    if os.path.exists(OBJ_FILE_PATH):
        print(f"Cargando modelo de referencia desde '{OBJ_FILE_PATH}'...")
        reference_mesh = pv.read(OBJ_FILE_PATH)
        if OBJ_SCALE_FACTOR != 1.0:
            reference_mesh.scale([OBJ_SCALE_FACTOR]*3, inplace=True)
        reference_mesh.rotate_x(90, inplace=True)
        reference_mesh.rotate_z(30, inplace=True)
        center, z_min = reference_mesh.center, reference_mesh.bounds[4]
        reference_mesh.translate([-center[0], -center[1], -z_min], inplace=True)
        plotter.add_mesh(reference_mesh, name='reference_obj', color='lightblue', opacity=0.5)

    plotter.show_grid()

    # --- AÑADIR SLIDERS (CORREGIDO) ---
    plotter.add_slider_widget(
        callback=lambda v: update_scan('CAM_PITCH', v),
        rng=[-45, 45],
        value=params['CAM_PITCH'],
        title="Inclinacion Cam"
    )
    plotter.add_slider_widget(
        callback=lambda v: update_scan('CAM_RADIUS', v),
        rng=[50, 400],
        value=params['CAM_RADIUS'],
        title="Radio Cam",
        pointa=(0.35, 0.1),
        pointb=(0.64, 0.1)
    )
    plotter.add_slider_widget(
        callback=lambda v: update_scan('CAM_HEIGHT', v),
        rng=[0, 300],
        value=params['CAM_HEIGHT'],
        title="Altura Cam",
        pointa=(0.35, 0.2),
        pointb=(0.64, 0.2)
    )
    plotter.add_slider_widget(
        callback=lambda v: update_scan('SCALE_FACTOR', v),
        rng=[0.1, 2.0],
        value=params['SCALE_FACTOR'],
        title="Escala General",
        pointa=(0.68, 0.1),
        pointb=(0.98, 0.1)
    )
    plotter.add_slider_widget(
        callback=lambda v: update_scan('OFFSET_Z', v),
        rng=[0, 500],
        value=params['OFFSET_Z'],
        title="Offset Z",
        pointa=(0.68, 0.2),
        pointb=(0.98, 0.2)
    )
    plotter.add_slider_widget(
        callback=lambda v: update_scan('OFFSET_RADIAL', v),
        rng=[0, 100],
        value=params['OFFSET_RADIAL'],
        title="Offset Radial",
        pointa=(0.02, 0.3),
        pointb=(0.31, 0.3)
    )
    plotter.add_slider_widget(
        callback=lambda v: update_scan('XY_ASPECT_FACTOR', v),
        rng=[0.5, 1.5],
        value=params['XY_ASPECT_FACTOR'],
        title="Aspecto XY",
        pointa=(0.68, 0.3),
        pointb=(0.98, 0.3)
    )
    plotter.add_slider_widget(
        callback=lambda v: update_scan('Z_ASPECT_FACTOR', v),
        rng=[0.5, 1.5],
        value=params['Z_ASPECT_FACTOR'],
        title="Aspecto Z",
        pointa=(0.02, 0.4),
        pointb=(0.31, 0.4)
    )
    plotter.add_slider_widget(
        callback=lambda v: update_scan('Z_MAX', v),
        rng=[0, 300],
        value=params['Z_MAX'],
        title="Limite Z Superior",
        pointa=(0.02, 0.9),
        pointb=(0.31, 0.9)
    )
    plotter.add_slider_widget(
        callback=lambda v: update_scan('Z_MIN', v),
        rng=[0, 300],
        value=params['Z_MIN'],
        title="Limite Z Inferior",
        pointa=(0.35, 0.9),
        pointb=(0.64, 0.9)
    )
    plotter.add_slider_widget(
        callback=lambda v: update_scan('MODULO_MAX', v),
        rng=[0, 500],
        value=params['MODULO_MAX'],
        title="Filtro Módulo Máx",
        pointa=(0.35, 0.4),
        pointb=(0.64, 0.4)
    )

    # --- AÑADIR BOTÓN DE GUARDAR ---
    plotter.add_checkbox_button_widget(save_params, value=False, size=30, position=(0.85, 0.85))
    
    print("Calculando y mostrando la primera visualización...")
    update_scan('THETA_DEG', params['THETA_DEG'])
    
    plotter.show()
else:
    print("No se detectaron rayos del láser en la captura inicial. No se puede iniciar el visualizador.")

