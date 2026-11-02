import json
import random
import pygame
from PIL import Image



pygame.init()
window = pygame.display.set_mode((960, 720))
font = pygame.font.Font(None, 48)
with open("pokedex.json") as f:
    pokedex = json.load(f)

# loop to capitalize names
for entry in pokedex.values():
    entry["name"] = entry["name"].capitalize()

# load all 151 sprites into a list of surfaces
surfaces = []
for number in range(1, 152):
    # black background, open sprite, resize to fit
    canvas = Image.new("RGB", (320, 240), "black")
    sprite = Image.open(f"sprites/{number}.png").convert("RGBA")
    sprite = sprite.resize((sprite.width * 2, sprite.height * 2), Image.NEAREST)

    # center sprite
    x = (canvas.width - sprite.width) // 2
    y = (canvas.height - sprite.height) // 2
    canvas.paste(sprite, (x, y), sprite)

    # convert pillow canvas to a pygame surface, scale 3x
    surface = pygame.image.frombytes(canvas.tobytes(), canvas.size, "RGB")
    surface = pygame.transform.scale(surface, (960, 720))
    surfaces.append(surface)

# show them one at a time
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    index = random.randint(0, 150)
    name = pokedex[str(index + 1)]["name"]
    hp = pokedex[str(index + 1)]["hp"]
    min_level = pokedex[str(index + 1)]["min_level"]
    level = random.randint(min_level, 99)
    hp_now = (2 * hp * level) // 100 + level + 10
    text = font.render(f"{name} Lv {level} HP {hp_now}", True, "white")
    print(pokedex[str(index + 1)]["name"], level, hp_now)
    window.blit(surfaces[index], (0, 0))
    window.blit(text, (40, 640))
    pygame.display.flip()
    pygame.time.wait(1000)
pygame.quit()
