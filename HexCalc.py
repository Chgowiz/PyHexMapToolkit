import random

def buildSettlement():
    settlementTypes = {}
    with open("data/settlementtypes.csv", "r") as inFile:
        lines = inFile.readlines()
    for line in lines[1:]:
        values = line.strip().split(',')
        settlementTypes[values[0]] = (values[1], int(values[2]), int(values[3]))

    # SettlementTypes = d10 : Type,Population,PercentGoodsAvail
    settlement = settlementTypes[str(random.randint(1,10))]

    return settlement

#idea - make a isMinor optional parameter that defaults to false. If true, read in minor data file.

