import json
import requests
import sys

# pick the pokemon from the command line, or ask for one
if len(sys.argv) > 1:
    pokemon = sys.argv[1]
else:
    pokemon = input("Which Pokemon? ")
pokemon = pokemon.strip().lower()

# call the pokemon api
response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")

# check response status
if response.status_code != 200:
    print("Error in get request, Team Rocket Takeover")
    sys.exit(1)
data = response.json()

# get moves
moves = []
for s in data["moves"]:
    moves.append(s["move"]["name"])
moves.sort()

# show them
print(f"#{data['id']} {data['name']} knows {len(moves)} moves:")
for m in moves:
    print(f"  {m}")

# save file
json.dump({"name": data["name"], "moves": moves}, open(f"{data['name']}_moves.json", "w"), indent=2)
