import os
import json
import yaml

import species_names
import item_names
import move_names
import ability_names
import various

trainer_parties = "trainer_parties.h"

count_trainers = 0
count = 0
sets = {}
Location = None
species_name = None
trainer_name = None
species_data = {
    "level": None,
    "ivs": None,
    "item": None,
    "ability": None,
    "nature": "NATURE_HARDY",
    "teraType": None,
    "status": "Healthy",
    "moves": [],
    "index": 0,
}

def handle_trainer_name(line):
    global count_trainers
    count_trainers = count_trainers + 1

    global trainer_name
    trainer_name = line.split(":")[1].strip("\n").strip(" ")
    if "[" in trainer_name:
        tmp = trainer_name.split("[")
        trainer_name = tmp[0].strip(" ")

def handle_species(line):
    global species_name
    species = line.split("=")[1].strip()[:-1]
    species_name = species_names.species_dictionary[species]

def handle_level(line):
    level = line.split("=")[1].strip()[:-1]
    species_data["level"] = int(level)

def handle_ivs(line):
    ivs = line.split("=")[1]
    if "IV_SPREAD_TRICK_ROOM_ZERO_SPATK" in ivs:
        temp_dict = {"sa": 0, "sp": 0}
        species_data["ivs"] = temp_dict
    elif "IV_SPREAD_TRICK_ROOM" in ivs:
        temp_dict = {"sp": 0}
        species_data["ivs"] = temp_dict
    elif "IV_SPREAD_ZERO_ATK" in ivs:
        temp_dict = {"at": 0}
        species_data["ivs"] = temp_dict
    elif "IV_SPREAD_HIDDEN_POWER_GRASS" in ivs:
        temp_dict = {"hp": 30, "sa": 30}
        species_data["ivs"] = temp_dict
    elif "IV_SPREAD_HIDDEN_POWER_FIRE" in ivs:
        temp_dict = {"at": 30, "sa": 30, "sp": 30}
        species_data["ivs"] = temp_dict
    elif "IV_SPREAD_HIDDEN_POWER_ICE" in ivs:
        temp_dict = {"sp": 30}
        species_data["ivs"] = temp_dict

def handle_held_item(line):
    held_item = line.split("=")[1].strip()[:-1]
    species_data["item"] = item_names.names[held_item]

def handle_ability(line):
    ability = line.split("=")[1].strip()[:-1]
    species_data["ability"] = ability_names.names[ability]

def handle_nature(line):
    nature = line.split("=")[1].strip()[:-1]
    species_data["nature"] = various.nature_names[nature]

def handle_status(line):
    status = line.split("=")[1].strip()[:-1]
    species_data["status"] = various.status_names[status]

def handle_gender(line):
    gender = line.split("=")[1].strip()[:-1]
    if gender == "TRAINER_MON_FEMALE":
        species_data["gender"] = "f"
    else:
        species_data["gender"] = "m"

def handle_status(line):
    status = line.split("=")[1].strip()[:-1]
    species_data["status"] = various.status_names[status]

def handle_tera_type(line):
    tera_type = line.split("=")[1].strip()[:-1]
    tera_type = various.tera_types[tera_type]
    species_data["teraType"] = tera_type

def handle_moves(line):
    moves = line.split("=")[1].strip()[:-1]
    moves = moves[1:-1].split(",")
    names = []
    for move in moves:
        move = move.strip()
        if move != "MOVE_NONE":
            names.append(move_names.names[move])
    species_data["moves"] = names

def process_species():
    global count
    copy_species_data = species_data.copy()

    species_data.update({
        "level": None,
        "ivs": None,
        "item": None,
        "ability": None,
        "nature": "NATURE_HARDY",
        "status": "Healthy",
        "teraType": None,
        "moves": [],
        "index": 0
    })

    if species_name != None:
        copy_species_data["index"] = count
        if species_name not in sets:
            sets[species_name] = {}
        sets[species_name].update({trainer_name: copy_species_data})

    count = count + 1


def parse_trainers():
    with open(trainer_parties, "r") as source:
        for line in source:
            if "// END" in line:
                break;

            elif "// Name" in line:
                handle_trainer_name(line)
            elif ".lvl" in line:
                handle_level(line)
            elif ".iv" in line:
                handle_ivs(line)
            elif ".species" in line:
                handle_species(line)
            elif ".heldItem" in line:
                handle_held_item(line)
            elif ".ability" in line:
                handle_ability(line)
            elif ".nature" in line:
                handle_nature(line)
            elif ".status" in line:
                handle_status(line)
            elif ".teraType" in line:
                handle_tera_type(line)
            elif ".moves" in line:
                handle_moves(line)
                process_species()

def try_delete_file(file):
    try:
        os.remove(file)
    except OSError:
        pass

if __name__ == "__main__":
    try_delete_file("sets.json")
    parse_trainers()
    print(count_trainers)
    with open('sets.json', 'w+') as ff:
        json.dump(sets, ff, indent=4)

    with open("sets.json", "r") as showdown_sets:
        try_delete_file("gen9.js")
        first_line = True
        for line in showdown_sets:
            if first_line:
                line = "var SETDEX_SV = {\n"
                first_line = False

            with open("gen9.js", "a+") as gen9_js:
                gen9_js.write(line)
