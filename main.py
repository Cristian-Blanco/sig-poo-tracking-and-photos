import gpxpy
import matplotlib.pyplot as plt

def leer_gpx_y_graficar(ruta_gpx):
    # Leer archivo GPX
    with open(ruta_gpx, 'r', encoding='utf-8') as archivo:
        gpx = gpxpy.parse(archivo)

    # Extraer puntos (latitud y longitud)
    latitudes = []
    longitudes = []

    for track in gpx.tracks:
        for segmento in track.segments:
            for punto in segmento.points:
                latitudes.append(punto.latitude)
                longitudes.append(punto.longitude)

    # Verificar si hay puntos
    if not latitudes or not longitudes:
        print("No se encontraron puntos en el archivo.")
        return

    # Dibujar ruta
    plt.figure(figsize=(10, 6))
    plt.plot(longitudes, latitudes, marker='o', linestyle='-', color='blue')
    plt.title('Ruta GPX')
    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    plt.grid(True)
    plt.axis('equal')
    plt.show()

# Cambia esta ruta por tu archivo GPX
ruta_del_archivo = 'Aug_4,_2025_8_06_48_PM.gpx'
leer_gpx_y_graficar(ruta_del_archivo)
