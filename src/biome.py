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

    isNewOrganism : boolean
        Tells if the organism was just born to prevent rules applying immediately
    """
    dnaOptions = ['🌱','💧','🌞','🎄','🍊']
    dnaCombust = ["🌱🌱🌱","💧💧💧","🌞🌞🌞","🎄🎄🎄","🍊🍊🍊"]

    def __init__(self, energy=100,dna=""):
        """
        Initialize a new Organism instance.

        Parameters
        -----------
        energy : int
            The amount of energy the organism starts with. Default is 100.

        """

        try:
            if energy < 0:
                 raise ValueError("Energy cannot be negative")
            # print("Organism initialized")
            if dna == "":
                self.dna = choices(Organism.dnaOptions, k=3)
                if self.dna in self.dnaCombust:
                    self.isAlive = False
                else:
                    self.isAlive = True
            else:
                self.dna = dna
                self.isAlive = True
            self.energy = energy
            self.isNewOrganism = True

        except ValueError as e:
            print(f"Error creating organism: {e}")
            self.energy = 0
            self.isAlive = False

        
    
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


    def __str__(self):
        """
        The string returned when the Organism is a method that requires a string
        """
        return f"{",".join(self.dna)} {self.energy:.2f}"

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
    def __init__(self, nRows=5, nCols=3, startEnergy=100,organismDna=""):
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
        self.grid = [[ Organism(startEnergy,dna=organismDna) if random() > .5 else "" for _ in range(self.cols)] for _ in range(self.rows)]
        self.cycleCount = 0
        # print("Biome initialized")
    
    def hydration(self, row, column):
        """
        Implements the hydration rule at location row, column
        
        Parameters
        ------------
        row : int 
            The row in which the hydration rule is activated on

        column: int
            The column in which the hydration rule is activated on
        """

        try:
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
                    self.grid[row][column].energy = (self.grid[row][column].energy)/(len(directionList)+1)
                if "N" in directionList:
                    self.grid[row-1][column] = Organism(energy=self.grid[row][column].energy)
                    print(f"[{row},{column}] hydrated [{row-1},{column}]")
                if "S" in directionList:
                    self.grid[row+1][column] = Organism(energy=self.grid[row][column].energy)
                    print(f"[{row},{column}] hydrated [{row+1},{column}]")
                if "W" in directionList:
                    self.grid[row][column-1] = Organism(energy=self.grid[row][column].energy)
                    print(f"[{row},{column}] hydrated [{row},{column-1}]")
                if "E" in directionList:
                    self.grid[row][column+1] = Organism(energy=self.grid[row][column].energy)
                    print(f"[{row},{column}] hydrated [{row},{column+1}]")

        except AttributeError:
            print(f"Invalid organism at [{row},{column}]")

        except IndexError:
            print(f"Out of bounds access at [{row},{column}]") 

    def predator(self,row,column,killing=True):
        """
        Implements the predator rule at location row, column

        Parameters
        --------------
        row : int
            The row in which the predator rule is activated on

        column : int
            The row in which the predator rule is activated on
        """

        #DNA sequence understanding: 
        #Spot in grid:[row of spot,column of spot, {dictionary of dna}, isPredator, exist]
        dnaSequence = self.infoCollector(row,column)
        #Finds which are predators
        for key in dnaSequence:
            for key2 in dnaSequence[key][2]:
                if dnaSequence[key][2][key2] >= 2:
                    dnaSequence[key][3] = True
        #Finds which directions are not available due to being predators, that grid spot is not there, or isNewOrganism
        directionNoGo = {}
        if dnaSequence["center"][3]: # Checks if center is predator
            for key in dnaSequence:
                if key != "center": # Looks at surrounding spots
                    if dnaSequence[key][3]: # Sees if surrounding spot is predator
                        if directionNoGo.get(key) != None: #If true, doesn't attack
                            directionNoGo[key] =+ 1
                        else:
                            directionNoGo[key] = 1
                if not dnaSequence[key][4]: # Sees if spot has an organism
                    if directionNoGo.get(key) != None: # If not, doesn't attack
                        directionNoGo[key] =+ 1
                    else:
                        directionNoGo[key] = 1
                else:
                    if self.grid[dnaSequence[key][0]][dnaSequence[key][1]].isNewOrganism: # Sees if new organism
                        if directionNoGo.get(key) != None: # If so, doesn't attack
                            directionNoGo[key] =+ 1
                        else:
                            directionNoGo[key] = 1
            # Checks any of the edge cases            
            if row == 0:
                if directionNoGo.get("N") != None:
                    directionNoGo["N"] =+ 1
                else:
                    directionNoGo["N"] = 1
            if row == self.rows - 1:
                if directionNoGo.get("S") != None:
                    directionNoGo["S"] =+ 1
                else:
                    directionNoGo["S"] = 1
            if column == 0:
                if directionNoGo.get("W") != None:
                    directionNoGo["W"] =+ 1
                else:
                    directionNoGo["W"] = 1
            if column == self.cols - 1:
                if directionNoGo.get("E") != None:
                    directionNoGo["E"] =+ 1
                else:
                    directionNoGo["E"] = 1
            # Determines what directions can be attacked
            avaliableDirections = ["N","S","W","E"]
            for direction in directionNoGo:
                avaliableDirections.remove(direction)
            # From these direction, one will be attacked
            if len(avaliableDirections) != 0:
                killingDirection = avaliableDirections[randint(0,len(avaliableDirections)-1)]
            else:
                #If no avaliable direction is avaliable
                killingDirection = ""
            # Attacking/Killing
            if killingDirection == "N":
                if killing == True:
                    self.grid[row-1][column] = ""
                    print(f"[{row-1},{column}] died from predator [{row},{column}]")
                else:
                    self.grid[row-1][column].energy -= 5
                    print(f"[{row-1},{column}] was attacked from predator [{row},{column}]")
                self.grid[row][column].energy += 5
            if killingDirection == "S":
                if killing == True:
                    self.grid[row+1][column] = ""
                    print(f"[{row+1},{column}] died from predator [{row},{column}]")
                else:
                    self.grid[row+1][column].energy -= 5
                    print(f"[{row+1},{column}] was attacked from predator [{row},{column}]")
                self.grid[row][column].energy += 5
            if killingDirection == "W":
                if killing == True:
                    self.grid[row][column-1] = ""
                    print(f"[{row},{column-1}] died from predator [{row},{column}]")
                else:
                    self.grid[row][column-1].energy -= 5
                    print(f"[{row},{column-1}] was attacked from predator [{row},{column}]")
                self.grid[row][column].energy += 5
            if killingDirection == "E":
                if killing == True:
                    self.grid[row][column+1] = ""
                    print(f"[{row},{column+1}] died from predator [{row},{column}]")
                else:
                    self.grid[row][column+1].energy -= 5
                    print(f"[{row},{column+1}] was attacked from predator [{row},{column}]")
                self.grid[row][column].energy += 5

    def solarFlare(self,row,column):
        """
        Implements the Solar Flare rule at location row, column

        Parameters
        --------------
        row : int
            The row in which the Solar Flare rule is activated on

        column : int
            The row in which the Solar Flare rule is activated on
        """
        multiple5 = []
        for x in range(10):
            multiple5.append((x+1)*5)
        if self.cycleCount in multiple5:
            #Spot in grid:[row of spot,column of spot, {dictionary of dna}, hasPlant, exist]
            dnaSequence = self.infoCollector(row,column)
            if "🌞" in dnaSequence["center"][2]:
                # Checks if adjacent spots have a plant
                for key in dnaSequence:
                    if key != "center":
                        if "🌱" in dnaSequence[key][2]:
                            dnaSequence["center"][3] = True
                # Depending if adjacent spots have plants, gains or loses 10 energy
                if dnaSequence["center"][3]:
                    self.grid[dnaSequence["center"][0]][dnaSequence["center"][1]].energy += 10
                    print(f"[{row},{column}] has gained 10 energy")
                else:
                    self.grid[dnaSequence["center"][0]][dnaSequence["center"][1]].energy -= 10
                    print(f"[{row},{column}] has lost 10 energy")

    def growth(self,row,column):
        """
        Implements the growth rule at location row, column

        Parameters
        -------------
        row : int
            The row in which the growth rule is activated

        column : int
            The column in which the growth rule is activated
        """
        
        if '🌱' in self.grid[row][column].dna and '💧' in self.grid[row][column].dna and '🌞' in self.grid[row][column].dna:
            self.grid[row][column].dna[self.grid[row][column].dna.index('🌱')] = "🎄"
            print(f"[{row},{column}] has grown to a tree")
    
    def fruiting(self,row,column):
        """
        Implements the fruiting rule at location row, column

        Parameters
        -------------
        row : int
            The row in which the fruiting rule is activated

        column : int
            The column in which the fruiting rule is activated
        """
        
        if '🎄' in self.grid[row][column].dna and '💧' in self.grid[row][column].dna and '🌞' in self.grid[row][column].dna and self.grid[row][column].energy <= 70 :
            self.grid[row][column].dna[self.grid[row][column].dna.index('🎄')] = "🍊"
            print(f"[{row},{column}] has fruited")

    def reproduction(self, row, column):
        #Spot in grid:[row of spot,column of spot, {dictionary of dna}, boolean, exists]
        dnaSequence = self.infoCollector(row,column)
        #dnaComponent:[inNorth,inSouth,inWest,inEast]
        dnaSurrounding = {'💧':[False,False,False,False],'🌞':[False,False,False,False],'🌱':[False,False,False,False]}
        index = 0
        totalTrues = 0
        totalExists = 0
        # Filling out the dnaSurrounding and details about it
        for key in dnaSequence:
            if key != "center":
                for dnaComponent in dnaSurrounding:
                    if dnaSequence[key][4]:
                        if dnaComponent in dnaSequence[key][2]:
                            dnaSurrounding[dnaComponent][index] = True
                            totalTrues += 1
                index += 1
        for key in dnaSequence:
            if key != "center":
                if dnaSequence[key][4]:
                    totalExists += 1
                    
        #If a component isn't available, then it can't reproduce
        for dnaComponent in dnaSurrounding:
            if True in dnaSurrounding[dnaComponent]:
                pass
            else:
                return
        # Keeping track of truths within "columns" from dnaSurrounding
        columnTrues = [0,0,0,0]
        dictColumnTrues = {}
        #Using details about dnaSurrounding
        if totalTrues >= 3 and totalExists >= 3:
            for i in range(4):
                for dnaComponent in dnaSurrounding:
                    if dnaSurrounding[dnaComponent][i]:
                        columnTrues[i] += 1
            for i in range(4):
                if dictColumnTrues.get(f"{columnTrues[i]}") != None:
                    dictColumnTrues[f"{columnTrues[i]}"] += 1
                else:
                    dictColumnTrues[f"{columnTrues[i]}"] = 1

            #If there are two columns with no trues, then it can't reproduce
            if dictColumnTrues["0"] >=2:
                return
            # Avoiding [3,1,1,1]
            if dictColumnTrues["3"] == 1 and dictColumnTrues["1"] == 3:
                return
            #To my knowledge, this is a sufficient enough conditions for what we want
            newDna = []
            for key in dnaSequence:
                #Isn't the center and exists
                if key != "center" and dnaSequence[key][4] and len(newDna) <= 3:
                    #Adds a random piece of dna from neighbors
                    newDna.append(list(dnaSequence[key][2])[randint(0,len(dnaSequence[key][2])-1)])

            self.grid[row][column] = Organism(dna=newDna)
            print(f"[{row},{column}] has been born")
    
                
    def combust(self,row,column):
        """
        Determines is an organism needs to combust
        Happens when an organism has all the same components in DNA

        Parameters
        --------------
        row : int
            The row in which the combustion may take place

        column : int
            The column in which the combustion may take place

        Returns
        -----------
        bool
            Tells if the Organism has combusted
        """
        dnaString = ""
        for component in self.grid[row][column].dna:
            dnaString = dnaString + component
        if dnaString in self.grid[row][column].dnaCombust:
            self.grid[row][column] = ""
            print(f"[{row},{column}] has combust")
            return True
        else:
            return False
            
    def infoCollector(self,row,column):
        """
        Looks at the center and the surrounding spots and collects information about

        Parameters
        --------------
        row : int
            The row of the center

        column : int
            The column of the center

        Return
        -----------
        dict
            Holds row, column, information of DNA make up, room for rule specific use, and existing
        """
        #Spot in grid:[row of spot,column of spot, {dictionary of dna}, ruleSpecific, exist]
        dnaSequence = {"center":[row,column,{},False,True],"N":[row-1,column,{},False,False],"S":[row+1,column,{},False,False],"W":[row,column-1,{},False,False],"E":[row,column+1,{},False,False]}
        for key in dnaSequence:
            if dnaSequence[key][0] >= 0 and dnaSequence[key][0] <= self.rows-1 and dnaSequence[key][1] >= 0 and dnaSequence[key][1] <= self.cols-1: #Make sure spot is in grid
                if self.grid[dnaSequence[key][0]][dnaSequence[key][1]] != "": #Makes sure spot is nonempty
                    dnaSequence[key][4] = True
                    for dnaComponent in self.grid[dnaSequence[key][0]][dnaSequence[key][1]].dna:
                        if dnaComponent not in dnaSequence[key][2]:
                            dnaSequence[key][2][dnaComponent] = 1
                        else:
                            dnaSequence[key][2][dnaComponent] = dnaSequence[key][2][dnaComponent] + 1
        return dnaSequence

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

                # Makes sure something is there, new organism don't immediately get rules applied, and not all same DNA

                try:
                    if self.grid[ii][jj] != '' and not self.grid[ii][jj].isNewOrganism and not self.combust(ii,jj): 
                        self.grid[ii][jj].energy -=1
                        # Hydration rule
                        if self.grid[ii][jj].energy > 0:
                            self.hydration(ii,jj)
                        # Solar flare rule
                        self.solarFlare(ii,jj)
                        # Mutation rule
                        if self.grid[ii][jj].energy < 5:
                            self.grid[ii][jj].mutate()
                        # Predator rule
                        self.predator(ii,jj,killing=False)
                        #Fruiting Rule
                        self.fruiting(ii,jj)
                        #Growth Rule
                        self.growth(ii,jj)
                        #Energy Death
                        if self.grid[ii][jj].energy <= 0 or not self.grid[ii][jj].isAlive:  # organism ceases
                            self.grid[ii][jj] = ''
                            print(f'Organism at [{ii},{jj}] ceased')
                    elif self.grid[ii][jj] == "":
                        #Reproduction Rule
                        self.reproduction(ii,jj)

                except Exception as e:
                    print(f"Error at [{ii},{jj}]: {e}")

        for ii in range(self.rows):
            for jj in range(self.cols):
                if self.grid[ii][jj] != "" and self.grid[ii][jj].isNewOrganism:
                    self.grid[ii][jj].isNewOrganism = False

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
    #myBiome.grid[0][0] = "not an organism"
    
    #myBiome.hydration(100, 100)

    #myBiome.display()
    for ii in range(10):

        myBiome.step()
        input("Press Enter for next cycle...")

if __name__ == '__main__':
    main()