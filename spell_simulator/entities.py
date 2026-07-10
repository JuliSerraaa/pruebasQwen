"""
Entity classes for the spell casting simulator.
Includes Player, Enemy, and Spell classes.
"""

import random


class Spell:
    """Represents a spell that can be cast."""
    
    def __init__(self, name, power, mana_cost, spell_type='damage', heal_power=0):
        """
        Initialize a spell.
        
        Args:
            name: Name of the spell
            power: Base damage/power of the spell
            mana_cost: Mana required to cast
            spell_type: 'damage', 'heal', or 'special'
            heal_power: Amount of healing if spell_type is 'heal'
        """
        self.name = name
        self.power = power
        self.mana_cost = mana_cost
        self.spell_type = spell_type
        self.heal_power = heal_power
    
    def __str__(self):
        if self.spell_type == 'heal':
            return f"{self.name} (Heal: {self.heal_power}, Cost: {self.mana_cost})"
        return f"{self.name} (Power: {self.power}, Cost: {self.mana_cost})"


class Entity:
    """Base class for all entities in the game."""
    
    def __init__(self, name, max_hp, attack_power):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack_power = attack_power
        self.is_defending = False
    
    def is_alive(self):
        """Check if entity is still alive."""
        return self.current_hp > 0
    
    def take_damage(self, damage):
        """Apply damage to the entity."""
        if self.is_defending:
            damage = damage // 2
            self.is_defending = False
            blocked = True
        else:
            blocked = False
        
        self.current_hp = max(0, self.current_hp - damage)
        return damage, blocked
    
    def heal(self, amount):
        """Heal the entity."""
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        return amount
    
    def defend(self):
        """Raise defense to block next attack."""
        self.is_defending = True
    
    def basic_attack(self, target):
        """Perform a basic attack on target."""
        damage = random.randint(self.attack_power - 2, self.attack_power + 2)
        damage = max(1, damage)
        actual_damage, blocked = target.take_damage(damage)
        return actual_damage, blocked


class Player(Entity):
    """Player character with mana and spells."""
    
    def __init__(self, name="Hero", max_hp=100, attack_power=10, max_mana=50):
        super().__init__(name, max_hp, attack_power)
        self.max_mana = max_mana
        self.current_mana = max_mana
        self.spells = []
        self.mana_regen = 5
    
    def add_spell(self, spell):
        """Add a spell to the player's spellbook."""
        self.spells.append(spell)
    
    def cast_spell(self, spell, target):
        """Cast a spell on target."""
        if spell.mana_cost > self.current_mana:
            return None, "not_enough_mana"
        
        self.current_mana -= spell.mana_cost
        
        if spell.spell_type == 'damage':
            damage = spell.power + random.randint(-2, 2)
            damage = max(1, damage)
            actual_damage, blocked = target.take_damage(damage)
            return {'type': 'damage', 'value': actual_damage, 'blocked': blocked}, "success"
        
        elif spell.spell_type == 'heal':
            heal_amount = spell.heal_power + random.randint(-1, 2)
            actual_heal = self.heal(heal_amount)
            return {'type': 'heal', 'value': actual_heal}, "success"
        
        return None, "invalid_spell"
    
    def rest(self):
        """Rest to recover mana."""
        recovered = min(self.max_mana - self.current_mana, self.mana_regen)
        self.current_mana += recovered
        return recovered
    
    def get_status(self):
        """Get player status as dictionary."""
        return {
            'name': self.name,
            'hp': self.current_hp,
            'max_hp': self.max_hp,
            'mana': self.current_mana,
            'max_mana': self.max_mana,
            'is_defending': self.is_defending
        }


class Enemy(Entity):
    """Enemy character with AI behavior."""
    
    def __init__(self, name, max_hp, attack_power, heal_chance=0.2, heal_power=10):
        super().__init__(name, max_hp, attack_power)
        self.heal_chance = heal_chance
        self.heal_power = heal_power
    
    def ai_action(self, target):
        """
        AI decides what action to take.
        
        Returns:
            tuple: (action_type, result_dict)
                action_type: 'attack', 'heal', or 'defend'
                result_dict: details about the action
        """
        # Low health - chance to heal or defend
        if self.current_hp < self.max_hp * 0.3:
            if random.random() < self.heal_chance:
                heal_amount = self.heal(self.heal_power)
                return 'heal', {'value': heal_amount}
            elif random.random() < 0.5:
                self.defend()
                return 'defend', {}
        
        # Normal attack
        damage, blocked = self.basic_attack(target)
        return 'attack', {'damage': damage, 'blocked': blocked}


# Predefined spells
DEFAULT_SPELLS = [
    Spell("Fireball", power=15, mana_cost=10, spell_type='damage'),
    Spell("Ice Bolt", power=10, mana_cost=6, spell_type='damage'),
    Spell("Lightning Strike", power=20, mana_cost=15, spell_type='damage'),
    Spell("Heal", power=0, mana_cost=8, spell_type='heal', heal_power=15),
    Spell("Greater Heal", power=0, mana_cost=15, spell_type='heal', heal_power=30),
    Spell("Magic Missile", power=8, mana_cost=4, spell_type='damage'),
]

# Predefined enemies
ENEMY_TYPES = [
    {"name": "Goblin", "max_hp": 40, "attack_power": 8},
    {"name": "Orc", "max_hp": 60, "attack_power": 12},
    {"name": "Dark Mage", "max_hp": 35, "attack_power": 15, "heal_chance": 0.3, "heal_power": 12},
    {"name": "Dragon", "max_hp": 100, "attack_power": 18},
    {"name": "Skeleton Warrior", "max_hp": 45, "attack_power": 10},
    {"name": "Demon", "max_hp": 70, "attack_power": 14, "heal_chance": 0.15, "heal_power": 8},
]
