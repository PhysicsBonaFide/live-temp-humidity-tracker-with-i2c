from core_tools.gui.live_plotter_GUI_class import LivePlotter
from core_tools.ESP32.save_temp_RH_readings_functions import create_temp_RH_log_csv

'''Launches GUI to plot temperature and humidity live as specified by the user in this file.'''
#Create the CSV files for logging data BEFORE adding the relevant plot to the GUI window because the plotter will look for the file when it is created. Use the create_temp_RH_log_csv function to create the file.
#Do NOT use any filenames with whitespaces in them, as this will cause issues with the terminal command buttons.
#The widgets (plots, buttons, etc.) are added to the GUI window in the order they are written here and fill from left to right, top to bottom.
#For more infromation on how to use the LivePlotter class, see GitHub readme file or the source code at core_tools/gui/live_plotter_GUI_class.py

plotter = LivePlotter("Temperature and Humidity Tracker")

temp_RH_log_filepath = 'live_plotting/temp_RH_log.csv'

create_temp_RH_log_csv(temp_RH_log_filepath)

plots_tab = plotter.create_tab(tab_name='Plots', plots_per_row=2)

plots_tab.add_plot(title='Plot Temperature', x_axis=('Time since present', 'hrs'), y_axis=('Temperature', '°C'), buffer_size=576, csv_filepath=temp_RH_log_filepath, datatype='temperature')
plots_tab.start_timer(title='Plot Temperature', interval_ms=100)

plots_tab.add_plot(title='Plot Humidity', x_axis=('Time since present', 'hrs'), y_axis=('RH', '%'), buffer_size=576, csv_filepath=temp_RH_log_filepath, datatype='humidity')
plots_tab.start_timer(title='Plot Humidity', interval_ms=100)

plots_tab.add_command_button(title='Log Temperature and Humidity', command=f'.venv\Scripts\python.exe live_plotting/log_temp_RH.py {temp_RH_log_filepath} COM5 0.5')
plots_tab.cmd_timer(500)

plotter.run()