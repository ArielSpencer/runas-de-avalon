import random
from models.player import reset_player, level_up, update_player_stats, update_temp_effects, get_effective_stats
from models.npc import reset_npc
from models.shop import mark_shop_refresh_needed
from models.constants import DIFFICULTY_SETTINGS
from models.achievements import check_achievements, apply_achievement_rewards, display_achievement_notification, update_achievement_progress

def calculate_critical_damage(base_damage, critical_chance):
    if random.random() <= critical_chance:
        critical_multiplier = random.uniform(1.5, 2.5)
        critical_damage = int(base_damage * critical_multiplier)
        return critical_damage, True
    return base_damage, False

def attack_npc(npc, player):
    stats = get_effective_stats(player)
    base_damage = stats["damage"]
    critical_chance = stats["critical_chance"]
    
    damage, is_critical = calculate_critical_damage(base_damage, critical_chance)
    
    npc["hp"] -= damage
    if npc["hp"] < 0:
        npc["hp"] = 0
    
    update_player_stats(player, damage, is_critical)
    
    if is_critical:
        newly_unlocked = update_achievement_progress(player, "critical")
        if newly_unlocked:
            for achievement_id in newly_unlocked:
                print(f"\n🎉 CONQUISTA DESBLOQUEADA: {achievement_id}")
    
    return damage, is_critical
    
def attack_player(npc, player):
    base_damage = npc["damage"]
    
    damage_variance = random.uniform(0.8, 1.2)
    damage = int(base_damage * damage_variance)
    
    npc_critical_chance = 0.05 + (npc["level"] * 0.01)
    damage, is_critical = calculate_critical_damage(damage, npc_critical_chance)
    
    player["hp"] -= damage
    if player["hp"] < 0:
        player["hp"] = 0
    
    return damage, is_critical

def display_battle_state(battle_state):
    print(f"{battle_state['player_name']}: hp {battle_state['player_hp']}/{battle_state['player_hp_max']} || {battle_state['npc_name']}: hp {battle_state['npc_hp']}/{battle_state['npc_hp_max']}")

def apply_difficulty_modifiers(player, npc, exp_gained, coins_gained):
    difficulty = player.get("difficulty", "Normal")
    modifiers = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["Normal"])
    
    modified_exp = int(exp_gained * modifiers["exp_multiplier"])
    modified_coins = int(coins_gained * modifiers["coin_multiplier"])
    
    return modified_exp, modified_coins

def end_battle(player, npc, won):
    print("\n-----------------------------")
    
    if won:
        print("\n=== VITÓRIA! ===")
        
        base_exp = npc["exp"]
        base_coins = random.randint(3, 8) * npc["level"]
        
        exp_multiplier = player.get("temp_effects", {}).get("exp_multiplier", 1.0)
        modified_exp = int(base_exp * exp_multiplier)
        
        modified_exp, modified_coins = apply_difficulty_modifiers(player, npc, modified_exp, base_coins)
        
        print(f"{player.get('name', 'Player')} venceu {npc['name']}!")
        print(f"Experiência ganha: +{modified_exp}")
        print(f"Moedas ganhas: +{modified_coins}")
        
        if exp_multiplier > 1.0:
            print(f"🌟 BÔNUS DE EXPERIÊNCIA ATIVO! (x{exp_multiplier})")
        
        old_level = player["level"]
        old_exp = player["exp"]
        old_exp_max = player["exp_max"]
        
        player["exp"] += modified_exp
        player["coins"] = player.get("coins", 0) + modified_coins
        player["total_victories"] = player.get("total_victories", 0) + 1
        
        if npc.get("is_boss", False):
            newly_unlocked = update_achievement_progress(player, "boss_defeat")
        else:
            newly_unlocked = update_achievement_progress(player, "victory")
        
        for achievement_id in newly_unlocked:
            display_achievement_notification(achievement_id)
            rewards = apply_achievement_rewards(player, [achievement_id])
            print("🎁 Recompensas aplicadas automaticamente!")
            print("Pressione Enter para continuar...")
            input()
        
        leveled_up = level_up(player)
        
        if leveled_up:
            print(f"Experiência: {old_exp}/{old_exp_max} -> {player['exp']}/{player['exp_max']}")
            print(f"🎉 LEVEL UP! Nível: {old_level} -> {player['level']}")
            
            level_achievements = check_achievements(player)
            if level_achievements:
                for achievement_id in level_achievements:
                    display_achievement_notification(achievement_id)
                    rewards = apply_achievement_rewards(player, [achievement_id])
                    print("Pressione Enter para continuar...")
                    input()
        else:
            print(f"Experiência: {old_exp}/{old_exp_max} -> {player['exp']}/{player['exp_max']}")
        
        update_temp_effects(player)
        
        mark_shop_refresh_needed(player)
        print("\n📦 A loja foi reabastecida com novos itens!")
    else:
        print("\n=== DERROTA ===")
        print(f"{npc['name']} venceu {player.get('name', 'Player')}!")
        
        coins_lost = min(player.get("coins", 0), random.randint(5, 15))
        if coins_lost > 0:
            player["coins"] -= coins_lost
            print(f"💰 Você perdeu {coins_lost} moedas!")
    
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
        player_damage, player_critical = attack_npc(npc, player)
        
        if player_critical:
            print(f"  💥 CRÍTICO! Causou {player_damage} de dano!")
        else:
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
        npc_damage, npc_critical = attack_player(npc, player)
        
        if npc_critical:
            print(f"  💥 CRÍTICO INIMIGO! Causou {npc_damage} de dano!")
        else:
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