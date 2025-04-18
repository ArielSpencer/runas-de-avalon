from models.constants import PLAYER_CLASSES
from models.player import player, create_player, set_player, show_player, apply_level_bonus
from models.npc import generate_npcs
from models.battle import start_battle
from models.ui import (
    clear_screen, display_logo, display_how_to_play, 
    display_about, display_credits, display_battle_header,
    display_victory, display_defeat
)
from models.inventory import drop_item, add_to_inventory, display_inventory, apply_equipped_items_bonuses, get_equipped_items, drop_coins

def display_main_menu():
    display_logo()
    print("\n1. Iniciar Aventura")
    print("2. Como Jogar")
    print("3. Sobre")
    print("4. Créditos")
    print("5. Sair")
    print("\nEscolha uma opção (1-5): ", end="")

def create_character():
    clear_screen()
    display_logo()
    print("\n=== CRIAÇÃO DE PERSONAGEM ===")
    
    name = input("\nQual é o nome do seu personagem? ")
    if not name.strip():
        name = "Aventureiro"
    
    print("\nEscolha sua classe:")
    for i, (class_name, class_data) in enumerate(PLAYER_CLASSES.items(), 1):
        print(f"{i}. {class_name} - {class_data['description']}")
        print(f"   HP: {class_data['hp_max']} | Dano: {class_data['damage']}")
    
    while True:
        try:
            choice = int(input("\nEscolha uma classe (1-3): "))
            if 1 <= choice <= 3:
                break
            else:
                print("Por favor, escolha um número entre 1 e 3.")
        except ValueError:
            print("Por favor, digite um número válido.")
    
    class_names = list(PLAYER_CLASSES.keys())
    selected_class = class_names[choice - 1]
    
    new_player = create_player(name, selected_class)
    set_player(new_player)
    
    clear_screen()
    display_logo()
    print(f"\nBem-vindo às Runas de Avalon, {name}!")
    print(f"Você escolheu a classe: {selected_class}")
    print("\nSeus atributos iniciais são:")
    show_player()
    
    print("\nPressione Enter para iniciar sua jornada ou 'x' para voltar ao menu principal...")
    choice = input().strip().upper()
    return choice != 'X'

def battle_loop(player, npcs):
    npc_index = 0
    total_npcs = len(npcs)
    
    while npc_index < total_npcs:
        current_npc = npcs[npc_index]
        
        display_battle_header(npc_index, total_npcs, current_npc, show_player)
        
        print("\nPressione Enter para iniciar a batalha ou 'x' para voltar ao menu principal...")
        choice = input().strip().upper()
        if choice == 'X':
            return
        
        clear_screen()
        old_level = player["level"]
        
        victory = start_battle(player, current_npc)
        
        if victory:
            dropped_item = drop_item(player.get("class", ""))
            if dropped_item:
                add_to_inventory(dropped_item)
                print(f"\nVocê encontrou: {dropped_item['name']} ({dropped_item['rarity'].capitalize()})!")
                print(f"- {dropped_item['description']}")
            else:
                print("\nVocê não encontrou nenhum item desta vez.")

            coins_dropped, is_bonus = drop_coins(current_npc["level"])
            if coins_dropped > 0:
                player["coins"] += coins_dropped
                if is_bonus:
                    print(f"\n💰 BÔNUS DE SORTE! Você encontrou {coins_dropped} moedas!")
                else:
                    print(f"\n💰 Você encontrou {coins_dropped} moedas!")
            else:
                print("\nVocê não encontrou nenhuma moeda desta vez.")
        
        if player["level"] > old_level:
            bonus = apply_level_bonus(player)
            
            print(f"\n=== LEVEL UP! ===")
            print(f"Você subiu para o nível {player['level']}!")
            print(f"Você recebeu um bônus: {bonus}")
            print("\nSeus novos atributos:")
            show_player()
        elif victory:
            print("\nVocê recuperou seu HP após a batalha.")
            print("\nSeus atributos atuais:")
            show_player()
        
        print("\nPressione Enter para continuar...")
        input()
        
        if victory:
            while True:
                clear_screen()
                display_logo()
                print(f"\n=== PRÓXIMOS PASSOS ===")
                print(f"Inimigo derrotado: {current_npc['name']}")
                
                if npc_index < total_npcs - 1:
                    print(f"\nPróximo inimigo: NPC #{npc_index + 2}")
                else:
                    print(f"\nEste era o último inimigo!")
                
                print("\n1. Continuar para a próxima batalha")
                print("2. Ver inventário")
                print("3. Visualizar status")
                
                print("\nEscolha uma opção: ", end="")
                choice = input().strip()
                
                if choice == '1':
                    npc_index += 1
                    break
                elif choice == '2':
                    display_inventory()
                    apply_equipped_items_bonuses(player)
                elif choice == '3':
                    display_player_status(player)
                else:
                    print("Opção inválida. Pressione Enter para continuar...")
                    input()
            
            if npc_index < total_npcs:
                continue
            else:
                display_victory()
                return
        else:
            display_defeat(current_npc["name"])
            return

def start_adventure():
    if not create_character():
        return
    
    from models.inventory import reset_inventory
    reset_inventory()
    
    npcs = generate_npcs(20)
    battle_loop(player, npcs)

def main_menu():
    while True:
        clear_screen()
        display_main_menu()
        
        try:
            choice = input().strip()
            
            if choice == '1':
                start_adventure()
            elif choice == '2':
                display_how_to_play()
            elif choice == '3':
                display_about()
            elif choice == '4':
                display_credits()
            elif choice == '5':
                clear_screen()
                print("Obrigado por jogar Runas de Avalon!")
                print("Até a próxima aventura!")
                break
            else:
                print("Opção inválida. Pressione Enter para continuar...")
                input()
        except Exception as e:
            print(f"Erro: {e}")
            print("Pressione Enter para continuar...")
            input()

def display_player_status(player):
    clear_screen()
    display_logo()
    print("\n=== STATUS DO PERSONAGEM ===")

    print(f"\nNome: {player['name']}")
    if 'class' in player:
        print(f"Classe: {player['class']}")

    print(f"\nNível: {player['level']}")
    print(f"Experiência: {player['exp']}/{player['exp_max']}")

    print(f"\nAtributos:")
    print(f"HP: {player['hp']}/{player['hp_max']}")
    print(f"Dano base: {player['damage']}")
    
    print(f"Moedas: {player.get('coins', 0)}")

    equipped_items = get_equipped_items()
    if equipped_items:
        print("\nBônus de itens equipados:")
        for item in equipped_items:
            print(f"\n{item['name']} ({item['rarity'].capitalize()}):")
            for stat, value in item.get('effects', {}).items():
                if stat == "hp_max":
                    print(f"  HP Máximo: {'+' if value > 0 else ''}{value}")
                elif stat == "damage":
                    print(f"  Dano: {'+' if value > 0 else ''}{value}")
                elif stat == "heal":
                    print(f"  Cura: {value} HP")
                else:
                    print(f"  {stat}: {value}")
    
    print("\nPressione Enter para voltar...")
    input()