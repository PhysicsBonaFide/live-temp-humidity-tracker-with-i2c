import time
import csv
import os
from .ESP32_serial_class import ESP32Serial

'''Functions to handle temperature and humidity readings and log them to a CSV file'''

# Reads data from the sensor, converting values as needed
def get_temp_RH_readings(sensor):
    timestamp, temp, humidity = sensor.read_temp_RH()
    return timestamp, float(temp), float(humidity)

# Creates a new CSV file with a header row if it doesn't already exist
def create_temp_RH_log_csv(filepath):
    if not os.path.exists(filepath):  # Check if the file already exists
        with open(filepath, mode='w', newline='') as file:  # Open in write mode
            writer = csv.writer(file)
            writer.writerow(['Time', 'Temperature', 'Humidity'])  # Write column headers

#Logs readings to CSV at regular intervals indefinitely or for a set duration
def log_temp_RH_to_csv(sensor, filepath, interval_sec, duration_sec=None): #None by default means run indefinitely unless specified
    start_time = time.time()

    with open(filepath, mode='a', newline='') as file:  # Open in append mode
        writer = csv.writer(file)

        while duration_sec is None or time.time() - start_time < duration_sec:  # Loop indefinitely or keep looping until time is up
            timestamp, temp, humidity = get_temp_RH_readings(sensor)  # Read current values

            writer.writerow([timestamp, temp, humidity])  # Write to CSV
            file.flush()               # Flush Python’s internal buffer
            os.fsync(file.fileno())   # Force OS to flush file to disk
            print(f"{timestamp} - Temperature (deg C): {temp}, Humidity (RH%): {humidity}")  # Console log, uncomment for debugging
            time.sleep(interval_sec)  # Wait before next reading

    sensor.close_port()  # Close serial connection when done

# Example usage
if __name__ == '__main__':
    log_filepath = 'live_plotting/temp_RH_log.csv'  # CSV log file path

    create_temp_RH_log_csv(log_filepath)  # Ensure the file exists and has a header

    esp32 = ESP32Serial('COM5')  # Initialize sensor on COM4
    log_temp_RH_to_csv(esp32, log_filepath, interval_sec=2)  # Start logging
