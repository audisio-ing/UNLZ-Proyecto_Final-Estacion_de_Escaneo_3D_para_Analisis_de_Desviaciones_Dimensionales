import numpy as np
import pyvista as pv

# --- Configuración ---
FILE_PATH = "Escaneo.csv"  # ruta del archivo .csv
Z_MIN = 0   # altura mínima
Z_MAX = 120  # altura máxima

# Cargar archivo CSV
points = np.loadtxt(FILE_PATH, delimiter=',', skiprows=1)

# Filtrar por altura
mask = (points[:, 2] >= Z_MIN) & (points[:, 2] <= Z_MAX)
filtered_points = points[mask]

print(f"Puntos totales: {len(points)}")
print(f"Puntos filtrados: {len(filtered_points)}")

# Crear nube de puntos
cloud = pv.PolyData(filtered_points)

# Crear visualizador
plotter = pv.Plotter()
plotter.set_background("white")

# Añadir puntos en rojo
plotter.add_points(cloud, color="red", point_size=4, render_points_as_spheres=True)

# Mostrar ejes numerados (grilla estilo matplotlib)
plotter.show_grid(
    color="black",        # color de los ejes
    grid="back",          # dibuja grilla detrás de los puntos
    location="outer",     # ubica los números afuera
    xtitle="X",
    ytitle="Y",
    ztitle="Z"
)

# Mostrar resultado
plotter.show()
