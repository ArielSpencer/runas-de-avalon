import random
from models.constants import ITEMS
from models.ui import clear_screen, display_logo, display_rarity_color
from models.inventory import add_to_inventory

shop_items = []
_shop_initialized = False
shop_discount = 0.0

def should_refresh_shop(player):
    global _shop_initialized
    if not _shop_initialized:
        return True
    return player.get('shop_needs_refresh', False)

def mark_shop_refresh_needed(player):
    player['shop_needs_refresh'] = True

def apply_shop_discount(discount_percentage):
    global shop_discount
    shop_discount = discount_percentage
    print(f"🎉 Desconto especial de {int(discount_percentage * 100)}% aplicado na loja!")

def generate_shop_items(player_class, player_level=1, max_items=6, difficulty="Normal"):
    global shop_items, _shop_initialized
    
    shop_items.clear()

    class_items = ITEMS.get(player_class, [])
    universal_items = ITEMS.get("Universal", [])
    
    other_class_items = []
    for class_name, items in ITEMS.items():
        if class_name != player_class and class_name != "Universal":
            other_class_items.extend(items[:2])

    available_items = class_items + universal_items + other_class_items
    
    if not available_items:
        return []

    num_items = min(max_items, random.randint(4, 6))

    base_rarity_chances = {
        "comum": 0.45 - (player_level * 0.015),
        "incomum": 0.35 + (player_level * 0.008),
        "raro": 0.15 + (player_level * 0.012),
        "lendário": 0.05 + (player_level * 0.008)
    }
    
    if difficulty == "Fácil":
        base_rarity_chances["raro"] *= 1.3
        base_rarity_chances["lendário"] *= 1.5
    elif difficulty == "Difícil":
        base_rarity_chances["comum"] *= 1.2
        base_rarity_chances["lendário"] *= 0.7
    elif difficulty == "Insano":
        base_rarity_chances["comum"] *= 1.4
        base_rarity_chances["lendário"] *= 0.5

    total = sum(base_rarity_chances.values())
    rarity_chances = {k: v/total for k, v in base_rarity_chances.items()}

    selected_items = []
    attempts = 0
    max_attempts = 50

    while len(selected_items) < num_items and attempts < max_attempts:
        attempts += 1
        
        rarity = random.choices(
            list(rarity_chances.keys()),
            weights=list(rarity_chances.values()),
            k=1
        )[0]

        rarity_items = [item for item in available_items if item["rarity"] == rarity]
        
        if rarity_items:
            item = random.choice(rarity_items)
            if not any(selected["id"] == item["id"] for selected in selected_items):
                item_copy = item.copy()
                
                base_price = calculate_base_price(rarity, player_level)
                price_variance = random.uniform(0.8, 1.2)
                final_price = int(base_price * price_variance)
                
                if difficulty == "Fácil":
                    final_price = int(final_price * 0.8)
                elif difficulty == "Difícil":
                    final_price = int(final_price * 1.3)
                elif difficulty == "Insano":
                    final_price = int(final_price * 1.6)
                
                item_copy["price"] = final_price
                selected_items.append(item_copy)

    if random.random() < 0.15:
        mystery_item = create_mystery_item(player_level)
        if mystery_item:
            selected_items.append(mystery_item)

    shop_items = selected_items
    _shop_initialized = True
    return shop_items

def calculate_base_price(rarity, player_level):
    base_prices = {
        "comum": random.randint(40, 80),
        "incomum": random.randint(120, 250),
        "raro": random.randint(300, 600),
        "lendário": random.randint(800, 1500)
    }
    
    level_multiplier = 1 + (player_level * 0.1)
    return int(base_prices[rarity] * level_multiplier)

def create_mystery_item(player_level):
    mystery_items = [
        {
            "id": "mystery_box",
            "name": "📦 Caixa Misteriosa",
            "description": "Uma caixa enigmática. Quem sabe o que há dentro?",
            "rarity": "incomum",
            "effects": {"mystery": True},
            "mystery": True
        },
        {
            "id": "ancient_scroll",
            "name": "📜 Pergaminho Antigo",
            "description": "Um pergaminho com runas antigas. Seus efeitos são desconhecidos.",
            "rarity": "raro", 
            "effects": {"mystery": True},
            "mystery": True
        }
    ]
    
    if random.random() < 0.7:
        item = random.choice(mystery_items).copy()
        item["price"] = random.randint(50, 200) + (player_level * 10)
        return item
    
    return None

def reveal_mystery_item(mystery_item, player_class):
    possible_effects = [
        {"hp_max": random.randint(20, 50)},
        {"damage": random.randint(15, 35)},
        {"critical_chance": random.uniform(0.05, 0.15)},
        {"heal": random.randint(100, 200)},
        {"damage_temp": random.randint(25, 45)},
        {"exp_multiplier": random.uniform(1.5, 2.5)}
    ]
    
    chosen_effect = random.choice(possible_effects)
    
    revealed_item = mystery_item.copy()
    revealed_item["effects"] = chosen_effect
    revealed_item["description"] += f" Foi revelado: {list(chosen_effect.keys())[0]}!"
    revealed_item["mystery"] = False
    
    return revealed_item

def attempt_purchase(item_index, player):
    global shop_discount
    
    if item_index >= len(shop_items):
        return False, "Item não encontrado"
    
    item = shop_items[item_index]
    
    final_price = item['price']
    if shop_discount > 0:
        final_price = int(final_price * (1 - shop_discount))
        discount_msg = f" (Desconto aplicado: -{int(shop_discount * 100)}%)"
    else:
        discount_msg = ""
    
    if player.get('coins', 0) < final_price:
        return False, f"Moedas insuficientes. Preço: {final_price}{discount_msg}"
    
    item_copy = {k: v for k, v in item.items() if k != 'price'}
    
    if item.get("mystery", False):
        item_copy = reveal_mystery_item(item_copy, player.get("class", "Guerreiro"))
        mystery_msg = f" O item misterioso foi revelado!"
    else:
        mystery_msg = ""
    
    try:
        success = add_to_inventory(item_copy)
        if success:
            player['coins'] -= final_price
            shop_items.pop(item_index)
            
            from models.achievements import update_achievement_progress
            newly_unlocked = update_achievement_progress(player, "item_purchased")
            
            if newly_unlocked:
                from models.achievements import display_achievement_notification, apply_achievement_rewards
                for achievement_id in newly_unlocked:
                    display_achievement_notification(achievement_id)
                    apply_achievement_rewards(player, [achievement_id])
                    print("Pressione Enter para continuar...")
                    input()
            
            if shop_discount > 0:
                shop_discount = 0
            
            return True, f"Item {item['name']} comprado com sucesso!{mystery_msg}{discount_msg}"
        else:
            return False, "Inventário cheio"
    except Exception as e:
        return False, f"Erro na compra: {str(e)}"

def display_shop(player):
    global shop_discount
    
    if should_refresh_shop(player):
        from models.ui import display_loading_screen
        display_loading_screen("Reabastecendo a loja")
        
        generate_shop_items(
            player.get('class', 'Guerreiro'), 
            player.get('level', 1),
            difficulty=player.get('difficulty', 'Normal')
        )
        player['shop_needs_refresh'] = False

    while True:
        clear_screen()
        display_logo()
        print("\n🏪 === LOJA DE ITENS MÁGICOS === 🏪")
        print(f"💰 Suas moedas: {player.get('coins', 0)}")
        
        if shop_discount > 0:
            print(f"🎉 DESCONTO ATIVO: {int(shop_discount * 100)}% em todos os itens!")
        
        if not shop_items:
            print("\n🚫 A loja está temporariamente vazia. Volte após algumas batalhas!")
            print("\nPressione Enter para voltar...")
            input()
            return
        
        print(f"\n📦 Itens disponíveis ({len(shop_items)} itens):")
        for i, item in enumerate(shop_items):
            rarity_icon = display_rarity_color(item['rarity'])
            
            final_price = item['price']
            if shop_discount > 0:
                final_price = int(final_price * (1 - shop_discount))
            
            mystery_indicator = " ❓" if item.get("mystery", False) else ""
            affordability = "✅" if player.get('coins', 0) >= final_price else "❌"
            
            print(f"{i+1}. {rarity_icon} {item['name']}{mystery_indicator} - {item['rarity'].capitalize()}")
            print(f"    💰 {final_price} moedas {affordability}")
        
        print("\n0. Voltar")
        print("R. Atualizar loja (100 moedas)")
        
        print("\n🛒 Escolha um item para detalhes ou 'R' para atualizar: ", end="")
        choice = input().strip().upper()
        
        if choice == '0':
            return
        elif choice == 'R':
            if player.get('coins', 0) >= 100:
                player['coins'] -= 100
                print("\n🔄 Atualizando loja...")
                generate_shop_items(
                    player.get('class', 'Guerreiro'), 
                    player.get('level', 1),
                    difficulty=player.get('difficulty', 'Normal')
                )
                print("✅ Loja atualizada!")
                input("Pressione Enter para continuar...")
            else:
                print("\n❌ Você precisa de 100 moedas para atualizar a loja.")
                input("Pressione Enter para continuar...")
        else:
            try:
                item_index = int(choice) - 1
                if 0 <= item_index < len(shop_items):
                    display_item_shop_details(item_index, player)
                else:
                    print("Escolha inválida. Pressione Enter para continuar...")
                    input()
            except ValueError:
                print("Por favor, digite um número válido. Pressione Enter para continuar...")
                input()

def display_item_shop_details(item_index, player):
    global shop_discount
    
    if item_index >= len(shop_items):
        print("Item não encontrado!")
        input()
        return

    item = shop_items[item_index]

    while True:
        clear_screen()
        display_logo()
        
        rarity_icon = display_rarity_color(item['rarity'])
        print(f"\n🔍 === DETALHES: {rarity_icon} {item['name']} ===")
        print(f"✨ Raridade: {item['rarity'].capitalize()}")
        
        final_price = item['price']
        original_price = final_price
        if shop_discount > 0:
            final_price = int(final_price * (1 - shop_discount))
            print(f"💰 Preço: ~~{original_price}~~ {final_price} moedas (DESCONTO!)")
        else:
            print(f"💰 Preço: {final_price} moedas")
            
        print(f"📝 Descrição: {item['description']}")
        
        if item.get("mystery", False):
            print("\n❓ ITEM MISTERIOSO:")
            print("Os efeitos deste item só serão revelados após a compra!")
            print("Pode conter qualquer tipo de bônus ou efeito especial.")
        else:
            print("\n⚡ Efeitos:")
            effects = item.get("effects", {})
            if effects:
                for stat, value in effects.items():
                    if stat == "hp_max":
                        print(f"  ❤️ HP Máximo: {'+' if value > 0 else ''}{value}")
                    elif stat == "damage":
                        print(f"  ⚔️ Dano: {'+' if value > 0 else ''}{value}")
                    elif stat == "critical_chance":
                        print(f"  💥 Crítico: {'+' if value > 0 else ''}{int(value*100)}%")
                    elif stat == "heal":
                        print(f"  💚 Cura: {value} HP")
                    elif stat == "damage_temp":
                        print(f"  🔥 Dano temporário: +{value}")
                    elif stat == "exp_multiplier":
                        print(f"  📈 Multiplicador XP: x{value}")
                    else:
                        print(f"  ✨ {stat}: {value}")
            else:
                print("  Nenhum efeito especial")
        
        print(f"\n💰 Suas moedas: {player.get('coins', 0)}")
        
        can_afford = player.get('coins', 0) >= final_price
        
        if can_afford:
            print("\n1. 🛒 Comprar item")
        else:
            print(f"\n1. 🛒 Comprar item (❌ Insuficiente - faltam {final_price - player.get('coins', 0)} moedas)")
            
        print("0. ⬅️ Voltar")
        
        print("\nEscolha uma opção: ", end="")
        choice = input().strip()
        
        if choice == '0':
            return
        elif choice == '1':
            if can_afford:
                print(f"\n🤔 Confirmar a compra de {item['name']} por {final_price} moedas? (S/N): ", end="")
                confirm = input().strip().upper()
                
                if confirm == 'S':
                    success, message = attempt_purchase(item_index, player)
                    print(f"\n{message}")
                    if "revelado" in message:
                        print("✨ Verifique seu inventário para ver o que foi revelado!")
                    print("Pressione Enter para continuar...")
                    input()
                    if success:
                        return
            else:
                print(f"\n❌ Você não tem moedas suficientes para comprar este item.")
                print("💡 Dica: Derrote mais inimigos para ganhar moedas!")
                print("Pressione Enter para continuar...")
                input()
        else:
            print("Opção inválida. Pressione Enter para continuar...")
            input()

def get_shop_save_data():
    return {
        'items': shop_items,
        'initialized': _shop_initialized,
        'discount': shop_discount
    }

def load_shop_data(shop_data):
    global shop_items, _shop_initialized, shop_discount
    if shop_data:
        shop_items = shop_data.get('items', [])
        _shop_initialized = shop_data.get('initialized', False)
        shop_discount = shop_data.get('discount', 0.0)