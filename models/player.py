from models.constants import PLAYER_CLASSES

player = {
    "name": "Player",
    "level": 1,
    "exp": 0,
    "exp_max": 30,
    "hp": 100,
    "hp_max": 100,
    "damage": 25,
    "coins": 0,
}

def create_player(name, player_class):
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
        "coins": 0,
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
    print(f"Nome: {player['name']}{class_info} // Level: {player['level']} // Dano: {player['damage']} // HP: {player['hp']}/{player['hp_max']} // Exp: {player['exp']}/{player['exp_max']}")

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
        hp_bonus = int(35 + (player_level * 5))
        dmg_bonus = int(12 + (player_level * 2))
        desc = f"Resistência do Guerreiro: HP Máximo +{hp_bonus}, Dano +{dmg_bonus}"
    
    elif player_class == "Mago":
        hp_bonus = int(20 + (player_level * 3))
        dmg_bonus = int(20 + (player_level * 3))
        desc = f"Poder Arcano: HP Máximo +{hp_bonus}, Dano +{dmg_bonus}"
    
    elif player_class == "Arqueiro":
        hp_bonus = int(25 + (player_level * 4))
        dmg_bonus = int(15 + (player_level * 2.5))
        desc = f"Precisão e Agilidade: HP Máximo +{hp_bonus}, Dano +{dmg_bonus}"
    
    else:
        hp_bonus = int(25 + (player_level * 4))
        dmg_bonus = int(15 + (player_level * 2))
        desc = f"Atributos Básicos: HP Máximo +{hp_bonus}, Dano +{dmg_bonus}"
    
    player["hp_max"] += hp_bonus
    player["hp"] += hp_bonus
    player["damage"] += dmg_bonus
    
    if player_level % 3 == 0:
        special_hp = int(50 + (player_level * 5))
        special_dmg = int(25 + (player_level * 2))
        player["hp_max"] += special_hp
        player["hp"] += special_hp
        player["damage"] += special_dmg
        desc += f" + BÔNUS ESPECIAL: HP Máximo +{special_hp}, Dano +{special_dmg}"
    
    player["hp_max"] += 10
    player["hp"] += 10
    player["damage"] += 5
    
    return desc