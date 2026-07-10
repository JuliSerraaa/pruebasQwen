# Spell Casting Simulator

A turn-based spell casting combat simulator with multiple enemies, spells, and multi-language support.

## Features

- **Multiple Spells**: Cast different spells with varying power and mana costs
  - Fireball, Ice Bolt, Lightning Strike (damage spells)
  - Heal, Greater Heal (healing spells)
  - Magic Missile (low cost damage)

- **Combat System**:
  - Turn-based battles
  - Mana management
  - Defend action to block attacks
  - Rest to recover mana
  - Basic weapon attack

- **Multiple Enemies**: Fight various enemy types
  - Goblin, Orc, Skeleton Warrior
  - Dark Mage, Demon (with healing abilities)
  - Dragon (boss-level enemy)

- **Enemy AI**: Enemies can attack, heal, or defend based on their health

- **Difficulty Levels**: Easy, Normal, Hard

- **Multi-language Support**: 
  - English (en)
  - Spanish (es)

## Project Structure

```
spell_simulator/
├── languages.py      # Translation strings for EN/ES
├── entities.py       # Player, Enemy, Spell classes
├── game.py           # Main game logic and loop
└── README.md         # This file
```

## How to Run

```bash
cd spell_simulator
python game.py
```

## Gameplay

1. Select your language (English or Spanish)
2. Choose difficulty level
3. Enter your hero's name
4. In battle:
   - Choose spells to cast (numbered options)
   - Manage your mana carefully
   - Use Defend to reduce incoming damage
   - Rest to recover mana when needed
5. Defeat enemies to progress
6. Continue fighting or stop after each victory

## Adding More Content

### Add a new spell:
Edit `entities.py` and add to `DEFAULT_SPELLS`:
```python
Spell("Fire Storm", power=25, mana_cost=20, spell_type='damage')
```

### Add a new enemy:
Edit `entities.py` and add to `ENEMY_TYPES`:
```python
{"name": "Phoenix", "max_hp": 80, "attack_power": 16, "heal_chance": 0.25, "heal_power": 15}
```

### Add a new language:
Edit `languages.py` and add a new entry to `TRANSLATIONS` dictionary with all the required keys.
