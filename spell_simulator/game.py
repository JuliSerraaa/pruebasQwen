"""
Main game logic for the spell casting simulator.
Handles combat, turns, and game flow.
"""

import random
from entities import Player, Enemy, DEFAULT_SPELLS, ENEMY_TYPES
from languages import get_text, get_supported_languages


class SpellCastingGame:
    """Main game class for the spell casting simulator."""
    
    def __init__(self, language='en', difficulty='normal'):
        """
        Initialize the game.
        
        Args:
            language: Language code ('en' or 'es')
            difficulty: 'easy', 'normal', or 'hard'
        """
        self.language = language
        self.difficulty = difficulty
        self.player = None
        self.current_enemy = None
        self.enemies_defeated = 0
        self.game_over = False
        
        # Difficulty modifiers
        self.difficulty_modifiers = {
            'easy': {'player_hp_mult': 1.2, 'enemy_hp_mult': 0.8, 'enemy_dmg_mult': 0.8},
            'normal': {'player_hp_mult': 1.0, 'enemy_hp_mult': 1.0, 'enemy_dmg_mult': 1.0},
            'hard': {'player_hp_mult': 0.9, 'enemy_hp_mult': 1.3, 'enemy_dmg_mult': 1.2},
        }
    
    def setup_player(self, name="Hero"):
        """Create and setup the player character."""
        mods = self.difficulty_modifiers[self.difficulty]
        max_hp = int(100 * mods['player_hp_mult'])
        max_mana = 50
        
        self.player = Player(name=name, max_hp=max_hp, attack_power=10, max_mana=max_mana)
        
        # Give player starting spells
        for spell in DEFAULT_SPELLS[:4]:  # First 4 spells
            self.player.add_spell(spell)
    
    def spawn_enemy(self):
        """Spawn a new enemy based on progress."""
        mods = self.difficulty_modifiers[self.difficulty]
        
        # Select enemy type based on enemies defeated
        available_enemies = min(len(ENEMY_TYPES), 2 + self.enemies_defeated // 2)
        enemy_template = random.choice(ENEMY_TYPES[:available_enemies])
        
        max_hp = int(enemy_template['max_hp'] * mods['enemy_hp_mult'])
        attack_power = int(enemy_template['attack_power'] * mods['enemy_dmg_mult'])
        heal_chance = enemy_template.get('heal_chance', 0.2)
        heal_power = enemy_template.get('heal_power', 10)
        
        self.current_enemy = Enemy(
            name=enemy_template['name'],
            max_hp=max_hp,
            attack_power=attack_power,
            heal_chance=heal_chance,
            heal_power=heal_power
        )
        
        return self.current_enemy
    
    def display_status(self):
        """Display current battle status."""
        t = lambda key: get_text(key, self.language)
        
        print("\n" + "=" * 50)
        
        # Player status
        status = self.player.get_status()
        print(t('player_hp').format(hp=status['hp'], max_hp=status['max_hp']))
        print(t('player_mana').format(mana=status['mana'], max_mana=status['max_mana']))
        
        if status['is_defending']:
            print(t('shield_active'))
        
        # Enemy status
        if self.current_enemy and self.current_enemy.is_alive():
            print(t('enemy_hp').format(
                enemy=self.current_enemy.name,
                hp=self.current_enemy.current_hp,
                max_hp=self.current_enemy.max_hp
            ))
        
        print("=" * 50)
    
    def display_spells(self):
        """Display available spells."""
        t = lambda key: get_text(key, self.language)
        
        print(f"\n{t('choose_spell')}")
        print("-" * 40)
        print(f"{'#':<3} {t('spell_name'):<20} {t('spell_power'):<15} {t('spell_mana_cost'):<12}")
        print("-" * 40)
        
        for i, spell in enumerate(self.player.spells, 1):
            if spell.spell_type == 'heal':
                power_str = f"Heal: {spell.heal_power}"
            else:
                power_str = f"Dmg: {spell.power}"
            print(f"{i:<3} {spell.name:<20} {power_str:<15} {spell.mana_cost:<12}")
        
        # Additional actions
        num_spells = len(self.player.spells) + 1
        print(f"{num_spells:<3} {t('attack'):<20} {'Dmg: 5-15':<15} {'0':<12}")
        num_spells += 1
        print(f"{num_spells:<3} {t('defend'):<20} {'Block next':<15} {'0':<12}")
        num_spells += 1
        print(f"{num_spells:<3} {t('rest'):<20} {'+5 Mana':<15} {'0':<12}")
        print("-" * 40)
    
    def player_turn(self):
        """Handle player's turn."""
        t = lambda key: get_text(key, self.language)
        
        print(f"\n>>> {t('player_turn')} <<<")
        self.display_status()
        self.display_spells()
        
        while True:
            try:
                choice = input(f"\nSelect action (1-{len(self.player.spells) + 3}): ").strip()
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(self.player.spells):
                    # Cast spell
                    spell = self.player.spells[choice_num - 1]
                    result, status = self.player.cast_spell(spell, self.current_enemy)
                    
                    if status == "not_enough_mana":
                        print(t('not_enough_mana'))
                        continue
                    
                    if result['type'] == 'damage':
                        print(t('cast_spell').format(player=self.player.name, spell=spell.name))
                        print(t('damage_dealt').format(damage=result['value'], target=self.current_enemy.name))
                        if result['blocked']:
                            print(t('blocked_damage'))
                    elif result['type'] == 'heal':
                        print(t('cast_spell').format(player=self.player.name, spell=spell.name))
                        print(t('heal_done').format(player=self.player.name, heal=result['value']))
                    
                    break
                    
                elif choice_num == len(self.player.spells) + 1:
                    # Basic attack
                    damage, blocked = self.player.basic_attack(self.current_enemy)
                    print(f"{self.player.name} attacks with weapon!")
                    print(t('damage_dealt').format(damage=damage, target=self.current_enemy.name))
                    if blocked:
                        print(t('blocked_damage'))
                    break
                    
                elif choice_num == len(self.player.spells) + 2:
                    # Defend
                    self.player.defend()
                    print(f"{self.player.name} raises shield!")
                    print(t('shield_active'))
                    break
                    
                elif choice_num == len(self.player.spells) + 3:
                    # Rest
                    recovered = self.player.rest()
                    print(f"{self.player.name} rests to recover mana...")
                    print(t('mana_recovered').format(mana=recovered))
                    break
                    
                else:
                    print(t('invalid_choice'))
                    
            except ValueError:
                print(t('invalid_choice'))
    
    def enemy_turn(self):
        """Handle enemy's turn."""
        t = lambda key: get_text(key, self.language)
        
        print(f"\n>>> {t('enemy_turn')} <<<")
        
        if not self.current_enemy or not self.current_enemy.is_alive():
            return
        
        action, result = self.current_enemy.ai_action(self.player)
        
        if action == 'attack':
            print(t('enemy_attacks').format(
                enemy=self.current_enemy.name,
                damage=result['damage']
            ))
            if result['blocked']:
                print(t('blocked_damage'))
                
        elif action == 'heal':
            print(t('enemy_heals').format(
                enemy=self.current_enemy.name,
                heal=result['value']
            ))
            
        elif action == 'defend':
            print(f"{self.current_enemy.name} takes defensive stance!")
            print(t('shield_active'))
    
    def check_battle_end(self):
        """
        Check if battle has ended.
        
        Returns:
            tuple: (battle_ended, game_ended, victory)
        """
        t = lambda key: get_text(key, self.language)
        
        # Check if enemy is defeated
        if not self.current_enemy.is_alive():
            print(f"\n{t('enemy_defeated').format(enemy=self.current_enemy.name)}")
            self.enemies_defeated += 1
            self.current_enemy = None
            
            # Check if player wants to continue or game ends
            return True, False, True
        
        # Check if player is defeated
        if not self.player.is_alive():
            print(f"\n{t('player_defeated')}")
            return True, True, False
        
        return False, False, False
    
    def run_battle(self):
        """Run a single battle encounter."""
        t = lambda key: get_text(key, self.language)
        
        # Spawn enemy if none exists
        if not self.current_enemy:
            enemy = self.spawn_enemy()
            print(f"\n{t('new_enemy_appears').format(enemy=enemy.name)}")
        
        # Battle loop
        while True:
            # Player turn
            self.player_turn()
            
            # Check battle end after player action
            battle_ended, game_ended, victory = self.check_battle_end()
            if game_ended:
                self.game_over = True
                return False
            if battle_ended and victory:
                break
            
            # Enemy turn
            self.enemy_turn()
            
            # Check battle end after enemy action
            battle_ended, game_ended, victory = self.check_battle_end()
            if game_ended:
                self.game_over = True
                return False
            if battle_ended and victory:
                break
        
        return True
    
    def ask_play_again(self):
        """Ask player if they want to play again."""
        t = lambda key: get_text(key, self.language)
        
        while True:
            choice = input(t('play_again')).strip().lower()
            if choice in ['y', 'yes', 's', 'sí']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print(t('invalid_yes_no'))
    
    def reset_game(self):
        """Reset game state for new game."""
        self.enemies_defeated = 0
        self.current_enemy = None
        self.game_over = False
        self.setup_player(self.player.name if self.player else "Hero")
    
    def run(self):
        """Main game loop."""
        t = lambda key: get_text(key, self.language)
        
        print("=" * 50)
        print(t('game_title'))
        print("=" * 50)
        
        # Get player name
        name = input("\nEnter your hero's name: ").strip()
        if not name:
            name = "Hero"
        
        self.setup_player(name)
        
        # Main game loop
        while not self.game_over:
            battle_won = self.run_battle()
            
            if self.game_over:
                break
            
            if battle_won:
                print(f"\n{t('victory')}")
                print(f"Enemies defeated: {self.enemies_defeated}")
                
                # Ask to continue
                if not self.ask_play_again():
                    print(f"\n{t('game_over')}")
                    print(f"Total enemies defeated: {self.enemies_defeated}")
                    break
                
                # Reset for next battle but keep player stats
                self.current_enemy = None
        
        print("\nThanks for playing!")


def select_language():
    """Let user select language."""
    print("Select language / Selecciona idioma:")
    print("1. English (en)")
    print("2. Español (es)")
    
    while True:
        choice = input("Enter choice (1-2): ").strip()
        if choice == '1':
            return 'en'
        elif choice == '2':
            return 'es'
        else:
            print("Invalid choice. Please enter 1 or 2.")


def select_difficulty():
    """Let user select difficulty."""
    print("\nSelect difficulty:")
    print("1. Easy")
    print("2. Normal")
    print("3. Hard")
    
    while True:
        choice = input("Enter choice (1-3): ").strip()
        if choice == '1':
            return 'easy'
        elif choice == '2':
            return 'normal'
        elif choice == '3':
            return 'hard'
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    lang = select_language()
    difficulty = select_difficulty()
    
    game = SpellCastingGame(language=lang, difficulty=difficulty)
    game.run()
