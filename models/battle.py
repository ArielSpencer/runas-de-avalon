from models.player import reset_player, level_up
from models.npc import reset_npc
from models.shop import mark_shop_refresh_needed

def attack_npc(npc, player):
    damage = player["damage"]
    npc["hp"] -= damage
    if npc["hp"] < 0:
        npc["hp"] = 0
    return damage
    
def attack_player(npc, player):
    damage = npc["damage"]
    player["hp"] -= damage
    if player["hp"] < 0:
        player["hp"] = 0
    return damage

def display_battle_state(battle_state):
    print(f"{battle_state['player_name']}: hp {battle_state['player_hp']}/{battle_state['player_hp_max']} || {battle_state['npc_name']}: hp {battle_state['npc_hp']}/{battle_state['npc_hp_max']}")

def end_battle(player, npc, won):
    print("\n-----------------------------")
    
    if won:
        print("\n=== VITÓRIA! ===")
        print(f"{player.get('name', 'Player')} venceu {npc['name']}! + {npc['exp']} de EXP")
        
        old_level = player["level"]
        old_exp = player["exp"]
        old_exp_max = player["exp_max"]
        
        player["exp"] += npc["exp"]
        
        leveled_up = level_up(player)
        
        if leveled_up:
            print(f"Experiência: {old_exp}/{old_exp_max} -> {player['exp']}/{player['exp_max']}")
            print(f"Nível: {old_level} -> {player['level']}")
        else:
            print(f"Experiência: {old_exp}/{old_exp_max} -> {player['exp']}/{player['exp_max']}")
        
        mark_shop_refresh_needed(player)
        print("\n📦 A loja foi reabastecida com novos itens!")
    else:
        print("\n=== DERROTA ===")
        print(f"{npc['name']} venceu {player.get('name', 'Player')}!")
    
    reset_player(player)
    reset_npc(npc)
    
    return won

def start_battle(player, npc):
    print(f"Iniciando batalha contra {npc['name']}!\n")
    
    battle_log = []
    round_count = 1
    
    while player["hp"] > 0 and npc["hp"] > 0:
        print(f"Rodada {round_count}:")
        
        print(f"- {player.get('name', 'Player')} ataca {npc['name']}!")
        player_damage = attack_npc(npc, player)
        print(f"  Causou {player_damage} de dano!")
        
        battle_state = {
            "player_name": player.get('name', 'Player'),
            "player_hp": player["hp"],
            "player_hp_max": player["hp_max"],
            "npc_name": npc['name'],
            "npc_hp": npc["hp"],
            "npc_hp_max": npc["hp_max"]
        }
        display_battle_state(battle_state)
        battle_log.append(battle_state)
        
        if npc["hp"] <= 0:
            break
            
        print(f"- {npc['name']} ataca {player.get('name', 'Player')}!")
        npc_damage = attack_player(npc, player)
        print(f"  Causou {npc_damage} de dano!")
        
        battle_state = {
            "player_name": player.get('name', 'Player'),
            "player_hp": player["hp"],
            "player_hp_max": player["hp_max"],
            "npc_name": npc['name'],
            "npc_hp": npc["hp"],
            "npc_hp_max": npc["hp_max"]
        }
        display_battle_state(battle_state)
        battle_log.append(battle_state)
        
        print("")
        round_count += 1
    
    won = player["hp"] > 0
    return end_battle(player, npc, won)