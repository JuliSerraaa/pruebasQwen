"""
Language translations for the spell casting simulator.
Supports English and Spanish.
"""

TRANSLATIONS = {
    'en': {
        'game_title': "Spell Casting Simulator",
        'player_turn': "Player's Turn",
        'enemy_turn': "Enemy's Turn",
        'choose_spell': "Choose a spell to cast:",
        'spell_name': "Spell",
        'spell_power': "Power",
        'spell_mana_cost': "Mana Cost",
        'invalid_choice': "Invalid choice! Please select a valid spell.",
        'not_enough_mana': "Not enough mana to cast this spell!",
        'cast_spell': "{player} casts {spell}!",
        'damage_dealt': "Dealt {damage} damage to {target}!",
        'heal_done': "{player} healed for {heal} HP!",
        'enemy_defeated': "{enemy} has been defeated!",
        'player_defeated': "You have been defeated! Game Over.",
        'victory': "Victory! You defeated all enemies!",
        'new_enemy_appears': "A wild {enemy} appears!",
        'player_hp': "Your HP: {hp}/{max_hp}",
        'player_mana': "Your Mana: {mana}/{max_mana}",
        'enemy_hp': "{enemy} HP: {hp}/{max_hp}",
        'attack': "Attack",
        'defend': "Defend",
        'rest': "Rest (recover mana)",
        'enemy_attacks': "{enemy} attacks you for {damage} damage!",
        'enemy_heals': "{enemy} heals for {heal} HP!",
        'blocked_damage': "Damage blocked by shield!",
        'mana_recovered': "Recovered {mana} mana!",
        'game_over': "Game Over",
        'play_again': "Do you want to play again? (y/n): ",
        'invalid_yes_no': "Please enter 'y' or 'n'.",
        'shield_active': "Shield active! Next attack will be blocked.",
        'no_enemies_left': "No enemies left to fight!",
    },
    'es': {
        'game_title': "Simulador de Lanzamiento de Hechizos",
        'player_turn': "Turno del Jugador",
        'enemy_turn': "Turno del Enemigo",
        'choose_spell': "Elige un hechizo para lanzar:",
        'spell_name': "Hechizo",
        'spell_power': "Poder",
        'spell_mana_cost': "Coste de Maná",
        'invalid_choice': "¡Opción inválida! Por favor selecciona un hechizo válido.",
        'not_enough_mana': "¡No tienes suficiente maná para lanzar este hechizo!",
        'cast_spell': "¡{player} lanza {spell}!",
        'damage_dealt': "¡Causó {damage} de daño a {target}!",
        'heal_done': "¡{player} se curó {heal} de vida!",
        'enemy_defeated': "¡{enemy} ha sido derrotado!",
        'player_defeated': "¡Has sido derrotado! Fin del juego.",
        'victory': "¡Victoria! ¡Derrotaste a todos los enemigos!",
        'new_enemy_appears': "¡Un {enemy} salvaje aparece!",
        'player_hp': "Tu vida: {hp}/{max_hp}",
        'player_mana': "Tu maná: {mana}/{max_mana}",
        'enemy_hp': "{enemy} vida: {hp}/{max_hp}",
        'attack': "Atacar",
        'defend': "Defender",
        'rest': "Descansar (recuperar maná)",
        'enemy_attacks': "¡{enemy} te ataca causando {damage} de daño!",
        'enemy_heals': "¡{enemy} se cura {heal} de vida!",
        'blocked_damage': "¡Daño bloqueado por el escudo!",
        'mana_recovered': "¡Recuperaste {mana} de maná!",
        'game_over': "Fin del juego",
        'play_again': "¿Quieres jugar de nuevo? (s/n): ",
        'invalid_yes_no': "Por favor ingresa 's' o 'n'.",
        'shield_active': "¡Escudo activo! El próximo ataque será bloqueado.",
        'no_enemies_left': "¡No quedan enemigos para luchar!",
    }
}

def get_text(key, lang='en'):
    """Get translated text for a given key."""
    if lang not in TRANSLATIONS:
        lang = 'en'
    return TRANSLATIONS[lang].get(key, f"[Missing: {key}]")

def get_supported_languages():
    """Return list of supported language codes."""
    return list(TRANSLATIONS.keys())
