# a Python object (dict):
dictionaryList = {
    "Ute": 2860968,
    "Rainer": 3905852,
    "Harald": 6235534,
    "Olaf": 9275980,
    "Sarah": 6548766
}


# return single Person
def find(name: str):
    if name in dictionaryList:
        return {name: dictionaryList[name]}
    return None


# return all Persons
def find_all():
    return dictionaryList
