import csv
import pandas as pd
import random
#Contains distances between capitals
Distances=[]

#loading the CSV file containing the distances between capitals
with open('base2.csv', newline='') as csvfile:
	allDistances = csv.reader(csvfile, delimiter=';')
	for index, row in enumerate(allDistances):
        
        #Recover the first line containing all capitals
		if(index == 0):
		    Capitals = row
            #Deleting the first element that contains no city
		    del Capitals[0]
		else:
		    del row[0]
		    Distances.append(row)
Data1 = pd.DataFrame(Distances, columns=Capitals, index=Capitals) # Dataframe for the capitals

print('---Create Population--')
#We start from Paris, so we already have this capital in our Path

for x in range(5000):
    random.shuffle(Capitals)
    path = ['Paris']
    #We are looking for a path through all the cities (so the size of our table of capitals)
    for x in range(len(Capitals)):
        #Loop on the list of capitals randomly ranked
        for index, cap in enumerate(Capitals):
            if(len(path) == len(Capitals) - 1):
                #print("Size of the current path {}, size of capitals {}".format(len(path), len(Capitals)))
                if(Data1.loc[path[len(path)-1], cap]!= "" and Data1.loc[path[0], cap]!= "" and cap not in path):
                    path.append(cap)
                    path.append("Paris")
            #If the proposed capital is a destination of the current capital, we add it to our solution
            elif (Data1.loc[path[len(path)-1],cap] != "" and cap not in path):
                path.append(cap)
                
    if(len(path)==18):
        print("--------")
        print(path)
        
        for index, geneCapital in enumerate(path):
            if(index == len(Capitals)):  
                print(geneCapital)
                print('********')
            else:
                print(geneCapital + "-" + path[index+1])
                print(Data1.loc[geneCapital,path[index+1]])
           
