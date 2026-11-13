import json
import random
import pygame
from PIL import Image



pygame.init()
window = pygame.display.set_mode((960, 720))
name_font = pygame.font.Font("fonts/pixel.ttf", 36)
stat_font = pygame.font.Font("fonts/pixel.ttf", 24)
move_font = pygame.font.Font("fonts/pixel.ttf", 22)

# splash screen while sprites load
window.fill("black")
title_image = name_font.render("Pokemon Pi", True, "white")
title_rect = title_image.get_rect(centerx=480, centery=320)
window.blit(title_image, title_rect)
status_image = stat_font.render("Loading...", True, "white")
window.blit(status_image, status_image.get_rect(centerx=480, centery=400))
pygame.display.flip()
with open("pokedex.json") as f:
    pokedex = json.load(f)

# loop to capitalize names
for entry in pokedex.values():
    entry["name"] = entry["name"].capitalize()

# load all 151 sprites into a list of surfaces
surfaces = []
for number in range(1, 152):
    # black background, open sprite, resize to fit
    canvas = Image.new("RGB", (960, 720), "black")
    sprite = Image.open(f"sprites/{number}.png").convert("RGBA")
    sprite = sprite.resize((sprite.width * 4, sprite.height * 4), Image.NEAREST)

    # center sprite
    x = (canvas.width - sprite.width) // 2
    y = 0
    canvas.paste(sprite, (x, y), sprite)

    # convert pillow canvas to a pygame surface
    surface = pygame.image.frombytes(canvas.tobytes(), canvas.size, "RGB")
    surfaces.append(surface)

# Click and display a random pokemon
running = True
# loading done, wait for a click
window.fill("black")
window.blit(title_image, title_rect)
start_image = stat_font.render("Click to start", True, "white")
window.blit(start_image, start_image.get_rect(centerx=480, centery=400))
pygame.display.flip()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            index = random.randint(0, 150)
            name = pokedex[str(index + 1)]["name"]
            hp = pokedex[str(index + 1)]["hp"]
            power = pokedex[str(index + 1)]["power"]
            types = pokedex[str(index + 1)]["types"]
            min_level = pokedex[str(index + 1)]["min_level"]
            moves = pokedex[str(index + 1)]["moves"]
            level = random.randint(min_level, 99)

            # moves known at this level, oldest to newest
            known = []
            for m in moves:
                if m["level"] <= level:
                    known.append(m)
            known.sort(key=lambda m: m["level"])

            # remove duplicates, keep the last four
            names = []
            for m in known:
                if m["name"] not in names:
                    names.append(m["name"])
            last_four = names[-4:]

            hp_now = (2 * hp * level) // 100 + level + 10
            print(name, level, hp_now, last_four)

            # sprite
            window.blit(surfaces[index], (0, 0))

            # name
            name_image = name_font.render(name, True, "white")
            name_rect = name_image.get_rect(centerx=480, top=370)
            window.blit(name_image, name_rect)

            # type
            type_text = " / ".join(types).title()
            type_image = stat_font.render(type_text, True, "white")
            type_rect = type_image.get_rect(centerx=480, top=415)
            window.blit(type_image, type_rect)

            # level, hp, power
            stats = f"Lv {level}   HP {hp_now}   PWR {power}"
            stats_image = stat_font.render(stats, True, "white")
            stats_rect = stats_image.get_rect(centerx=480, top=448)
            window.blit(stats_image, stats_rect)

            # moveset heading
            heading_image = stat_font.render("Moveset", True, "white")
            heading_rect = heading_image.get_rect(centerx=480, top=500)
            window.blit(heading_image, heading_rect)

            # turn each move into a picture of its text
            move_images = []
            for move in last_four:
                move_name = move.replace("-", " ").title()
                move_images.append(move_font.render(move_name, True, "white"))

            # find the widest move so the whole list can be centered
            widest = 0
            for image in move_images:
                if image.get_width() > widest:
                    widest = image.get_width()
            list_left = 480 - (widest + 20) // 2

            # draw each move with a small square bullet in front
            for n, image in enumerate(move_images):
                top = 535 + n * 30
                pygame.draw.rect(window, "white", (list_left, top + 8, 6, 6))
                window.blit(image, (list_left + 20, top))

            pygame.display.flip()
    pygame.time.wait(30)
pygame.quit()
