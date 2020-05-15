import random
import json
import jsonrollabletable
import settlement
import fortress
import ruin

class Hex(jsonrollabletable.JsonRollableTable):

    def __init__(self, tup_filenames, terrain_type = 'None'):
        self.major_encounter_dict = {}
        self.minor_encounters_dict = {}

        self.encounters_file = tup_filenames[0]
        self.settlement_file = tup_filenames[1]
        self.fortress_file = tup_filenames[2]
        self.ruin_file = tup_filenames[3]

        self.terrain_type = terrain_type
        self.pct_major_encounter = 0.0
        self.num_minor_encounters = 0

        self.load_encounter_tables()

        table = [tbl for tbl in self.data_tables if tbl['name'] == 'Terrain Types'][0]
        self.pct_major_encounter, self.num_minor_encounters = [
            ( float(d['pct_maj_encounter']), int(d['num_min_encounters']) ) 
            for d in table['entries'] if d['terrain'] == self.terrain_type][0]

        self.build()


    def __str__(self):
        return "Major Encounter\n{}\nMinor Encounters\n{}".format(str(self.major_encounter_dict),str(self.minor_encounters_dict))


    def build(self):
        self.major_encounter_dict = self.build_major_encounter()
        self.minor_encounters_dict = self.build_minor_encounters()


    def load_encounter_tables(self):
        json_str = ""
        with open(self.encounters_file, "r") as inFile:
            json_str = inFile.read()

        # The way the JSON is formatted, it creates a dictionary w/key of some value.
        # I use dict.values to create a view object of the values of the dict.
        # I then use iter to create an iterable, and next to get the first value - 
        # which will have a list of the data tables (which are dictionaries themselves).
        self.data_tables = next( iter( json.loads(json_str).values() ) )


    def build_major_encounter(self):
        # Determine if we have a major encounter
        enc_dict = {}

        if random.randint(1,100) <= int(self.pct_major_encounter * 100): # s/b randint(1,100)
            enc_dict['Type'] = self.roll_for_entry('Major Encounter Types')

            # Generate details about encounter
            if enc_dict['Type'] == 'Settlement':
                enc_dict['Details'] = str(settlement.Settlement(self.settlement_file))
                # If village has fort or keep, what are details?
                print('DEBUG - If settlement has fort/keep - need to build.')
            elif enc_dict['Type'] == 'Fortress':
                enc_dict['Details'] = str(fortress.Fortress(self.fortress_file))
                # If fortress protects settlement - what are details of settlement (a village)
                print('DEBUG - If fortress protects settlement - need to build.')
            elif enc_dict['Type'] == 'Ruin':
                enc_dict['Details'] = str(ruin.Ruin(self.ruin_file))
            else:
                enc_dict['Details'] = enc_dict['Type'] + " - Not yet defined. DEBUG"

        else:
            enc_dict = {'Type': "None", 'Details': "No Major Encounter"}
    
        return enc_dict 
    

    def build_minor_encounters(self):
        # Determine how many (if any) minor encounters - for each possibility, roll a d6. On a 1, we have a minor encounter!
        num_minor_encs = 0
        encounters_dict = {}

        for x in range(self.num_minor_encounters):
            if random.randint(1,6) == 1:
                num_minor_encs += 1

                #Create the individual Minor Encounter Dictionary
                enc_dict = {}
                
                #Determine Minor Encounter Type - randint(1,20) drives which type is chosen. 
                enc_dict['Type'] = self.roll_for_entry('Minor Encounter Types')

                # Generate details about encounter
                if enc_dict['Type'] == 'Settlement':
                    enc_dict['Details'] = str(settlement.Settlement(self.settlement_file, is_minor=True))
                elif enc_dict['Type'] == 'Fort':
                    enc_dict['Details'] = str(fortress.Fortress(self.fortress_file, is_minor=True))
                elif enc_dict['Type'] == 'Ruin':
                    enc_dict['Details'] = "RUINS NOT YET DEFINED"
                else:
                    enc_dict['Details'] = "Not yet defined."

                #Add the individual Minor Encounter to the hex's Minor Encounter Dictionary
                encounters_dict[str(num_minor_encs)] = enc_dict 

        if not encounters_dict:
            encounters_dict['0'] = {'Type':"None", 'Details': "No minor encounters."}
                
        return encounters_dict
    
