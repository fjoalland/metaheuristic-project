import parametre as parametre
import matplotlib.pyplot as plt
import numpy as np
def dessinerGraphiqueMeilleurScore():
	plt.figure("Best score")
	plt.plot(parametre.generationList, parametre.meilleurScoreList)
	plt.title('The best score through the evolution')
	plt.ylabel('Score (km)')
	plt.xlabel('Generation')

def dessinerGraphiqueRapportQPprice():
	plt.figure("Best price / time ratio")
	plt.plot(parametre.generationList, parametre.meilleurQPprixList,'C1', label='Price')
	plt.title('best price / time ratio. Price display')
	plt.ylabel('Price (€)')
	plt.xlabel('Generation')

def dessinerGraphiqueRapportQPtime():
	plt.figure("best price / time ratio")
	plt.plot(parametre.generationList, parametre.meilleurQPtempsList,'C1', label='Time')
	plt.title('best price / time ratio. Time display')
	plt.ylabel('Time (in hour)')
	plt.xlabel('Generation')

def dessinerGraphiqueMeilleurPrix():
	plt.figure("Least expensive")
	plt.plot(parametre.generationList, parametre.meilleurlowCostRoutePrixList)
	plt.title('The least expensive way')
	plt.ylabel('Price (€)')
	plt.xlabel('Generation')

def afficherLesGraphiques():
	plt.show()