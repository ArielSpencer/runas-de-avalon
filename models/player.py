player = {
    "name": "Player",
    "level": 1,
    "exp": 0,
    "exp_max": 30,
    "hp": 100,
    "hp_max": 100,
    "damage": 25,
}

def show_player():
    print(f"Nome: {player['name']} // Level: {player['level']} // Dano: {player['damage']} // HP: {player['hp']}/{player['hp_max']} // Exp: {player['exp']}/{player['exp_max']}")

def reset_player(player):
    player["hp"] = player["hp_max"]

def level_up(player):
    if player["exp"] >= player["exp_max"]:
        player["level"] += 1
        player["exp"] = 0
        print("Level UP!")