import exifread

def obtener_gps(path_imagen):
    with open(path_imagen, 'rb') as f:
        etiquetas = exifread.process_file(f)

    gps_lat = etiquetas.get('GPS GPSLatitude')
    gps_lat_ref = etiquetas.get('GPS GPSLatitudeRef')
    gps_lon = etiquetas.get('GPS GPSLongitude')
    gps_lon_ref = etiquetas.get('GPS GPSLongitudeRef')

    if gps_lat and gps_lat_ref and gps_lon and gps_lon_ref:
        def convertir_a_decimal(coord, ref):
            grados, minutos, segundos = [float(x.num) / float(x.den) for x in coord.values]
            decimal = grados + minutos / 60 + segundos / 3600
            if ref.values[0] in ['S', 'W']:
                decimal = -decimal
            return decimal

        lat = convertir_a_decimal(gps_lat, gps_lat_ref)
        lon = convertir_a_decimal(gps_lon, gps_lon_ref)

        print(f"Latitud: {lat}, Longitud: {lon}")
        return lat, lon
    else:
        print("No se encontraron datos GPS en la imagen.")
        return None

# Reemplaza con la ruta a tu imagen
obtener_gps('./pictures/IMG_20250804_202253_700.JPG')