import random
from models.constants import ITEMS, DROP_CHANCES
from models.ui import clear_screen, display_logo

player_inventory = []
equipped_items = []

def drop_item(player_class, is_boss=False, difficulty="Normal"):
    class_items = ITEMS.get(player_class, [])
    universal_items = ITEMS.get("Universal", [])

    available_items = class_items + universal_items

    if not available_items:
        return None

    adjusted_chances = DROP_CHANCES.copy()
    
    if is_boss:
        adjusted_chances["comum"] *= 0.3
        adjusted_chances["incomum"] *= 1.2
        adjusted_chances["raro"] *= 2.0
        adjusted_chances["lendário"] *= 3.0
    
    if difficulty == "Difícil":
        for rarity in adjusted_chances:
            adjusted_chances[rarity] *= 0.9
    elif difficulty == "Insano":
        for rarity in adjusted_chances:
            adjusted_chances[rarity] *= 0.7

    for rarity, chance in adjusted_chances.items():
        if random.random() <= chance:
            rarity_items = [item for item in available_items if item["rarity"] == rarity]
            
            if rarity_items:
                return random.choice(rarity_items)
    
    return None

def drop_coins(npc_level, is_boss=False, difficulty="Normal"):
    base_chance = 0.85
    
    if is_boss:
        base_chance = 1.0
    
    if random.random() <= base_chance:
        if is_boss:
            base_amount = random.randint(15, 25) * npc_level
            bonus_chance = 0.3
        else:
            base_amount = random.randint(5, 10) * npc_level
            bonus_chance = 0.1
        
        if random.random() <= bonus_chance:
            bonus_multiplier = random.randint(2, 4) if is_boss else random.randint(2, 3)
            coins = base_amount * bonus_multiplier
            return coins, True
        else:
            return base_amount, False
    else:
        return 0, False

def add_to_inventory(item):
    if item:
        item_copy = item.copy()
        item_copy["equipped"] = False
        player_inventory.append(item_copy)
        return True
    return False

def remove_from_inventory(item_index):
    if 0 <= item_index < len(player_inventory):
        removed_item = player_inventory.pop(item_index)
        return removed_item
    return None

def equip_item(item_index):
    if 0 <= item_index < len(player_inventory):
        item = player_inventory[item_index]

        if item["equipped"]:
            return False, "Item já está equipado"

        if len([i for i in player_inventory if i["equipped"]]) >= 3:
            return False, "Você só pode equipar 3 itens por vez"

        item["equipped"] = True
        return True, f"Item {item['name']} equipado com sucesso"
    
    return False, "Item não encontrado"

def unequip_item(item_index):
    if 0 <= item_index < len(player_inventory):
        item = player_inventory[item_index]
        
        if not item["equipped"]:
            return False, "Item não está equipado"
        
        item["equipped"] = False
        return True, f"Item {item['name']} desequipado com sucesso"
    
    return False, "Item não encontrado"

def use_consumable_item(item_index, player):
    if 0 <= item_index < len(player_inventory):
        item = player_inventory[item_index]
        
        if not item.get("consumable", False):
            return False, "Este item não é consumível"
        
        effects = item.get("effects", {})
        message = f"Você usou {item['name']}!\n"
        
        for effect, value in effects.items():
            if effect == "heal":
                old_hp = player["hp"]
                player["hp"] = min(player["hp"] + value, player["hp_max"])
                healed = player["hp"] - old_hp
                message += f"Você recuperou {healed} HP!\n"
            
            elif effect == "damage_temp":
                if "temp_effects" not in player:
                    player["temp_effects"] = {}
                duration = item.get("duration", 3)
                player["temp_effects"]["damage_temp"] = player["temp_effects"].get("damage_temp", 0) + value
                message += f"Seu dano foi aumentado em {value} por {duration} batalhas!\n"
            
            elif effect == "critical_chance_temp":
                if "temp_effects" not in player:
                    player["temp_effects"] = {}
                duration = item.get("duration", 3)
                player["temp_effects"]["critical_chance_temp"] = player["temp_effects"].get("critical_chance_temp", 0) + value
                crit_percent = int(value * 100)
                message += f"Sua chance de crítico foi aumentada em {crit_percent}% por {duration} batalhas!\n"
            
            elif effect == "exp_multiplier":
                if "temp_effects" not in player:
                    player["temp_effects"] = {}
                duration = item.get("duration", 3)
                player["temp_effects"]["exp_multiplier"] = value
                message += f"Sua experiência será multiplicada por {value} pelas próximas {duration} batalhas!\n"
        
        remove_from_inventory(item_index)
        return True, message.strip()
    
    return False, "Item não encontrado"

def get_equipped_items():
    return [item for item in player_inventory if item["equipped"]]

def apply_equipped_items_bonuses(player):
    equipped_items = get_equipped_items()
    
    for item in equipped_items:
        effects = item.get("effects", {})
        
        for stat, value in effects.items():
            if stat in player and isinstance(player[stat], (int, float)) and stat != "heal":
                player[stat] += value

def get_inventory_stats():
    total_items = len(player_inventory)
    equipped_count = len([item for item in player_inventory if item["equipped"]])
    
    rarity_count = {}
    for item in player_inventory:
        rarity = item.get("rarity", "comum")
        rarity_count[rarity] = rarity_count.get(rarity, 0) + 1
    
    return {
        "total_items": total_items,
        "equipped_count": equipped_count,
        "rarity_distribution": rarity_count
    }

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

        stats = get_inventory_stats()
        print(f"\nItens no inventário: {stats['total_items']} | Equipados: {stats['equipped_count']}/3")
        
        if stats['rarity_distribution']:
            print("Distribuição por raridade:", end=" ")
            rarity_display = []
            for rarity, count in stats['rarity_distribution'].items():
                rarity_display.append(f"{rarity.capitalize()}: {count}")
            print(" | ".join(rarity_display))

        print("\nSeus itens:")
        for i, item in enumerate(player_inventory):
            equipped_status = "[Equipado]" if item["equipped"] else "[Não equipado]"
            consumable_status = "[Consumível]" if item.get("consumable", False) else ""
            print(f"{i+1}. {item['name']} - {item['rarity'].capitalize()} {equipped_status} {consumable_status}")
        
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
        
        if item.get("consumable", False):
            print("Tipo: Consumível")
            if "duration" in item:
                print(f"Duração do efeito: {item['duration']} batalhas")
        else:
            print("Tipo: Equipamento")
        
        print("\nEfeitos:")
        effects = item.get("effects", {})
        for stat, value in effects.items():
            if stat == "hp_max":
                print(f"  HP Máximo: {'+' if value > 0 else ''}{value}")
            elif stat == "damage":
                print(f"  Dano: {'+' if value > 0 else ''}{value}")
            elif stat == "critical_chance":
                print(f"  Crítico: {'+' if value > 0 else ''}{int(value*100)}%")
            elif stat == "heal":
                print(f"  Cura: {value} HP")
            elif stat == "damage_temp":
                print(f"  Dano temporário: +{value}")
            elif stat == "critical_chance_temp":
                print(f"  Crítico temporário: +{int(value*100)}%")
            elif stat == "exp_multiplier":
                print(f"  Multiplicador de XP: x{value}")
            else:
                print(f"  {stat}: {value}")
        
        equipped_status = "Equipado" if item["equipped"] else "Não equipado"
        print(f"\nStatus: {equipped_status}")
        
        if item.get("consumable", False):
            print("\n1. Usar item")
            print("2. Descartar item")
        else:
            if item["equipped"]:
                print("\n1. Desequipar")
            else:
                print("\n1. Equipar")
            print("2. Descartar item")
        
        print("0. Voltar")
        
        print("\nEscolha uma opção: ", end="")
        choice = input().strip()
        
        if choice == '0':
            return
        elif choice == '1':
            if item.get("consumable", False):
                from models.player import player
                success, message = use_consumable_item(item_index, player)
                print(f"\n{message}")
                print("Pressione Enter para continuar...")
                input()
                if success:
                    return
            else:
                if item["equipped"]:
                    success, message = unequip_item(item_index)
                    print(f"\n{message} Pressione Enter para continuar...")
                    input()
                else:
                    equipped_count = len([i for i in player_inventory if i["equipped"]])
                    if equipped_count >= 3:
                        print("\nVocê só pode equipar 3 itens por vez! Desequipe um item primeiro.")
                        print("Pressione Enter para continuar...")
                        input()
                    else:
                        success, message = equip_item(item_index)
                        print(f"\n{message} Pressione Enter para continuar...")
                        input()
        elif choice == '2':
            print(f"\nTem certeza que deseja descartar {item['name']}? (S/N): ", end="")
            confirm = input().strip().upper()
            if confirm == 'S':
                removed_item = remove_from_inventory(item_index)
                if removed_item:
                    print(f"\n{removed_item['name']} foi descartado!")
                    print("Pressione Enter para continuar...")
                    input()
                    return
        else:
            print("Opção inválida. Pressione Enter para continuar...")
            input()

def reset_inventory():
    player_inventory.clear()

def get_inventory_value():
    total_value = 0
    for item in player_inventory:
        rarity = item.get("rarity", "comum")
        if rarity == "comum":
            total_value += 25
        elif rarity == "incomum":
            total_value += 75
        elif rarity == "raro":
            total_value += 200
        elif rarity == "lendário":
            total_value += 500
    return total_value