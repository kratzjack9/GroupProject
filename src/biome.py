"""
biome.py
=========
Implements a "game of life" simulated biome

| Seth McNeill
| 2026 March 19
"""

from random import choices, random


class Organism:
    dnaOptions = ['🌱','💧','🌞','🎄','🍊']

    def __init__(self, energy=100):
        # print("Organism initialized")
        self.dna = choices(Organism.dnaOptions, k=3)
        self.energy = energy
        self.isAlive = True
    
    def mutate(self):
        pass

    def consume(self, other):
        pass

    def __str__(self):
        return ",".join(self.dna) + str(self.energy)

class Biome:
    def __init__(self, nRows=5, nCols=3, startEnergy=100):
        self.grid = []
        self.rows = nRows
        self.cols = nCols
        for ii in range(self.rows):
            newRow = []
            for jj in range(self.cols):
                if random() < 0.5:  # fill half the spaces on average
                    newOrg = Organism(startEnergy)
                else:
                    newOrg = ''
                newRow.append(newOrg)
            self.grid.append(newRow)
        self.cycleCount = 0
        # print("Biome initialized")
    
    def hydration(self, row, column):
        """Implements the hydration rule at location row,column"""
        if '💧' in self.grid[row][column].dna:
            print(f'[{row},{column}] has water')
            if row > 0:  # can check above
                if self.grid[row-1][column] == '':
                    self.grid[row-1][column] = Organism()
                    self.grid[row][column].energy = self.grid[row][column].energy/2 
            if row < (self.rows - 1):  # can check below
                pass
            if column > 0:  # can check left
                pass
            if column < (self.cols - 1):  # can check right
                pass
    
    def step(self):
        self.cycleCount += 1  # increments count
        print('='*25)
        print(f"Currently day {self.cycleCount}")
        # go through all the organisms
        for ii in range(len(self.grid)):
            for jj in range(len(self.grid[ii])):
                if self.grid[ii][jj] != '':  # make sure something is there
                    self.grid[ii][jj].energy -=1
                    # Hydration rule
                    self.hydration(ii,jj)
                    # Solar flare rule
                    # Mutation rule
                    # Predator rule
                    if self.grid[ii][jj].energy <= 0:  # organism ceases
                        self.grid[ii][jj] = ''
                        print(f'Organism at [{ii},{jj}] ceased')
        self.display()
    
    def display(self):
        # print("Displaying the biome")
        for ii in range(len(self.grid)):
            for jj in range(len(self.grid[ii])):
                print(f'[{self.grid[ii][jj]}]\t', end='')
            print()


def main():
    # o1 = Organism()
    # print(o1)
    myBiome = Biome(nRows=5, nCols=3, startEnergy=100)
    myBiome.display()
    for ii in range(5):
        myBiome.step()


if __name__ == '__main__':
    main()