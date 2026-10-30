import requests
import sys

for i in range(1, 152):
    # call the pokemon api
    pokemon = f"https://pokeapi.co/api/v2/pokemon/{i}"
    response = requests.get(pokemon)

    # check response status
    if response.status_code != 200:
        print("Error in get request, Team Rocket Takeover")
        sys.exit(1)
    data = response.json()

    # get sprites
    sprite_url = data["sprites"]["front_default"]
    image = requests.get(sprite_url)

    # check sprite status
    if image.status_code != 200:
        print("The Pokemon escaped!")
        sys.exit(1)

    # save file
    with open(f"sprites/{i}.png", "wb") as f:
        f.write(image.content)
    print(f"Gotcha! #{i}")
