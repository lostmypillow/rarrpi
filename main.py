import serial
import requests
import time

# Initialize the serial connection to the Arduino
ser = serial.Serial("/dev/ttyACM0", 9600)
ser.baudrate = 9600

# Define the base URL for your Django backend
BASE_URL = "https://rarserver.lostmypillow.duckdns.org/api"

status_code = "1"


while True:
    
    read_ser = ser.readline()
    serm = read_ser.decode('utf-8')
    
    if "Card UID: " in serm:
        uid = serm.split("Card UID: ")[1].strip()
        print(f"Extracted UID: {uid}")

        try:
            response = requests.get(f"{BASE_URL}/card/{uid}")
            response_data = response.json()

            if response.status_code == 200 and "card_val" in response_data:
                attempt_response = requests.post(f"{BASE_URL}/attempt", json={"successful": True})
                print(f"Attempt logged: {attempt_response.json()}")
                status_code = "9"


            else:
                attempt_response = requests.post(f"{BASE_URL}/attempt", json={"successful": False})
                print(f"Attempt logged: {attempt_response.json()}")
                status_code = "0"

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    ser.write(status_code.encode())
    time.sleep(1)

