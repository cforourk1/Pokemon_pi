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

# get list of types
pktype = []
for entry in pokedex.values():
    for type_name in entry["types"]:
        if type_name not in pktype:
            pktype.append(type_name)

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

# turn keeps track of where we are:
# 0 = start screen, 1 = player 1 rolls, 2 = player 2 rolls, 3 = battle
turn = 0

# each player's pokemon gets saved here after they roll
fighter1 = None
fighter2 = None

# loading done, show the start screen
window.fill("black")
window.blit(title_image, title_rect)
start_image = stat_font.render("Tap to battle", True, "white")
window.blit(start_image, start_image.get_rect(centerx=480, centery=400))
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:

            # start screen was tapped: ask player 1 to roll
            if turn == 0:
                turn = 1
                window.fill("black")
                window.blit(title_image, title_rect)
                prompt_image = stat_font.render("Player 1 - tap to roll", True, "white")
                window.blit(prompt_image, prompt_image.get_rect(centerx=480, centery=400))
                pygame.display.flip()

            # player 1 or player 2 tapped: roll for class, then get a pokemon
            elif turn == 1 or turn == 2:

                # roll for class
                rolled_type = random.choice(pktype)

                # get pokemon of matching type
                matches = []
                for key in pokedex:
                    if rolled_type in pokedex[key]["types"]:
                        matches.append(key)

                # show what class they rolled
                window.fill("black")
                rolled_image = stat_font.render(f"Player {turn} rolled", True, "white")
                window.blit(rolled_image, rolled_image.get_rect(centerx=480, centery=300))
                class_image = name_font.render(rolled_type.title(), True, "white")
                window.blit(class_image, class_image.get_rect(centerx=480, centery=360))
                pygame.display.flip()
                pygame.time.wait(1500)

                # pick a random pokemon of that type
                fighter_key = random.choice(matches)
                index = int(fighter_key) - 1
                name = pokedex[fighter_key]["name"]
                hp = pokedex[fighter_key]["hp"]
                power = pokedex[fighter_key]["power"]
                types = pokedex[fighter_key]["types"]
                min_level = pokedex[fighter_key]["min_level"]
                moves = pokedex[fighter_key]["moves"]
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
                print(f"Player {turn} rolled {rolled_type}: {name}", level, hp_now, last_four)

                # sprite
                window.blit(surfaces[index], (0, 0))

                # which player this pokemon belongs to
                player_image = stat_font.render(f"Player {turn}", True, "white")
                window.blit(player_image, (20, 20))

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

                # save this player's pokemon for the battle
                fighter = {"key": fighter_key, "name": name, "level": level,
                           "hp": hp_now, "moves": last_four}

                if turn == 1:
                    # player 1 is done: ask player 2 to roll
                    fighter1 = fighter
                    prompt_image = stat_font.render("Player 2 - tap to roll", True, "white")
                    window.blit(prompt_image, prompt_image.get_rect(centerx=480, centery=690))
                    pygame.display.flip()
                    turn = 2
                else:
                    # player 2 is done: show their pokemon, then go to battle
                    fighter2 = fighter
                    pygame.display.flip()
                    pygame.time.wait(2000)

                    # battle placeholder - the real battle goes here later
                    window.fill("black")
                    battle_image = name_font.render("Battle!", True, "white")
                    window.blit(battle_image, battle_image.get_rect(centerx=480, centery=320))
                    versus = f"{fighter1['name']}  vs  {fighter2['name']}"
                    versus_image = stat_font.render(versus, True, "white")
                    window.blit(versus_image, versus_image.get_rect(centerx=480, centery=400))
                    pygame.display.flip()
                    turn = 3

                # ignore any taps made while the screen was waiting
                pygame.event.clear(pygame.MOUSEBUTTONDOWN)

            # turn 3 is the battle: tapping does nothing yet

    pygame.time.wait(30)
pygame.quit()
