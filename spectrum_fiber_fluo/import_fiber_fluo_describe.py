#import

import numpy as np
import os
import csv

#stockage

list_files = os.listdir() #list of all the files
final_dico = {}
start_number = 12 #start position where the number of the file is supposed to be
end_number = 14 #end position where the number of the file is supposed to be

#functions

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
    """(numpy array) -> numpy array return the mean of the coef for each lengthwave"""
    new_data = []
    dico_mean = {} #dico to store with the key the lengthwave and the value the list of coef that we want to average

    for i in range(len(data)): #we loop over all the data
        data[i][0] = int(data[i][0])

        if data[i][0] not in dico_mean : #if the key is not in the dico, we add it
            dico_mean[data[i][0]] = [data[i][1]]
        else : #if the key is already in the dico, we append the value
            dico_mean[data[i][0]].append(data[i][1])


    for key in dico_mean:
        if 380 <= key <= 780 : #iltering the lengthwave and saving only those who are between 380 and 780
            new_data.append([key, np.mean(dico_mean[key])]) #we append the key and the mean of the value

    return np.array(new_data)



for file in list_files: #we loop over all the files
    if '.txt' in file:
        replace_comma_by_dot(file)
        data = convert_to_numpy(file)
        new_file = mean_lengthwave(data)
        name = file[start_number:end_number]
        if '_' in name:
            name = name[0]
        final_dico[name] = [file, name, new_file] #we store the name of the file, the name of the fiber and the data in the same place for better use

#working

for i in range(1,26): #we loop over all the files
    filename = 'fiber_fluo_' + str(i) + '.csv' #we create the name of the file
    with open(filename, mode='w', newline="") as file:
        writer = csv.writer(file, delimiter = ",")
        writer.writerow(['Wavelength', 'Coef']) #header
        writer.writerows(final_dico[str(i)][2]) #data























