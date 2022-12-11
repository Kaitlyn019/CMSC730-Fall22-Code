import socket
import pandas as pd
from esp32networkstruct import *
import csv
import pickle
from datetime import datetime

# to get module, do pip install scikit-learn
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression

class esp32():
    s = socket.socket()
    count = 1
    classmap = {}
    loaded_model = pickle.load(open("Data/finalized_model_RF.sav", 'rb'))
    
    def __init__(self, *args, **kwargs):
        self.s.bind(('0.0.0.0', 8090))
        self.s.listen(0)

        temp = pd.read_csv("Data/set_c.csv").values
        vals = temp[0][1:]
        keys = temp[1][1:]
        for i in range(0, len(keys)):
            self.classmap[int(keys[i])] = vals[i]

        csvfile = open('Data/live_data.csv', 'w', newline='')
        csvfile.close()

    def run(self):

        client, addr = self.s.accept()
        content = client.recv(imu_wifi_packet_t.sizeof() * MAX_IMU_READINGS)

        print(str(self.count) + " ====================================")
        print(imu_wifi_packet_t.sizeof())
        
        if len(content) != 0:
            parsed = imu_wifi_packet_t.parse(content)

            data = []
            data_print = []

            data_print.append(datetime.now().strftime("%H:%M:%S"))

            i = 0
            while (i < MAX_IMU_READINGS):
                r = parsed['readings'][i]
                round = []

                round.append((r['accel_x_raw']/100)-16)
                round.append((r['accel_y_raw']/100)-16)
                round.append((r['accel_z_raw']/100)-16)

                data_print += round

                round.append(r['gyro_x_raw'] - 360)
                round.append(r['gyro_y_raw'] - 360)
                round.append(r['gyro_z_raw'] - 360)

                data += round
                i += 1

            result = self.loaded_model.predict([data])
            data_print.append(self.classmap[result[0]])
            print(data_print)

            csvfile = open('Data/live_data.csv', 'a', newline='')
            writer = csv.writer(csvfile, delimiter=',',
                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(data_print)

            csvfile.close()

            print(self.classmap[result[0]])  # is it a spike (live)

        print("Closing connection")
        client.close()