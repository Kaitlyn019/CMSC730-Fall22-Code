import socket
import pandas as pd
from esp32networkstruct import *
import csv
import pickle
from datetime import datetime

# to get module, do pip install scikit-learn
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression

s = socket.socket()         
 
s.bind(('0.0.0.0', 8090 ))
s.listen(0)
 
cont = 'y' ## stop program running
count = 1 ## counting # of iterations
max_count = 15
dataset = [] ## for training
classmap = {}  ## for training

## SET THIS VALUE:
training = False ## set to true if training model

manual = False;
default = "bump"

loaded_model = 0;

if (not training): ## load in a classmap file
    temp = pd.read_csv("Data/set_c.csv").values
    vals = temp[0][1:]
    keys = temp[1][1:]
    for i in range(0, len(keys)):
        classmap[int(keys[i])] = vals[i]

    csvfile = open('Data/live_data.csv', 'w', newline='')
    #writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    #head_cs = [str(i) for i in range(0, MAX_IMU_READINGS)]
    #writer.writerow(['timestamp'] + head_cs + ['classification'])
    
    csvfile.close()

    filename = "Data/finalized_model_RF.sav"
    loaded_model = pickle.load(open(filename, 'rb'))



while count <= max_count:

    print (str(count) + " ====================================")
    print (imu_wifi_packet_t.sizeof())
     
    client, addr = s.accept()

    while True:
        content = client.recv(imu_wifi_packet_t.sizeof() * MAX_IMU_READINGS)
 
        if len(content) ==0:
            dataset.append(data)
            break
 
        else:
            parsed = imu_wifi_packet_t.parse(content)
            #print(parsed['readings'])

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

            #print(data)
        

            if (training):
                # For the training phase, comment out later:
                # After each packet is received, can note what the action was to save
                if manual:
                    c = (input("Classify the action (not case sensitive): \n")).lower()
                else:
                    c = default

                if (c not in classmap.values()):
                    classmap[c] = len(classmap)
                
                data.append(classmap[c])
            else:
                # For purely classifying based on a previously loaded in model:
                result = loaded_model.predict([data])

                data_print.append(classmap[result[0]])
                print (data_print)

                csvfile = open('Data/live_data.csv', 'a', newline='')
                writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(data_print)

                csvfile.close()

                print(classmap[result[0]]) ## is it a spike (live)

    print("Closing connection")
    client.close()

    #cont = (input("Continue Collecting (Y/N)? ")).lower()
    count += 1

if (training):
    save = input("Save data (Y/N)? ").lower()

    if (save == 'y'):
        fname = input("Enter filename for dataset: ")
        pd.DataFrame(dataset).to_csv("Data/"+fname+".csv")

        fname = input("Enter filename for classifications: ")
        pd.DataFrame([list(classmap.keys()), list(classmap.values())]).to_csv("Data/"+fname+".csv")


