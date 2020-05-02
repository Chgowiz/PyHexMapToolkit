import random
import namegenerator as namegen
import charactergenerator as npcgen

class Settlement:
    def __init__(self, is_minor=False, is_village=False):
        self.settlementTypes = []
        #Commerce,Government,Resources,AvailModifier
        self.commerceTypes = []
        self.govtTypes = []
        self.rulerAlignment = []
        self.resourceTypes = []
        self.featureTypes = []

        self.settlement = {}

        self.is_minor = is_minor
        self.is_village = is_village

        self.load_tables()
        self.build()
    
    
    def __str__(self):
        settlementStr = ""
        settlementStr = """{} is a {}.
        \t{} inhabitants. Commerce: {}. 
        \tResources are {}, {}% chance of specific good being available.
        \tGoverning body is {} ({}), ruled by {}.
        \tThis {} is known for its {}
        \tMerchants/Services available: \n""".format(self.settlement['Name'], self.settlement['Type'], self.settlement['Population'],
                                                        self.settlement['Commerce'], self.settlement['Resources'],self.settlement['PercentGoodsAvail'],
                                                        self.settlement['Government'], self.settlement['RulerAlignment'], self.settlement['Ruler'], 
                                                        str(self.settlement['Type']).lower(), self.settlement['VillageFeature'])

        x = 1
        for merchant,merchantNum in self.settlement['Merchants']:
            merchantStr = "\t{} ({})".format(merchant, merchantNum)
            if x % 2 == 0:
                merchantStr = merchantStr + "\n"
            x += 1
            settlementStr = settlementStr + merchantStr

        return settlementStr

    
    def load_tables(self):
        if self.is_minor:
            fileName = "data/minsettlementtypes.csv"
        else:
            fileName = "data/majsettlementtypes.csv"

        with open(fileName, "r") as inFile:
            lines = inFile.readlines()
        for line in lines[1:]:
            values = line.strip().split(',')
            self.settlementTypes.append((values[1], values[2], values[3]))
            self.commerceTypes.append(values[4])
            self.govtTypes.append((values[5],values[6]))
            self.rulerAlignment.append(values[7])
            self.resourceTypes.append((values[8], values[9]))
            self.featureTypes.append(values[10])

        # Generate Merchants and Services
        with open('data/merchantsservices.csv', "r") as inFile:
            lines = inFile.readlines()

        self.merchant_table = []
        for line in lines[1:]:
            values = line.strip().split(',')
            self.merchant_table.append((values[0],int(values[1])))


    def build(self):
        # This param forces us to do a village, so I get all the village items and take the first one. 
        if not self.is_village:
            self.settlement['Type'],self.settlement['Population'],strPctGoodsAvail = self.settlementTypes[random.randint(0,9)]
        else:
            self.settlement['Type'],self.settlement['Population'],strPctGoodsAvail = [item for item in self.settlementTypes if item[0] == 'Village'][0]

        self.settlement['Commerce'] = self.commerceTypes[random.randrange(0,9)]
        self.settlement['Government'], self.settlement['Ruler'] = self.govtTypes[random.randrange(0,9)]
        self.settlement['RulerAlignment'] = self.rulerAlignment[random.randrange(0,9)]
    
        self.settlement['Resources'], strAvailModifier = self.resourceTypes[random.randint(0,9)]
        self.settlement['PercentGoodsAvail'] = int((float(strAvailModifier) + float(strPctGoodsAvail)) * 100)
        self.settlement['VillageFeature'] = self.featureTypes[random.randint(0,9)]

        merchants = []

        for merchant_type, merchant_sv in self.merchant_table:
            merchantNum = int(self.settlement['Population']) / merchant_sv
            # if num < 1, then that's a percentage of the likelihood that this merchant exists
            # calculate if it is so
            if merchantNum < 1:
                if random.randint(1,100) <= int(merchantNum * 100):
                    merchantNum = 1
                else:
                    merchantNum = 0
            # add merchant to the list
            if merchantNum > 0:
                merchants.append((merchant_type, int(merchantNum)))

        self.settlement['Merchants'] = merchants

        # If ruler is NPC, determine type/level
        if self.settlement['Ruler'] == 'NPC':
            name,cls,level,alignment = npcgen.create_npc()
            self.settlement['Ruler'] = "{}, {} level {} ({})".format(name,level,cls,alignment)

        # Get a random settlement name from the Internet
        self.settlement['Name'] = namegen.get_settlement_name()

