import requests

def obtener_coordenadas(ciudad):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={ciudad}&count=1"
    respuesta = requests.get(url)
    data = respuesta.json()

    if "results" in data and len(data["results"]) > 0:
        latitud = data["results"][0]["latitude"]
        longitud = data["results"][0]["longitude"]
        return latitud, longitud
    else:
        print(f"No se encontraron coordenadas para {ciudad}.")
        return None, None

def obtener_clima(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&current_weather=true"
    )
    respuesta = requests.get(url)
    data = respuesta.json()
    if "current_weather" in data:
        clima = data["current_weather"]
        temperatura = clima["temperature"]
        viento = clima["windspeed"]
        codigo_clima = clima["weathercode"]
        estado_cielo = interpretar_estado_cielo(codigo_clima)
        return round(temperatura, 2), round(viento, 2), estado_cielo
    else:
        print("No se pudo obtener el clima.")
        return None, None, None

def interpretar_estado_cielo(codigo):
    estados = {
        0: "despejado",
        1: "principalmente despejado",
        2: "parcialmente nublado",
        3: "nublado",
        45: "niebla",
        48: "niebla con escarcha",
        51: "llovizna ligera",
        53: "llovizna moderada",
        55: "llovizna intensa",
        61: "lluvia ligera",
        63: "lluvia moderada",
        65: "lluvia intensa",
        80: "chubascos ligeros",
        81: "chubascos moderados",
        82: "chubascos violentos"
    }
    return estados.get(codigo, "estado desconocido")

def main():
    print("Presiona 'q' en cualquier momento para salir.")

    while True:
        origen = input("Ingrese ciudad de origen: ")
        if origen.lower() == 'q':
            break

        destino = input("Ingrese ciudad de destino: ")
        if destino.lower() == 'q':
            break

        lat1, lon1 = obtener_coordenadas(origen)
        lat2, lon2 = obtener_coordenadas(destino)

        if None in (lat1, lon1, lat2, lon2):
            continue

        temp1, viento1, cielo1 = obtener_clima(lat1, lon1)
        temp2, viento2, cielo2 = obtener_clima(lat2, lon2)

        if None in (temp1, temp2):
            continue

        print(f"\nClima actual:")
        print(f"{origen}: {temp1:.2f} °C, {viento1:.2f} km/h, {cielo1}")
        print(f"{destino}: {temp2:.2f} °C, {viento2:.2f} km/h, {cielo2}")

        print(
            f"\nRESUMEN: En {origen} actualmente hay {temp1:.2f} °C con cielos {cielo1}, "
            f"mientras que en {destino} hay {temp2:.2f} °C y está {cielo2}.\n"
        )

if __name__ == "__main__":
    main()
