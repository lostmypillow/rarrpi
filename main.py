import serial
import requests
import time

# Initialize the serial connection to the Arduino
ser = serial.Serial("/dev/ttyACM0", 9600)
ser.baudrate = 9600

# Define the base URL for your Django backend
BASE_URL = "https://rarserver.lostmypillow.duckdns.org/api"

status_code = "1"


def sendAttempt(n):
    if n == "yes":
        attempt_response = requests.post(f"{BASE_URL}/attempt?successornot=True")
        print(f"Attempt logged: {attempt_response.json()}")
    else:
        attempt_response = requests.post(f"{BASE_URL}/attempt?successornot=False")
        print(f"Attempt logged: {attempt_response.json()}")





while True:
    ser.write(status_code.encode())
    ser.write("")
    print("sent status code " + status_code)
    read_ser = ser.readline()
    uid = read_ser.decode('utf-8').strip()
    print(f"Extracted UID: {uid}")
    if uid != "":
        try:
            response = requests.get(f"{BASE_URL}/card/{uid}")
            response_data = response.json()

            if response.status_code == 200 and "card_val" in response_data:
                sendAttempt("yes")
                status_code = "9"


            else:
                sendAttempt("no")
                status_code = "0"

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        


