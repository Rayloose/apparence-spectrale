# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 09:38:48 2024

@author: dherb

Ce code vise à générer un colorchecker avec huit couleurs différentes à partir du spectre d'une source et des albédos des huit carrés'
"""


#%%Imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import trapz  # Pour l'intégration numérique
import csv





#%%FONCTIONS (dans l'ordre d'utilisation)

def plot_source():
    """
    Retourne le plot de l'intensité de la source en fonction de la longueur d'onde entre 380 et 780nm

    Args:
        
    Returns:
        figure

    """
       
    plt.figure()
    plt.plot(wavelength, intensite_spectre)
    plt.grid()
    plt.title("Spectre de la source 6500K")
    plt.xlabel("Lambda (nm)")
    plt.ylabel("Intensite (W.m^(-2))")
    plt.show()
    
    
    
    
    
def calcul_brdf(albedo):
    """
    Retourne la brdf à partir d'un albédo

    Args:
        spectre (liste de float): Une liste contenant les valeurs de l'albédo d'un spectre entre 380nm et 780nm.

    Returns:
        brdf: liste de float contenant les valeurs de brdf d'une surface entre 380 et 780nm'

    """
    return albedo/np.pi + ks #lambertien
    
    
    
    
def calcul_spectre_reflexion(source, brdf):
    """
    Retourne le spectre de réflexion à partir de l'intensité du spectre d'une source et de la brdf de la surface

    Args:
        source (liste de float): Une liste contenant les valeurs de de l'intensité de la source entre 380nm et 780nm.
        brdf: liste de float contenant les valeurs de brdf d'une surface entre 380 et 780nm'
        
    Returns:
        reflexion: Une liste contenant les valeurs de de l'intensité de la réflexion sur la surface entre 380nm et 780nm.

    """
    
    return source*brdf    





def plot_spectres_reflexions():
    """
    Plot les spectres de réflexion en fonction de la longueur d'onde sur un même graphe'

    Args:
        
    Returns:
        figure

    """   
    # Affichage des spectres de réflexion pour 8 carrés sur une même figure

    # Dictionnaire des couleurs sRGB associées aux carrés (pour plot les courbes avec la bonne couleur)
    couleurs_sRGB = {
    "1": (0.8, 0.8, 0.8),  # Blanc grisé pour la visibilité
    "2": (0.0, 0.0, 0.0),  # Noir
    "3": (0.0, 0.0, 0.5),  # Bleu marine
    "4": (0.0, 0.5, 0.0),  # Vert
    "5": (0.8, 0.0, 0.0),  # Rouge
    "6": (0.85, 0.7, 0.0),  # Jaune 
    "7": (0.9, 0.0, 0.9),  # Magenta 
    "8": (0.0, 0.7, 0.9)   # Cyan 
    }

    # Tracé des spectres avec les couleurs associées
    plt.figure(figsize=(10, 6))
    for key, spectre_reflexion in spectre_reflexion_dict.items():
        if key in couleurs_sRGB:
            plt.plot(wavelength, spectre_reflexion, label=key, color=couleurs_sRGB[key])

    plt.title("Spectres de réflexion des 8 carrés (6500K)")
    plt.xlabel("Longueur d'onde (nm)")
    plt.ylabel("Réflexion intensité")
    plt.legend()
    plt.grid()
    plt.show()





def spectrum_to_XYZ(spectre, k):
    """
    Retourne le triplet XYZ associé à un spectre.

    Args:
        spectre (liste de float): Une liste contenant les valeurs du spectre entre 380nm et 780nm.
        k: facteur de normalisation, il doit être commun à tous les spectres
        
    Returns:
        liste: [X, Y, Z]

    """
    
    #Importation et traitement des données de la cie (1931)
    cie_xyz = pd.read_csv(r"data\CIE data\CIE_xyz_1931_2deg.csv") 
    cie_xyz_np = cie_xyz.to_numpy()
    cie_xyz_np_truncated = cie_xyz_np[19:len(cie_xyz_np) - 80] #de 380 à 780

    x = cie_xyz_np_truncated[:, 1]  # x_bar
    y = cie_xyz_np_truncated[:, 2]  # y_bar
    z = cie_xyz_np_truncated[:, 3]  # z_bar

    
    X = k*trapz(spectre * x, wavelength) #On applique la formule en intégrant
    Y = k*trapz(spectre * y, wavelength)
    Z = k*trapz(spectre * z, wavelength)

    return [X, Y, Z]





def plot_cie_data():
    """
    Plot les data de la CIE 1931 (colour matching function)

    Args:

    Returns:
        figure

    """
    #Importation et traitement des données de la cie (1931)
    cie_xyz = pd.read_csv(r"data\CIE data\CIE_xyz_1931_2deg.csv") 
    cie_xyz_np = cie_xyz.to_numpy()
    cie_xyz_np_truncated = cie_xyz_np[19:len(cie_xyz_np) - 80] #de 380 à 780
    
    x = cie_xyz_np_truncated[:, 1]  # x_bar
    y = cie_xyz_np_truncated[:, 2]  # y_bar
    z = cie_xyz_np_truncated[:, 3]  # z_bar
    
    plt.figure()
    plt.plot(wavelength, x, color='red', label='x')
    plt.plot(wavelength, y, color='green', label='y')
    plt.plot(wavelength, z, color='blue', label='z')
    plt.legend()
    plt.title("CIE1931 colour-matching functions")
    plt.grid()
    plt.show()





def gamma_correction(rgb):
    """
    Plot les data de la CIE 1931 (colour matching function)

    Args:

    Returns:
        figure

    """
    return np.where(rgb <= 0.0031308, 12.92 * rgb, 1.055 * (rgb ** (1 / 2.4)) - 0.055)







def XYZ_to_sRGB(X, Y, Z):
    """
    Convertit un triplet XYZ en un triplet sRGB
    
    Args: X, Y, Z: floats

    Returns:
            list: [R, G, B]

    """    
    #On utilise la matrice de conversion sRGB
    M_XYZ_to_sRGB = np.array([[3.2406, -1.5372, -0.4986],
                              [-0.9689, 1.8758, 0.0415],
                              [0.0557, -0.2040, 1.0570]])


    RGB = np.dot(M_XYZ_to_sRGB, np.array([X, Y, Z])) #On applique la transformation en sRGB
    RGB_clipped = np.clip(RGB, 0, 1) #On enlève les valeurs supérieures à 1
    RGB_corrected = gamma_correction(RGB_clipped) #On applique la correction gamma
    RGB_255 = np.floor(RGB_corrected * 255).astype(int) #On convertit dans le formet [0, 255] plus intuitif


    return RGB_255







def plot_colorchecker(order, rgb_dict):
    """
    Plot le colorchecker
    
    Args: 
        order: tableau de int spécifiant la mise en page avec nous voulons mettre chaque couleur représentée par un numéro
        rgb_dict: dictionnaire contenant les valeurs [R, G, B] de chaque carré représenté par un numéro
        
    Returns:
            figure

    """       
    
    # Récupérer la couleur de la première case (le blanc) pour le plot
    #Cela permet d'écrire le titre de l'image et celui des textes à partir du blanc de référence
    #de l'éclairage. Pour éviter l'adaptation chromatique
    first_idx = order[0][0] #index
    RGB_first_255 = rgb_dict[f"{first_idx}"]
    # Couleur de la première case en format hexadécimal
    RGB_first_hex = '#{:02x}{:02x}{:02x}'.format(*RGB_first_255)


    #Forme figure Colorchecker
    fig, axes = plt.subplots(2, 4, figsize=(15, 6), facecolor='black')
    fig.suptitle("Couleurs sRGB pour 8 carrés, éclairage 6500K, konica", fontsize=16, color=RGB_first_hex)

    #Plot des carrés
    for row in range(2):
        for col in range(4):
            idx = order[row][col]
            RGB_image = rgb_dict[f"{idx}"] 
            ax = axes[row, col] #plot du carré
            ax.imshow(np.ones((10, 10, 3)) * RGB_image / 255)
            ax.axis('off')
            # Titre avec la couleur de la première case pour éviter l'adaptation chromatique avec le blanc de python
            ax.set_title(f"Case {idx}\nRGB = {tuple(RGB_image)}", fontsize=8, color=RGB_first_hex)

    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()




#%% CODE
#IMPORTATION ET TRAITEMENT DU SPECTRE DE LA SOURCE ET DES ALBEDOS

# Lire le fichier CSV avec pandas, 
source = pd.read_csv(r"data\Spectre des sources\output_ref_konica_led_6500K.csv") #konica

source_numpy = source.to_numpy() #On convertit en numpy pour retravailler les données plus facilement
#Extraction de la longueur d'onde et de l'intensité
#konica, les données sélectionnées varient en fonction de l'appareil utilisé, ici c'est pour le konica
wavelength = source_numpy[0:371,0]
intensite_spectre = source_numpy[0:371,1]
#Normalisation du spectre
intensite_spectre = intensite_spectre/np.max(intensite_spectre)



plot_source()

# output_filename1 = r"C:\Etudes\SupOp - Copie\2A\Projet\Resultats Simulations\6500K\spectre_source_6500K.png"
# plt.savefig(output_filename1, dpi=300, bbox_inches='tight')  




#Importation de l'albédo pour chaque carré

# Initialisation d'un dictionnaire pour stocker les données d'albédo
albedo_dict = {}

# Boucle pour importer chaque fichier
for i in range(1, 9):  # de 1 à 9 inclus
    # Chemin du fichier
    filepath = rf"data\albedo\led_4000K_USB4H112691__{i}.csv" 
    # Importation des données
    albedo_import = pd.read_csv(filepath, header=None)
    albedo_np_import = albedo_import.to_numpy()
    
    # Extraction de la colonne d'albédo (sans la colonne de longueur d'onde)
    albedo = albedo_np_import[: , 2]
    
    # Stockage des données dans le dictionnaire avec un nom unique
    albedo_dict[f"albedo_{i}"] = albedo


# # Vérification des données
# for key, value in albedo_dict.items():
#     print(f"{key}: {value[:5]}")  # Affiche les 5 premières valeurs pour chaque albédo





# Initialisation des dictionnaires pour stocker les résultats de BRDF et du spectre de réflexion
brdf_dict = {}
spectre_reflexion_dict = {}

# Boucle pour calculer le BRDF et le spectre de réflexion pour chaque albédo
for i in range(1, 9):
    # Récupérer l'albédo pour le carré actuel
    albedo_np = albedo_dict[f"albedo_{i}"]

    # Calculer le BRDF pour chaque carré
    brdf = calcul_brdf(albedo_np)   
    brdf_dict[f"brdf_{i}"] = brdf  # Stocker dans le dictionnaire brdf_dict

    # Calcul du spectre de réflexion
    spectre_reflexion = calcul_spectre_reflexion(intensite_spectre, brdf)  
    spectre_reflexion_dict[f"{i}"] = spectre_reflexion  # Stocker dans le dictionnaire spectre_reflexion_dict





plot_spectres_reflexions()

# output_filename2  = r"C:\Etudes\SupOp - Copie\2A\Projet\Resultats Simulations\6500K\spectres_reflexions_6500K.png"
# plt.savefig(output_filename2, dpi=300, bbox_inches='tight')  



# CONVERSION EN XYZ

#Calcul de k
k = 1/ trapz(spectre_reflexion_dict["1"], wavelength)

xyz_normalized_dict = {}

for key, spectre_reflexion in spectre_reflexion_dict.items():
    xyz_normalized_dict[key] = spectrum_to_XYZ(spectre_reflexion, k) #On applique la fonction



#CONVERSION EN sRGB et affichage


rgb_dict = {}

for key, XYZ in xyz_normalized_dict.items():
    rgb_dict[key] = XYZ_to_sRGB(XYZ[0], XYZ[1], XYZ[2]) #On applique la fonction



#Pour le plot, ordre des carrés qui correspond à l'ordre des mesures et au numéro dans les fichiers.
order = [
    [1, 2, 3, 4],
    [5, 6, 7, 8]
]


plot_colorchecker(order, rgb_dict)


#On enregistre le résultat

# output_filename3 = r"C:\Etudes\SupOp - Copie\2A\Projet\Resultats Simulations\6500K\colorchecker_8carres_6500K.png"
# plt.savefig(output_filename3, dpi=300, bbox_inches='tight')  


# Afficher les valeurs RGB calculées
# for key, value in rgb_dict.items():
#     print(f"{key}: RGB = {value}")


#%% ####################EXPORTATION DONNEES#########################


# # # Dictionnaire des couleurs associées aux spectres
# color_names = {
#     "spectre_reflexion_1": "blanc",
#     "spectre_reflexion_2": "noir",
#     "spectre_reflexion_3": "bleu marine",
#     "spectre_reflexion_4": "vert",
#     "spectre_reflexion_5": "rouge",
#     "spectre_reflexion_6": "jaune",
#     "spectre_reflexion_7": "magenta",
#     "spectre_reflexion_8": "cyan"
# }

# # # Nom du fichier de sortie

# output_csv_file = "couleurs_rgb_export_2700K.csv"



# # Écriture dans le fichier CSV
# with open(output_csv_file, mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
    
#     # Écriture de l'en-tête
#     writer.writerow(["Couleur", "R", "G", "B"])
    
#     # Écriture des valeurs du dictionnaire
#     for key, rgb in rgb_dict.items():
#         color_name = color_names.get(key, "inconnu")  # Récupérer le nom de la couleur
#         writer.writerow([color_name, rgb[0], rgb[1], rgb[2]])





