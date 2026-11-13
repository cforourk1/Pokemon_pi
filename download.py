import time
import json
import requests
import sys

pokedex = {}

for i in range(1, 152):
    # call the pokemon api
    pokemon = f"https://pokeapi.co/api/v2/pokemon/{i}"
    response = requests.get(pokemon)

    # check response status
    if response.status_code != 200:
        print("Error in get request, Team Rocket Takeover")
        sys.exit(1)
    data = response.json()

    # get pokemon data
    hp = data["stats"][0]["base_stat"]
    power = 0
    for s in data["stats"]:
        power = power + s["base_stat"]

    # get pokemon type 
    types = []
    for s in data["types"]:
        types.append(s["type"]["name"])

    # get moves 
    moves = []
    for s in data["moves"]:
        for d in s["version_group_details"]:
            if d["version_group"]["name"] == "red-blue" and d["move_learn_method"]["name"] == "level-up":
               moves.append({"name": s["move"]["name"], "level": d["level_learned_at"]})

    # evolution
    species = requests.get(data["species"]["url"]).json()
    chain = requests.get(species["evolution_chain"]["url"]).json()["chain"]
    min_level = 1
    for stage2 in chain["evolves_to"]:
        if stage2["species"]["name"] == data["name"]:
            min_level = stage2["evolution_details"][0]["min_level"] or 20
        for stage3 in stage2["evolves_to"]:
            if stage3["species"]["name"] == data["name"]:
                min_level = stage3["evolution_details"][0]["min_level"] or 30
    pokedex[i] = {"name": data["name"], "types": types,  "hp": hp, "power": power, "min_level": min_level, "moves": moves}
    # get sprites
   # sprite_url = data["sprites"]["front_default"]
  #  image = requests.get(sprite_url)

    # check sprite status
   # if image.status_code != 200:
    #    print("The Pokemon escaped!")
     #   sys.exit(1)

    # save file
   # with open(f"sprites/{i}.png", "wb") as f:
       # f.write(image.content)
    print(f"Gotcha! #{i}")
    time.sleep(0.5)
json.dump(pokedex, open("pokedex.json", "w"))
