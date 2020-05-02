# Generate Info for a Hex
# Use Welsh-Piper approach, plus additional OSR/web finds

import random 
import hex
import HexPrint as hexp

# Global/Argument set up - this will be changed later when I learn about arguments to a python script
argTerrainType = "Grassland"

# Build the hex and determine encounters
newHex = hex.Hex(argTerrainType)

#hexp.printHex(hex)
        
#Debug
print("\nGenerated hex\n----------")
print(newHex)
