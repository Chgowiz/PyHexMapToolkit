import random
import jsonrollabletable
import namegenerator as namegen
import charactergenerator as npcgen

class Settlement(jsonrollabletable.JsonRollableTable):
    def __init__(self, json_file, is_minor=False, is_village=False):

        jsonrollabletable.JsonRollableTable.__init__(self, json_file)
        
        self.name = ""
        self.settlement_type = ""
        self.population = ""
        self.commerce = ""
        self.resources = ""
        self.percent_goods_avail = ""
        self.government = ""
        self.ruler = ""
        self.ruleralign = ""
        self.feature = ""
        self.merchants = []

        self.is_minor = is_minor
        self.is_village = is_village

        self.build()
    
    
    def __str__(self):
        settlementStr = ""
        settlementStr = """{} is a {}.
        \t{} inhabitants. Commerce: {}. 
        \tResources are {}, {}% chance of specific good being available.
        \tGoverning body is {} ({}), ruled by {}.
        \tThis {} is known for its {}
        \tMerchants/Services available: \n""".format(self.name, self.settlement_type, self.population,
                                                        self.commerce, self.resources,self.percent_goods_avail,
                                                        self.government, self.ruleralign, self.ruler, 
                                                        self.settlement_type.lower(), self.feature)

        x = 1
        for merchant,merchantNum in self.merchants:
            merchantStr = "\t{} ({})".format(merchant, merchantNum)
            if x % 2 == 0:
                merchantStr = merchantStr + "\n"
            x += 1
            settlementStr = settlementStr + merchantStr

        return settlementStr


    def build(self):
        if not self.is_minor:
            type_table = 'Major Settlement Types'
        else:
            type_table = 'Minor Settlement Types'

        if not self.is_village:
            self.settlement_type, self.population, str_percent_goods_avail = tuple(self.roll_for_entry(type_table).split(','))
        else:
            ## This param forces us to do a village, so I get all the village items and take the first one. 
            # entry will be a list of values, which comes from getting the dictionary of 'entries' from the table named 'Minor Settlement Types' from
            # the list of data_tables (which is a list of dictionaries). 
            entries = list([tbl['entries'] for tbl in self.data_tables if tbl['name'] == 'Minor Settlement Types'][0].values())
            #Get the first entry's tuple that starts with 'Village'
            self.settlement_type, self.population, self.percent_goods_avail = [tuple(entry.split(',')) for entry in entries if str(entry).startswith('Village')][0]

        self.commerce = self.roll_for_entry('Commerce')
        self.government = self.roll_for_entry('Government')
        self.ruler = self.roll_for_entry('Ruler')
        self.ruleralign = self.roll_for_entry('Alignment')
        self.resources, str_avail_modifier = tuple(self.roll_for_entry('Resources').split(','))
        self.percent_goods_avail = int( (float(str_avail_modifier) + float(str_percent_goods_avail)) * 100 )
        self.feature = self.roll_for_entry('Feature')

        # This looks confusing! data_tables is a list of dictionaries, which has keys of name/entries. 
        # I use list comprehension to go through the list of dicts to get one named Merchants. Then I pull out 
        # out the nested dictionary named entries. Now since list comprehension returns a list of 1 dictionary, 
        # I just refer to the [0] (first) index of the list to get the dict item itself. THEN, using the items function,
        # and the list function, I create a list of tuples from that dict. *WHEW* Blame json... ;)
        merchant_table = list( [tbl['entries'] for tbl in self.data_tables if tbl['name'] == 'Merchants'][0].items() )

        for merchant_type, merchant_sv in merchant_table:
            merchantNum = int(self.population) / merchant_sv
            # if num < 1, then that's a percentage of the likelihood that this merchant exists
            # calculate if it is so
            if merchantNum < 1:
                if random.randint(1,100) <= int(merchantNum * 100):
                    merchantNum = 1
                else:
                    merchantNum = 0
            # add merchant and number (as tuple) to the list if there's 1 or more
            if merchantNum > 0:
                self.merchants.append((merchant_type, int(merchantNum)))


        # If ruler is NPC, determine type/level
        if self.ruler == 'NPC':
            name,cls,level,alignment = npcgen.create_npc()
            self.ruler = "{}, {} level {} ({})".format(name,level,cls,alignment)

        # Get a random settlement name from the Internet
        self.name = namegen.get_settlement_name()

