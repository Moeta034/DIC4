import time
import requests
import random

SERVER_URL = "http://localhost:5000/sensor"
DEVICE_ID = "ESP32_SIM_001"
IP_ADDRESS = "192.168.1.102"

print(f"Starting ESP32 Simulator... Sending data to {SERVER_URL} every 2 seconds.")

while True:
    temp = round(random.uniform(20.0, 35.0), 1)
    humd = round(random.uniform(40.0, 70.0), 1)
    
    payload = {
        "device_id": DEVICE_ID,
        "ip_address": IP_ADDRESS,
        "temp": temp,
        "humd": humd
    }
    
    try:
        response = requests.post(SERVER_URL, json=payload, timeout=2)
        if response.status_code == 201:
            print(f"[SUCCESS] Sent: {payload}")
        else:
            print(f"[ERROR] Server returned {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[FAILED] Could not connect to server: {e}")
        
    time.sleep(2)
