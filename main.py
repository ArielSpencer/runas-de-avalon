from random import randint

npc_list = []

player = {
    "name": "Player",
    "level": 1,
    "exp": 0,
    "exp_max": 30,
    "hp": 100,
    "hp_max": 100,
    "damage": 25,
}

def create_npc(level):
    new_npc = {
        "name": f"NPC #{level}",
        "level": level,
        "damage": 5 * level,
        "hp": 100 * level,
        "hp_max": 100 * level,
        "exp": 7 * level,
    }
    return new_npc

def generate_npcs(n_npcs):
    for x in range(n_npcs):
        new_npc = create_npc(x + 1)
        npc_list.append(new_npc)

def display_npcs():
    for npc in npc_list:
        display_npc(npc)

def display_npc(npc):
    print(
        f"Nome: {npc['name']} // Level: {npc['level']} // Dano: {npc['damage']} // HP: {npc['hp']} // Exp: {npc['exp']}"
    )

def display_player():
    print(
        f"Nome: {player['name']} // Level: {player['level']} // Dano: {player['damage']} // HP: {player['hp']}/{player['hp_max']} // Exp: {player['exp']}/{player['exp_max']}"
    )

def reset_player():
    player["hp"] = player["hp_max"]

def reset_npc(npc):
    npc["hp"] = npc["hp_max"]

def level_up():
    if player["exp"] >= player["exp_max"]:
        player["level"] += 1
        player["exp"] = 0
        print("Level UP!")

def start_battle(npc):
    while player["hp"] > 0 and npc["hp"] > 0:
        attack_npc(npc)
        attack_player(npc)
        display_battle_info(npc)

    if player["hp"] > 0:
        print(f"Player venceu! + {npc['exp']} de EXP")
        player["exp"] += npc["exp"]
        display_player()
    else:
        print(f"{npc['name']} venceu!")

    level_up()

    reset_player()
    reset_npc(npc)

def attack_npc(npc):
    npc["hp"] -= player["damage"]

def attack_player(npc):
    player["hp"] -= npc["damage"]

def display_battle_info(npc):
    print(f"Player: {player['hp']}/{player['hp_max']}")
    print(f"{npc['name']}: {npc['hp']}/{npc['hp_max']}")
    print("-----------------------------\n")

generate_npcs(3)

selected_npc = npc_list[0]
start_battle(selected_npc)

display_player()