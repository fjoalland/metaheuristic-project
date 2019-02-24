# Travelling Salesman Problem (TSP) solver
In pure Python.
This project aims to use the genetic algorithm to find a good local minimum for traveling salesman problem.

## The demo script require
- Pandas
- Matplotlib

## Usage
If you want to run the comparisons yourself, just go

    python .\main.py

## Files descriptions
main.py: This is the python script to execute
parametre.py: Contains all project parameters (number of individuals, generations, etc.)
README.md: file for github


Directory donnees:
- data_complete.csv: Customized inter-capital datasets
- data_contexte: datasets of the project context


Directory fonctions:
- calcul_score.py: Contains all the functions of calculations of the scores of individual.
- data_provider.py: CSV file reader.
- graph.py: Contains functions for drawing graphics
- population.py: Contains the functions specific to individuals (mutation, crossover, etc.).

## Dependencies
- Python3

## RUN
Launch of the genetic algorithm
![](https://image.noelshack.com/fichiers/2019/08/7/1551023182-screengif.gif)

Display of results at the end of the genetic algorithm
![](https://image.noelshack.com/fichiers/2019/08/7/1551023456-capture.png)

We can notice that over the generations, the curve stagnates.
![](https://image.noelshack.com/fichiers/2019/08/7/1551023571-capture.png)

We display the curve of the best time / quality price. We notice that the price does not follow the same curve as the others. Indeed, knowing that we are looking for quality here, we do not always look for the best score.
![](https://image.noelshack.com/fichiers/2019/08/7/1551023710-capture.png)

In the graph below, we display the evolution of the lowest price according to generations.
![](https://image.noelshack.com/fichiers/2019/08/7/1551023840-capture.png)

