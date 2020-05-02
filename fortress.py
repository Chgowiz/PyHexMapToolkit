import json
import dice
import settlement
import charactergenerator as chargen

class Fortress:
    def __init__(self, is_minor=False):
        self.fortress_type = ""
        self.fortress_ruler = ""
        self.fortress_protects = ""
        self.fortress_guards = ""
        self.fortress_majordomo = ""
        self.fortress_num_floors = 0
        self.fortress_num_guards = 0
        if not is_minor:
            self.build()
        else:
            self.build_minor()


    def __str__(self):
        fortress_str = ""
        # Create the description string
        fortress_str = "{} (floors: {}, guards: {} {}/floor)\n\tprotecting {}, ruler: {}, majordomo: {})".format(self.fortress_type, 
                                                                                                            self.fortress_num_floors, 
                                                                                                            self.fortress_num_guards, 
                                                                                                            self.fortress_guards, 
                                                                                                            self.fortress_protects , 
                                                                                                            self.fortress_ruler, 
                                                                                                            self.fortress_majordomo)

        # If fortress protects settlement - what are details of settlement (a village)
        if self.fortress_protects == 'Village':
            fortress_str += "\n\t" + str(settlement.Settlement(isVillage = True))

        return fortress_str


    def build(self):
        json_str = ""

        with open("data/fortresstables.json", "r") as inFile:
            json_str = inFile.read()

        # The way the JSON is formatted, it creates a dictionary w/key of 'fortresstables'
        # which will have a list of the tables (which are dictionaries themselves). I just want that list.
        tables = json.loads(json_str)['fortresstables']

        # Type of fortress
        table = [tbl for tbl in tables if tbl['name'] == 'Fortress Type'][0]
        d = table['dtype']
        self.fortress_type = table['entries'][str(sum(dice.roll('1d' + str(d))))]

        # Ruler of fortress
        table = [tbl for tbl in tables if tbl['name'] == 'Fortress Ruler'][0]
        d = table['dtype']
        self.fortress_ruler = table['entries'][str(sum(dice.roll('1d' + str(d))))]

        # What does fortress protect 
        table = [tbl for tbl in tables if tbl['name'] == 'Protecting'][0]
        d = table['dtype']
        self.fortress_protects = table['entries'][str(sum(dice.roll('1d' + str(d))))]

        # Who are guards of the fortress
        table = [tbl for tbl in tables if tbl['name'] == 'Guards'][0]
        d = table['dtype']
        self.fortress_guards = table['entries'][str(sum(dice.roll('1d' + str(d))))]

        # Who is majordomo of fortress
        table = [tbl for tbl in tables if tbl['name'] == 'Majordomo'][0]
        d = table['dtype']
        self.fortress_majordomo = table['entries'][str(sum(dice.roll('1d' + str(d))))]

        # How many floors/guards for fortress
        table = [tbl for tbl in tables if tbl['name'] == 'Type Details'][0]

        n, s, mod = tuple(table['entries'][self.fortress_type]['floors'].split(','))
        self.fortress_num_floors = sum(dice.roll(str(n) + 'd' + str(s))) + int(mod)

        n, s, mod = tuple(table['entries'][self.fortress_type]['guards'].split(','))
        self.fortress_num_guards = sum(dice.roll(str(n) + 'd' + str(s))) + int(mod)

        # If ruler or majordomo is NPC - what are details of NPC
        if self.fortress_ruler == 'NPC':
            name, cls, level, align = chargen.create_npc()
            self.fortress_ruler = "{}, {} level {} ({})".format(name, cls, level, align)
        # If ruler is Noble - what are the details of the noble
        elif self.fortress_ruler == 'Noble':
            self.fortress_ruler += ' (NEED DETAILS)'

        if self.fortress_majordomo == 'NPC':
            name, cls, level, align = chargen.create_npc()
            self.fortress_majordomo = "{}, {} level {} ({})".format(name, cls, level, align)


    def build_minor(self):
        # a small fortified holding 
        # noble, military leader, fighting order, or adventurer

        self.fortress_type = "Minor Fort - DETAILS NEEDED"