from machine import I2C, Pin
import machine
from time import sleep
import sys

#SHT3x Temperature and Humidity Sensor Datasheet: https://sensirion.com/media/documents/213E6A3B/63A5A569/Datasheet_SHT3x_DIS.pdf

i2c = I2C(id=0, scl=Pin(22), sda=Pin(21), freq=400000, timeout=50000) #I2C setup

SHT_ADDR = 0x44 #SHT31-D address

def crc8(data): #CRC checksum to see if data is valid
    crc = 0xFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ 0x31) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
    return crc

def read_SHT_single_shot_mode(): #single shot mode grabs the temperature and RH once, then shuts off (see datasheet)
    i2c.writeto(SHT_ADDR, b'\x24\x00') #high repeatability, clock stretching off
    sleep(20/100) #wait 20ms for sensor
    
    data = i2c.readfrom(SHT_ADDR, 6)  # Read 6 bytes, first two are temperature, third is temperature CRC checksum, next two are RH, last is RH CRC checksum
    
    return data

def check_data_validity(data): #performs CRC checksum on data and compares to CRC checksum output from SHT to determine if data is valid to use
    crc_temp = data[2]
    crc_rh = data[5]
    
    crc_temp_result = crc8(data[0:2]) == crc_temp
    crc_rh_result = crc8(data[3:5]) == crc_rh
    
    if not crc_temp_result or not crc_rh_result:
        print(f'ERROR,{crc_temp_result},{crc_rh_result}')
        return False
    else:
        return True

def get_temperature_and_RH(): #after checking validity of data, returns current temperature and RH from SHT
    while True:
        data = read_SHT_single_shot_mode()
        
        if check_data_validity(data):
            temp_raw = data[0] << 8 | data[1] #convert two separate bytes into one 16-bit number
            rh_raw = data[3] << 8 | data[4]
            
            temp = -45 + 175 * (temp_raw / (2**16 - 1)) #formulas grabbed from datasheet
            rh = 100 * (rh_raw / (2**16 - 1))
            
            return temp, rh
        else:
            sleep(1) #if data fails CRC check, then wait a second before trying again

while True:
    try:
        cmd = sys.stdin.readline().strip()
        if cmd == "d":
            temp, rh = get_temperature_and_RH()
            print(f"DATA,{temp:.2f},{rh:.2f}")
        elif cmd == "r":
            machine.soft_reset()
    except Exception as e:
        # Optional: print error or ignore
        pass
