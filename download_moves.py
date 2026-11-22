import json
import requests
import time

with open("pokedex.json") as f:
    pokedex = json.load(f)

# save move names to a list and check if move exists
move_names = []
for entry in pokedex.values():
    for m in entry["moves"]:
        if m["name"] not in move_names:
            move_names.append(m["name"])

# loop through moves and save each one
moves = {}
for name in move_names:
    response = requests.get(f"https://pokeapi.co/api/v2/move/{name}")
    data = response.json()
    move_name = data["name"]
    power = data["power"]
    accuracy = data["accuracy"]
    move_type = data["type"]["name"]
    damage_class = data["damage_class"]["name"]
    priority = data["priority"]
    min_hits = data["meta"]["min_hits"]
    max_hits = data["meta"]["max_hits"]
    drain = data["meta"]["drain"]
    crit_rate = data["meta"]["crit_rate"]
    moves[move_name] = {"power": power, "accuracy": accuracy, "type": move_type,
                        "damage_class": damage_class, "priority": priority,
                        "min_hits": min_hits, "max_hits": max_hits,
                        "drain": drain, "crit_rate": crit_rate}
    print(f"Got {move_name}")
    time.sleep(0.5)

# save all moves to a file (after the loop, so it only happens once)
json.dump(moves, open("moves.json", "w"))
print("done")
