from models.ui import clear_screen, display_logo

ACHIEVEMENTS = {
    "first_victory": {
        "name": "🏆 Primeira Vitória",
        "description": "Vença sua primeira batalha",
        "condition": lambda player: player.get("total_victories", 0) >= 1,
        "reward": {"coins": 50},
        "secret": False
    },
    "critical_master": {
        "name": "💥 Mestre dos Críticos", 
        "description": "Cause 25 ataques críticos",
        "condition": lambda player: player.get("total_critical_hits", 0) >= 25,
        "reward": {"coins": 150, "exp": 100},
        "secret": False
    },
    "coin_collector": {
        "name": "💰 Colecionador de Moedas",
        "description": "Acumule 1000 moedas",
        "condition": lambda player: player.get("coins", 0) >= 1000,
        "reward": {"critical_chance": 0.05},
        "secret": False
    },
    "level_10": {
        "name": "⭐ Veterano",
        "description": "Alcance o nível 10",
        "condition": lambda player: player.get("level", 1) >= 10,
        "reward": {"hp_max": 100, "damage": 25},
        "secret": False
    },
    "perfectionist": {
        "name": "🎯 Perfeccionista",
        "description": "Complete o jogo sem morrer",
        "condition": lambda player: player.get("total_victories", 0) >= 20 and player.get("total_battles", 0) == player.get("total_victories", 0),
        "reward": {"coins": 500, "damage": 50},
        "secret": False
    },
    "insane_warrior": {
        "name": "🔥 Guerreiro Insano",
        "description": "Complete o jogo na dificuldade Insano",
        "condition": lambda player: player.get("game_completed", False) and player.get("difficulty") == "Insano",
        "reward": {"hp_max": 200, "damage": 75, "critical_chance": 0.1},
        "secret": False
    },
    "damage_dealer": {
        "name": "⚔️ Devastador",
        "description": "Cause 500 pontos de dano em um único ataque",
        "condition": lambda player: player.get("highest_damage", 0) >= 500,
        "reward": {"damage": 30},
        "secret": False
    },
    "boss_slayer": {
        "name": "👹 Matador de Bosses",
        "description": "Derrote todos os 4 bosses",
        "condition": lambda player: player.get("bosses_defeated", 0) >= 4,
        "reward": {"coins": 300, "hp_max": 75},
        "secret": False
    },
    "lucky_finder": {
        "name": "🍀 Sortudo",
        "description": "Encontre 5 itens lendários",
        "condition": lambda player: player.get("legendary_items_found", 0) >= 5,
        "reward": {"coins": 400},
        "secret": True
    },
    "shopaholic": {
        "name": "🛍️ Comprador Compulsivo",
        "description": "Compre 20 itens na loja",
        "condition": lambda player: player.get("items_purchased", 0) >= 20,
        "reward": {"coins": 200},
        "secret": True
    },
    "speed_runner": {
        "name": "⚡ Corredor Veloz",
        "description": "Complete o jogo em menos de 50 batalhas totais",
        "condition": lambda player: player.get("game_completed", False) and player.get("total_battles", 999) <= 50,
        "reward": {"damage": 40, "critical_chance": 0.08},
        "secret": True
    },
    "treasure_hunter": {
        "name": "💎 Caçador de Tesouros",
        "description": "Acumule 2000 moedas em uma única aventura",
        "condition": lambda player: player.get("coins", 0) >= 2000,
        "reward": {"hp_max": 150},
        "secret": True
    },
    "undying": {
        "name": "🛡️ Imortal",
        "description": "Alcance o nível 15 sem morrer",
        "condition": lambda player: player.get("level", 1) >= 15 and player.get("total_battles", 0) == player.get("total_victories", 0),
        "reward": {"hp_max": 250, "damage": 60},
        "secret": True
    },
    "rune_master": {
        "name": "🔮 Mestre das Runas",
        "description": "Use 15 itens consumíveis",
        "condition": lambda player: player.get("consumables_used", 0) >= 15,
        "reward": {"critical_chance": 0.07},
        "secret": True
    }
}

def check_achievements(player):
    if "achievements" not in player:
        player["achievements"] = {}
    
    newly_unlocked = []
    
    for achievement_id, achievement in ACHIEVEMENTS.items():
        if achievement_id not in player["achievements"]:
            if achievement["condition"](player):
                player["achievements"][achievement_id] = True
                newly_unlocked.append(achievement_id)
    
    return newly_unlocked

def apply_achievement_rewards(player, achievement_ids):
    total_rewards = {}
    
    for achievement_id in achievement_ids:
        achievement = ACHIEVEMENTS[achievement_id]
        rewards = achievement.get("reward", {})
        
        for reward_type, value in rewards.items():
            if reward_type in total_rewards:
                total_rewards[reward_type] += value
            else:
                total_rewards[reward_type] = value
    
    for reward_type, value in total_rewards.items():
        if reward_type in player:
            player[reward_type] += value
        else:
            player[reward_type] = value
    
    return total_rewards

def display_achievement_notification(achievement_id):
    achievement = ACHIEVEMENTS[achievement_id]
    
    print("\n" + "═" * 50)
    print("🎉 CONQUISTA DESBLOQUEADA! 🎉")
    print("═" * 50)
    print(f"{achievement['name']}")
    print(f"📝 {achievement['description']}")
    
    rewards = achievement.get("reward", {})
    if rewards:
        print("\n🎁 Recompensas:")
        for reward_type, value in rewards.items():
            if reward_type == "coins":
                print(f"  💰 +{value} moedas")
            elif reward_type == "hp_max":
                print(f"  ❤️ +{value} HP máximo")
            elif reward_type == "damage":
                print(f"  ⚔️ +{value} dano")
            elif reward_type == "critical_chance":
                print(f"  💥 +{int(value*100)}% chance de crítico")
            elif reward_type == "exp":
                print(f"  📈 +{value} experiência")
    
    print("═" * 50)

def display_achievements_menu(player):
    while True:
        clear_screen()
        display_logo()
        print("\n🏆 === CONQUISTAS === 🏆")
        
        if "achievements" not in player:
            player["achievements"] = {}
        
        unlocked_count = len(player["achievements"])
        total_count = len(ACHIEVEMENTS)
        completion_rate = (unlocked_count / total_count) * 100
        
        print(f"\n📊 Progresso: {unlocked_count}/{total_count} ({completion_rate:.1f}%)")
        
        from models.ui import display_progress_bar
        display_progress_bar(unlocked_count, total_count, "Conquistas")
        
        print("\n🎯 CONQUISTAS PÚBLICAS:")
        public_achievements = {k: v for k, v in ACHIEVEMENTS.items() if not v.get("secret", False)}
        
        for achievement_id, achievement in public_achievements.items():
            status = "✅" if achievement_id in player["achievements"] else "❌"
            print(f"{status} {achievement['name']} - {achievement['description']}")
        
        unlocked_secrets = [k for k in player["achievements"].keys() if ACHIEVEMENTS[k].get("secret", False)]
        
        if unlocked_secrets:
            print("\n🔓 CONQUISTAS SECRETAS DESBLOQUEADAS:")
            for achievement_id in unlocked_secrets:
                achievement = ACHIEVEMENTS[achievement_id]
                print(f"✅ {achievement['name']} - {achievement['description']}")
        
        remaining_secrets = len([k for k, v in ACHIEVEMENTS.items() if v.get("secret", False)]) - len(unlocked_secrets)
        if remaining_secrets > 0:
            print(f"\n🔒 {remaining_secrets} conquistas secretas ainda não descobertas...")
        
        print("\n0. Voltar")
        choice = input("\nPressione Enter para voltar... ")
        
        if choice == '0' or choice == '':
            return

def get_achievement_points(player):
    if "achievements" not in player:
        return 0
    
    points = 0
    for achievement_id in player["achievements"]:
        achievement = ACHIEVEMENTS[achievement_id]
        if achievement.get("secret", False):
            points += 15
        else:
            points += 10
    
    return points

def update_achievement_progress(player, action, value=1):
    progress_mapping = {
        "victory": "total_victories",
        "critical": "total_critical_hits", 
        "boss_defeat": "bosses_defeated",
        "legendary_found": "legendary_items_found",
        "item_purchased": "items_purchased",
        "consumable_used": "consumables_used"
    }
    
    if action in progress_mapping:
        stat = progress_mapping[action]
        player[stat] = player.get(stat, 0) + value
        
        newly_unlocked = check_achievements(player)
        if newly_unlocked:
            return newly_unlocked
    
    return []