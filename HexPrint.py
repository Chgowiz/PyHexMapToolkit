# Print out formatted hex information

def printHex(hex):
    print("This hex has:")
    printMajorEncounter(hex)
    printMinorEncounters(hex)


def printMajorEncounter(hex):
    if hex['Major Encounter']:
        print("Major Encounter: {}".format(hex['Major Encounter']['Type']))
        print("\t{}".format(hex['Major Encounter']['Details']))
    else:
        print("No major encounter.")


def printMinorEncounters(hex):
    if hex['Minor Encounters']:
        print("Minor Encounters:")
        # In order to read a dictionary in a dictionary, I had to use 
        # items(). Iterating over a dictionary just pulls its keys.
        for minEnc, minEncDetails in hex['Minor Encounters'].items():
            print("\t{}. {}".format(minEnc, minEncDetails['Type']))
            print("\t\t{}".format(minEncDetails['Details']))
    else:
        print("No minor encounters.")
