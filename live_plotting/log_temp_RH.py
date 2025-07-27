from core_tools.ESP32.save_temp_RH_readings_functions import create_temp_RH_log_csv, log_temp_RH_to_csv
from core_tools.ESP32.ESP32_serial_class import ESP32Serial
import sys

#To run script, use format: python3 <log_temp_RH.py filepath> <log_filepath (make sure to add .csv)> <serial_port> <interval_sec> <duration_sec (optional, leave empty for indefinite)>
#If using venv, use format: .venv\Scripts\python.exe <log_temp_RH.py filepath> <log_filepath (make sure to add .csv)> <serial_port> <interval_sec> <duration_sec (optional, leave empty for indefinite)>

log_filepath = sys.argv[1]
serial_port = sys.argv[2]
interval_sec = float(sys.argv[3])
duration_sec = float(sys.argv[4]) if len(sys.argv) > 4 else None

create_temp_RH_log_csv(log_filepath)  # Ensure the file exists and has a header
esp32 = ESP32Serial(serial_port)
log_temp_RH_to_csv(esp32, log_filepath, interval_sec=interval_sec, duration_sec=duration_sec)