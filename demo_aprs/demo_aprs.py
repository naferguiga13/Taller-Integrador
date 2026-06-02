import socket
import time
import urllib.request
import json

APRS_HOST = "localhost"
APRS_PORT = 14580

TEC_POINTS = [
    ("0951.29N", "08354.43W", "Electronica TEC"),
    ("0951.30N", "08354.42W", "Movimiento TEC 1"),
    ("0951.31N", "08354.41W", "Movimiento TEC 2"),
    ("0951.32N", "08354.40W", "Movimiento TEC 3"),
]

def send_aprs(callsign, packet):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((APRS_HOST, APRS_PORT))
        s.sendall(f"user {callsign} pass -1 vers DemoTIOTEC 1.0\r\n".encode())
        time.sleep(0.5)
        s.sendall((packet + "\r\n").encode())

def get_weather():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=9.8548828&longitude=-83.9071331"
        "&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,wind_direction_10m"
    )
    with urllib.request.urlopen(url, timeout=10) as r:
        data = json.loads(r.read().decode())
    return data["current"]

while True:
    for lat, lon, msg in TEC_POINTS:
        tracker_packet = f"TIOTEC1-7>APLRT1,WIDE1-1:={lat}/{lon}> {msg}"
        send_aprs("TIOTEC1-7", tracker_packet)
        print("Enviado tracker:", tracker_packet)

        try:
            w = get_weather()
            temp = round(w["temperature_2m"])
            hum = round(w["relative_humidity_2m"])
            wind = round(w["wind_speed_10m"])
            direction = round(w["wind_direction_10m"])
            pressure = round(w["surface_pressure"] * 10)

            wx_packet = (
                f"TIOTECWX>APRS,TCPIP*:!0951.29N/08354.43W_"
                f"{direction:03d}/{wind:03d}g000t{temp:03d}h{hum:02d}b{pressure:05d}"
            )
            send_aprs("TIOTECWX", wx_packet)
            print("Enviado weather:", wx_packet)

        except Exception as e:
            print("Error clima:", e)

        time.sleep(15)