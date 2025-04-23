from models.constants import PLAYER_CLASSES, DIFFICULTY_SETTINGS
from models.player import player, create_player, set_player, show_player, apply_level_bonus
from models.npc import generate_npcs
from models.battle import start_battle
from models.shop import display_shop, mark_shop_refresh_needed
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

def select_difficulty():
    clear_screen()
    display_logo()
    print("\n=== SELEÇÃO DE DIFICULDADE ===")
    print("\nEscolha o nível de dificuldade:")
    
    difficulties = list(DIFFICULTY_SETTINGS.keys())
    for i, (difficulty, settings) in enumerate(DIFFICULTY_SETTINGS.items(), 1):
        exp_mult = settings["exp_multiplier"]
        coin_mult = settings["coin_multiplier"]
        enemy_hp = settings["enemy_hp_multiplier"]
        enemy_dmg = settings["enemy_damage_multiplier"]
        
        print(f"\n{i}. {difficulty}")
        print(f"   Experiência: {'+' if exp_mult > 1 else ''}{int((exp_mult - 1) * 100)}%")
        print(f"   Moedas: {'+' if coin_mult > 1 else ''}{int((coin_mult - 1) * 100)}%")
        print(f"   HP Inimigos: {'+' if enemy_hp > 1 else ''}{int((enemy_hp - 1) * 100)}%")
        print(f"   Dano Inimigos: {'+' if enemy_dmg > 1 else ''}{int((enemy_dmg - 1) * 100)}%")
    
    while True:
        try:
            choice = int(input(f"\nEscolha uma dificuldade (1-{len(difficulties)}): "))
            if 1 <= choice <= len(difficulties):
                selected_difficulty = difficulties[choice - 1]
                print(f"\nDificuldade selecionada: {selected_difficulty}")
                return selected_difficulty
            else:
                print(f"Por favor, escolha um número entre 1 e {len(difficulties)}.")
        except ValueError:
            print("Por favor, digite um número válido.")

def create_character():
    clear_screen()
    display_logo()
    print("\n=== CRIAÇÃO DE PERSONAGEM ===")
    
    name = input("\nQual é o nome do seu personagem? ")
    if not name.strip():
        name = "Aventureiro"
    
    print("\nEscolha sua classe:")
    for i, (class_name, class_data) in enumerate(PLAYER_CLASSES.items(), 1):
        critical_percent = int(class_data['critical_chance'] * 100)
        print(f"{i}. {class_name} - {class_data['description']}")
        print(f"   HP: {class_data['hp_max']} | Dano: {class_data['damage']} | Crítico: {critical_percent}%")
    
    while True:
        try:
            choice = int(input(f"\nEscolha uma classe (1-{len(PLAYER_CLASSES)}): "))
            if 1 <= choice <= len(PLAYER_CLASSES):
                break
            else:
                print(f"Por favor, escolha um número entre 1 e {len(PLAYER_CLASSES)}.")
        except ValueError:
            print("Por favor, digite um número válido.")
    
    class_names = list(PLAYER_CLASSES.keys())
    selected_class = class_names[choice - 1]
    
    difficulty = select_difficulty()
    
    new_player = create_player(name, selected_class, difficulty)
    set_player(new_player)
    
    clear_screen()
    display_logo()
    print(f"\nBem-vindo às Runas de Avalon, {name}!")
    print(f"Você escolheu a classe: {selected_class}")
    print(f"Dificuldade: {difficulty}")
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
            mark_shop_refresh_needed(player)

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

            print("\n📦 A loja foi reabastecida com novos itens!")
        
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
                print("4. Acessar loja")
                print("5. Ver estatísticas")
                
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
                elif choice == '4':
                    display_shop(player)
                elif choice == '5':
                    display_player_statistics(player)
                else:
                    print("Opção inválida. Pressione Enter para continuar...")
                    input()
            
            if npc_index < total_npcs:
                continue
            else:
                display_victory()
                display_final_statistics(player)
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
    print(f"Dificuldade: {player.get('difficulty', 'Normal')}")

    print(f"\nNível: {player['level']}")
    print(f"Experiência: {player['exp']}/{player['exp_max']}")

    critical_percent = int(player.get('critical_chance', 0) * 100)
    print(f"\nAtributos:")
    print(f"HP: {player['hp']}/{player['hp_max']}")
    print(f"Dano base: {player['damage']}")
    print(f"Chance de crítico: {critical_percent}%")
    
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
                elif stat == "critical_chance":
                    print(f"  Crítico: {'+' if value > 0 else ''}{int(value*100)}%")
                elif stat == "heal":
                    print(f"  Cura: {value} HP")
                else:
                    print(f"  {stat}: {value}")
    
    if player.get('temp_effects'):
        print("\nEfeitos temporários ativos:")
        for effect, duration in player['temp_effects'].items():
            print(f"  {effect}: {duration} batalhas restantes")
    
    print("\nPressione Enter para voltar...")
    input()

def display_player_statistics(player):
    clear_screen()
    display_logo()
    print("\n=== ESTATÍSTICAS DO JOGADOR ===")
    
    total_battles = player.get('total_battles', 0)
    total_victories = player.get('total_victories', 0)
    total_critical_hits = player.get('total_critical_hits', 0)
    highest_damage = player.get('highest_damage', 0)
    
    win_rate = (total_victories / total_battles * 100) if total_battles > 0 else 0
    critical_rate = (total_critical_hits / total_battles * 100) if total_battles > 0 else 0
    
    print(f"\nBatalhas totais: {total_battles}")
    print(f"Vitórias: {total_victories}")
    print(f"Taxa de vitória: {win_rate:.1f}%")
    print(f"Críticos dados: {total_critical_hits}")
    print(f"Taxa de crítico: {critical_rate:.1f}%")
    print(f"Maior dano causado: {highest_damage}")
    print(f"Moedas totais: {player.get('coins', 0)}")
    print(f"Nível atual: {player['level']}")
    print(f"Dificuldade: {player.get('difficulty', 'Normal')}")
    
    print("\nPressione Enter para voltar...")
    input()

def display_final_statistics(player):
    clear_screen()
    display_logo()
    print("\n=== ESTATÍSTICAS FINAIS ===")
    
    total_battles = player.get('total_battles', 0)
    total_victories = player.get('total_victories', 0)
    total_critical_hits = player.get('total_critical_hits', 0)
    highest_damage = player.get('highest_damage', 0)
    
    win_rate = (total_victories / total_battles * 100) if total_battles > 0 else 0
    critical_rate = (total_critical_hits / total_battles * 100) if total_battles > 0 else 0
    
    print(f"\n🏆 JORNADA COMPLETA!")
    print(f"Personagem: {player['name']} ({player.get('class', 'Desconhecida')})")
    print(f"Nível final: {player['level']}")
    print(f"Dificuldade: {player.get('difficulty', 'Normal')}")
    print(f"\nEstatísticas da jornada:")
    print(f"Batalhas travadas: {total_battles}")
    print(f"Taxa de vitória: {win_rate:.1f}%")
    print(f"Críticos desferidos: {total_critical_hits}")
    print(f"Taxa de crítico: {critical_rate:.1f}%")
    print(f"Maior dano causado: {highest_damage}")
    print(f"Moedas coletadas: {player.get('coins', 0)}")
    
    if player.get('difficulty') == 'Insano':
        print(f"\n🔥 MESTRE SUPREMO! Você completou o jogo na dificuldade Insana!")
    elif player.get('difficulty') == 'Difícil':
        print(f"\n⚔️ GUERREIRO EXPERIENTE! Você venceu na dificuldade Difícil!")
    
    print("\nPressione Enter para voltar ao menu principal...")
    input()