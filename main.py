import serial
import requests
import time

ser = serial.Serial("/dev/ttyACM0", 9600)
ser.baudrate = 9600

BASE_URL = "https://rarserver.lostmypillow.duckdns.org/api"

while True:

    read_ser = ser.readline()
    serm = read_ser.decode('utf-8')
    
    if serm != "":
        uid = serm.strip()
        print(f"Extracted UID: {uid}")

        try:
            response = requests.get(f"{BASE_URL}/card/{uid}")
            response_data = response.json()

            if response.status_code == 200 and "card_val" in response_data:
                attempt_response = requests.post(f"{BASE_URL}/attempt?successornot=True")
                print(f"Attempt logged: {attempt_response.json()}")
                status_code = "9"


            else:
                attempt_response = requests.post(f"{BASE_URL}/attempt?successornot=False")
                print(f"Attempt logged: {attempt_response.json()}")
                status_code = "0"

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    ser.write(status_code.encode())