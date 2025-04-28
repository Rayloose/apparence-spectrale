# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 14:49:28 2024

@author: dherb
"""

#%%Imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import trapz  # Pour l'intégration numérique

#colorchecker macbeth
#srgb => d65 (on peut télécharger le spectre en ligne sur le site de la cie dans data)


#%%

#################IMPORTATION DE L'ALBEDO POUR CHAQUE CARRE####################
#

# Initialisation d'un dictionnaire pour stocker les données d'albédo
albedo_dict = {}

# Boucle pour importer chaque fichier
for i in range(1, 9):  # de 1 à 9 inclus
    # Chemin du fichier, à adapter
    filepath = rf"C:\Etudes\SupOp - Copie\2A\Projet\albedo\led_4000K_USB4H112691__{i}.csv"
    #ici les valeurs d'albedo sont calculées avec les mesures de la fibre
    # Importation des données
    albedo_import = pd.read_csv(filepath, header=None)
    albedo_np_import = albedo_import.to_numpy()
    
    # Extraction de la colonne d'albédo (sans la colonne de longueur d'onde)
    albedo = albedo_np_import[: , 2]
    
    # Stockage des données dans le dictionnaire avec un nom unique
    albedo_dict[f"albedo_{i}"] = albedo

# Vérification des données
# for key, value in albedo_dict.items():
#     print(f"{key}: {value[:5]}")  # Affiche les 5 premières valeurs pour chaque albédo






#################IMPORTATION DU SPECTRE DE LA SOURCE########################

# Lire le fichier CSV avec pandas, chemin à adapter
source = pd.read_csv(r"C:\Etudes\SupOp - Copie\2A\Projet\led_6500K\fiber\ref_led6500.csv") #fibre, attention si c'est la 4000K rajouter header = None
#source = pd.read_csv(r"C:\Etudes\SupOp - Copie\2A\Projet\Traitement données\output_ref_konica_led_4000K.csv") #konica



# # Afficher le tableau comme DataFrame pandas
# print(source)

source_numpy = source.to_numpy()
# #FIBRE
# wavelength = source_numpy[:,0]
# intensite_spectre = source_numpy[:,2]#/3920

# #KONICA
wavelength = source_numpy[0:371,0]
intensite_spectre = source_numpy[0:371,1]#/3920

#normalisation du spectre
#intensite_spectre = intensite_spectre/np.max(intensite_spectre)


#plot
plt.figure()
plt.plot(wavelength, intensite_spectre)
plt.title("Spectre de la source")
plt.xlabel("Lambda (nm)")
plt.ylabel("Intensite (?)")
plt.show()







##################CALCUL BRDF ET SPECTRE DE REFLEXION##########################
# Initialisation des dictionnaires pour stocker les résultats de BRDF et du spectre de réflexion
brdf_dict = {}
spectre_reflexion_dict = {}

# Boucle pour calculer le BRDF et le spectre de réflexion pour chaque albédo
for i in range(1, 9):
    # Récupérer l'albédo pour le carré actuel
    albedo_np = albedo_dict[f"albedo_{i}"]

    # Calculer le BRDF pour chaque carré
    brdf = albedo_np / np.pi #On suppose que c'est lambertien
    brdf_dict[f"brdf_{i}"] = brdf  # Stocker dans le dictionnaire brdf_dict

    # Calcul du spectre de réflexion
    spectre_reflexion = brdf * intensite_spectre  # Assurez-vous que intensite_spectre a la même taille
    spectre_reflexion_dict[f"spectre_reflexion_{i}"] = spectre_reflexion  # Stocker dans le dictionnaire spectre_reflexion_dict


#plot de chaque spectre comme le colorchecker

#% Affichage des spectres de réflexion pour 8 carrés
order = [
    [1, 2, 3, 4],
    [5, 6, 7, 8]
]

fig, axes = plt.subplots(2, 4, figsize=(15, 6))
fig.suptitle("Spectres de réflexion pour 8 carrés du ColorChecker", fontsize=16)

for row in range(2):
    for col in range(4):
        idx = order[row][col]
        spectre = spectre_reflexion_dict[f"spectre_reflexion_{idx}"]
        ax = axes[row, col]
        ax.plot(wavelength, spectre)
        ax.set_title(f"Case {idx}")


plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# Ajustement de l'espacement entre les subplots
plt.tight_layout(rect=[0, 0, 1, 0.96])  # Laisser de l'espace pour le titre principal
plt.show()









#%% ###############CONVERSION EN XYZ####################
cie_xyz = pd.read_csv(r"C:\Etudes\SupOp - Copie\2A\Projet\CIE data\CIE_xyz_1931_2deg.csv")
cie_xyz_np = cie_xyz.to_numpy()
cie_xyz_np_truncated = cie_xyz_np[19:len(cie_xyz_np) - 80] #de 380 à 750nm

x = cie_xyz_np_truncated[:, 1]  # x_bar
y = cie_xyz_np_truncated[:, 2]  # y_bar
z = cie_xyz_np_truncated[:, 3]  # z_bar

# plt.figure()
# plt.plot(wavelength, x, color='red', label='x')
# plt.plot(wavelength, y, color='green', label='y')
# plt.plot(wavelength, z, color='blue', label='z')
# plt.legend()
# plt.title("CIE1931 colour-matching functions")
# plt.grid()
# plt.show()

xyz_normalized_dict = {}
y_sum = np.sum(y)

for key, spectre_reflexion in spectre_reflexion_dict.items():
    X = trapz(spectre_reflexion * x, wavelength) #*683 ??
    Y = trapz(spectre_reflexion * y, wavelength)
    Z = trapz(spectre_reflexion * z, wavelength)

    X_normalized = X / y_sum
    Y_normalized = Y / y_sum
    Z_normalized = Z / y_sum

    xyz_normalized_dict[key] = (X_normalized, Y_normalized, Z_normalized)







#%% ############CONVERSION EN SRGB ET AFFICHAGE COLORCHECKER###################
M_XYZ_to_sRGB = np.array([[3.2406, -1.5372, -0.4986],
                          [-0.9689, 1.8758, 0.0415],
                          [0.0557, -0.2040, 1.0570]])



def gamma_correction(rgb):
    return np.where(rgb <= 0.0031308, 12.92 * rgb, 1.055 * (rgb ** (1 / 2.4)) - 0.055)

# def gamma_correction(rgb):
#      return rgb

# Déterminer la couleur de la première case
first_idx = order[0][0]
Xn, Yn, Zn = xyz_normalized_dict[f"spectre_reflexion_{first_idx}"]
RGB_first = np.dot(M_XYZ_to_sRGB, np.array([Xn, Yn, Zn]))
RGB_first_clipped = np.clip(RGB_first, 0, 1)
RGB_first_corrected = gamma_correction(RGB_first_clipped)
RGB_first_255 = np.floor(RGB_first_corrected * 255).astype(int)

# Couleur de la première case en format hexadécimal
RGB_first_hex = '#{:02x}{:02x}{:02x}'.format(*RGB_first_255)

#Forme figure
fig, axes = plt.subplots(2, 4, figsize=(15, 6), facecolor='black')
fig.suptitle("Couleurs sRGB pour 8 carrés, éclairage 6500K, fibre", fontsize=16, color=RGB_first_hex)
rgb_dict = {}


for row in range(2):
    for col in range(4):
        idx = order[row][col]
        Xn, Yn, Zn = xyz_normalized_dict[f"spectre_reflexion_{idx}"]
        RGB = np.dot(M_XYZ_to_sRGB, np.array([Xn, Yn, Zn]))
        RGB_clipped = np.clip(RGB, 0, 1)
        RGB_corrected = gamma_correction(RGB_clipped)
        RGB_255 = np.floor(RGB_corrected * 255).astype(int)
        rgb_dict[f"spectre_reflexion_{idx}"] = tuple(RGB_corrected)
        
        rgb_image = np.reshape(RGB_corrected, (1, 1, 3))
        ax = axes[row, col]
        ax.imshow(rgb_image)
        ax.axis('off')
        # Titre avec la couleur de la première case
        ax.set_title(f"Case {idx}\nRGB = {tuple(RGB_255)}", fontsize=8, color=RGB_first_hex)

#output_filename = r"C:\Etudes\SupOp - Copie\2A\Projet\PLOTS Colorchecker\colorchecker_sRGB_8carres_6500K_fiber.png"
#plt.savefig(output_filename, dpi=300, bbox_inches='tight')  # Export avec haute qualité et marges ajustées


plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# Afficher les valeurs RGB calculées
for key, value in rgb_dict.items():
    print(f"{key}: RGB = {value}")

#%%
# plt.figure(figsize=(10, 6))
# for key, spectre_reflexion in spectre_reflexion_dict.items():
#     plt.plot(wavelength, spectre_reflexion, label=key)

# plt.title("Spectres de réflexion des 8 carrés (4000K)")
# plt.xlabel("Longueur d'onde (nm)")
# plt.ylabel("Réflexion intensité")
# plt.legend()
# plt.grid()
# plt.show()


