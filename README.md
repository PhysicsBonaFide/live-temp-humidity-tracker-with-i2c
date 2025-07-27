# temp-humidity-tracker-esp32-i2c
Live temperature &amp; humidity tracking using an ESP32 with an I2C sensor.


##live_plotting

This folder contains the files for the live plotting GUI. User only needs to edit the launch_GUI.py file to their desired settings (e.g., serial port name, filepath for the CSV, and interval timers for getting data and plotting it). Once set, just run launch_GUI.py and the window should pop up automatically.

The LivePlotter class is very flexible, so if the user adds more sensors and functionality to the project, they can all be tracked live by editing launch_GUI.py to add more plots, buttons, and tabs. See live_plotting/core_tools/gui/live_plotter_GUI_class.py for the source code.

##microcontroller_files

After flashing MicroPython onto your microcontroller (this repo was made specifically for an ESP32, but any micocontroller with MicroPython should also work), copy these files onto the microcontroller. I reccomend using Thonny to do this, as it is the easiest method.
