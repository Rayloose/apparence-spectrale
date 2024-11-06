import numpy as np
import matplotlib.pyplot as plt

rgb_d65 = np.loadtxt('rgb_d65.txt', delimiter=';', skiprows=1)[:,1:4]
rgb_led = np.loadtxt('rgb_led_6700k_iphone15pro.txt', delimiter=';', skiprows=1)[:,1:4]


def difference_color_rgb(rgb_1, rgb_2):

    diff_relative = np.abs(rgb_1-rgb_2)/rgb_1
    print(diff_relative)
    diff_norm = np.sqrt((np.sum((rgb_1-rgb_2)**2, axis = 1)))
    norm_reference = np.sqrt(np.sum(rgb_1**2, axis = 1))

    plt.figure()

    color_list = ['r', 'g', 'b']

    for i in range(3):
        plt.subplot(2,2,i+1)
        plt.plot(diff_relative[:, i]*100,'o', label= color_list[i], color = color_list[i])
        plt.ylim(0,100)
        plt.xlabel('colornum')
        plt.ylabel('relative color difference in percentage')
        plt.legend()
        plt.grid()

    plt.subplot(2,2,4)
    plt.plot(diff_norm/norm_reference*100, label='euclidean norm', marker = 'x')
    mean = np.mean(diff_norm/norm_reference*100)
    plt.axhline(mean, color='r', linestyle='--', label='mean')
    plt.xlabel('colornum')
    plt.ylabel('relative RGB difference in percentage')
    plt.legend()
    plt.grid()
    plt.show()

difference_color_rgb(rgb_d65,rgb_led)