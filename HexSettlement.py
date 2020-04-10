import random

def BuildSettlement(isMinor = False):
    settlementTypes = {}

    settlement = {}

    if isMinor:
        fileName = "data/minsettlementtypes.csv"
    else:
        fileName = "data/majsettlementtypes.csv"

    with open(fileName, "r") as inFile:
        lines = inFile.readlines()
    for line in lines[1:]:
        values = line.strip().split(',')
        settlementTypes[values[0]] = (values[1], values[2], values[3])

    # SettlementTypes = d10 : Type,Population,PercentGoodsAvail
    # settlementType is a tuple of the chosen type
    settlementType = settlementTypes[str(random.randint(1,10))]

    settlement['Type'] = settlementType[0]
    settlement['Population'] = int(settlementType[1])
    settlement['PercentGoodsAvail'] = float(settlementType[2])

    return settlement

