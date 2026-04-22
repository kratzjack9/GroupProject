"""
biome.py
====================================
Game of life project with custom rules

| Author: Collin, Eein, Kade, Tobias
| Date: 2026 April 20
"""

from random import choices, random, randint


class Organism:
    """
    Creates Organism that has randomly created DNA

    Parameters
    -----------
    energy : int
        The amount of energy the organism starts with. Default is 100.

    Attributes
    ------------
    dna : str
        The organism's dna. 
        Is three characters long

    energy : int
        The amount of energy that organism has at that moment.

    isAlive : boolean
        Tells if the organism is alive
    """
    dnaOptions = ['🌱','💧','🌞','🎄','🍊']
    dnaCombust = ["🌱🌱🌱","💧💧💧","🌞🌞🌞","🎄🎄🎄","🍊🍊🍊"]

    def __init__(self, energy=100):
        """
        Initialize a new Organism instance.

        Parameters
        -----------
        energy : int
            The amount of energy the organism starts with. Default is 100.

        """
        # print("Organism initialized")
        self.dna = choices(Organism.dnaOptions, k=3)
        if self.dna in self.dnaCombust:
            self.isAlive = False
        else:
            self.isAlive = True
        self.energy = energy
    
    def mutate(self):
        """
        This allows the Organism to change its dna and kills it is DNA is all the same
        """
        changingDna = randint(0,len(self.dna)-1)
        newDna = ""
        for x in range(len(self.dna)):
            if x == changingDna:
                newDna = newDna + self.dnaOptions[randint(0,len(self.dnaOptions)-1)]
            else:
                newDna = newDna + self.dna[x]
        if newDna not in self.dnaCombust:
            self.dna = newDna
        else:
            self.isAlive = False


    def consume(self, other):
        """
        This allows an Organism to eat another Organism to gain energy
        """
        pass

    def __str__(self):
        """
        The string returned when the Organism is a method that requires a string
        """
        return ",".join(self.dna) + str(self.energy)

class Biome:
    """
    Creates a Biome that holds all of the organisms

    Parameters
    ------------
    nRows : int
        The amount of rows in the biome grid

    nCols : int
        The amount of columns in the biome grid

    startEnergy : int
        The amount of start energy that Organisms have

    Attributes
    ------------
    rows : int 
        The amount of rows in the grid

    cols : int
        The amount of cols in the grid

    grid : 2D list
        The grid which holds Organisms

    """
    def __init__(self, nRows=5, nCols=3, startEnergy=100):
        """
        Initialize a new Biome instance
        
        Parameters
        ------------
        nRows : int
            The amount of rows in the biome grid

        nCols : int
            The amount of columns in the biome grid

        startEnergy : int
            The amount of start energy that Organisms have

        """
        self.rows = nRows
        self.cols = nCols
        #List Comprehension Grid
        self.grid = [[ Organism(startEnergy) if random() > .5 else "" for _ in range(self.cols)] for _ in range(self.rows)]
        self.cycleCount = 0
        # print("Biome initialized")
    
    def hydration(self, row, column):
        """
        Implements the hydration rule at location row,column
        
        Parameters
        ------------
        row : int 
            The row in which the hydration rule is activated on

        column: int
            The column in which the hydration rule is activated on
        """
        directionList = []
        if '💧' in self.grid[row][column].dna:
            #print(f'[{row},{column}] has water')
            if row > 0:  # can check above
                if self.grid[row-1][column] == '':
                    # 30% Chance
                    if random() < .3 :
                        directionList.append("N")
            if row < (self.rows - 1):  # can check below
                if self.grid[row+1][column] == "":
                    # 30% Chance
                    if random() < .3 :
                        directionList.append("S")
            if column > 0:  # can check left
                if self.grid[row][column-1] == "":
                    # 30% Chance
                    if random() < .3 : 
                        directionList.append("W")
            if column < (self.cols - 1):  # can check right
                if self.grid[row][column+1] == "":
                    # 30% Chance
                    if random() < .3 :
                        directionList.append("E")
            if len(directionList) != 0:
                self.grid[row][column].energy = (self.grid[row][column].energy)/len(directionList)
            if "N" in directionList:
                self.grid[row-1][column] = Organism(energy=self.grid[row][column].energy)
            if "S" in directionList:
                self.grid[row+1][column] = Organism(energy=self.grid[row][column].energy)
            if "W" in directionList:
                self.grid[row][column-1] = Organism(energy=self.grid[row][column].energy)
            if "E" in directionList:
                self.grid[row][column+1] = Organism(energy=self.grid[row][column].energy)

    
    def step(self):
        """
        Implementation of all rules and reducing the energy of all Organisms
        """
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
                    if self.grid[ii][jj].energy < 5:
                        self.grid[ii][jj].mutate()
                    # Predator rule
                    if self.grid[ii][jj].energy <= 0:  # organism ceases
                        self.grid[ii][jj] = ''
                        print(f'Organism at [{ii},{jj}] ceased')
        self.display()
    
    def display(self):
        """
        Displays the grid with all of the Organisms in their respective spots
        """
        # print("Displaying the biome")
        for ii in range(len(self.grid)):
            for jj in range(len(self.grid[ii])):
                print(f'[{self.grid[ii][jj]}]\t', end='')
            print()


def main():
    """
    The primary running of the code
    """
    # o1 = Organism()
    # print(o1)
    myBiome = Biome(nRows=5, nCols=3, startEnergy=100)
    myBiome.display()
    for ii in range(5):
        myBiome.step()


if __name__ == '__main__':
    main()