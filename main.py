import csv
import pandas as pd
import random

import parametre as parametre
import fonctions.population as population
import fonctions.calcul_score as calcul_score
import fonctions.fournisseur_donnees as fournisseur_donnees

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


#**********************************
#**********x GENERATION************
#**********************************

#Boucle sur le nombres de générations
for x in range(parametre.generationTotal):
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


	print("***************")
	print("generation: ", x)
	print("population: ", len(parametre.populationList))
	print("meilleur score de cette generation:", parametre.scoreList[0][0])

print("***************")
print("***************")
print("prix le plus bas:", parametre.meilleurlowCostRoutePrix)
print("chemin le moin couteux:", parametre.meilleurlowCostRoute)
print("meilleur score:", parametre.meilleurScore)
print("meilleure score route:", parametre.meilleurScoreRoute)
print("temps le plus long:", parametre.routeLenteScore)
print("temps le plus long route:", parametre.routeLenteScoreRoute)
print("***************")
print('MEILLEUR RAPPORT QUALITE PRIX:')
print("Chemin", parametre.meilleurQPchemin)
print("Transport", parametre.meilleurQPtransport)
print("Score", parametre.meilleurQPscore)
print("Prix", parametre.meilleurQPprix)
print("Temps", parametre.meilleurQPtemps)