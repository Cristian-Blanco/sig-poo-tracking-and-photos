import os
import sys

# Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Agregar la carpeta src/ al path
SRC_DIR = os.path.join(BASE_DIR, 'src')
sys.path.insert(0, SRC_DIR)

# Ahora puedes importar normalmente
from src.drawWayAndPictures import create_map

# Entradas
gpx_path = os.path.join(SRC_DIR, 'assets', 'coordinates', 'aug_4,_2025_8_06_48_PM.gpx')
pictures_folder = os.path.join(BASE_DIR, 'docs', 'assets', 'pictures')

# Salida
output_path = os.path.join(BASE_DIR, 'docs', 'index.html')

# Crear el mapa
create_map(gpx_path, pictures_folder, output_path)