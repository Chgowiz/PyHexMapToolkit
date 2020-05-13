import random
import settlement
import fortress
import ruin

class Hex:
    """description of class"""

    def __init__(self, terrain_type = 'None'):
        self.major_encounter_dict = {}
        self.minor_encounter_dict = []
        self.major_encounter_types = {}
        self.minor_encounter_types = {}
        self.terrain_table = []

        self.terrain_type = terrain_type
        self.load_tables(terrain_type)

        self.build()


    def __str__(self):
        return "Major Encounter\n{}\nMinor Encounters\n{}".format(str(self.major_encounter_dict),str(self.minor_encounter_dict))


    def build(self):
        self.major_encounter_dict = self.build_major_encounter()
        self.minor_encounter_dict = self.build_minor_encounter()


    def load_tables(self, terrain_type):
        # was - majorEncounterTypes = {'1':('Settlement'), '2':('Fortress'), '3':('Ruin'), '4':('Monster'), '5':('Religious'), '6':('Natural')}
        with open("data/majencountertypes.csv", "r") as inFile:
            lines = inFile.readlines()
        for line in lines[1:]:
            values = line.strip().split(',')
            self.major_encounter_types[values[0]] = (values[1])

        # was - minorEncounterTypes = {'1':('Settlement'),'2':('Fort'),'3':('Ruin'),'4':('Monster'),'5':('Wandering Monster'),'6':('Camp'),'7':('Way Station'),'8':('Beacon'),'9':('Construction Site'),'10':('Battlefield'),
        #                       '11':('Isolated'),'12':('Sacred Ground'),'13':('Crossing'),'14':('Ancient Structure'),'15':('Hazard'),'16':('Treasure'),'17':('Contested'),'18':('Natural Resource'),'19':('Supernatural'),'20':('Gathering Place')}
        with open("data/minencountertypes.csv", "r") as inFile:
            lines = inFile.readlines()
        for line in lines[1:]:
            values = line.strip().split(',')
            self.minor_encounter_types[values[0]] = (values[1])

        primary_terrain_types = {}
        # was - primaryTerrainTypes = {'Water':(.1,1),'Marsh':(.2,2),'Desert':(.2,2), 'Grassland': (.6,6), 'Forest':(.4,4), 'Hills/Rough':(.4,4), 'Mountains':(.2,2)}
        with open("data/primaryterraintypes.csv", "r") as inFile:
            lines = inFile.readlines()
        for line in lines[1:]:
            values = line.strip().split(',')
            primary_terrain_types[values[0]] = float(values[1]), int(values[2])
        
        self.terrain_table = primary_terrain_types[terrain_type]


    def build_major_encounter(self):
        # Determine if we have a major encounter
        maj_enc_dict = {}

        if random.randint(1,100) <= int(self.terrain_table[0] * 100):
        
            #Determine Major Encounter Type - randint(x,y) controls which type(s) get gen'd
            maj_enc_type = self.major_encounter_types[str(random.randint(2,2))]

            # Generate details about encounter
            maj_enc_details = ""
            if maj_enc_type == 'Settlement':
                maj_enc_details = str(settlement.Settlement())
            elif maj_enc_type == 'Fortress':
                maj_enc_details = str(fortress.Fortress("data/fortresstables.json"))
            elif maj_enc_type == 'Ruin':
                maj_enc_details = str(ruin.Ruin('data/ruintables.json'))
            else:
                maj_enc_details = "Not yet defined."

            maj_enc_dict['Type'] = maj_enc_type
            maj_enc_dict['Details'] = maj_enc_details
        else:
            maj_enc_dict = {'Type': "None", 'Details': "No Major Encounter"}
    
        return maj_enc_dict 
    

    def build_minor_encounter(self):
        # Determine how many (if any) minor encounters - for each possibility, roll a d6. On a 1, we have a minor encounter!
        num_minor_encs = 0
        min_enc_dict = {}

        for x in range(1,self.terrain_table[1]):
            if random.randint(1,6) == 1:
                num_minor_encs += 1

                #Create the individual Minor Encounter Dictionary
                enc_dict = {}
                
                #Determine Minor Encounter Type - randint(1,20) drives which type is chosen. 
                enc_dict['Type'] = self.minor_encounter_types[str(random.randint(1,3))]

                # Generate details about encounter
                min_enc_details = ""
                if enc_dict['Type'] == 'Settlement':
                    enc_dict['Details'] = str(settlement.Settlement(is_minor=True))
                elif enc_dict['Type'] == 'Fort':
                    enc_dict['Details'] = str(fortress.Fortress("data/fortresstables.json", is_minor=True))
                elif enc_dict['Type'] == 'Ruin':
                    enc_dict['Details'] = "RUINS NOT YET DEFINED"
                else:
                    enc_dict['Details'] = "Not yet defined."

                #Add the individual Minor Encounter to the hex's Minor Encounter Dictionary
                min_enc_dict[str(num_minor_encs)] = enc_dict 

        if not min_enc_dict:
            min_enc_dict['0'] = {'Type':"None", 'Details': "No minor encounters."}
                
        return min_enc_dict
    
