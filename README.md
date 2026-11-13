# Pokemon Pi

A Raspberry Pi display of the original 151 Pokémon, written in Python with pygame.
Each click shows a random Gen 1 Pokémon with its sprite, types, level, HP and
the moves it would know at that level in Red/Blue.

This is my first Raspberry Pi project and my first Python project.

<!-- TODO: add a photo of the Pi screen here -->

## What it does

- Shows a **Loading...** screen while the sprites load, then **Click to start**
- On each click, picks a random Pokémon (#1–151) and shows:
  - its sprite, scaled up 4x
  - name and type, such as "Grass / Poison"
  - a random level, current HP and PWR (base stat total)
  - **Moveset**: the last 4 moves it would know at that level

## Files

| File | What it is |
|---|---|
| `download.py` | Pulls Gen 1 data from [PokeAPI](https://pokeapi.co) and saves it to `pokedex.json`. It can also download the sprites (that part is commented out because they're already downloaded). |
| `pokedex.json` | Data for all 151 Pokémon, keyed `"1"` to `"151"` |
| `preview.py` | The pygame display program |
| `sprites/` | Sprite images, saved as `1.png` to `151.png` |
| `fonts/pixel.ttf` | The pixel font used for all text |

### pokedex.json format

```json
"1": {
  "name": "bulbasaur",
  "types": ["grass", "poison"],
  "hp": 45,
  "power": 318,
  "min_level": 1,
  "moves": [{"name": "vine-whip", "level": 13}, {"name": "tackle", "level": 1}]
}
```

- `hp`: base HP stat
- `power`: all six base stats added together
- `min_level`: the lowest level this Pokémon can be. It's the level it evolves at, or 20 for a
  2nd stage and 30 for a 3rd stage when evolving isn't based on level (for example, stones or trading).
- `moves`: Red/Blue level-up moves only. They aren't sorted and can contain duplicates.

## How the numbers work

- **Level**: random, from `min_level` to 99
- **HP**: `(2 × base HP × level) ÷ 100 + level + 10`, a simplified version of the game's formula
- **Moveset**:
  1. keep the moves learned at or below the current level
  2. sort them by level
  3. remove duplicates
  4. keep the last 4, matching how the games keep your 4 most recent moves

## Setup

### On the Mac (only needed to re-download the data)

```bash
cd ~/ClaudeWork/RaspberryPi/poke151
pip3 install requests
python3 download.py
```

This takes a few minutes, because it pauses for half a second between Pokémon to be polite to PokeAPI.

### Copy to the Pi

```bash
rsync -av ~/ClaudeWork/RaspberryPi/poke151/ cforourk@mewtwo-pi.local:~/poke151/
```

### On the Pi (Raspberry Pi OS)

```bash
sudo apt install python3-pygame python3-pil
```

No internet is needed to run the program, because everything it needs is in the folder.

## Running it

On the Pi itself:

```bash
cd ~/poke151 && python3 preview.py
```

Over SSH (the program shows up on the Pi's screen, not the Mac's):

```bash
ssh cforourk@mewtwo-pi.local
cd ~/poke151 && DISPLAY=:0 python3 preview.py
```

**Controls:** click (or tap) for a new Pokémon. Close the window to quit.

## Known quirks

- The pixel font's lowercase "o" looks like a capital "O". This comes from the font, not the code.

## Roadmap

- [ ] Start menu with two buttons: **Get a Pokémon** and **Battle**
- [ ] Menu button to go back from any screen
- [ ] Play each Pokémon's cry (from PokeAPI's `cries`) when it appears
- [ ] Battle mode
  - [ ] Roll a random type, then pick a random Pokémon of that type. Roll again for the challenger.
  - [ ] Download Attack, Defense, Special, Speed and move power/type/accuracy
  - [ ] Simulate the battle using the Gen 1 damage formula and type chart
  - [ ] Show a win prediction by simulating the matchup many times
- [ ] Animation (bobbing, shake when hit, flash when fainting)
- [ ] Fullscreen
- [ ] Start automatically when the Pi boots

## Credits

- Pokémon data, sprites and cries: [PokeAPI](https://pokeapi.co)
- Pokémon is © Nintendo / Game Freak / The Pokémon Company. This is a personal,
  non-commercial fan project and isn't affiliated with them.
<!-- TODO: add where pixel.ttf came from and its license -->
