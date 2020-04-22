import random
import HexNameGenerator as namegen

def BuildSettlement(isMinor = False):
    settlementTypes = []
    #Commerce,Government,Resources,AvailModifier
    commerceTypes = []
    govtTypes = []
    rulerAlignment = []
    resourceTypes = []
    featureTypes = []

    settlement = {}

    if isMinor:
        fileName = "data/minsettlementtypes.csv"
    else:
        fileName = "data/majsettlementtypes.csv"

    with open(fileName, "r") as inFile:
        lines = inFile.readlines()
    for line in lines[1:]:
        values = line.strip().split(',')
        settlementTypes.append((values[1], values[2], values[3]))
        commerceTypes.append(values[4])
        govtTypes.append((values[5],values[6]))
        rulerAlignment.append(values[7])
        resourceTypes.append((values[8], values[9]))
        featureTypes.append(values[10])

    settlement['Type'],settlement['Population'],strPctGoodsAvail = settlementTypes[random.randint(0,9)]
    settlement['Commerce'] = commerceTypes[random.randrange(0,9)]
    settlement['Government'], settlement['Ruler'] = govtTypes[random.randrange(0,9)]
    settlement['RulerAlignment'] = rulerAlignment[random.randrange(0,9)]
    
    settlement['Resources'], strAvailModifier = resourceTypes[random.randint(0,9)]
    settlement['PercentGoodsAvail'] = int((float(strAvailModifier) + float(strPctGoodsAvail)) * 100)
    settlement['VillageFeature'] = featureTypes[random.randint(0,9)]

    # Generate Merchants and Services
    with open('data/merchantsservices.csv', "r") as inFile:
        lines = inFile.readlines()

    merchants = []
    for line in lines[1:]:
        values = line.strip().split(',')
        merchantType = values[0]
        merchantSV = int(values[1])
        population = int(settlement['Population'])
        merchantNum = population / merchantSV
        # if num < 1, then that's a percentage of the likelihood that this merchant exists
        # calculate if it is so
        if merchantNum < 1:
            if random.randint(1,100) <= int(merchantNum * 100):
                merchantNum = 1
            else:
                merchantNum = 0
        # add merchant to the list
        if merchantNum > 0:
            merchants.append((merchantType, int(merchantNum)))

    settlement['Merchants'] = merchants

    # If ruler is NPC, determine type/level
    if settlement['Ruler'] == 'NPC':
        npcClasses = []
        npcAlignments = []
        npcLevels = []
        with open('data/NPCRuler.csv', "r") as inFile:
            lines = inFile.readlines()
        for line in lines[1:]:
            values = line.strip().split(',')
            npcClasses.append(values[1])
            npcLevels.append(values[2])
            npcAlignments.append(values[3])

        cls = npcClasses[random.randint(0,9)]
        alignment = npcAlignments[random.randint(0,9)]
        if cls == 'Thief' and alignment == 'Lawful':
            alignment = 'Neutral'
        level = npcLevels[random.randint(0,9)]

        settlement['Ruler'] = "NPC({}, {} level, {})".format(cls,level,alignment)

    # Get a random name from the Internet
    settlement['Name'] = namegen.GenerateSettlementName()

    settlementStr = ""
    settlementStr = """{} is a {}.
    \t{} inhabitants. Commerce: {}. 
    \tResources are {}, {}% chance of specific good being available.
    \tGoverning body is {}, ruled by {}. Alignment: {}.
    \tThis {} is known for its {}
    \tMerchants/Services available: \n""".format(settlement['Name'], settlement['Type'], settlement['Population'],settlement['Commerce'],
                                                      settlement['Resources'],settlement['PercentGoodsAvail'],
                                                      settlement['Government'],settlement['Ruler'],settlement['RulerAlignment'],
                                                      str(settlement['Type']).lower(), settlement['VillageFeature'])

    x = 1
    for merchant,merchantNum in merchants:
        merchantStr = "\t{} ({})".format(merchant, merchantNum)
        if x % 2 == 0:
            merchantStr = merchantStr + "\n"
        x += 1
        settlementStr = settlementStr + merchantStr

    return settlementStr


