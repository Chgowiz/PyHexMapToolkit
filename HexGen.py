# Generate Info for a Hex
# Use Welsh-Piper, plus additional OSR/web finds

import random 
import HexCalc as hexc

# Global/Argument set up - this will be changed later when I learn about arguments to a python script
argTerrainType = "Grassland"


# Table setup
primaryTerrainTypes = {}
# was - primaryTerrainTypes = {'Water':(.1,1),'Marsh':(.2,2),'Desert':(.2,2), 'Grassland': (.6,6), 'Forest':(.4,4), 'Hills/Rough':(.4,4), 'Mountains':(.2,2)}
with open("data/primaryterraintypes.csv", "r") as inFile:
    lines = inFile.readlines()
for line in lines[1:]:
    values = line.strip().split(',')
    primaryTerrainTypes[values[0]] = (float(values[1]), int(values[2]))

majorEncounterTypes = {}
# was - majorEncounterTypes = {'1':('Settlement'), '2':('Fortress'), '3':('Religious'), '4':('Ruin'), '5':('Monster'), '6':('Natural')}
with open("data/majencountertypes.csv", "r") as inFile:
    lines = inFile.readlines()
for line in lines[1:]:
    values = line.strip().split(',')
    majorEncounterTypes[values[0]] = (values[1])

minorEncounterTypes = {}
# was - minorEncounterTypes = {'1':('Settlement'),'2':('Fort'),'3':('Ruin'),'4':('Monster'),'5':('Wandering Monster'),'6':('Camp'),'7':('Way Station'),'8':('Beacon'),'9':('Construction Site'),'10':('Battlefield'),
#                       '11':('Isolated'),'12':('Sacred Ground'),'13':('Crossing'),'14':('Ancient Structure'),'15':('Hazard'),'16':('Treasure'),'17':('Contested'),'18':('Natural Resource'),'19':('Supernatural'),'20':('Gathering Place')}
with open("data/minencountertypes.csv", "r") as inFile:
    lines = inFile.readlines()
for line in lines[1:]:
    values = line.strip().split(',')
    minorEncounterTypes[values[0]] = (values[1])

# Build the hex and determine encounters
hex = {}

terrainType = primaryTerrainTypes[argTerrainType]

# Determine if we have a major encounter
rndMaj = random.randint(1,100)

if rndMaj <= int(terrainType[0] * 100):
    hex['Major Encounter'] = {}
    
    majEncDict = hex['Major Encounter']

    rndMajType = random.randint(1,6)

    #Determine Major Encounter Type
    majEncType = majorEncounterTypes[str(rndMajType)]
    majEncDict['Type'] = majEncType

    majEncDetails = ""
    if majEncType == 'Settlement':
        majEncDetails = hexc.buildSettlement()
    else:
        majEncDetails = "Not yet defined."

    majEncDict['Details'] = majEncDetails
        

# Determine how many (if any) minor encounters - for each possibility, roll a d6. On a 1, we have a minor encounter!
numMin = 0
for x in range(1,terrainType[1]):
    rndIsMin = random.randint(1,6)
    if rndIsMin == 1:
        numMin += 1

        #Create Minor Encounters dictionary if not yet created
        if 'Minor Encounters' not in hex:
            hex['Minor Encounters'] = {}
        minEncounters = hex['Minor Encounters']

        #Create the individual Minor Encounter Dictionary
        minEncDict = {}

        #Determine Minor Encounter Type
        rndMinType = random.randint(1,20)
        minEncDict['Type'] = minorEncounterTypes[str(rndMinType)]

        #Add the individual Minor Encounter to the hex's Minor Encounter Dictionary
        minEncounters[numMin] = minEncDict 



#Debug
#print (primaryTerrainTypes)
#print (majorEncounterTypes)
#print (minorEncounterTypes)
#for terrain in primaryTerrainTypes:
#    print('For {}, chance of major is {}%, variable number of minor is {}'.format(terrain[0], int(terrain[1]*100), terrain[2]))
#print(terrainType)
print("Generated hex\n----------")
print(hex)
