from models.constants import PLAYER_CLASSES

player = {
    "name": "Player",
    "level": 1,
    "exp": 0,
    "exp_max": 30,
    "hp": 100,
    "hp_max": 100,
    "damage": 25,
    "critical_chance": 0.15,
    "coins": 0,
    "shop_needs_refresh": True,
    "shop_last_refresh": 0,
    "difficulty": "Normal",
    "total_battles": 0,
    "total_victories": 0,
    "total_critical_hits": 0,
    "highest_damage": 0,
}

def create_player(name, player_class, difficulty="Normal"):
    if player_class not in PLAYER_CLASSES:
        player_class = "Guerreiro"

    new_player = {
        "name": name,
        "class": player_class,
        "level": 1,
        "exp": 0,
        "exp_max": 30,
        "hp_max": PLAYER_CLASSES[player_class]["hp_max"],
        "damage": PLAYER_CLASSES[player_class]["damage"],
        "critical_chance": PLAYER_CLASSES[player_class]["critical_chance"],
        "coins": 0,
        "shop_needs_refresh": True,
        "shop_last_refresh": 0,
        "difficulty": difficulty,
        "total_battles": 0,
        "total_victories": 0,
        "total_critical_hits": 0,
        "highest_damage": 0,
        "temp_effects": {},
    }

    new_player["hp"] = new_player["hp_max"]
    
    return new_player

def set_player(new_player):
    global player
    player.clear()
    for key, value in new_player.items():
        player[key] = value

def show_player():
    class_info = f" // Classe: {player['class']}" if 'class' in player else ""
    difficulty_info = f" // Dificuldade: {player.get('difficulty', 'Normal')}"
    print(f"Player: Nome: {player['name']}{class_info}{difficulty_info} // Level: {player['level']}")
    
    critical_percent = int(player.get('critical_chance', 0) * 100)
    print(f"Status: Dano: {player['damage']} // HP: {player['hp']}/{player['hp_max']} // Crítico: {critical_percent}%")
    print(f"Exp: {player['exp']}/{player['exp_max']} // Moedas: {player.get('coins', 0)}")
    
    if player.get('temp_effects'):
        print("Efeitos ativos:")
        for effect, duration in player['temp_effects'].items():
            print(f"  {effect}: {duration} batalhas restantes")

def reset_player(player):
    player["hp"] = player["hp_max"]
    bonus_hp = player["hp_max"] // 10
    if player["hp"] + bonus_hp <= player["hp_max"]:
        player["hp"] += bonus_hp

def level_up(player):
    if player["exp"] >= player["exp_max"]:
        player["level"] += 1
        player["exp"] = player["exp"] - player["exp_max"]
        player["exp_max"] = int(player["exp_max"] * 1.4)
        player["hp"] = player["hp_max"]
        return True
    return False

def apply_level_bonus(player):
    player_class = player.get("class", "")
    player_level = player["level"]
    
    if player_class == "Guerreiro":
        hp_bonus = int(40 + (player_level * 6))
        dmg_bonus = int(14 + (player_level * 2.5))
        crit_bonus = 0.01
        desc = f"Resistência do Guerreiro: HP +{hp_bonus}, Dano +{dmg_bonus}, Crítico +{int(crit_bonus*100)}%"
    
    elif player_class == "Mago":
        hp_bonus = int(25 + (player_level * 4))
        dmg_bonus = int(22 + (player_level * 3.5))
        crit_bonus = 0.02
        desc = f"Poder Arcano: HP +{hp_bonus}, Dano +{dmg_bonus}, Crítico +{int(crit_bonus*100)}%"
    
    elif player_class == "Arqueiro":
        hp_bonus = int(30 + (player_level * 5))
        dmg_bonus = int(18 + (player_level * 3))
        crit_bonus = 0.015
        desc = f"Precisão e Agilidade: HP +{hp_bonus}, Dano +{dmg_bonus}, Crítico +{int(crit_bonus*100)}%"
    
    elif player_class == "Assassino":
        hp_bonus = int(20 + (player_level * 3))
        dmg_bonus = int(20 + (player_level * 3))
        crit_bonus = 0.025
        desc = f"Arte Letal: HP +{hp_bonus}, Dano +{dmg_bonus}, Crítico +{int(crit_bonus*100)}%"
    
    elif player_class == "Paladino":
        hp_bonus = int(50 + (player_level * 7))
        dmg_bonus = int(10 + (player_level * 1.5))
        crit_bonus = 0.005
        desc = f"Bênção Divina: HP +{hp_bonus}, Dano +{dmg_bonus}, Crítico +{int(crit_bonus*100)}%"
    
    else:
        hp_bonus = int(30 + (player_level * 5))
        dmg_bonus = int(15 + (player_level * 2.5))
        crit_bonus = 0.01
        desc = f"Atributos Básicos: HP +{hp_bonus}, Dano +{dmg_bonus}, Crítico +{int(crit_bonus*100)}%"
    
    player["hp_max"] += hp_bonus
    player["hp"] += hp_bonus
    player["damage"] += dmg_bonus
    player["critical_chance"] += crit_bonus
    
    if player_level % 3 == 0:
        special_hp = int(60 + (player_level * 6))
        special_dmg = int(30 + (player_level * 3))
        special_crit = 0.02
        player["hp_max"] += special_hp
        player["hp"] += special_hp
        player["damage"] += special_dmg
        player["critical_chance"] += special_crit
        desc += f" + BÔNUS ESPECIAL: HP +{special_hp}, Dano +{special_dmg}, Crítico +{int(special_crit*100)}%"
    
    player["hp_max"] += 15
    player["hp"] += 15
    player["damage"] += 8
    player["critical_chance"] += 0.005
    
    return desc

def update_player_stats(player, damage_dealt, was_critical):
    player["total_battles"] = player.get("total_battles", 0) + 1
    
    if damage_dealt > player.get("highest_damage", 0):
        player["highest_damage"] = damage_dealt
    
    if was_critical:
        player["total_critical_hits"] = player.get("total_critical_hits", 0) + 1

def update_temp_effects(player):
    if "temp_effects" not in player:
        player["temp_effects"] = {}
    
    effects_to_remove = []
    for effect, duration in player["temp_effects"].items():
        duration -= 1
        if duration <= 0:
            effects_to_remove.append(effect)
        else:
            player["temp_effects"][effect] = duration
    
    for effect in effects_to_remove:
        del player["temp_effects"][effect]

def get_effective_stats(player):
    base_damage = player["damage"]
    base_hp_max = player["hp_max"]
    base_critical_chance = player["critical_chance"]
    
    if "temp_effects" in player:
        base_damage += player["temp_effects"].get("damage_temp", 0)
        base_critical_chance += player["temp_effects"].get("critical_chance_temp", 0)
    
    return {
        "damage": base_damage,
        "hp_max": base_hp_max,
        "critical_chance": min(base_critical_chance, 0.95)
    }