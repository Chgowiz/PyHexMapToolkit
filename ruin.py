import json
import dice
import jsonrollabletable

# https://welshpiper.com/ruinous-ruins/
# CDD #4 - http://kellri.blogspot.com/2008/07/cdd4-final-version-3.html
# https://www.enworld.org/threads/one-million-ancient-ruins.249553/

class Ruin(jsonrollabletable.JsonRollableTable):

    def __init__(self, json_file):

        jsonrollabletable.JsonRollableTable.__init__(self, json_file)
        
        self.type = ""
        self.condition = ""
        self.backstory = ""
        self.defenses = ""
        self.contents = ""
        self.primaryoccupants = ""
        self.majormonsters = ""
        self.minions = ""
        self.danger = ""
        self.wonder = ""

        self.build()

    def __str__(self):
        return """A {} in {} shape. 
        Backstory is {}. 
        Defended by {}. 
        Contains {} and may be occupied by {}. 
        May be lair for {} and {}.
        A danger could be {}. 
        A wonder could be {}.""".format(self.type, 
                                        self.condition, 
                                        self.backstory, 
                                        self.defenses, 
                                        self.contents, 
                                        self.primaryoccupants, 
                                        self.majormonsters, 
                                        self.minions,                                        
                                        self.danger,
                                        self.wonder )


    def build(self):
        self.type = self.roll_for_entry('Ruins Type')
        self.condition = self.roll_for_entry('Condition')
        self.backstory = self.roll_for_entry('Backstory')
        self.defenses = self.roll_for_entry('Defenses')
        #self.contents = self.roll_for_entry('Contents')  # TODO Contents is a d100 table with ranges. Need to code
        self.contents = "NOT YET IMPLEMENTED"
        self.primaryoccupants = self.roll_for_entry('Primary Occupants')
        self.majormonsters = self.roll_for_entry('Major Monster')
        self.minions = self.roll_for_entry('Minions')
        self.danger = self.roll_for_entry('Dangers')
        self.wonder = self.roll_for_entry('Wonders')



