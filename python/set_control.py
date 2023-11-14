import serial
import json
import time
from datetime import datetime
import pytz

# Setup serial communication
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

def send_request(request):
    # Convert dictionary to JSON string and append line breaks
    request_str = json.dumps(request) + "\r\n"
#    print("request: "+request_str)
    # Write request to serial port
    ser.write(request_str.encode('utf-8'))
    # Read response from serial port
    response_str = ser.read_until().decode('utf-8')
#    print("response: "+response_str)
    # Parse response string to dictionary
    response = json.loads(response_str)
    return response

def main():
    # Get current date and time in CET/Berlin timezone
    berlin_tz = pytz.timezone('Europe/Berlin')
    now = datetime.now(berlin_tz)

    # Record the initial time
    initial_time = now

    state = 0
    hour_on = 0
    minute_on = 2
    hour_off = 0
    minute_off = 3

    # Send initial request to set date and time
    initial_request = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "control",
        "params": {
            "state": state,
            "hour-on": hour_on,
            "minute-on": minute_on,
            "hour-off": hour_off,
            "minute-off": minute_off
        }
    }
    response = send_request(initial_request)
    print(response)  # Expecting: {"jsonrpc":"2.0","id":"1","result":"ok"}

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ser.close()  # Ensure the serial connection is closed upon exiting
