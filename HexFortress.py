import json
import dice
import HexSettlement
import HexCharacter 


def BuildFortress(isMinor = False):
    strFortress = ""
    strJson = ""

    with open("data/fortresstables.json", "r") as inFile:
        strJson = inFile.read()

    # The way the JSON is formatted, it creates a dictionary w/key of 'fortresstables'
    # which will have a list of the tables (which are dictionaries themselves). I just want that list.
    tables = json.loads(strJson)['fortresstables']

    # Type of fortress
    table = [tbl for tbl in tables if tbl['name'] == 'Fortress Type'][0]
    d = table['dtype']
    fType = table['entries'][str(sum(dice.roll('1d' + str(d))))]
    # []

    # Ruler of fortress
    table = [tbl for tbl in tables if tbl['name'] == 'Fortress Ruler'][0]
    d = table['dtype']
    fRuler = table['entries'][str(sum(dice.roll('1d' + str(d))))]

    # What does fortress protect 
    table = [tbl for tbl in tables if tbl['name'] == 'Protecting'][0]
    d = table['dtype']
    fProtecting = table['entries'][str(sum(dice.roll('1d' + str(d))))]

    # Who are guards of the fortress
    table = [tbl for tbl in tables if tbl['name'] == 'Guards'][0]
    d = table['dtype']
    fGuards = table['entries'][str(sum(dice.roll('1d' + str(d))))]

    # Who is majordomo of fortress
    table = [tbl for tbl in tables if tbl['name'] == 'Majordomo'][0]
    d = table['dtype']
    fMajorDomo = table['entries'][str(sum(dice.roll('1d' + str(d))))]

    # How many floors/guards for fortress
    table = [tbl for tbl in tables if tbl['name'] == 'Type Details'][0]

    fNumFloors = 0
    n, s, mod = tuple(table['entries'][fType]['floors'].split(','))
    fNumFloors = sum(dice.roll(str(n) + 'd' + str(s))) + int(mod)

    fNumGuards = 0
    n, s, mod = tuple(table['entries'][fType]['guards'].split(','))
    fNumGuards = sum(dice.roll(str(n) + 'd' + str(s))) + int(mod)

    fRuler = 'NPC'

    # If ruler or majordomo is NPC - what are details of NPC
    if fRuler == 'NPC':
        sClass, sLevel, sAlign = HexCharacter.CreateNPC()
        fRuler = "{} level {} ({})".format(sLevel, sClass, sAlign)

    if fMajorDomo == 'NPC':
        sClass, sLevel, sAlign = HexCharacter.CreateNPC()
        fMajorDomo = "{} level {} ({})".format(sLevel, sClass, sAlign)

    # If ruler is noble - what are details of noble

    # Create the description string
    strFortress = "{} (floors: {}, guards: {} {}/floor)\n\tprotecting {}, ruler: {}, majordomo: {}".format(fType, fNumFloors, fNumGuards, fGuards, fProtecting , fRuler, fMajorDomo)

    # If fortress protects settlement - what are details of settlement (a village)
    if fProtecting == 'Village':
        strFortress += "\n\t" + HexSettlement.BuildSettlement(isVillage = True)

    return strFortress


