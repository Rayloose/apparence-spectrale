import numpy as np
import matplotlib.pyplot as plt
import os


list_files = os.listdir()

files = 'FLMT021711__2__16-27-56-114.txt'

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
        data[i][0] = round(data[i][0], 0)

        if data[i][0] not in dico_mean :
            dico_mean[data[i][0]] = [data[i][1]]
        else :
            dico_mean[data[i][0]].append(data[i][1])

    for key in dico_mean:
        if 380 <= key <= 780 :
            new_data.append([key, np.mean(dico_mean[key])])

    return np.array(new_data)

replace_comma_by_dot(files)
data = convert_to_numpy(files)

new_file = mean_lengthwave(data)
plt.figure()
plt.plot(new_file[:,0], new_file[:,1])
plt.grid()
plt.show()














