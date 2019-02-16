import csv
import pandas as pd
import random

import parametre as parametre

#******************************************************
#******CALCULER LE MEILLEUR PRIX POUR UN INDIVIDU******
#******************************************************

def verifierPrixMoinCher(individu):
	global meilleurlowCostRoutePrix
	global meilleurlowCostRoute

	#Prix de départ, 0 euro.
	lowCostRouteIndividu=0

	for index, geneVille in enumerate(individu):
		if(index != len(parametre.CapitalesList)):  
			moyenTransport = parametre.distanceInterCapitales.loc[geneVille,individu[index+1]].split("/")

			#On priorise les distances par autocar, très peu couteuses. Puis bateau, et enfin, l'avion. 
			if(moyenTransport[0] != '-'):
				lowCostRouteIndividu += (int(moyenTransport[0]) * parametre.autocarPrix)
			elif(moyenTransport[2] != '-'):
				lowCostRouteIndividu += (int(moyenTransport[2]) * parametre.bateauPrix)
			elif(moyenTransport[1] != '-'):
				lowCostRouteIndividu += (int(moyenTransport[1]) * parametre.avionPrix)
		
	#Si l'individu est le meilleur candidat, on actualise la variable globale.
	if parametre.meilleurlowCostRoutePrix > lowCostRouteIndividu:
		parametre.meilleurlowCostRoutePrix = lowCostRouteIndividu
		parametre.meilleurlowCostRoute = individu


#******************************************************
#********VERIFIER SI INDIVIDU MEILLEURE SCORE**********
#******************************************************

def verifierMeilleurScore(individu, scoreIndividu):
	global meilleurScore
	global meilleurScoreRoute
	if(scoreIndividu < parametre.meilleurScore):
		parametre.meilleurScore = scoreIndividu
		parametre.meilleurScoreRoute = individu


#******************************************************
#*****VERIFIER SI INDIVIDU MEILLEURE ROUTE LENTE*******
#******************************************************

def verifierRouteLente(individu):
	global routeLenteScore
	global routeLenteScoreRoute

	#Intialise le temps total du chemin à 0.
	tempsTotal=0

	for index, gene in enumerate(individu):
		if(index != len(parametre.CapitalesList)):  
			moyenTransport = parametre.distanceInterCapitales.loc[gene,individu[index+1]].split("/")

			#Prioritisation des trajets par bateau (très long), puis autocar et enfin avion.
			if(moyenTransport[2] != '-'):
				tempsTotal += (int(moyenTransport[2]) / parametre.bateauVitesse)
			elif(moyenTransport[0] != '-'):
				tempsTotal += (int(moyenTransport[0]) / parametre.autocarVitesse)
			elif(moyenTransport[1] != '-'):
				tempsTotal += (int(moyenTransport[1]) / parametre.avionVitesse) + 1

	#Si l'individu a le trajet le plus long jamais trouvé, on actualise la variable globale.
	if(parametre.routeLenteScore < tempsTotal):
		parametre.routeLenteScore = tempsTotal
		parametre.routeLenteScoreRoute = individu


#******************************************************
#**********VERIFIER SI CHEMIN POSSIBLE*****************
#******************************************************

def calculerScoreIndividu(individu):
	score=0
	for index, gene in enumerate(individu):
		if(index != len(parametre.CapitalesList)):  
			moyenTransport = parametre.distanceInterCapitales.loc[gene,individu[index+1]].split("/")
			moyenTransportDisponible = [ elem for elem in moyenTransport if elem != "-"]
			distanceMinimum = min(moyenTransportDisponible, key=float)
			score=score+int(distanceMinimum)
	return score

def calculerRapportQualitePrix(individu):

	transportListe = []
	temps=0
	prix = 0

	for index, gene in enumerate(individu):
			if(index != len(parametre.CapitalesList)):
				moyenTransport = parametre.distanceInterCapitales.loc[gene,individu[index+1]].split("/")
				for i, transportDistance in enumerate(moyenTransport):
					if(transportDistance == "-"):
						moyenTransport[i] = 0


				transportTerrestre = int(moyenTransport[0])
				transportAvion = int(moyenTransport[1])
				transportMaritine = int(moyenTransport[2])
				trajetSelectionne = ""

				#CALCUL DU MEILLEUR TRAJET ENTRE VILLE A ET VILLE B
				#La meilleur qualité prix se base sur ma propre experience de qualité
				#Privilegier le avions si grande difference avec la voiture par exemple
				if (transportTerrestre != 0):
					if(transportTerrestre - transportAvion > 500 and transportAvion != 0):
						trajetSelectionne = "avion"
					elif(transportMaritine - transportTerrestre > 200 
						and transportMaritine - transportTerrestre < 1000 
						and transportMaritine != 0):
						trajetSelectionne = "bateau"
					else: 
						trajetSelectionne ="voiture"
				elif (transportAvion != 0):
					if(transportMaritine - transportAvion > 500 and transportMaritine - transportAvion < 1200 and transportMaritine != 0):
						trajetSelectionne = "bateau"
					else:
						trajetSelectionne = "avion"
				else:
					trajetSelectionne = "bateau"


				if(trajetSelectionne == "voiture"):
					if(transportTerrestre < parametre.distanceVoitureMaximumQualite):
						transportListe.append('car')
						temps += transportTerrestre / parametre.voitureVitesse
						prix += transportTerrestre * parametre.voiturePrix
					elif(transportTerrestre < parametre.distanceAutocarMaximumQualite and transportTerrestre > parametre.distanceVoitureMaximumQualite):
						transportListe.append('autocar')
						temps += transportTerrestre / parametre.autocarVitesse
						prix += transportTerrestre * parametre.autocarPrix
					else:
						transportListe.append('train')
						temps += transportTerrestre / parametre.trainVitesse
						prix += transportTerrestre * parametre.trainPrix
				elif(trajetSelectionne == "bateau"):
					transportListe.append('boat')
					temps += transportMaritine / parametre.bateauVitesse
					prix += transportMaritine * parametre.bateauPrix
				elif(trajetSelectionne == "avion"):		
					transportListe.append('plane')
					temps += transportAvion / parametre.avionVitesse
					prix += transportAvion * parametre.avionPrix

	score =  ((prix * 10) + temps)/2
	if(parametre.meilleurQPscore > score):
		parametre.meilleurQPscore = score
		parametre.meilleurQPprix = prix
		parametre.meilleurQPtemps = temps
		parametre.meilleurQPchemin = individu
		parametre.meilleurQPtransport = transportListe



#******************************************************
#*****FONCTION GLOBAL CALCULANT TOUS LES SCORES********
#******************************************************

def calculDesScores(individu, individuId):
	#Calculation de son score
	scoreIndividu = calculerScoreIndividu(individu)
	#Verifier si individu a le prix le plus bas
	verifierPrixMoinCher(individu)
	#Verifier si individu a le meilleur score
	verifierMeilleurScore(individu, scoreIndividu)
	#Verifier si individu a la route la plus lente
	verifierRouteLente(individu)

	calculerRapportQualitePrix(individu)

	#Ajout du score et de son ID dans la liste de tous les scores des individus
	parametre.scoreList.append([scoreIndividu, individuId])
	#Ajout du score dans la liste de tous les chemins des individus
	parametre.populationList.append(individu)


