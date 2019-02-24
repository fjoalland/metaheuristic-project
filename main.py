import csv
import pandas as pd
import random
import matplotlib.pyplot as plt


import parametre as parametre
import fonctions.population as population
import fonctions.calcul_score as calcul_score
import fonctions.fournisseur_donnees as fournisseur_donnees
import fonctions.graphique as graphique

#***************************************************
#******CHARGEMENT DES DONNEES DU FICHIER CSV********
#***************************************************
fournisseur_donnees.chargement_donnees()


#**********************************
#********1ere GENERATION***********
#**********************************

#Création de la premiere generation 
premiereGeneration = population.genererPopulation(parametre.populationTotal)
#Afin de retrouver l'individu, on assigne un identifiant unique
individuId = 0

#Boucle sur la liste des individus de la premiere generation
for index, individu in enumerate(premiereGeneration):

	#Verification que l'individu représente bien un chemin hamiltonien
	#Retourne vrai ou faux
	hamiltonienChemin = population.verichierCheminHamiltonien(individu)

	#Si le chemin est bien hamiltonien
	if(hamiltonienChemin):
		#Calcul des différents scores de cet individu
		calcul_score.calculDesScores(individu, individuId)
		individuId += 1

parametre.generationList.append(0)
parametre.meilleurScoreList.append(parametre.scoreList[0][0])
parametre.meilleurQPprixList.append(parametre.meilleurQPprix)
parametre.meilleurQPtempsList.append(parametre.meilleurQPtemps)
parametre.meilleurlowCostRoutePrixList.append(parametre.meilleurlowCostRoutePrix)
parametre.routeLenteScoreList.append(parametre.routeLenteScore)

#**********************************
#**********x GENERATION************
#**********************************

#Boucle sur le nombres de générations
for x in range(parametre.generationTotal):

	parametre.generationList.append(x + 1)

	#Copie les scores de la generation precedente dans une liste parent
	scoreListParent=parametre.scoreList.copy()

	survivantList = population.survivantElite(scoreListParent)

	#Liste des scores à vide
	parametre.scoreList=[]
	#Copie les chemins de la generation precedente dans une liste parent
	populationParent = parametre.populationList.copy()
	#Liste des chemins à vide
	parametre.populationList = []	
	#Identifiant remit à 0
	individuId = 0

	#Boucle sur tous les scores de la generation precedente
	for index, score in enumerate(scoreListParent):

		#Combat des candidats pour faire resortir les meilleurs
		parent1 = population.tournament(score, scoreListParent)
		parent2 = population.tournament(score, scoreListParent)

		#Croisement de l'ADN du parent 1 et parent 2
		enfant = population.croisement(parent1, parent2, populationParent)

		#Verification que l'individu représente bien un chemin hamiltonien
		#Retourne vrai ou faux
		hamiltonienChemin = population.verichierCheminHamiltonien(enfant)
		if(hamiltonienChemin):
			#Calcul des différents scores de cet individu
			calcul_score.calculDesScores(enfant, individuId)
			individuId += 1

	#On genere un surplue de population pour garentir une disparité
	nouvellePopulationIntegre = population.genererPopulation(parametre.populationTotal // 15)
	for index, individual in enumerate(nouvellePopulationIntegre):

		#Verification que l'individu représente bien un chemin hamiltonien
		#Retourne vrai ou faux
		hamiltonienChemin = population.verichierCheminHamiltonien(individual)
		if(hamiltonienChemin):
			#Calcul des différents scores de cet individu
			calcul_score.calculDesScores(individual, individuId)
			individuId += 1

	for index, survivantScore in enumerate(survivantList):
		survivant = populationParent[survivantScore[1]]
		calcul_score.calculDesScores(survivant, individuId)
		individuId += 1

	parametre.scoreList.sort()
	parametre.meilleurScoreList.append(parametre.scoreList[0][0])
	parametre.meilleurQPprixList.append(parametre.meilleurQPprix)
	parametre.meilleurQPtempsList.append(parametre.meilleurQPtemps)
	parametre.meilleurlowCostRoutePrixList.append(parametre.meilleurlowCostRoutePrix)
	parametre.routeLenteScoreList.append(parametre.routeLenteScore)
	print("***************")
	print("generation: ", x)
	print("population: ", len(parametre.populationList))
	print("Best score of this generation:", parametre.scoreList[0][0])

print("***************")
print("THE BEST SCORE THROUGH THE EVOLUTION")
print("Best score:", parametre.meilleurScore)
print("The route:", parametre.meilleurScoreRoute)
print("***************")
print("***************")
print("BEST PRICE / TIME RATION")
print("Price:", parametre.meilleurQPprix)
print("Time:", parametre.meilleurQPtemps)
print("Conveyance:", parametre.meilleurQPtransport)
print("The route:", parametre.meilleurQPchemin)
print("***************")
print("***************")
print("THE LEAST EXPENSIVE WAY")
print("Price:", parametre.meilleurlowCostRoutePrix)
print("The route:", parametre.meilleurlowCostRoute)
print("***************")
print("***************")
print("THE LONGEST WAY")
print("Time:", parametre.routeLenteScore)
print("The route:", parametre.routeLenteScoreRoute)

graphique.dessinerGraphiqueMeilleurScore()
graphique.dessinerGraphiqueRapportQPprice()
graphique.dessinerGraphiqueRapportQPtime()
graphique.dessinerGraphiqueMeilleurPrix()
graphique.afficherLesGraphiques()