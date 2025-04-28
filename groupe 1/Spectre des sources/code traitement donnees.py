# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 09:46:13 2024

@author: dherb
"""

import pandas as pd
import numpy as np

#%%
####################POUR DONNES DU KONICA####################

# Chargement du fichier d'entrée
input_file = r"C:\Etudes\SupOp - Copie\2A\Projet\led_2700K\konica\values\ref_led_2700K.csv"  # Fichier d'entrée
output_file = "output_ref_konica_led_2700K.csv"       # Fichier de sortie


# Lecture des données existantes
data = pd.read_csv(input_file, header=None)


# Définir le point de départ (ligne 120, donc index 119 en Python)
start_line = 115  # Python commence les index à 0

# Filtrer les données à partir de la ligne 120
filtered_data = data.iloc[start_line:]

# Génération des longueurs d'onde correspondantes
start_wavelength = 380  # La longueur d'onde commence à 380
end_wavelength = 780
wavelengths = np.arange(start_wavelength, end_wavelength +1 , 1)


# Création du DataFrame final avec les longueurs d'onde et valeurs
output_data = pd.DataFrame({
    "Longueur d'onde (nm)": wavelengths,
    "Valeurs": filtered_data[1].values  # La 2e colonne des données d'entrée
})

# Sauvegarde dans un fichier CSV
output_data.to_csv(output_file, index=False, sep=',')

print(f"Le fichier CSV a été généré : {output_file}")

#%%
# ####################POUR DONNES DE LA FIBRE####################

# # Chargement du fichier texte
input_file = r"C:\Etudes\SupOp - Copie\2A\Projet\led_6500K\fiber\ref_led6500K.txt" # Nom du fichier à traiter
output_file = "export_fiber_led6500K.csv"  # Nom du fichier CSV de sortie

# Définir la ligne à partir de laquelle lire les données (par exemple, la ligne où commencent les valeurs)
start_line = 15  

# Lecture des données à partir de la ligne spécifiée
data = pd.read_csv(input_file, delim_whitespace=True, skiprows=start_line, header=None, names=["Wavelength", "Intensity"])

# Remplacement des virgules par des points et conversion en float
data["Wavelength"] = data["Wavelength"].str.replace(',', '.').astype(float)
data["Intensity"] = data["Intensity"].str.replace(',', '.').astype(float)

# Filtrer les longueurs d'onde entre 380 et 750 nm
data_filtered = data[(data["Wavelength"] >= 380) & (data["Wavelength"] <= 750)]

# Arrondir les longueurs d'onde à l'entier le plus proche
data_filtered.loc[:, "Wavelength"] = data_filtered["Wavelength"].round().astype(int)

# Grouper par longueurs d'onde entières et calculer la moyenne des intensités
data_grouped = data_filtered.groupby("Wavelength").mean().reset_index()

# Sauvegarde dans un fichier CSV
data_grouped.to_csv(output_file, index=False, sep=',', header=["Wavelength (nm)", "Average Intensity"])

print(f"Les données ont été exportées dans le fichier : {output_file}")

