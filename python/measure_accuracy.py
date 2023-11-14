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

    # Send initial request to set date and time
    initial_request = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "set",
        "params": {
            "year": now.year,
            "month": now.month,
            "date": now.day,
            "hours": now.hour,
            "minutes": now.minute,
            "seconds": now.second
        }
    }
    response = send_request(initial_request)
    print(response)  # Expecting: {"jsonrpc":"2.0","id":"1","result":"ok"}

    # Loop to send get request and compare the time and date
 # Loop to send get request and compare the time and date
    while True:
        time.sleep(1)  # Wait for a second

        get_request = {"jsonrpc": "2.0", "id": "1", "method": "get"}
        response = send_request(get_request)
        result = response.get('result', {})

        # Get current time and date from response
        response_datetime = datetime(
            result.get('year', 0),
            result.get('month', 0),
            result.get('day', 0),
            result.get('hours', 0),
            result.get('minutes', 0),
            result.get('seconds', 0),
        ).astimezone(berlin_tz)

        # Get current time and date locally
        current_datetime = datetime.now(berlin_tz)

        # Scale the time difference to the elapsed time
        drift = (response_datetime - current_datetime).total_seconds()

        print(f"clock: {response_datetime}")
        print(f"now  : {current_datetime}")
        print(f"Difference is {drift:.3f}s (in {current_datetime-initial_time})")
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ser.close()  # Ensure the serial connection is closed upon exiting
