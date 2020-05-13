import json
import dice

class JsonRollableTable():

    def __init__(self, json_file):
        json_str = ""

        with open(json_file, "r") as inFile:
            json_str = inFile.read()

        # The way the JSON is formatted, it creates a dictionary w/key of some value.
        # I use dict.values to create a view object of the values of the dict.
        # I then use iter to create an iterable, and next to get the first value - 
        # which will have a list of the data tables (which are dictionaries themselves).
        self.data_tables = next( iter( json.loads(json_str).values() ) )

    def roll_for_entry(self, entry_name):
        """ Get a random entry from a table. 
            Assumes self.data_tables is a list of dictionaries (multiple tables)
            w/'name','dtype','entries' keys/values."""
        table = [tbl for tbl in self.data_tables if tbl['name'] == entry_name][0]
        d = table['dtype']
        return table['entries'][str(sum(dice.roll('1d' + str(d))))]


