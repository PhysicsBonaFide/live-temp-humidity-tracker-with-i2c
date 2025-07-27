# live-temp-humidity-tracker-with-i2c
Live temperature & humidity tracking using a microcontroller with an I2C temperature and humidity sensor.

## live_plotting

This folder contains the files for the live plotting GUI. User only needs to edit the live_plotting/launch_GUI.py file to their desired settings (e.g., serial port name, filepath for the CSV, and interval timers for getting data and plotting it). Once set, just run launch_GUI.py and the window should pop up automatically.

The LivePlotter class is very flexible, so if the user adds more sensors and functionality to the project, they can all be tracked live. To do so, edit launch_GUI.py to add more plots, buttons, and tabs. See live_plotting/core_tools/gui/live_plotter_GUI_class.py for the source code.

## microcontroller_files

After flashing MicroPython onto your microcontroller, copy these files onto it. I reccomend using Thonny to do this, as it is the easiest method.

You may need to change main.py to the address of your I2C sensor and the SDA/SCL pins you are using on your microcontroller.


## Important Notes!

### Note 1
While this repo was made specifically for an ESP32, most microcontrollers should also work with little issue. If you are encountering problems, you will likely need to edit some or all of the following files to fit your needs:

microcontroller_files/main.py

live_plotting/core_tools/ESP32/ESP32_serial_class.py

live_plotting/core_tools/ESP32/save_temp_RH_readings_functions.py

### Note 2

To run the files in live_plotting, you will need to setup a Python environment and pip install numpy, pandas, pyqtgraph, pyqt5, and pyserial.
