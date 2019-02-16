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
generationTotal=200
#Nombre d'individu qui vont combatre dans un tournoi.
combattantParTournoi=2
#EN % - Probabilité d'avoir une mutation par individu (en pourcentage).
mutationProbabilite = 5#%
#EN % - L'élite pouvant survivre à la génération suivante  (en pourcentage).
survivantElitePourcentage = 2#%
# Afin d'avoir une bonne diversité entre les individus, il est possible de creer une nouvelle population dans une génération
# Il est preferable que cette nouvelle population soit faible par raport à la population de début
#Par défaut elle correspond à 3% de la population totale de début
#0.3 correpond à 3%
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

#Indicateur permettant de determiner ou non l'utilisation d'un moyen de transport
#Dans le cadre d'un calcul de rapport qualite prix

#La distance maximum en voiture accepté comme gage de qualité
distanceVoitureMaximumQualite = 200
#La distance maximum en autocar accepté comme gage de qualité
distanceAutocarMaximumQualite = 600


#***************************
#******VARIABLE GLOBALE*****
#***************************
#******NE PAS MODIFIER******

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
#Représente les distances d'une ville A à une ville B
distanceInterCapitales= []
#Représente la liste des capitales
CapitalesList=[]
#Représente le totale des capitales 
capitaleTotal=0

meilleurQPscore = 9999999
meilleurQPprix = 0
meilleurQPtemps = 0
meilleurQPchemin  = []
meilleurQPtransport = []

