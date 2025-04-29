import random
from models.ui import clear_screen, display_logo
from models.inventory import add_to_inventory
from models.shop import apply_shop_discount

RANDOM_EVENTS = {
    "treasure_chest": {
        "name": "🎁 Baú do Tesouro",
        "description": "Você encontra um baú antigo brilhando com energia mágica!",
        "rarity": 0.15,
        "min_battle": 3,
        "effects": {
            "coins": (50, 200),
            "exp": (20, 80),
            "item_chance": 0.3
        }
    },
    "merchant": {
        "name": "🧙‍♂️ Comerciante Misterioso",
        "description": "Um comerciante encapuzado aparece do nada oferecendo seus serviços.",
        "rarity": 0.12,
        "min_battle": 2,
        "effects": {
            "shop_discount": 0.25,
            "free_item": 0.2
        }
    },
    "magic_fountain": {
        "name": "⛲ Fonte Mágica",
        "description": "Uma fonte cristalina emana energia curativa e revigorante.",
        "rarity": 0.10,
        "min_battle": 4,
        "effects": {
            "heal_percentage": 0.8,
            "temp_boost": True
        }
    },
    "ancient_shrine": {
        "name": "🏛️ Santuário Antigo",
        "description": "Um santuário esquecido pulsa com poder ancestral.",
        "rarity": 0.08,
        "min_battle": 6,
        "effects": {
            "permanent_boost": True,
            "blessing_duration": 5
        }
    },
    "cursed_artifact": {
        "name": "💀 Artefato Amaldiçoado",
        "description": "Um objeto sombrio sussurra promessas de poder... com um preço.",
        "rarity": 0.05,
        "min_battle": 8,
        "effects": {
            "curse_choice": True,
            "high_risk_reward": True
        }
    },
    "lost_traveler": {
        "name": "🚶‍♂️ Viajante Perdido",
        "description": "Um viajante desesperado implora por ajuda.",
        "rarity": 0.20,
        "min_battle": 1,
        "effects": {
            "karma_choice": True,
            "help_reward": (30, 100),
            "ignore_penalty": (10, 30)
        }
    },
    "meteor_shower": {
        "name": "☄️ Chuva de Meteoros",
        "description": "Meteoros caem do céu, deixando fragmentos mágicos para trás.",
        "rarity": 0.03,
        "min_battle": 10,
        "effects": {
            "rare_materials": True,
            "craft_bonus": True
        }
    },
    "time_rift": {
        "name": "🌀 Fenda Temporal",
        "description": "Uma fenda no tempo se abre, oferecendo vislumbres do futuro.",
        "rarity": 0.02,
        "min_battle": 15,
        "effects": {
            "preview_enemies": True,
            "exp_boost": 2.0,
            "future_knowledge": True
        }
    }
}

def should_trigger_random_event(battle_number, player_level):
    if battle_number < 2:
        return False
    
    base_chance = 0.15 + (battle_number * 0.01)
    
    if player_level >= 10:
        base_chance += 0.05
    if player_level >= 15:
        base_chance += 0.05
    
    return random.random() <= base_chance

def select_random_event(battle_number):
    eligible_events = []
    
    for event_id, event_data in RANDOM_EVENTS.items():
        if battle_number >= event_data["min_battle"]:
            rarity = event_data["rarity"]
            eligible_events.extend([event_id] * int(rarity * 100))
    
    if not eligible_events:
        return None
    
    return random.choice(eligible_events)

def execute_random_event(event_id, player):
    if event_id not in RANDOM_EVENTS:
        return False
    
    event = RANDOM_EVENTS[event_id]
    
    clear_screen()
    display_logo()
    print(f"\n🌟 === EVENTO ESPECIAL === 🌟")
    print(f"\n{event['name']}")
    print(f"{event['description']}")
    
    effects = event["effects"]
    
    if event_id == "treasure_chest":
        return handle_treasure_chest(effects, player)
    elif event_id == "merchant":
        return handle_merchant(effects, player)
    elif event_id == "magic_fountain":
        return handle_magic_fountain(effects, player)
    elif event_id == "ancient_shrine":
        return handle_ancient_shrine(effects, player)
    elif event_id == "cursed_artifact":
        return handle_cursed_artifact(effects, player)
    elif event_id == "lost_traveler":
        return handle_lost_traveler(effects, player)
    elif event_id == "meteor_shower":
        return handle_meteor_shower(effects, player)
    elif event_id == "time_rift":
        return handle_time_rift(effects, player)
    
    return False

def handle_treasure_chest(effects, player):
    print("\n🔓 Você abre o baú misterioso...")
    
    coins_range = effects["coins"]
    exp_range = effects["exp"]
    
    coins_found = random.randint(*coins_range)
    exp_found = random.randint(*exp_range)
    
    player["coins"] = player.get("coins", 0) + coins_found
    player["exp"] = player.get("exp", 0) + exp_found
    
    print(f"💰 Você encontrou {coins_found} moedas!")
    print(f"📈 Você ganhou {exp_found} de experiência!")
    
    if random.random() <= effects["item_chance"]:
        from models.inventory import drop_item
        random_item = drop_item(player.get("class", "Guerreiro"))
        if random_item:
            add_to_inventory(random_item)
            print(f"🎁 Você também encontrou: {random_item['name']}!")
    
    print("\nPressione Enter para continuar...")
    input()
    return True

def handle_merchant(effects, player):
    print("\n💼 O comerciante abre sua bolsa misteriosa...")
    
    print("\n1. 🛒 Pedir desconto na loja")
    print("2. 🎁 Pedir um item gratuito")
    print("3. 🚶‍♂️ Partir sem negociar")
    
    choice = input("\nO que você escolhe? ").strip()
    
    if choice == "1":
        apply_shop_discount(effects["shop_discount"])
        print(f"\n✨ O comerciante concede {int(effects['shop_discount'] * 100)}% de desconto na loja!")
    elif choice == "2":
        if random.random() <= effects["free_item"]:
            from models.inventory import drop_item
            free_item = drop_item(player.get("class", "Guerreiro"))
            if free_item:
                add_to_inventory(free_item)
                print(f"\n🎁 O comerciante lhe dá: {free_item['name']}!")
            else:
                print("\n😔 O comerciante não tem nada adequado para você.")
        else:
            print("\n😔 O comerciante recusa sua solicitação.")
    else:
        print("\n👋 Você se afasta respeitosamente.")
    
    print("\nPressione Enter para continuar...")
    input()
    return True

def handle_magic_fountain(effects, player):
    print("\n💧 Você bebe da fonte cristalina...")
    
    heal_amount = int(player["hp_max"] * effects["heal_percentage"])
    old_hp = player["hp"]
    player["hp"] = min(player["hp"] + heal_amount, player["hp_max"])
    actual_heal = player["hp"] - old_hp
    
    print(f"💚 Você recuperou {actual_heal} HP!")
    
    if effects["temp_boost"]:
        if "temp_effects" not in player:
            player["temp_effects"] = {}
        
        player["temp_effects"]["damage_temp"] = player["temp_effects"].get("damage_temp", 0) + 15
        player["temp_effects"]["critical_chance_temp"] = player["temp_effects"].get("critical_chance_temp", 0) + 0.1
        
        print("✨ Você sente uma energia mágica fluindo por seu corpo!")
        print("🔥 Dano aumentado em 15 e crítico em 10% pelas próximas batalhas!")
    
    print("\nPressione Enter para continuar...")
    input()
    return True

def handle_ancient_shrine(effects, player):
    print("\n🙏 Você se ajoelha diante do santuário antigo...")
    print("Uma voz etérea ecoa em sua mente...")
    
    print("\nEscolha uma bênção:")
    print("1. ⚔️ Bênção do Guerreiro (+20 Dano permanente)")
    print("2. 🛡️ Bênção da Resistência (+50 HP máximo permanente)")
    print("3. ⚡ Bênção da Precisão (+5% crítico permanente)")
    
    choice = input("\nQual bênção você escolhe? ").strip()
    
    if choice == "1":
        player["damage"] += 20
        print("\n⚔️ Suas armas brilham com poder divino!")
        print("Dano permanentemente aumentado em 20!")
    elif choice == "2":
        player["hp_max"] += 50
        player["hp"] += 50
        print("\n🛡️ Seu corpo é envolvido por uma aura protetora!")
        print("HP máximo permanentemente aumentado em 50!")
    elif choice == "3":
        player["critical_chance"] += 0.05
        print("\n⚡ Seus sentidos se aguçam com precisão sobrenatural!")
        print("Chance de crítico permanentemente aumentada em 5%!")
    else:
        print("\n🌟 Você escolhe não aceitar nenhuma bênção...")
        player["coins"] = player.get("coins", 0) + 100
        print("O santuário recompensa sua humildade com 100 moedas!")
    
    print("\nPressione Enter para continuar...")
    input()
    return True

def handle_cursed_artifact(effects, player):
    print("\n💀 O artefato pulsa com energia sombria...")
    print("Você sente sua maldição, mas também seu poder...")
    
    print("\n⚠️ AVISO: Este artefato é perigoso!")
    print("\n1. 🤝 Aceitar a maldição (Grande risco, grande recompensa)")
    print("2. 🚫 Recusar e destruir o artefato")
    print("3. 🏃‍♂️ Fugir imediatamente")
    
    choice = input("\nO que você faz? ").strip()
    
    if choice == "1":
        if random.random() <= 0.6:
            print("\n😈 A maldição aceita sua alma...")
            curse_type = random.choice(["hp", "damage", "coins"])
            
            if curse_type == "hp":
                hp_loss = int(player["hp_max"] * 0.2)
                player["hp_max"] -= hp_loss
                player["hp"] = min(player["hp"], player["hp_max"])
                player["damage"] += 40
                print(f"💔 Você perdeu {hp_loss} HP máximo!")
                print("⚔️ Mas ganhou +40 de dano!")
            elif curse_type == "damage":
                player["damage"] -= 10
                player["critical_chance"] += 0.15
                print("⚔️ Você perdeu 10 de dano!")
                print("💥 Mas ganhou +15% de chance de crítico!")
            else:
                coins_lost = min(player.get("coins", 0), 100)
                player["coins"] -= coins_lost
                player["exp"] += 200
                print(f"💰 Você perdeu {coins_lost} moedas!")
                print("📈 Mas ganhou 200 de experiência!")
        else:
            print("\n🌟 O artefato reconhece sua coragem!")
            player["damage"] += 30
            player["hp_max"] += 40
            player["critical_chance"] += 0.08
            print("⚔️ +30 Dano, +40 HP máximo, +8% crítico!")
            print("Você dominou a maldição!")
    
    elif choice == "2":
        print("\n🔥 Você destrói o artefato com determinação!")
        player["exp"] += 150
        player["coins"] = player.get("coins", 0) + 80
        print("📈 Sua coragem é recompensada com experiência e moedas!")
    
    else:
        print("\n🏃‍♂️ Você foge da presença sombria...")
        print("Às vezes, a sabedoria está em evitar o perigo.")
    
    print("\nPressione Enter para continuar...")
    input()
    return True

def handle_lost_traveler(effects, player):
    print("\n😰 'Por favor, herói! Bandidos roubaram tudo que eu tinha!'")
    print("'Você poderia me ajudar com algumas moedas?'")
    
    player_coins = player.get("coins", 0)
    suggested_amount = min(50, player_coins // 2)
    
    print(f"\n1. 💝 Dar {suggested_amount} moedas (Generoso)")
    print("2. 💰 Dar 20 moedas (Cauteloso)")
    print("3. 🤷‍♂️ Não dar nada")
    
    choice = input("\nO que você faz? ").strip()
    
    if choice == "1" and player_coins >= suggested_amount:
        player["coins"] -= suggested_amount
        reward = random.randint(*effects["help_reward"])
        blessing_duration = random.randint(3, 5)
        
        print(f"\n🙏 'Que os deuses abençoem sua generosidade!'")
        print(f"💫 Você recebe uma bênção especial por {blessing_duration} batalhas!")
        
        if "temp_effects" not in player:
            player["temp_effects"] = {}
        player["temp_effects"]["blessing_duration"] = blessing_duration
        player["temp_effects"]["damage_temp"] = player["temp_effects"].get("damage_temp", 0) + 10
        
        print("⚔️ +10 de dano temporário pela sua bondade!")
        
    elif choice == "2" and player_coins >= 20:
        player["coins"] -= 20
        print("\n😊 'Obrigado pela ajuda!'")
        exp_gain = random.randint(30, 60)
        player["exp"] += exp_gain
        print(f"📈 Você ganhou {exp_gain} de experiência!")
        
    else:
        print("\n😞 O viajante se afasta tristemente...")
        guilt_penalty = random.randint(*effects["ignore_penalty"])
        player["exp"] = max(0, player.get("exp", 0) - guilt_penalty)
        print(f"😔 Você perde {guilt_penalty} de experiência por remorso...")
    
    print("\nPressione Enter para continuar...")
    input()
    return True

def handle_meteor_shower(effects, player):
    print("\n☄️ Fragmentos de meteoro brilham ao seu redor!")
    print("Você coleta os materiais cósmicos...")
    
    materials_found = random.randint(3, 6)
    print(f"\n✨ Você encontrou {materials_found} fragmentos estelares!")
    
    for _ in range(materials_found):
        if random.random() <= 0.4:
            from models.inventory import drop_item
            cosmic_item = drop_item(player.get("class", "Guerreiro"))
            if cosmic_item:
                cosmic_item["name"] = f"⭐ {cosmic_item['name']} Estelar"
                cosmic_item["description"] += " (Aprimorado por energia cósmica)"
                
                for effect, value in cosmic_item.get("effects", {}).items():
                    if isinstance(value, (int, float)) and effect != "heal":
                        cosmic_item["effects"][effect] = int(value * 1.3)
                
                add_to_inventory(cosmic_item)
                print(f"🌟 Item aprimorado: {cosmic_item['name']}!")
    
    player["coins"] = player.get("coins", 0) + random.randint(100, 250)
    print("💰 Você também encontrou moedas antigas entre os destroços!")
    
    print("\nPressione Enter para continuar...")
    input()
    return True

def handle_time_rift(effects, player):
    print("\n🌀 Você espia através da fenda temporal...")
    print("Vislumbres do futuro dançam diante de seus olhos...")
    
    print("\n🔮 Você vê seus próximos 3 inimigos!")
    print("1. Um orc brutal com armadura pesada")
    print("2. Um mago sombrio cercado por energia mágica") 
    print("3. Um dragão juvenil cuspindo fogo")
    
    print(f"\n💡 Com esse conhecimento, você se prepara melhor!")
    
    if "temp_effects" not in player:
        player["temp_effects"] = {}
    
    player["temp_effects"]["future_sight"] = 3
    player["temp_effects"]["damage_temp"] = player["temp_effects"].get("damage_temp", 0) + 25
    player["temp_effects"]["critical_chance_temp"] = player["temp_effects"].get("critical_chance_temp", 0) + 0.12
    
    exp_boost = int(effects["exp_boost"] * 100)
    player["exp"] += exp_boost
    
    print("⚔️ +25 Dano temporário")
    print("💥 +12% Crítico temporário") 
    print(f"📈 +{exp_boost} Experiência por conhecimento futuro")
    print("🔮 Próximas 3 batalhas serão mais fáceis!")
    
    print("\nPressione Enter para continuar...")
    input()
    return True