import gpxpy
import folium
from folium.plugins import MarkerCluster
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# ========== 1. Función para convertir DMS a decimal ==========
def get_decimal_from_dms(dms, ref):
    def to_float(x):
        # Soporta tuplas tipo (num, den) y también IFDRational directo
        try:
            return float(x[0]) / float(x[1])
        except TypeError:
            return float(x)

    degrees = to_float(dms[0])
    minutes = to_float(dms[1])
    seconds = to_float(dms[2])

    decimal = degrees + minutes / 60 + seconds / 3600
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

# ========== 2. Extraer coordenadas GPS de una imagen ==========
def get_gps_from_image(img_path):
    try:
        img = Image.open(img_path)
        exif_data = img._getexif()
        if not exif_data:
            return None
        gps_info = {}
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag)
            if tag_name == "GPSInfo":
                for key in value:
                    name = GPSTAGS.get(key)
                    gps_info[name] = value[key]
        if 'GPSLatitude' in gps_info and 'GPSLongitude' in gps_info:
            lat = get_decimal_from_dms(gps_info['GPSLatitude'], gps_info['GPSLatitudeRef'])
            lon = get_decimal_from_dms(gps_info['GPSLongitude'], gps_info['GPSLongitudeRef'])
            return (lat, lon)
    except Exception as e:
        print(f"Error leyendo {img_path}: {e}")
    return None

# ========== 3. Leer el archivo GPX ==========
def parse_gpx(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        points = [(point.latitude, point.longitude) for track in gpx.tracks for segment in track.segments for point in segment.points]
        return points

# ========== 4. Crear el mapa con la ruta y fotos ==========
def create_map(gpx_path, pictures_folder):
    ruta = parse_gpx(gpx_path)

    # Centrar el mapa en el primer punto de la ruta
    mapa = folium.Map(location=ruta[0], zoom_start=15)

    # Dibujar la ruta
    folium.PolyLine(ruta, color="blue", weight=3).add_to(mapa)

    # Marcar las fotos
    cluster = MarkerCluster().add_to(mapa)
    for filename in os.listdir(pictures_folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(pictures_folder, filename)
            coords = get_gps_from_image(img_path)
            if coords:
                popup = folium.Popup(f"<b>{filename}</b><br><img src='{img_path}' width='200'>", max_width=300)
                folium.Marker(location=coords, popup=popup, icon=folium.Icon(color='red', icon='camera')).add_to(cluster)

    mapa.save("index.html")
    print("✅ Mapa creado como index.html")

# ========== 5. Ejecutar ==========
gpx_path = "assets/coordinates/aug_4,_2025_8_06_48_PM.gpx"  # <- Cambia por tu archivo GPX
pictures_folder = "assets/pictures/"  # <- Cambia si tu carpeta tiene otro nombre
create_map(gpx_path, pictures_folder)
