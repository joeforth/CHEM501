import serial
import serial.tools.list_ports
import pandas as pd
import numpy as np

def data_read(n_readings, iteration):
    # Number of readings to take
    n_readings = 20
    column_titles = ['time', 'acc_x', 'acc_y', 'acc_z']

    # Connect to the Nicla
    ports = serial.tools.list_ports.comports()
    nicla = serial.Serial(port='COM8', baudrate=115200, timeout=.1)

    # Clear the buffer for the Nicla serial port
    nicla.flush()
    nicla.reset_input_buffer()

    # Collect data
    data_table = np.zeros((n_readings,len(column_titles)))
    for n in range(n_readings):
        data = nicla.readline()
        data = np.fromstring(data, sep=',')

        # Check that the data is the right length
        if len(data) == len(column_titles):
            data_table[n,:] = data

    # Remove the often-rubbish first row of data
    data_table = data_table[1:]

    # Convert to DataFrame and save
    data_table = pd.DataFrame(data_table, columns=column_titles)
    data_table.to_csv('./data_table' + str(i) + '.csv', header=column_titles, index=False)

n_files = 10
for i in range(0, n_files):
    data_read(n_files, i)