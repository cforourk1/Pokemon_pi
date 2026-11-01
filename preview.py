import pygame
from PIL import Image

pygame.init()
window = pygame.display.set_mode((960, 720))

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
index = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    window.blit(surfaces[index], (0, 0))
    pygame.display.flip()
    pygame.time.wait(1000)
    index = index + 1
    if index == 151:
        index = 0
pygame.quit()
