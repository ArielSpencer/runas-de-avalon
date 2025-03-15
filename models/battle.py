from models.player import reset_player, level_up
from models.npc import reset_npc

def attack_npc(npc, player):
    npc["hp"] -= player["damage"]
    
def attack_player(npc, player):
    player["hp"] -= npc["damage"]

def display_battle_info(npc, player):
    print(f"Player: {player['hp']}/{player['hp_max']}")
    print(f"{npc['name']}: {npc['hp']}/{npc['hp_max']}")
    print("-----------------------------\n")

def start_battle(player, npc):
    while player["hp"] > 0 and npc["hp"] > 0:
        attack_npc(npc, player)
        attack_player(npc, player)
        display_battle_info(npc, player)

    if player["hp"] > 0:
        print(f"Player venceu! + {npc['exp']} de EXP")
        player["exp"] += npc["exp"]
    else:
        print(f"{npc['name']} venceu!")
    
    level_up(player)
    reset_player(player)
    reset_npc(npc)