import random
import HexSettlement as hexSettle
import HexFortress as hexFort

def GenerateMajorEncounter(sTerrainType):
    terrainType = GetPrimaryTerrainData(sTerrainType)

    majorEncounterTypes = {}
    # was - majorEncounterTypes = {'1':('Settlement'), '2':('Fortress'), '3':('Religious'), '4':('Ruin'), '5':('Monster'), '6':('Natural')}
    with open("data/majencountertypes.csv", "r") as inFile:
        lines = inFile.readlines()
    for line in lines[1:]:
        values = line.strip().split(',')
        majorEncounterTypes[values[0]] = (values[1])

    # Determine if we have a major encounter
    rndMaj = random.randint(1,100)

    majEncDict = {}

    if rndMaj <= int(terrainType[0] * 100):
        
        rndMajType = random.randint(1,6)

        #Determine Major Encounter Type
        majEncType = majorEncounterTypes[str(rndMajType)]
        majEncDict['Type'] = majEncType

        # Generate details about encounter
        majEncDetails = ""
        if majEncType == 'Settlement':
            majEncDetails = hexSettle.BuildSettlement()
        elif majEncType == 'Fortress':
            majEncDetails = hexFort.BuildFortress()
        else:
            majEncDetails = "Not yet defined."

        majEncDict['Details'] = majEncDetails
    
    return majEncDict 

def GenerateMinorEncounters(sTerrainType):
    minorEncounterTypes = {}
    # was - minorEncounterTypes = {'1':('Settlement'),'2':('Fort'),'3':('Ruin'),'4':('Monster'),'5':('Wandering Monster'),'6':('Camp'),'7':('Way Station'),'8':('Beacon'),'9':('Construction Site'),'10':('Battlefield'),
    #                       '11':('Isolated'),'12':('Sacred Ground'),'13':('Crossing'),'14':('Ancient Structure'),'15':('Hazard'),'16':('Treasure'),'17':('Contested'),'18':('Natural Resource'),'19':('Supernatural'),'20':('Gathering Place')}
    with open("data/minencountertypes.csv", "r") as inFile:
        lines = inFile.readlines()
    for line in lines[1:]:
        values = line.strip().split(',')
        minorEncounterTypes[values[0]] = (values[1])

    terrainType = GetPrimaryTerrainData(sTerrainType)

    # Determine how many (if any) minor encounters - for each possibility, roll a d6. On a 1, we have a minor encounter!
    numMin = 0
    minEncountersDict = {}

    for x in range(1,terrainType[1]):
        rndIsMin = random.randint(1,6)
        if rndIsMin == 1:
            numMin += 1

            #Create the individual Minor Encounter Dictionary
            minEncDict = {}

            #Determine Minor Encounter Type
            minEncType = minorEncounterTypes[str(random.randint(1,20))]
            minEncDict['Type'] = minEncType

            # Generate details about encounter
            minEncDetails = ""
            if minEncType == 'Settlement':
                minEncDetails = hexSettle.BuildSettlement(True)
            else:
                minEncDetails = "Not yet defined."
            
            minEncDict['Details'] = minEncDetails

            #Add the individual Minor Encounter to the hex's Minor Encounter Dictionary
            minEncountersDict[str(numMin)] = minEncDict 

    return minEncountersDict

def GetPrimaryTerrainData(sTerrainType):
    primaryTerrainTypes = {}
    # was - primaryTerrainTypes = {'Water':(.1,1),'Marsh':(.2,2),'Desert':(.2,2), 'Grassland': (.6,6), 'Forest':(.4,4), 'Hills/Rough':(.4,4), 'Mountains':(.2,2)}
    with open("data/primaryterraintypes.csv", "r") as inFile:
        lines = inFile.readlines()
    for line in lines[1:]:
        values = line.strip().split(',')
        primaryTerrainTypes[values[0]] = float(values[1]), int(values[2])
    return primaryTerrainTypes[sTerrainType]
