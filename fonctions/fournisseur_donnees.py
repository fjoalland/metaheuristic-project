import csv
import pandas as pd
import random

import parametre as parametre


#***************************************************
#******CHARGEMENT DES DONNEES DU FICHIER CSV********
#***************************************************

def chargement_donnees():
	#Chargement du fichier CSV avec toutes les données
	with open("donnees/" + parametre.fichierDonnees, newline='', encoding = "ISO-8859-1") as csvFichier:
		#On récupère les données dans une liste
		csvFichierDonnees = csv.reader(csvFichier, delimiter=';')
		for index, ligne in enumerate(csvFichierDonnees):
			#parametre.capitaleTotal correspond au nombre total des capitales
			parametre.capitaleTotal = len(ligne)

			if(index == 0):
				parametre.CapitalesList = ligne
				#Supprime le premiere element qui est une case vide dans le fichier CSV
				del parametre.CapitalesList[0]
			else:
				#Supprime la premiere ligne correspondant aux capitales et non au distance
				del ligne[0]
				parametre.Distances.append(ligne)

	#Contiend toutes les distances entre les capitales
	parametre.distanceInterCapitales = pd.DataFrame(parametre.Distances, columns=parametre.CapitalesList, index=parametre.CapitalesList) 
	