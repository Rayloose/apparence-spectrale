import numpy as np
import os
import csv
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

list_files = os.listdir() #list of all the files

def lecture(file):
    """(str) -> csv file converted to numpy array"""
    L = []
    with open(file) as f:
        i = 0
        for ligne in f:
            if i!= 0 :
                ligne = ligne.strip()
                ligne_carac = ligne.split(',')
                ligne_carac[0], ligne_carac[1] = float(ligne_carac[0]), float(ligne_carac[1])
                L.append(ligne_carac)
            i+=1
    return np.array(L)

def wavelength_to_rgb(wavelength):
    gamma = 0.8
    intensity_max = 255
    factor = 0
    red, green, blue = 0, 0, 0

    if 380 <= wavelength <= 439:
        red = -(wavelength - 440) / (440 - 380)
        green = 0.0
        blue = 1.0
    elif 440 <= wavelength <= 489:
        red = 0.0
        green = (wavelength - 440) / (490 - 440)
        blue = 1.0
    elif 490 <= wavelength <= 509:
        red = 0.0
        green = 1.0
        blue = -(wavelength - 510) / (510 - 490)
    elif 510 <= wavelength <= 579:
        red = (wavelength - 510) / (580 - 510)
        green = 1.0
        blue = 0.0
    elif 580 <= wavelength <= 644:
        red = 1.0
        green = -(wavelength - 645) / (645 - 580)
        blue = 0.0
    else :
        red = 1.0
        green = 0.0
        blue = 0.0

    #ajustement de l'intensité
    if 380 <= wavelength <= 419:
        factor = 0.3 + 0.7 * (wavelength - 380) / (420 - 380)
    elif 701 <= wavelength <= 780:
        factor = 0.3 + 0.7 * (780 - wavelength) / (780 - 700)
    else :
        factor = 1.0

    if red != 0:
        red = int(intensity_max * (red * factor) ** gamma)
    if green != 0:
        green = int(intensity_max * (green * factor) ** gamma)
    if blue != 0:
        blue = int(intensity_max * (blue * factor) ** gamma)

    return red/255, green/255, blue/255

def plot_spectrum(data):
    """(numpy array) -> None plot the spectrum"""
    for i in range(len(data)):
        plt.vlines(data[i][0],0, data[i][1], color = wavelength_to_rgb(data[i][0]), linewidth=2)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity')
    plt.title('Spectrum')
    plt.grid()

data_fluo_1 = lecture('fiber_fluo_15.csv')
data_fluo_1[:,1]/=np.max(data_fluo_1[:,1])
data_fluo_2 = lecture('fiber_fluo_25.csv')
data_fluo_2[:,1]/=np.max(data_fluo_2[:,1])
data_led_4000k_1 = lecture('fiber_led_4000k_15.csv')
data_led_4000k_1[:,1]/=np.max(data_led_4000k_1[:,1])
data_led_4000k_2 = lecture('fiber_led_4000k_25.csv')
data_led_4000k_2[:,1]/=np.max(data_led_4000k_2[:,1])

albedo_1 = np.zeros((len(data_fluo_1), 2))
albedo_1[:,0] = data_fluo_1[:,0]
albedo_1[:,1] = data_fluo_1[:,1] / data_fluo_2[:,1]

albedo_2 = np.zeros((len(data_led_4000k_1), 2))
albedo_2[:,0] = data_led_4000k_1[:,0]
albedo_2[:,1] = data_led_4000k_1[:,1] / data_led_4000k_2[:,1]


plt.figure()
plt.subplot(3,2,1)
plot_spectrum(data_fluo_1)
plt.subplot(3,2,2)
plot_spectrum(data_fluo_2)
plt.subplot(3,2,3)
plot_spectrum(albedo_1)
plt.subplot(3,2,4)
plot_spectrum(data_led_4000k_1)
plt.subplot(3,2,5)
plot_spectrum(data_led_4000k_2)
plt.subplot(3,2,6)
plot_spectrum(albedo_2)

plt.show()
