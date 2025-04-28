# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 14:48:59 2025

@author: user
"""

import numpy as np
import pandas as pd
import scipy.optimize as opt
import scipy.stats as stats
import matplotlib.pyplot as plt

# Charger les données du spectre de la source
source_data = pd.read_csv('/mnt/data/led6500K_30_1.txt', delimiter='\t', header=None, comment='#')
wavelength = source_data.iloc[:, 0].values
intensite_spectre = source_data.iloc[:, 1].values

# Charger le fichier de calcul de l'albédo
from nn_lambertien_pr_juliette2 import calcul_brdf

# Paramètres
angles = np.radians([25, 30, 35])  # Seulement 25, 30 et 35 degrés
n_values = np.arange(1, 100, 1)  # Valeurs de n à tester

best_n = None
best_ks = None
best_r2 = -np.inf  # On cherche à maximiser R²

for n in n_values:
    brdf_values = calcul_brdf(intensite_spectre, angles, n) / intensite_spectre
    
    x_values = ((n + 1) / (n + 2)) * np.cos(angles) ** n
    y_values = brdf_values - intensite_spectre  # y = brdf - k_d
    
    slope, intercept, r_value, _, _ = stats.linregress(x_values, y_values)
    
    if r_value ** 2 > best_r2:
        best_r2 = r_value ** 2
        best_n = n
        best_ks = slope

print(f"Meilleur k_s: {best_ks}, pour n = {best_n}, avec R² = {best_r2}")
