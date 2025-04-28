import json
import os
from datetime import datetime

SAVE_DIRECTORY = "saves"
SAVE_FILE_EXTENSION = ".json"

def ensure_save_directory():
    if not os.path.exists(SAVE_DIRECTORY):
        os.makedirs(SAVE_DIRECTORY)

def get_save_filename(player_name, slot=1):
    safe_name = "".join(c for c in player_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_name = safe_name.replace(' ', '_')
    return f"{SAVE_DIRECTORY}/save_{safe_name}_slot{slot}{SAVE_FILE_EXTENSION}"

def save_game(player, inventory_data, shop_data, save_slot=1):
    ensure_save_directory()
    
    save_data = {
        "version": "2.0",
        "timestamp": datetime.now().isoformat(),
        "player": player,
        "inventory": inventory_data,
        "shop": shop_data,
        "metadata": {
            "save_slot": save_slot,
            "game_version": "2.0",
            "total_playtime": player.get("total_playtime", 0)
        }
    }
    
    filename = get_save_filename(player.get("name", "Unknown"), save_slot)
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        return True, f"Jogo salvo com sucesso em {filename}"
    except Exception as e:
        return False, f"Erro ao salvar o jogo: {str(e)}"

def load_game(player_name, save_slot=1):
    filename = get_save_filename(player_name, save_slot)
    
    if not os.path.exists(filename):
        return False, None, "Arquivo de save não encontrado"
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            save_data = json.load(f)
        
        if save_data.get("version") != "2.0":
            return False, None, "Versão do save incompatível"
        
        return True, save_data, "Jogo carregado com sucesso"
    except Exception as e:
        return False, None, f"Erro ao carregar o jogo: {str(e)}"

def get_save_list():
    ensure_save_directory()
    saves = []
    
    try:
        for filename in os.listdir(SAVE_DIRECTORY):
            if filename.endswith(SAVE_FILE_EXTENSION):
                filepath = os.path.join(SAVE_DIRECTORY, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        save_data = json.load(f)
                    
                    player_data = save_data.get("player", {})
                    metadata = save_data.get("metadata", {})
                    
                    save_info = {
                        "filename": filename,
                        "player_name": player_data.get("name", "Desconhecido"),
                        "level": player_data.get("level", 1),
                        "class": player_data.get("class", "Desconhecida"),
                        "difficulty": player_data.get("difficulty", "Normal"),
                        "timestamp": save_data.get("timestamp", ""),
                        "save_slot": metadata.get("save_slot", 1),
                        "playtime": metadata.get("total_playtime", 0)
                    }
                    saves.append(save_info)
                except:
                    continue
    except:
        pass
    
    return sorted(saves, key=lambda x: x["timestamp"], reverse=True)

def delete_save(player_name, save_slot=1):
    filename = get_save_filename(player_name, save_slot)
    
    if not os.path.exists(filename):
        return False, "Arquivo de save não encontrado"
    
    try:
        os.remove(filename)
        return True, "Save deletado com sucesso"
    except Exception as e:
        return False, f"Erro ao deletar save: {str(e)}"

def auto_save(player, inventory_data, shop_data):
    ensure_save_directory()
    
    auto_save_filename = f"{SAVE_DIRECTORY}/autosave{SAVE_FILE_EXTENSION}"
    
    save_data = {
        "version": "2.0",
        "timestamp": datetime.now().isoformat(),
        "player": player,
        "inventory": inventory_data,
        "shop": shop_data,
        "metadata": {
            "save_slot": "auto",
            "game_version": "2.0",
            "is_autosave": True
        }
    }
    
    try:
        with open(auto_save_filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

def load_auto_save():
    auto_save_filename = f"{SAVE_DIRECTORY}/autosave{SAVE_FILE_EXTENSION}"
    
    if not os.path.exists(auto_save_filename):
        return False, None, "Auto-save não encontrado"
    
    try:
        with open(auto_save_filename, 'r', encoding='utf-8') as f:
            save_data = json.load(f)
        
        return True, save_data, "Auto-save carregado com sucesso"
    except Exception as e:
        return False, None, f"Erro ao carregar auto-save: {str(e)}"

def export_statistics(player):
    ensure_save_directory()
    
    stats_filename = f"{SAVE_DIRECTORY}/stats_{player.get('name', 'player')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    stats_data = {
        "player_name": player.get("name", "Desconhecido"),
        "final_level": player.get("level", 1),
        "class": player.get("class", "Desconhecida"),
        "difficulty": player.get("difficulty", "Normal"),
        "total_battles": player.get("total_battles", 0),
        "total_victories": player.get("total_victories", 0),
        "total_critical_hits": player.get("total_critical_hits", 0),
        "highest_damage": player.get("highest_damage", 0),
        "bosses_defeated": player.get("bosses_defeated", 0),
        "coins_collected": player.get("coins", 0),
        "achievements": player.get("achievements", {}),
        "game_completed": player.get("game_completed", False),
        "export_timestamp": datetime.now().isoformat()
    }
    
    try:
        with open(stats_filename, 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, indent=2, ensure_ascii=False)
        return True, f"Estatísticas exportadas para {stats_filename}"
    except Exception as e:
        return False, f"Erro ao exportar estatísticas: {str(e)}"

def display_save_menu(player, inventory_data, shop_data):
    from models.ui import clear_screen, display_logo
    
    while True:
        clear_screen()
        display_logo()
        print("\n💾 === SISTEMA DE SAVE === 💾")
        
        print("\n1. 💾 Salvar jogo")
        print("2. 📁 Carregar jogo")
        print("3. 🗂️ Ver saves existentes")
        print("4. 🗑️ Deletar save")
        print("5. 📊 Exportar estatísticas")
        print("0. ⬅️ Voltar")
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == '0':
            return None
        elif choice == '1':
            return handle_save_game(player, inventory_data, shop_data)
        elif choice == '2':
            return handle_load_game()
        elif choice == '3':
            display_save_list()
        elif choice == '4':
            handle_delete_save()
        elif choice == '5':
            handle_export_stats(player)
        else:
            print("Opção inválida. Pressione Enter para continuar...")
            input()

def handle_save_game(player, inventory_data, shop_data):
    print("\nDigite o slot de save (1-5) ou Enter para slot 1: ", end="")
    slot_input = input().strip()
    
    try:
        save_slot = int(slot_input) if slot_input else 1
        if save_slot < 1 or save_slot > 5:
            save_slot = 1
    except ValueError:
        save_slot = 1
    
    success, message = save_game(player, inventory_data, shop_data, save_slot)
    print(f"\n{message}")
    input("Pressione Enter para continuar...")
    
    return None

def handle_load_game():
    saves = get_save_list()
    
    if not saves:
        print("\nNenhum save encontrado.")
        input("Pressione Enter para continuar...")
        return None
    
    print("\nSaves disponíveis:")
    for i, save_info in enumerate(saves, 1):
        timestamp = save_info["timestamp"][:19].replace('T', ' ')
        print(f"{i}. {save_info['player_name']} (Nível {save_info['level']}) - {save_info['class']}")
        print(f"   Dificuldade: {save_info['difficulty']} | Salvo em: {timestamp}")
    
    print("\n0. Cancelar")
    
    try:
        choice = int(input("\nEscolha um save para carregar: "))
        if choice == 0:
            return None
        elif 1 <= choice <= len(saves):
            selected_save = saves[choice - 1]
            success, save_data, message = load_game(selected_save["player_name"], selected_save["save_slot"])
            
            if success:
                print(f"\n{message}")
                input("Pressione Enter para continuar...")
                return save_data
            else:
                print(f"\nErro: {message}")
                input("Pressione Enter para continuar...")
        else:
            print("Escolha inválida.")
            input("Pressione Enter para continuar...")
    except ValueError:
        print("Por favor, digite um número válido.")
        input("Pressione Enter para continuar...")
    
    return None

def display_save_list():
    saves = get_save_list()
    
    if not saves:
        print("\nNenhum save encontrado.")
    else:
        print(f"\n📁 Saves encontrados ({len(saves)}):")
        for i, save_info in enumerate(saves, 1):
            timestamp = save_info["timestamp"][:19].replace('T', ' ')
            print(f"\n{i}. 👤 {save_info['player_name']}")
            print(f"   ⭐ Nível: {save_info['level']} | 🎭 Classe: {save_info['class']}")
            print(f"   🎯 Dificuldade: {save_info['difficulty']}")
            print(f"   📅 Salvo em: {timestamp}")
            print(f"   💾 Slot: {save_info['save_slot']}")
    
    input("\nPressione Enter para continuar...")

def handle_delete_save():
    saves = get_save_list()
    
    if not saves:
        print("\nNenhum save encontrado para deletar.")
        input("Pressione Enter para continuar...")
        return
    
    print("\nSaves disponíveis para deletar:")
    for i, save_info in enumerate(saves, 1):
        print(f"{i}. {save_info['player_name']} (Slot {save_info['save_slot']})")
    
    print("\n0. Cancelar")
    
    try:
        choice = int(input("\nEscolha um save para deletar: "))
        if choice == 0:
            return
        elif 1 <= choice <= len(saves):
            selected_save = saves[choice - 1]
            
            confirm = input(f"\nTem certeza que deseja deletar o save de {selected_save['player_name']}? (S/N): ").strip().upper()
            if confirm == 'S':
                success, message = delete_save(selected_save["player_name"], selected_save["save_slot"])
                print(f"\n{message}")
            else:
                print("\nOperação cancelada.")
        else:
            print("Escolha inválida.")
    except ValueError:
        print("Por favor, digite um número válido.")
    
    input("Pressione Enter para continuar...")

def handle_export_stats(player):
    success, message = export_statistics(player)
    print(f"\n{message}")
    input("Pressione Enter para continuar...")