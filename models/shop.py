import random
from models.constants import ITEMS
from models.ui import clear_screen, display_logo
from models.inventory import add_to_inventory

shop_items = []
_shop_initialized = False

def should_refresh_shop(player):
    global _shop_initialized
    if not _shop_initialized:
        return True
    return player.get('shop_needs_refresh', False)

def mark_shop_refresh_needed(player):
    player['shop_needs_refresh'] = True

def generate_shop_items(player_class, player_level=1, max_items=5):
    global shop_items, _shop_initialized
    
    shop_items.clear()

    class_items = ITEMS.get(player_class, [])
    universal_items = ITEMS.get("Universal", [])

    available_items = class_items + universal_items
    
    if not available_items:
        return []

    num_items = min(max_items, random.randint(3, 5))

    rarity_chances = {
        "comum": 0.5 - (player_level * 0.01),
        "incomum": 0.3 + (player_level * 0.005),
        "raro": 0.15 + (player_level * 0.01),
        "lendário": 0.05 + (player_level * 0.005)
    }

    total = sum(rarity_chances.values())

    for rarity in rarity_chances:
        rarity_chances[rarity] /= total

    selected_items = []

    while len(selected_items) < num_items and available_items:
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
                if rarity == "comum":
                    item_copy["price"] = random.randint(50, 100)
                elif rarity == "incomum":
                    item_copy["price"] = random.randint(150, 300)
                elif rarity == "raro":
                    item_copy["price"] = random.randint(400, 800)
                elif rarity == "lendário":
                    item_copy["price"] = random.randint(1000, 2000)
                selected_items.append(item_copy)

    shop_items = selected_items
    _shop_initialized = True
    return shop_items

def attempt_purchase(item_index, player):
    if item_index >= len(shop_items):
        return False, "Item não encontrado"
    
    item = shop_items[item_index]
    
    if player.get('coins', 0) < item['price']:
        return False, "Moedas insuficientes"
    
    item_copy = {k: v for k, v in item.items() if k != 'price'}
    
    try:
        success = add_to_inventory(item_copy)
        if success:
            player['coins'] -= item['price']
            shop_items.pop(item_index)
            return True, f"Item {item['name']} comprado com sucesso!"
        else:
            return False, "Inventário cheio"
    except Exception as e:
        return False, f"Erro na compra: {str(e)}"

def display_shop(player):
    if should_refresh_shop(player):
        print("Novos itens chegaram à loja!")
        generate_shop_items(
            player.get('class', 'Guerreiro'), 
            player.get('level', 1)
        )
        player['shop_needs_refresh'] = False

    while True:
        clear_screen()
        display_logo()
        print("\n=== LOJA DE ITENS ===")
        print(f"Suas moedas: {player.get('coins', 0)}")
        
        if not shop_items:
            print("\nA loja está vazia. Volte mais tarde!")
            print("\nPressione Enter para voltar...")
            input()
            return
        
        print("\nItens disponíveis para compra:")
        for i, item in enumerate(shop_items):
            print(f"{i+1}. {item['name']} - {item['rarity'].capitalize()} - {item['price']} moedas")
        
        print("\n0. Voltar")
        
        print("\nEscolha um item para mais detalhes (ou '0' para voltar): ", end="")
        choice = input().strip()
        
        if choice == '0':
            return
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
    if item_index >= len(shop_items):
        print("Item não encontrado!")
        input()
        return

    item = shop_items[item_index]

    while True:
        clear_screen()
        display_logo()
        print(f"\n=== DETALHES DO ITEM: {item['name']} ===")
        print(f"Raridade: {item['rarity'].capitalize()}")
        print(f"Preço: {item['price']} moedas")
        print(f"Descrição: {item['description']}")
        
        print("\nEfeitos:")
        effects = item.get("effects", {})
        for stat, value in effects.items():
            if stat == "hp_max":
                print(f"  HP Máximo: {'+' if value > 0 else ''}{value}")
            elif stat == "damage":
                print(f"  Dano: {'+' if value > 0 else ''}{value}")
            elif stat == "heal":
                print(f"  Cura: {value} HP")
            else:
                print(f"  {stat}: {value}")
        
        print(f"\nSuas moedas: {player.get('coins', 0)}")
        
        can_afford = player.get('coins', 0) >= item['price']
        
        print("\n1. Comprar item" if can_afford else "\n1. Comprar item (moedas insuficientes)")
        print("0. Voltar")
        
        print("\nEscolha uma opção: ", end="")
        choice = input().strip()
        
        if choice == '0':
            return
        elif choice == '1':
            if can_afford:
                print(f"\nConfirmar a compra de {item['name']} por {item['price']} moedas? (S/N): ", end="")
                confirm = input().strip().upper()
                
                if confirm == 'S':
                    success, message = attempt_purchase(item_index, player)
                    print(f"\n{message}")
                    print("Pressione Enter para continuar...")
                    input()
                    if success:
                        return
            else:
                print("\nVocê não tem moedas suficientes para comprar este item.")
                print("Pressione Enter para continuar...")
                input()
        else:
            print("Opção inválida. Pressione Enter para continuar...")
            input()

def get_shop_save_data():
    return {
        'items': shop_items,
        'initialized': _shop_initialized
    }

def load_shop_data(shop_data):
    global shop_items, _shop_initialized
    if shop_data:
        shop_items = shop_data.get('items', [])
        _shop_initialized = shop_data.get('initialized', False)