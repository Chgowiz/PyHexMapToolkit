# Generate Info for a Hex
# Use Welsh-Piper, plus additional OSR/web finds

import random 
import HexCalc as hexc

# Global/Argument set up - this will be changed later when I learn about arguments to a python script
argTerrainType = "Grassland"

# Build the hex and determine encounters
hex = {}

hex['Major Encounter'] = hexc.GenerateMajorEncounter(argTerrainType)

hex['Minor Encounters'] = hexc.GenerateMinorEncounters(argTerrainType)
        
#Debug
#print (primaryTerrainTypes)
#print (majorEncounterTypes)
#print (minorEncounterTypes)
#for terrain in primaryTerrainTypes:
#    print('For {}, chance of major is {}%, variable number of minor is {}'.format(terrain[0], int(terrain[1]*100), terrain[2]))
#print(terrainType)
print("Generated hex\n----------")
print(hex)
