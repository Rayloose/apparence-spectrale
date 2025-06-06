import numpy as np
import matplotlib.pyplot as plt
import os

start_number = 22 #là où il faut commencer à prendre la longueur d'onde
end_number = 23 #fin du string
final_dico = {}
list_files = os.listdir()

def replace_comma_by_dot(file):
    """(str) -> None Change the coma to dot in a .txt file"""

    with open(file, 'r') as f: #opening
        lines = f.readlines()

    with open(file, 'w') as f:
        for line in lines:
            f.write(line.replace(',', '.')) #replace

def convert_to_numpy(file):
    """(str) -> numpy array convert to numpy a .txt file"""
    return np.loadtxt(file, skiprows=14)

def mean_lengthwave(data):
    new_data = []
    dico_mean = {}

    for i in range(len(data)):
        data[i][0] = int(data[i][0]) #conversion en entier

    for j in range(len(data)):
        if data[j][0] not in dico_mean :
            dico_mean[data[j][0]] = [data[j][1]]
        else :
            dico_mean[data[j][0]].append(data[j][1])

    for key in dico_mean:
        if 380 <= key <= 780 :
            new_data.append([key, np.mean(dico_mean[key])])

    return np.array(new_data)

for files in list_files:
    if '.txt' in files:
        replace_comma_by_dot(files)
        data = convert_to_numpy(files)
        new_file = mean_lengthwave(data)
        print('fichier sélectionné', files)
        name = files[start_number:end_number]
        print('nom sélectionné (int)', name)

        if '_' in name:
            name = name[0]
        print('nouvelle sélection si > 10', name)

        print(name)
        final_dico[name] = [files, name, new_file]

print(final_dico.keys())



import csv

for i in range(1,26):
    print(i)
    filename = 'fiber_led_6500k_' + str(i) + '.csv'
    print(filename)
    with open(filename, mode='w', newline="") as file:
        writer = csv.writer(file, delimiter = ",")
        writer.writerow(['Wavelength', 'Coef'])
        writer.writerows(final_dico[str(i-1)][2])
        print(final_dico[str(i-1)][0])

        if i == 1:
            print(final_dico[str(i-1)][2])
#





















