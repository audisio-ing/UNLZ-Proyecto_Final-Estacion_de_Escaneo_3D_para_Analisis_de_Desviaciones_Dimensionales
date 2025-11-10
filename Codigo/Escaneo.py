import cv2
import numpy as np
import math
import serial
import time
import json 
import sys 

# Archivos de configuración y salida
SETUP = "Setup.json"
CALIBRACION = "CalibracionZoom.npz"
PARAMETROS = "Parametros.json"
OUTPUT = "Escaneo.csv" 

# Parámetros de comunicación
BAUDRATE = 115200

# Parámetros de cámara
IND_CAM, THRESHOLD, ARDUINO = None, None, None
THETA_DEG, CAM_RADIUS, CAM_HEIGHT, CAM_PITCH = (None,) * 4
OFFSET_RADIAL, OFFSET_ANGLE_DEG, OFFSET_Z, SCALE_FACTOR = (None,) * 4
XY_ASPECT_FACTOR, Z_ASPECT_FACTOR = (None,) * 2
Z_MIN, Z_MAX, MODULO_MAX = (None,) * 3

print("\n────────────────────────────────\n")
print("Escaner por triangulación láser")
print("\n────────────────────────────────\n")

# Carga de parámetros

print("Cargando ajustes de escaneo...\n")
try:
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

    print(f"  > Parámetros cargados desde '{PARAMETROS}'\n")

except FileNotFoundError:
    print(f"Error: El archivo de parámetros '{PARAMETROS}' no fue encontrado.")
    sys.exit(1)
except Exception as e:
    print(f"Error al cargar los parámetros de ajuste: {e}")
    sys.exit(1)

# Configuración de cámara
try:
    with open(SETUP, 'r') as f: config = json.load(f)
    IND_CAM = config["camera_index"]
    THRESHOLD = config["threshold"]
    ARDUINO = config["arduino_port"]

    print(f"  > Configuración de cámara cargada de {SETUP}:")
    print(f"   » Índice de Cámara: {IND_CAM}\n")
    print(f"   » Treshold: {THRESHOLD}\n")
    print(f"   » Puerto Arduino: {ARDUINO}\n")
except Exception as e: print(f"Error al cargar la configuración de cámara: {e}"); sys.exit(1)

# Calibración
try:
    calib = np.load(CALIBRACION)
    K = calib["K"]
    dist = calib["dist"]

    print(f"  > Calibración de cámara cargada de {CALIBRACION}\n")

except Exception as e: print(f"Error cargando calibración: {e}"); sys.exit(1)

# Conexión Arduino
try:
    ser = serial.Serial(ARDUINO, BAUDRATE, timeout=2); time.sleep(2)
    print(f"  > Conectado exitosamente a Arduino en {ARDUINO}")
except Exception as e: print(f"Error conectando a Arduino: {e}"); sys.exit(1)

# Captura de láser
def capturar_laser(IND_CAM, threshold_val, k_matrix, coef_dist):
    cap = cv2.VideoCapture(IND_CAM)
    if not cap.isOpened():
        print(f"Error: No se pudo abrir la cámara {IND_CAM}")
        return np.array([])

    time.sleep(1)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Error: no se pudo capturar un frame.")
        return np.array([])

    # Extraer canal rojo
    red_channel = frame[:, :, 2]

    # Aplicar suavizado gaussiano horizontal
    red_channel = cv2.GaussianBlur(red_channel, (15, 1), 0)

    # Detectar píxeles del láser
    laser_pixels = []
    for y, row in enumerate(red_channel):
        max_val = np.max(row)
        if max_val > threshold_val:
            x = np.argmax(row)
            laser_pixels.append([x, y])

    if not laser_pixels:
        return np.array([])

    laser_pixels = np.array(laser_pixels, dtype=np.float32)

    # Corregir distorsión de la cámara
    undistorted = cv2.undistortPoints(laser_pixels.reshape(-1, 1, 2), k_matrix, coef_dist).reshape(-1, 2)

    # Normalizar los rayos
    rays = np.hstack([undistorted, np.ones((undistorted.shape[0], 1))])
    rays /= np.linalg.norm(rays, axis=1, keepdims=True)

    return rays

# Intersección de rayos con plano
def intersectar_rayos_y_calcular_perfil(rays):
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
        if abs(denom) < 1e-9: continue
        t = np.dot(normal_plano_mundo, T_cam_mundo) / -denom
        if t > 0:
            punto = T_cam_mundo + t * ray_mundo
            # --- CAMBIO: Usar el signo de la coordenada X del rayo de la cámara ---
            # Esto resuelve la inversión concavo/convexo.
            # Si ray_cam[0] es negativo (izquierda del centro de la imagen), el radio es negativo.
            radius = np.sqrt(punto[0]**2 + punto[1]**2) * np.sign(ray_cam[0])
            points_2d.append([radius, punto[2]])
    return np.array(points_2d) if points_2d else np.array([])

# Escaneo
def escanear_pieza(num_muestras_arduino):
    points_all = []
    ser.write(f"{num_muestras_arduino}\n".encode())
    print(f"Iniciando escaneo con {num_muestras_arduino} muestras.\n")

    for i in range(num_muestras_arduino):
        current_angle = None
        while current_angle is None:
            line = ser.readline().decode().strip()
            if line:
                try: current_angle = float(line)
                except ValueError: print(f"Advertencia: Línea inesperada de Arduino: '{line}'.")
        
        print(f"Muestra {i+1}/{num_muestras_arduino} - Ángulo recibido: {current_angle}°")
        rays = capturar_laser(IND_CAM, THRESHOLD, K, dist)

        if rays.shape[0] == 0:
            print(f"  -> No se detectó láser en esta vista.\n"); continue

        perfil_2d = intersectar_rayos_y_calcular_perfil(rays)
        if perfil_2d.shape[0] > 0:
            # 1. Aplicar el offset radial y asegurar que el radio no sea negativo
            radii = np.abs(perfil_2d[:, 0] + OFFSET_RADIAL)
            heights = -perfil_2d[:, 1] # Mantener inversión de altura
            
            # 2. Aplicar el offset angular al ángulo del Arduino
            total_angle_deg = current_angle + OFFSET_ANGLE_DEG
            angle_rad = np.radians(total_angle_deg)
            
            # 3. Convertir a coordenadas 3D con los valores corregidos
            puntos_transformados = np.column_stack((
                radii * np.cos(angle_rad), 
                radii * np.sin(angle_rad), 
                heights
            ))
            
            # 4. Aplicar los ajustes globales de Z, escala y aspecto
            puntos_transformados[:, 2] += OFFSET_Z
            puntos_transformados *= SCALE_FACTOR
            puntos_transformados[:, :2] *= XY_ASPECT_FACTOR
            puntos_transformados[:, 2] *= Z_ASPECT_FACTOR
            
            points_all.append(puntos_transformados)
            print(f"  -> Muestra procesada ({puntos_transformados.shape[0]} puntos)\n")
        else:
            print(f"  -> No se generaron puntos para esta vista.\n")
    return points_all if points_all else []

# Bucle Principal

print("\n────────────────────────────────\n")

num_muestras = 0

try:
    while True:
        linea_arduino = ser.readline().decode('utf-8', errors='ignore').strip()

        if linea_arduino:
            print(f"  > {linea_arduino}")

            # Si Arduino hace una pregunta, espera una respuesta del usuario
            if '?' in linea_arduino:
                respuesta_usuario = input("Respuesta: ")

                if respuesta_usuario.lower() == 'exit':
                    print("Saliendo del programa.")
                    break

                if "¿Cuántas muestras desea tomar?" in linea_arduino:
                    try:
                        num_muestras = int(respuesta_usuario)
                    except ValueError:
                        print("Error: Se esperaba un número para la cantidad de muestras.")
                        # Enviamos un 0 o un valor no válido para que Arduino lo maneje
                        ser.write("0\n".encode())
                        continue

                ser.write((respuesta_usuario + '\n').encode())

            # Si Arduino indica que el escaneo comienza, llamamos a la función
            elif "Iniciando escaneo..." in linea_arduino:
                if num_muestras > 0:
                    nube_por_escaneo = escanear_pieza(num_muestras)

                    if nube_por_escaneo:
                        nube_completa = np.vstack(nube_por_escaneo)
                        mask = (
                            (nube_completa[:, 2] >= Z_MIN) &
                            (nube_completa[:, 2] <= Z_MAX) &
                            (np.linalg.norm(nube_completa[:, :2], axis=1) <= MODULO_MAX)  # Filtrar por módulo
                        )
                        nube_filtrada = nube_completa[mask]

                        # Desplazar las muestras filtradas en Z para que Z_MIN sea 0
                        nube_filtrada[:, 2] -= Z_MIN

                        print(f"\nEscaneo completado. Total: {nube_completa.shape[0]}. Tras filtrado: {nube_filtrada.shape[0]}.")

                        # Guardar la nube de puntos en formato CSV
                        np.savetxt(
                            OUTPUT, 
                            nube_filtrada, 
                            delimiter=',', 
                            header='X,Y,Z', 
                            comments='',
                            fmt='%.6f' # Formato para 6 decimales
                        )

                        print(f"  > Nube de puntos guardada como '{OUTPUT}'")

                        try:
                            import pyvista as pv
                            plotter = pv.Plotter(window_size=[1024, 768])
                            plotter.set_background('white')
                            if nube_filtrada.shape[0] > 0:
                                plotter.add_mesh(pv.PolyData(nube_filtrada), color='red', point_size=5, render_points_as_spheres=True)
                            plotter.show_grid()
                            plotter.show_axes()
                            plotter.view_isometric()
                            plotter.show()
                        except ImportError:
                            print("\nPyVista no está instalado. Instálalo para ver el resultado: pip install pyvista")
                    else:
                        print("\nNo se generó ninguna nube de puntos.")
                else:
                    print("Escaneo omitido porque no se especificó un número de muestras válido.")

            elif "¿Expulsar pieza?" in linea_arduino:
                respuesta_usuario = input("Respuesta: ")
                ser.write((respuesta_usuario + '\n').encode())

            # Si el Arduino finaliza el ciclo, salimos del bucle en Python
            elif "Pieza expulsada" in linea_arduino or "Escaneo finalizado" in linea_arduino and num_muestras > 0:
                print("\nCiclo de escaneo completado, finalizando.")

                break

except KeyboardInterrupt:
    print("\nInterrupción por teclado. Saliendo del programa.")
finally:
    plotter.close()
    ser.close()
    print("\nPuerto serial cerrado.")
