import csv
import pandas as pd
import random

#Contains distances between capitals
Distances=[]

#The beginning city and the point of arrival
firstCity="Paris"

#Number of cities
cityCount=18

#This corresponds to the percentage of mortality of individuals. 
#The stronger an individual, the more likely he is to stay alive and reproduce
individualsTournamentCount=5

listIdentifierUser = []

#The chance percentage that allows an elite to survive the next generation
survivalElite=0.10


#**********************************
#******LOADING THE CSV FILE********
#**********************************
#loading the CSV file containing the distances between capitals
with open('base2.csv', newline='') as csvfile:
	csvFileData = csv.reader(csvfile, delimiter=';')
	for index, row in enumerate(csvFileData):
        
    #Recover the first line containing all capitals
		if(index == 0):
		    Capitals = row
        #Deleting the first element that contains no capitals
		    del Capitals[0]
		else:
        #Deleting the first element that contains only the capitals and not the distances
		    del row[0]
		    Distances.append(row)

# Dataframe for the capitals
intercapitalDistanceData = pd.DataFrame(Distances, columns=Capitals, index=Capitals) 
listScore=[]

population=[]
incrementPath=0
#****************************************
#******GENERATION OF THE POPULATION******
#****************************************
print('---Create Population--')
for x in range(20000):
    #In order to have genes of random individuals, capitals are randomly arranged.
    random.shuffle(Capitals)
    #We start from Paris, so we already have this capital in our Path
    path = [firstCity]
    
    #Loop in all capitals
    for column in range(len(Capitals)):
        #Loop on the list of capitals randomly ranked
        for index, cap in enumerate(Capitals):
            if(len(path) == len(Capitals) - 1):
                #print("Size of the current path {}, size of capitals {}".format(len(path), len(Capitals)))
                if(intercapitalDistanceData.loc[path[len(path)-1], cap]!= "" and intercapitalDistanceData.loc[path[0], cap]!= "" and cap not in path):
                    path.append(cap)
                    path.append(firstCity)
            #If the proposed capital is a destination of the current capital, we add it to our solution
            elif (intercapitalDistanceData.loc[path[len(path)-1],cap] != "" and cap not in path):
                path.append(cap)
                
    if(len(path)==cityCount):
        #print("--------")
        #print(path)
        score=0
        for index, geneCapital in enumerate(path):
            if(index != len(Capitals)):  
                #print(geneCapital + "-" + path[index+1])
                listOfDistance = intercapitalDistanceData.loc[geneCapital,path[index+1]].split("/")
                if("-" in listOfDistance):
                    listOfDistance.remove("-")
                    if("-" in listOfDistance):
                        listOfDistance.remove("-")
                listOfDistance.sort()
                #print(listOfDistance)
                score=score+int(listOfDistance[0])
        #print(score)
        
        listScore.append([ score , incrementPath])
        population.append(path)
        incrementPath += 1

listScore.sort()
print(len(listScore))
print(listScore)

scoreCount = len(listScore)

def calculateScore(candidate, id):
    score=0
    for index, geneCapital in enumerate(candidate):
        if(index != len(Capitals)):  
            #print(geneCapital + "-" + candidate[index+1])
            listOfDistance = intercapitalDistanceData.loc[geneCapital,candidate[index+1]].split("/")
            if("-" in listOfDistance):
                listOfDistance.remove("-")
                if("-" in listOfDistance):
                    listOfDistance.remove("-")
            listOfDistance.sort()
            #print(listOfDistance[0])
            if(listOfDistance[0] == ''):
                score = 0
                break
            else:
                score=score+int(listOfDistance[0])
    
    if(score != 0):
        listScore.append([score, id])
        
    return score
    
def crossover(parent1Id, parent2Id):
    
    winner1 = tournament(populationScore[parent1Id])
    winner2 = tournament(populationScore[parent2Id])
    
    parent1 = population[winner1[1]].copy()
    parent2 = population[winner2[1]].copy()
    
    if(winner1[0]>winner2[1]):
        crossOverPoint=random.randint(1,cityCount-1)
    else:
        crossOverPoint=random.randint(1,cityCount-6)
    
    crossOverPartOne = parent1[1:crossOverPoint-1]

    for index, geneCapital in enumerate(crossOverPartOne):
        parent2.remove(geneCapital)
    
    enfant = parent2[0:len(parent2)-1] + crossOverPartOne + [firstCity] 
    return enfant

#This function takes into account a candidate and will make him face several fighters. 
#The outgoing winner is the one with the highest score
def tournament(candidate):
    parent = candidate
    for x in range(individualsTournamentCount):
        fighter = random.choice(populationScore)
        if(parent[0] > fighter[0]):
            parent = fighter
    return parent
        


#****************************************
#**********MATINF OF INDIVIDUALS*********
#****************************************



initial = listScore.copy()



for x in range(50):
    listScore.sort()
    populationScore = listScore.copy()
    populationScore.sort()

    listScore = []
    incrementPop = 0
    scoreCount = len(populationScore)

    for index, individu in enumerate(populationScore):
        pathParent1= []
        pathParent2= []
    
        if(index != scoreCount-1):
    
            enfant = crossover(index, index + 1)
            calculateScore(enfant, index)
    

print(initial)
print('******************************')
print('******************************')
print('******************************')

listScore.sort()

print(listScore)




        
    #print(min(((k, v[0]) for k, v in listScore), key=lambda key:min(individu[0])))
    

    
    