import csv
import pandas as pd
import random
#Contains distances between capitals
Distances=[]

#loading the CSV file containing the distances between capitals
with open('base.csv', newline='') as csvfile:
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

print(Capitals)
print(Distances)
print(len(Capitals))
print(len(Distances))
Data1 = pd.DataFrame(Distances, columns=Capitals, index=Capitals) # Dataframe for the capitals

print(Data1.loc["Paris", "Bruxelles"])
print(len(Data1.get("Paris")))

print('-----')
#We start from Paris, so we already have this capital in our Path
path = ['Paris']
random.shuffle(Capitals)
for index, capi in enumerate(Capitals):
    for index, cap in enumerate(Capitals):
        if(Data1.loc[path[len(path)-1],cap] != "-" and cap not in path):
            print(Data1.loc[path[len(path)-1],cap])
            path.append(cap)
            break
    
print(path)
print(len(path))