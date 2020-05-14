import json
import dice
import jsonrollabletable
import settlement
import charactergenerator as chargen

class Fortress(jsonrollabletable.JsonRollableTable):
    def __init__(self, json_file, is_minor=False):

        jsonrollabletable.JsonRollableTable.__init__(self, json_file)
        
        self.fortress_type = ""
        self.fortress_ruler = ""
        self.fortress_protects = ""
        self.fortress_guards = ""
        self.fortress_majordomo = ""
        self.fortress_num_floors = 0
        self.fortress_num_guards = 0
        self.build(is_minor)


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

        ## If fortress protects settlement - what are details of settlement (a village)
        #if self.fortress_protects == 'Village':
        #    fortress_str += "\n\t" + str(settlement.Settlement(is_village = True))

        return fortress_str


    def build(self, is_minor):
        # Type of fortress
        if is_minor:
            desired_type = 'Minor Fortress Type'
        else:
            desired_type = 'Major Fortress Type'

        self.fortress_type = self.roll_for_entry(desired_type)
        self.fortress_ruler = self.roll_for_entry('Fortress Ruler')
        self.fortress_protects = self.roll_for_entry('Protecting')
        self.fortress_guards = self.roll_for_entry('Guards')
        self.fortress_majordomo = self.roll_for_entry('Majordomo')

        # How many floors/guards for fortress - refer to base class data_tables to get entries
        if is_minor:
            table = [tbl for tbl in self.data_tables if tbl['name'] == 'Minor Type Details'][0]

            n, s, mod = tuple(table['floors'].split(','))
            self.fortress_num_floors = sum(dice.roll(str(n) + 'd' + str(s))) + int(mod)

            n, s, mod = tuple(table['guards'].split(','))
            self.fortress_num_guards = sum(dice.roll(str(n) + 'd' + str(s))) + int(mod)
        else:
            table = [tbl for tbl in self.data_tables if tbl['name'] == 'Major Type Details'][0]

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
