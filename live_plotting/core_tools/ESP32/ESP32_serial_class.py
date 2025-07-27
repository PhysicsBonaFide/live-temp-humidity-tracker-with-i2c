import serial
import time
from time import sleep

'''Class to handle serial communication with an ESP32 device running MicroPython.'''

class ESP32Serial:
    def __init__(self, port_name, baudrate=115200):
        self.ser = serial.Serial(
            port=port_name,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )
        time.sleep(2)  # Wait for ESP32 to finish booting

    def read_temp_RH(self):
        self.ser.reset_input_buffer()  # Clear any leftover bytes from previous reads or sensor noise
        # Send the 'd' command to the ESP32 to request temperature and humidity readings
        # Need to send command in binary with a new line \n, hence b'd\n'
        self.ser.write(b'd\n')
        time.sleep(0.1)  # Short delay to allow sensor to process and respond
        
        while True:
            # Read one line from the serial port, decode from bytes to string
            response = self.ser.readline().decode('utf-8').strip()

            try:
            # Attempt to split the response into gauge 1 and gauge 2 values
                read_type, temp, humidity = response.split(',')
            except Exception:
                # If anything goes wrong, return an error
                read_type, temp, humidity = 'ERROR_TYPE_2', None, None
            
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            if read_type == 'DATA':
                return timestamp, temp, humidity
            elif read_type == 'ERROR':
                if temp == 'False':
                    print(f'Temperature CRC Failed at {timestamp}')
                if humidity == 'False':
                    print(f'Humidity CRC failed at {timestamp}')
                sleep(0.5)
            elif read_type == 'ERROR_TYPE_2':
                print(f'Error occured when reading data from serial port at {timestamp}')
                sleep(1)
                self.ser.write(b'd\n')
    
    def soft_reset(self):
        self.ser.reset_input_buffer()  # Clear any leftover bytes from previous reads or sensor noise
        # Send the 'r' command to the ESP32 to command ESP32 to soft reboot
        # Need to send command in binary with a new line \n, hence b'r\n'
        self.ser.write(b'r\n')
        sleep(1) #Give time to reboot

        response_1 = self.ser.readline().decode('utf-8').strip() #MPY: 'soft reboot', ESP32 prints this upon soft reboot
        response_2 = self.ser.readline().decode('utf-8').strip() #This line is the print statement from boot.py

        # Return the two lines upon reboot as strings
        return response_1, response_2

    def close_port(self):
        self.ser.close()
    
# Example usage
if __name__ == "__main__":
    # Create an instance of the ESP32Serial class
    esp32 = ESP32Serial('COM5')
    
    while True:
        print(esp32.read_temp_RH())
        sleep(1)
        print(esp32.read_temp_RH())
        sleep(1)
        print(esp32.soft_reset())
    
    # Close the serial port when done
    esp32.close_port()