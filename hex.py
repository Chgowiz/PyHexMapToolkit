import random

class Hex:
    """description of class"""

    def __init__(self, terraintype = 'None'):
        self.majorencounter = {}
        self.minorencounters = []
        self.majorEncounterTypes = {}
        self.minorEncounterTypes = {}
        self.terrainTable = []

        self.terraintype = terraintype
        self.loadEncounterTypeTables(terraintype)


    def __str__(self):
        return "Major Encounter\n{}\nMinor Encounters\n{}".format(str(self.majorencounter),str(self.minorencounters))


    def buildHex(self):
        self.majorencounter = self.buildMajorEncounter()
        self.minorencounters = self.buildMinorEncounters()


    def loadEncounterTypeTables(self, terraintype):
        # was - majorEncounterTypes = {'1':('Settlement'), '2':('Fortress'), '3':('Religious'), '4':('Ruin'), '5':('Monster'), '6':('Natural')}
        with open("data/majencountertypes.csv", "r") as inFile:
            lines = inFile.readlines()
        for line in lines[1:]:
            values = line.strip().split(',')
            self.majorEncounterTypes[values[0]] = (values[1])

        # was - minorEncounterTypes = {'1':('Settlement'),'2':('Fort'),'3':('Ruin'),'4':('Monster'),'5':('Wandering Monster'),'6':('Camp'),'7':('Way Station'),'8':('Beacon'),'9':('Construction Site'),'10':('Battlefield'),
        #                       '11':('Isolated'),'12':('Sacred Ground'),'13':('Crossing'),'14':('Ancient Structure'),'15':('Hazard'),'16':('Treasure'),'17':('Contested'),'18':('Natural Resource'),'19':('Supernatural'),'20':('Gathering Place')}
        with open("data/minencountertypes.csv", "r") as inFile:
            lines = inFile.readlines()
        for line in lines[1:]:
            values = line.strip().split(',')
            self.minorEncounterTypes[values[0]] = (values[1])

        primaryTerrainTypes = {}
        # was - primaryTerrainTypes = {'Water':(.1,1),'Marsh':(.2,2),'Desert':(.2,2), 'Grassland': (.6,6), 'Forest':(.4,4), 'Hills/Rough':(.4,4), 'Mountains':(.2,2)}
        with open("data/primaryterraintypes.csv", "r") as inFile:
            lines = inFile.readlines()
        for line in lines[1:]:
            values = line.strip().split(',')
            primaryTerrainTypes[values[0]] = float(values[1]), int(values[2])
        
        self.terrainTable = primaryTerrainTypes[terraintype]


    def buildMajorEncounter(self):
        # Determine if we have a major encounter
        rndMaj = random.randint(1,100)

        majEncDict = {}

        if rndMaj <= int(self.terrainTable[0] * 100):
        
            rndMajType = random.randint(1,2)

            #Determine Major Encounter Type
            majEncType = self.majorEncounterTypes[str(rndMajType)]
            majEncDict['Type'] = majEncType

            # Generate details about encounter
            majEncDetails = ""
            #if majEncType == 'Settlement':
            #    majEncDetails = hexSettle.BuildSettlement()
            #elif majEncType == 'Fortress':
            #    majEncDetails = hexFort.BuildFortress()
            #else:
            #    majEncDetails = "Not yet defined."

            majEncDict['Details'] = majEncDetails
        else:
            majEncDict['Type'] = "None"
            majEncDict['Details'] = "No Major Encounter"
    
        return majEncDict 
    

    def buildMinorEncounters(self):
        # Determine how many (if any) minor encounters - for each possibility, roll a d6. On a 1, we have a minor encounter!
        numMin = 0
        minEncountersDict = {}

        for x in range(1,self.terrainTable[1]):
            rndIsMin = random.randint(1,6)
            if rndIsMin == 1:
                numMin += 1

                #Create the individual Minor Encounter Dictionary
                minEncDict = {}

                #Determine Minor Encounter Type
                minEncType = self.minorEncounterTypes[str(random.randint(1,20))]
                minEncDict['Type'] = minEncType

                # Generate details about encounter
                minEncDetails = ""
                #if minEncType == 'Settlement':
                #    minEncDetails = hexSettle.BuildSettlement(isMinor = True)
                #elif minEncType == 'Fort':
                #    minEncDetails = hexFort.BuildMinorFort()
                #else:
                #    minEncDetails = "Not yet defined."
            
                #minEncDict['Details'] = minEncDetails

                #Add the individual Minor Encounter to the hex's Minor Encounter Dictionary
                minEncountersDict[str(numMin)] = minEncDict 

        if not minEncountersDict:
            minEncountersDict['0'] = {'Type':"None", 'Details': "No minor encounters."}
                
        return minEncountersDict
    
