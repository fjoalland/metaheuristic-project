import csv
import pandas as pd
import random

#***************************
#****VARIABLE MODIFIABLE****
#***************************

#Contiend toutes les donnees inter capitales dans un fichier logique de type CSV
fichierDonnees = "base2.csv"
#Point de départ du circuit
pointDeDepart="Paris"
#nombre d'individu dans la premiere génération.
populationTotal=200
#Nombre de generation.
generationTotal=50
#Nombre d'individu qui vont combatre dans un tournoi.
combattantParTournoi=3
#EN % - Probabilité d'avoir une mutation par individu (en pourcentage).
mutationProbabilite = 10#%
#EN % - L'élite pouvant survivre à la génération suivante
survivantElitePourcentage = 1#%
# Afin d'avoir une bonne diversité entre les individus, il est possible de creer une nouvelle population dans une génération
# Il est preferable que cette nouvelle population soit faible par raport à la populationTotal
#Par défaut elle correspond à 5% de la population totale de début
nouvellePopulationParGeneration = int(populationTotal * 0.3)

#Prix en euro d'un kilometre pour un moyen de transport donné.
autocarPrix=0.07#€/km
bateauPrix=0.08#€/km
trainPrix=0.10#€/km
avionPrix=0.15#€/km
voiturePrix=0.19#€/km

#vitesse d'un vehicule en km/h.
autocarVitesse=90#km/h
bateauVitesse=40#km/h
trainVitesse=320#km/h
avionVitesse=900#km/h
voitureVitesse=130#km/h


#***************************
#******VARIABLE GLOBALE*****
#***************************

#Permets de récupérer les distances inter-capitales du fichier CSV.
Distances=[]
#Liste contenant les scores de chaque individu de la génération actuelle.
scoreList=[]
#Liste contenant les individus de la génération actuelle.
populationList=[]
#Score le plus lent en temps de tous les individus. Elle est initiée à 0 au début et sera modifiée
#lorsque l'algorithme identifiera un score plus lent.
routeLenteScore = 0
#Route la plus longue en temps du point de départ au point d'arrivé.
routeLenteScoreRoute = []
#Route avec le chemin le plus rapide.
meilleurScoreRoute =[]
#Score avec le chemin le plus rapide. Variable initiée avec un score élévé au début, elle sera
#modifiée l'algorithme identifiera un meilleur score.
meilleurScore=99999
#Route avec le prix le plus bas
meilleurlowCostRoute=[]
#Score avec le prix le plus bas. Variable initiée avec un score élévé au début, elle sera
#modifiée l'algorithme identifiera un meilleur score.
meilleurlowCostRoutePrix=99999


#***************************************************
#******CHARGEMENT DES DONNEES DU FICHIER CSV********
#***************************************************

#Chargement du fichier CSV avec toutes les données
with open(fichierDonnees, newline='') as csvFichier:
	#On récupère les données dans une liste
	csvFichierDonnees = csv.reader(csvFichier, delimiter=';')
	for index, ligne in enumerate(csvFichierDonnees):
		#capitaleTotal correspond au nombre total des capitales
		capitaleTotal = len(ligne)

		if(index == 0):
			CapitalesList = ligne
			#Supprime le premiere element qui est une case vide dans le fichier CSV
			del CapitalesList[0]
		else:
			#Supprime la premiere ligne correspondant aux capitales et non au distance
			del ligne[0]
			Distances.append(ligne)

#Conteind toutes les distances entre les capitales
distanceInterCapitales = pd.DataFrame(Distances, columns=CapitalesList, index=CapitalesList) 


#**********************************
#******GENERER UNE POPULATION******
#**********************************

def genererPopulation(taille):
	#Contiend la liste de tous les individus d'une nouvelle population
	nouvellePopulationListe = []

	#On boucle sur la taille renseigné en paramètre de la fonction
	for x in range(taille):

		#On ordonne les capitales au hasard
		random.shuffle(CapitalesList)
		#On renseigne comme premiere ville du chemin, la ville de départ
		chemin = [pointDeDepart]
		#Nombre de capitales qui peuvent être visité
		#On enlève une capitale correspondant à la ville de départ
		capitaleVisitable = capitaleTotal -1

		#Boucle sur le nombre de capitales visitables
		for x in range(capitaleVisitable):

			#Boucle sur la liste des capitales
			for index, uneCapitale in enumerate(CapitalesList):

				#Calcul de la distance entre la ville précedente et la ville en cours
				distanceVillePrecedenteVilleActuelle = distanceInterCapitales.loc[chemin[len(chemin)-1], uneCapitale]

				#Verification si il nous reste une ville a visiter
				if(len(chemin) == len(CapitalesList) - 1):
					#Calcul de la distance entre la ville actuelle et le point de départ / arrivée
					distanceVilleActuellePointDepart = distanceInterCapitales.loc[pointDeDepart, uneCapitale]
					
					#Verification que la ville actuelle est bien déservie par la ville précedente et le point d'arrivée
					if(distanceVillePrecedenteVilleActuelle!= "" 
					and distanceVilleActuellePointDepart!= "" 
					and uneCapitale not in chemin):
						#ajout de la ville dans le chemin
						chemin.append(uneCapitale)
						chemin.append(pointDeDepart)

				#Sinon, si ce n'est pas la deriere ville a visiter.
				#Verification que le chemin est bien possible
				elif (distanceVillePrecedenteVilleActuelle != "" and uneCapitale not in chemin):
					chemin.append(uneCapitale)

		#Si le chemin est une graphe hamiltonien, on ajoute ce chemin à la nouvelle population. 			
		if(len(chemin) == capitaleTotal):
			nouvellePopulationListe.append(chemin)

	return nouvellePopulationListe


#******************************************************
#******CALCULER LE MEILLEUR PRIX POUR UN INDIVIDU******
#******************************************************

def verifierPrixMoinCher(individu):
	global meilleurlowCostRoutePrix
	global meilleurlowCostRoute

	#Prix de départ, 0 euro.
	lowCostRouteIndividu=0

	for index, geneVille in enumerate(individu):
		if(index != len(CapitalesList)):  
			moyenTransport = distanceInterCapitales.loc[geneVille,individu[index+1]].split("/")

			#On priorise les distances par autocar, très peu couteuses. Puis bateau, et enfin, l'avion. 
			if(moyenTransport[0] != '-'):
				lowCostRouteIndividu += (int(moyenTransport[0]) * autocarPrix)
			elif(moyenTransport[2] != '-'):
				lowCostRouteIndividu += (int(moyenTransport[2]) * bateauPrix)
			elif(moyenTransport[1] != '-'):
				lowCostRouteIndividu += (int(moyenTransport[1]) * avionPrix)
		
	#Si l'individu est le meilleur candidat, on actualise la variable globale.
	if meilleurlowCostRoutePrix > lowCostRouteIndividu:
		meilleurlowCostRoutePrix = lowCostRouteIndividu
		meilleurlowCostRoute = individu


#******************************************************
#********VERIFIER SI INDIVIDU MEILLEURE SCORE**********
#******************************************************

def verifierMeilleurScore(individu, scoreIndividu):
	global meilleurScore
	global meilleurScoreRoute
	if(scoreIndividu < meilleurScore):
		meilleurScore = scoreIndividu
		meilleurScoreRoute = individu


#******************************************************
#*****VERIFIER SI INDIVIDU MEILLEURE ROUTE LENTE*******
#******************************************************

def verifierRouteLente(individu):
	global routeLenteScore
	global routeLenteScoreRoute

	#Intialise le temps total du chemin à 0.
	tempsTotal=0

	for index, gene in enumerate(individu):
		if(index != len(CapitalesList)):  
			moyenTransport = distanceInterCapitales.loc[gene,individu[index+1]].split("/")

			#Prioritisation des trajets par bateau (très long), puis autocar et enfin avion.
			if(moyenTransport[2] != '-'):
				tempsTotal += (int(moyenTransport[2]) / bateauVitesse)
			elif(moyenTransport[0] != '-'):
				tempsTotal += (int(moyenTransport[0]) / autocarVitesse)
			elif(moyenTransport[1] != '-'):
				tempsTotal += (int(moyenTransport[1]) / avionVitesse) + 1

	#Si l'individu a le trajet le plus long jamais trouvé, on actualise la variable globale.
	if(routeLenteScore < tempsTotal):
		routeLenteScore = tempsTotal
		routeLenteScoreRoute = individu


#******************************************************
#********VERIFIER SI CHEMIN EST HAMILTONIEN************
#******************************************************

def verifierChemin(individu):
	estPossible = True

	#On boucle sur les capitales de l'individu
	for index, geneCapital in enumerate(individu):

		#Verification qu'on est pas sur la dernière ville à visiter
		if(index != len(CapitalesList)):  
			moyenTransport = distanceInterCapitales.loc[geneCapital,individu[index+1]].split("/")

			#Si la taille de la liste des distances inter capitales est 1, le chemin n'est pas possible 
			#La list des distances retournent toujours 3 moyens de transports (voiture, avion, bateau)
			if(len(moyenTransport) == 1):
				estPossible = False

	return estPossible


#******************************************************
#**********VERIFIER SI CHEMIN POSSIBLE*****************
#******************************************************

def calculerScoreIndividu(individu):
	score=0
	for index, gene in enumerate(individu):
		if(index != len(CapitalesList)):  
			moyenTransport = distanceInterCapitales.loc[gene,individu[index+1]].split("/")
			moyenTransportDisponible = [ elem for elem in moyenTransport if elem != "-"]
			distanceMinimum = min(moyenTransportDisponible, key=float)
			score=score+int(distanceMinimum)
	return score


#**********************************
#******CROISEMENT DES PARENTS******
#**********************************

def croisement(parent1, parent2, populationParent):
	AdnParent1 = populationParent[parent1[1]].copy()
	AdnParent2 = populationParent[parent2[1]].copy()
	
	if(parent1[0]>parent2[0]):
		#Si le parent1 a un meilleur score que le parent2
		#Point de croisement sera entre 1 et le total des capitales -1
		pointDeCroisement=random.randint(1,capitaleTotal-1)
	else:
		#Si le parent2 a un meilleur score que le parent1
		#Point de croisement sera entre 1 et la moitie du totale des capitales
		pointDeCroisement=random.randint(1,capitaleTotal- (capitaleTotal // 2))
	
	#Coupage de l'ADN du parent 1 avec le point de croisement
	croisementAdnPartie1 = AdnParent1[1:pointDeCroisement-1]

	#Supression des gênes (capitales) déjà existantes dans l'enfant dans le Parent 2
	for index, geneCapital in enumerate(croisementAdnPartie1):
		AdnParent2.remove(geneCapital)
	
	#Creation de l'enfant
	enfant = AdnParent2[0:len(AdnParent2)-1] + croisementAdnPartie1 + [pointDeDepart] 
	
	#Chance de mutation de l'enfant
	mutationChance = random.randint(1,100)
	if(mutationChance<mutationProbabilite):
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
	for x in range(combattantParTournoi):
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
	survivantTotale = int(len(scoreListParent)*(1*survivantElitePourcentage/100))
	if(survivantTotale == 0):
		survivantTotale = 1

	survivantListe = scoreListParent[0:survivantTotale]
	return survivantListe


#**********************************
#************MUTATION**************
#**********************************

def mutation(individu):
	#Point de mutation aléatoire correspondant à un gêne
	pointDeMutation1 =random.randint(1,capitaleTotal-2)
	pointDeMutation2 =random.randint(1,capitaleTotal-2)
	
	#Recupération des deux gênes qui vont être mutés
	villeMutation = individu[pointDeMutation1]
	villeMutation2 = individu[pointDeMutation2]
	
	#Inversement des deux gênes pour provoquer une mutation
	individu[pointDeMutation1] = villeMutation2
	individu[pointDeMutation2] = villeMutation
	
	return individu


def calculDesScores(individu, individuId):
	#Calculation de son score
	scoreIndividu = calculerScoreIndividu(individu)
	#Verifier si individu a le prix le plus bas
	verifierPrixMoinCher(individu)
	#Verifier si individu a le meilleur score
	verifierMeilleurScore(individu, scoreIndividu)
	#Verifier si individu a la route la plus lente
	verifierRouteLente(individu)

	#Ajout du score et de son ID dans la liste de tous les scores des individus
	scoreList.append([scoreIndividu, individuId])
	#Ajout du score dans la liste de tous les chemins des individus
	populationList.append(individu)



#**********************************
#**********************************
#****EXECUTION DE l'ALGORITHME*****
#**********************************
#**********************************

#**********************************
#********1ere GENERATION***********
#**********************************

#Création de la premiere generation 
premiereGeneration = genererPopulation(populationTotal)
#Afin de retrouver l'individu, on assigne un identifiant unique
individuId = 0

#Boucle sur la liste des individus de la premiere generation
for index, individu in enumerate(premiereGeneration):

	#Verification que l'individu représente bien un chemin hamiltonien
	#Retourne vrai ou faux
	hamiltonienChemin = verifierChemin(individu)

	#Si le chemin est bien hamiltonien
	if(hamiltonienChemin):
		#Calcul des différents scores de cet individu
		calculDesScores(individu, individuId)
		individuId += 1


#**********************************
#**********x GENERATION************
#**********************************

#Boucle sur le nombres de générations
for x in range(generationTotal):
	#Copie les scores de la generation precedente dans une liste parent
	scoreListParent=scoreList.copy()

	survivantList = survivantElite(scoreListParent)

	#Liste des scores à vide
	scoreList=[]
	#Copie les chemins de la generation precedente dans une liste parent
	populationParent = populationList.copy()
	#Liste des chemins à vide
	populationList = []	
	#Identifiant remit à 0
	individuId = 0

	#Boucle sur tous les scores de la generation precedente
	for index, score in enumerate(scoreListParent):

		#Combat des candidats pour faire resortir les meilleurs
		parent1 = tournament(score, scoreListParent)
		parent2 = tournament(score, scoreListParent)

		#Croisement de l'ADN du parent 1 et parent 2
		enfant = croisement(parent1, parent2, populationParent)

		#Verification que l'individu représente bien un chemin hamiltonien
		#Retourne vrai ou faux
		hamiltonienChemin = verifierChemin(enfant)
		if(hamiltonienChemin):
			#Calcul des différents scores de cet individu
			calculDesScores(enfant, individuId)
			individuId += 1

	#On genere un surplue de population pour garentir une disparité
	gen = genererPopulation(populationTotal // 15)
	for index, individual in enumerate(gen):

		#Verification que l'individu représente bien un chemin hamiltonien
		#Retourne vrai ou faux
		hamiltonienChemin = verifierChemin(individual)
		if(hamiltonienChemin):
			#Calcul des différents scores de cet individu
			calculDesScores(individual, individuId)
			individuId += 1

	for index, survivant in enumerate(survivantList):
		survivantChemin = populationParent[survivant[1]]
		calculDesScores(survivantChemin, individuId)
		individuId += 1

	scoreList.sort()


	print("***************")
	print("generation: ", x)
	print("population: ", len(populationList))
	print("meilleur score de cette generation:", scoreList[0][0])

print("***************")
print("***************")
print("prix le plus bas:", meilleurlowCostRoutePrix)
print("chemin le moin couteux:", meilleurlowCostRoute)
print("meilleur score:", meilleurScore)
print("meilleure score route:", meilleurScoreRoute)
print("temps le plus long:", routeLenteScore)
print("temps le plus long route:", routeLenteScoreRoute)
