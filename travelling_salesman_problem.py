import csv
import pandas as pd
import random
#Contains distances between capitals
Distances=[]
firstCity="Paris"
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
                
    if(len(path)==18):
        #print("--------")
        print(path)
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
#print(listScore)




#****************************************
#**********MATINF OF INDIVIDUALS*********
#****************************************
for index, individu in enumerate(listScore):
    charismaticRay=len(population)//random.randint(7,12)
    #print(min(((k, v[0]) for k, v in listScore), key=lambda key:min(individu[0])))