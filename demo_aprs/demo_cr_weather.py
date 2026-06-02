import socket
import time
import json
import urllib.request
from urllib.parse import urlencode

APRS_HOST = "localhost"
APRS_PORT = 14580

STATIONS = [
    {"call": "TIOSJWX", "name": "San Jose",   "lat": 9.9281,  "lon": -84.0907, "aprs_lat": "0955.69N", "aprs_lon": "08405.44W"},
    {"call": "TIOALWX", "name": "Alajuela",   "lat": 10.0163, "lon": -84.2116, "aprs_lat": "1000.98N", "aprs_lon": "08412.70W"},
    {"call": "TIOCAWX", "name": "Cartago",    "lat": 9.8644,  "lon": -83.9194, "aprs_lat": "0951.86N", "aprs_lon": "08355.16W"},
    {"call": "TIOHEWX", "name": "Heredia",    "lat": 9.9985,  "lon": -84.1165, "aprs_lat": "0959.91N", "aprs_lon": "08406.99W"},
    {"call": "TIOGUWX", "name": "Liberia",    "lat": 10.6350, "lon": -85.4377, "aprs_lat": "1038.10N", "aprs_lon": "08526.26W"},
    {"call": "TIOPUWX", "name": "Puntarenas", "lat": 9.9763,  "lon": -84.8384, "aprs_lat": "0958.58N", "aprs_lon": "08450.30W"},
    {"call": "TIOLIWX", "name": "Limon",      "lat": 9.9907,  "lon": -83.0359, "aprs_lat": "0959.44N", "aprs_lon": "08302.15W"},

    {"call": "TIOGUA1", "name": "Parque Central Guapiles", "lat": 10.214359, "lon": -83.788367, "aprs_lat": "1012.86N", "aprs_lon": "08347.30W"},
    {"call": "TIOCUL1","name": "Casa de la Cultura", "lat": 10.097147, "lon": -83.5062637, "aprs_lat": "1005.83N", "aprs_lon": "08330.38W"},
    {"call": "TIOSR01", "name": "San Ramon", "lat": 10.0910284, "lon": -84.4703933, "aprs_lat": "1005.46N", "aprs_lon": "08428.22W"},
    {"call": "TIORIO1", "name": "Rio Celeste", "lat": 10.7150425, "lon": -84.9875342, "aprs_lat": "1042.90N", "aprs_lon": "08459.25W"},
]


def send_aprs(callsign: str, packet: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((APRS_HOST, APRS_PORT))
        s.sendall(f"user {callsign} pass -1 vers CRWeatherDemo 1.0\r\n".encode())
        time.sleep(0.3)
        s.sendall((packet + "\r\n").encode())
        time.sleep(0.3)

def get_weather(lat: float, lon: float):
    params = urlencode({
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,wind_direction_10m",
        "timezone": "America/Costa_Rica",
    })
    url = f"https://api.open-meteo.com/v1/forecast?{params}"
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.loads(r.read().decode())["current"]

def build_wx_packet(station, weather):
    temp_c = weather["temperature_2m"]
    print(f"Temperatura real: {temp_c} °C")
    temp = round((temp_c * 9/5) + 32)
    hum = round(weather["relative_humidity_2m"])
    wind = round(weather["wind_speed_10m"])
    direction = round(weather["wind_direction_10m"])
    pressure = round(weather["surface_pressure"] * 10)

    return (
        f"{station['call']}>APRS,TCPIP*:!"
        f"{station['aprs_lat']}/{station['aprs_lon']}_"
        f"{direction:03d}/{wind:03d}g000t{temp:03d}h{hum:02d}b{pressure:05d}"
        f" {station['name']} CR"
    )

while True:
    for station in STATIONS:
        try:
            weather = get_weather(station["lat"], station["lon"])

            print("\n====================")
            print(station["name"])
            print(weather)

            packet = build_wx_packet(station, weather)

            send_aprs(station["call"], packet)

            print("Enviado:", packet)
        except Exception as e:
            print(f"Error con {station['name']}:", e)

        time.sleep(2)

    print("Ciclo completo. Esperando 5 minutos...")
    time.sleep(300)
    