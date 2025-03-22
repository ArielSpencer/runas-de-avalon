player_classes = {
    "Guerreiro": {
        "hp_max": 120,
        "damage": 20,
        "description": "Forte e resistente, o Guerreiro tem mais HP mas causa menos dano."
    },
    "Mago": {
        "hp_max": 80,
        "damage": 35,
        "description": "Frágil mas poderoso, o Mago causa mais dano mas tem menos HP."
    },
    "Arqueiro": {
        "hp_max": 100,
        "damage": 25,
        "description": "Balanceado, o Arqueiro tem atributos medianos."
    }
}

player = {
    "name": "Player",
    "level": 1,
    "exp": 0,
    "exp_max": 30,
    "hp": 100,
    "hp_max": 100,
    "damage": 25,
}

def create_player(name, player_class):

    if player_class not in player_classes:
        player_class = "Guerreiro"

    new_player = {
        "name": name,
        "class": player_class,
        "level": 1,
        "exp": 0,
        "exp_max": 30,
        "hp_max": player_classes[player_class]["hp_max"],
        "damage": player_classes[player_class]["damage"],
    }

    new_player["hp"] = new_player["hp_max"]
    
    return new_player

def set_player(new_player):
    global player
    player = new_player

def show_player():
    print(f"Nome: {player['name']} // Classe: {player['class']} // Level: {player['level']} // Dano: {player['damage']} // HP: {player['hp']}/{player['hp_max']} // Exp: {player['exp']}/{player['exp_max']}")

def reset_player(player):
    player["hp"] = player["hp_max"]

def level_up(player):
    if player["exp"] >= player["exp_max"]:
        player["level"] += 1
        player["exp"] = 0
        print("Level UP!")