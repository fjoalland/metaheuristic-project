import csv
import pandas as pd
import random

import parametre as parametre


#**********************************
#******GENERER UNE POPULATION******
#**********************************

def genererPopulation(taille):
	#Contiend la liste de tous les individus d'une nouvelle population
	nouvellePopulationListe = []

	#On boucle sur la taille renseigné en paramètre de la fonction
	for x in range(taille):

		#On ordonne les capitales au hasard
		random.shuffle(parametre.CapitalesList)
		#On renseigne comme premiere ville du chemin, la ville de départ
		chemin = [parametre.pointDeDepart]
		#Nombre de capitales qui peuvent être visité
		#On enlève une capitale correspondant à la ville de départ
		capitaleVisitable = parametre.capitaleTotal -1

		#Boucle sur le nombre de capitales visitables
		for x in range(capitaleVisitable):

			#Boucle sur la liste des capitales
			for index, uneCapitale in enumerate(parametre.CapitalesList):

				#Calcul de la distance entre la ville précedente et la ville en cours
				distanceVillePrecedenteVilleActuelle = parametre.distanceInterCapitales.loc[chemin[len(chemin)-1], uneCapitale]

				#Verification si il nous reste une ville a visiter
				if(len(chemin) == len(parametre.CapitalesList) - 1):
					#Calcul de la distance entre la ville actuelle et le point de départ / arrivée
					distanceVilleActuellePointDepart = parametre.distanceInterCapitales.loc[parametre.pointDeDepart, uneCapitale]
					
					#Verification que la ville actuelle est bien déservie par la ville précedente et le point d'arrivée
					if(distanceVillePrecedenteVilleActuelle!= "" 
					and distanceVilleActuellePointDepart!= "" 
					and uneCapitale not in chemin):
						#ajout de la ville dans le chemin
						chemin.append(uneCapitale)
						chemin.append(parametre.pointDeDepart)

				#Sinon, si ce n'est pas la deriere ville a visiter.
				#Verification que le chemin est bien possible
				elif (distanceVillePrecedenteVilleActuelle != "" and uneCapitale not in chemin):
					chemin.append(uneCapitale)

		#Si le chemin est une graphe hamiltonien, on ajoute ce chemin à la nouvelle population. 			
		if(len(chemin) == parametre.capitaleTotal):
			nouvellePopulationListe.append(chemin)

	return nouvellePopulationListe


#**********************************
#******CROISEMENT DES PARENTS******
#**********************************

def croisement(parent1, parent2, populationParent):
	AdnParent1 = populationParent[parent1[1]].copy()
	AdnParent2 = populationParent[parent2[1]].copy()
	
	if(parent1[0]>parent2[0]):
		#Si le parent1 a un meilleur score que le parent2
		#Point de croisement sera entre 1 et le total des capitales -1
		pointDeCroisement=random.randint(1,parametre.capitaleTotal-1)
	else:
		#Si le parent2 a un meilleur score que le parent1
		#Point de croisement sera entre 1 et la moitie du totale des capitales
		pointDeCroisement=random.randint(1,parametre.capitaleTotal- (parametre.capitaleTotal // 2))
	
	#Coupage de l'ADN du parent 1 avec le point de croisement
	croisementAdnPartie1 = AdnParent1[1:pointDeCroisement-1]

	#Supression des gênes (capitales) déjà existantes dans l'enfant dans le Parent 2
	for index, geneCapital in enumerate(croisementAdnPartie1):
		AdnParent2.remove(geneCapital)
	
	#Creation de l'enfant
	enfant = AdnParent2[0:len(AdnParent2)-1] + croisementAdnPartie1 + [parametre.pointDeDepart] 
	
	#Chance de mutation de l'enfant
	mutationChance = random.randint(1,100)
	if(mutationChance<parametre.mutationProbabilite):
		#Mutation de l'enfant
		enfant = mutation(enfant)

	return enfant


#**********************************
#***********TOURNOI****************
#**********************************

def tournament(candidat, scoreListParent):
	#On atribue comme vainqueur, le candidat au début du tournoi
	vainqueur = candidat

	#On boucle sur le nombre combattant définie dans les variables globales
	for x in range(parametre.combattantParTournoi):
		combattant = random.choice(scoreListParent)
		#Si le précédent vainqueur perd contre l'actueur combattant 
		if(vainqueur[0] > combattant[0]):
			#Le nouveau vainqueur est l'actuel combattant
			vainqueur = combattant

	#On retourne le grand vainqueur du tournoi
	return vainqueur


#**********************************
#***********SURVIVANT**************
#**********************************

def survivantElite(scoreListParent):

	scoreListParent.sort()
	survivantTotale = int(len(scoreListParent)*(1*parametre.survivantElitePourcentage/100))
	if(survivantTotale == 0):
		survivantTotale = 1

	survivantListe = scoreListParent[0:survivantTotale]
	return survivantListe


#**********************************
#************MUTATION**************
#**********************************

def mutation(individu):
	#Point de mutation aléatoire correspondant à un gêne
	pointDeMutation1 =random.randint(1,parametre.capitaleTotal-2)
	pointDeMutation2 =random.randint(1,parametre.capitaleTotal-2)
	
	#Recupération des deux gênes qui vont être mutés
	villeMutation = individu[pointDeMutation1]
	villeMutation2 = individu[pointDeMutation2]
	
	#Inversement des deux gênes pour provoquer une mutation
	individu[pointDeMutation1] = villeMutation2
	individu[pointDeMutation2] = villeMutation
	
	return individu


#******************************************************
#********VERIFIER SI CHEMIN EST HAMILTONIEN************
#******************************************************

def verichierCheminHamiltonien(individu):
	estPossible = True

	#On boucle sur les capitales de l'individu
	for index, geneCapital in enumerate(individu):

		#Verification qu'on est pas sur la dernière ville à visiter
		if(index != len(parametre.CapitalesList)):  
			moyenTransport = parametre.distanceInterCapitales.loc[geneCapital,individu[index+1]].split("/")

			#Si la taille de la liste des distances inter capitales est 1, le chemin n'est pas possible 
			#La liste des distances retournent toujours 3 moyens de transports (voiture, avion, bateau)
			if(len(moyenTransport) == 1):
				estPossible = False

	return estPossible

