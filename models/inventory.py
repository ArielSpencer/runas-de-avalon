import random
from models.constants import ITEMS, DROP_CHANCES
from models.ui import clear_screen, display_logo

player_inventory = []
equipped_items = []

def drop_item(player_class):
    class_items = ITEMS.get(player_class, [])
    universal_items = ITEMS.get("Universal", [])

    available_items = class_items + universal_items

    if not available_items:
        return None

    for rarity, chance in DROP_CHANCES.items():
        if random.random() <= chance:
            rarity_items = [item for item in available_items if item["rarity"] == rarity]
            
            if rarity_items:
                return random.choice(rarity_items)
    
    return None

def add_to_inventory(item):
    if item:
        item_copy = item.copy()
        item_copy["equipped"] = False
        player_inventory.append(item_copy)
        return True
    return False

def equip_item(item_index):
    if 0 <= item_index < len(player_inventory):
        item = player_inventory[item_index]

        if item["equipped"]:
            return False

        if len([i for i in player_inventory if i["equipped"]]) >= 2:
            return False

        item["equipped"] = True
        return True
    
    return False

def unequip_item(item_index):
    if 0 <= item_index < len(player_inventory):
        item = player_inventory[item_index]
        
        if not item["equipped"]:
            return False
        
        item["equipped"] = False
        return True
    
    return False

def get_equipped_items():
    return [item for item in player_inventory if item["equipped"]]

def apply_equipped_items_bonuses(player):
    equipped_items = get_equipped_items()
    
    for item in equipped_items:
        effects = item.get("effects", {})
        
        for stat, value in effects.items():
            if stat in player and isinstance(player[stat], (int, float)):
                player[stat] += value

def display_inventory():
    while True:
        clear_screen()
        display_logo()
        print("\n=== INVENTÁRIO ===")
        
        if not player_inventory:
            print("\nSeu inventário está vazio.")
            print("\nPressione Enter para voltar...")
            input()
            return

        print("\nSeus itens:")
        for i, item in enumerate(player_inventory):
            equipped_status = "[Equipado]" if item["equipped"] else "[Não equipado]"
            print(f"{i+1}. {item['name']} - {item['rarity'].capitalize()} {equipped_status}")
        
        print("\nEscolha um item para ver detalhes (ou '0' para voltar): ", end="")
        choice = input().strip()
        
        if choice == '0':
            return
        
        try:
            item_index = int(choice) - 1
            if 0 <= item_index < len(player_inventory):
                display_item_details(item_index)
            else:
                print("Escolha inválida. Pressione Enter para continuar...")
                input()
        except ValueError:
            print("Por favor, digite um número válido. Pressione Enter para continuar...")
            input()

def display_item_details(item_index):
    item = player_inventory[item_index]
    
    while True:
        clear_screen()
        display_logo()
        print(f"\n=== DETALHES DO ITEM: {item['name']} ===")
        print(f"Raridade: {item['rarity'].capitalize()}")
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
        
        equipped_status = "Equipado" if item["equipped"] else "Não equipado"
        print(f"\nStatus: {equipped_status}")
        
        if item["equipped"]:
            print("\n1. Desequipar")
        else:
            print("\n1. Equipar")
        
        print("0. Voltar")
        
        print("\nEscolha uma opção: ", end="")
        choice = input().strip()
        
        if choice == '0':
            return
        elif choice == '1':
            if item["equipped"]:
                unequip_item(item_index)
                print("\nItem desequipado! Pressione Enter para continuar...")
                input()
            else:
                equipped_count = len([i for i in player_inventory if i["equipped"]])
                if equipped_count >= 2:
                    print("\nVocê só pode equipar 2 itens por vez! Desequipe um item primeiro.")
                    print("Pressione Enter para continuar...")
                    input()
                else:
                    equip_item(item_index)
                    print("\nItem equipado! Pressione Enter para continuar...")
                    input()
        else:
            print("Opção inválida. Pressione Enter para continuar...")
            input()

def reset_inventory():
    player_inventory.clear()