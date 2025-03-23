import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_logo():
    print("꧁•⊹٭ ʀᴜɴᴀꜱ ᴅᴇ ᴀᴠᴀʟᴏɴ ٭⊹•꧂")
    print("=" * 40)

def display_how_to_play():
    clear_screen()
    display_logo()
    print("\n=== COMO JOGAR ===")
    print("Runas de Avalon é um jogo de RPG de texto onde você enfrenta NPCs em batalhas.")
    print("1. Escolha sua classe: Guerreiro, Mago ou Arqueiro")
    print("2. Enfrente inimigos em batalhas por turnos")
    print("3. Ganhe experiência e suba de nível")
    print("4. Ao subir de nível, ganhe melhorias para seu personagem")
    print("5. Derrote 20 NPCs para vencer o jogo")
    print("\nDurante as batalhas:")
    print("- Seu personagem e o inimigo atacam automaticamente")
    print("- Vença o inimigo reduzindo seu HP a zero")
    print("\nPressione Enter para voltar ao menu principal...")
    input()

def display_about():
    clear_screen()
    display_logo()
    print("\n=== SOBRE ===")
    print("Runas de Avalon é um jogo de RPG de texto desenvolvido em Python.")
    print("Neste mundo místico, você é um aventureiro em busca das lendárias Runas de Avalon.")
    print("Enfrente inimigos cada vez mais poderosos e evolua seu personagem nesta jornada épica!")
    print("\nPressione Enter para voltar ao menu principal...")
    input()

def display_credits():
    clear_screen()
    display_logo()
    print("\n=== CRÉDITOS ===")
    print("Desenvolvido por Ariel Spencer")
    print("GitHub: https://github.com/ArielSpencer/runas-de-avalon")
    print("\nPressione Enter para voltar ao menu principal...")
    input()

def display_battle_header(npc_index, total_npcs, current_npc, player_show_func):
    clear_screen()
    display_logo()
    print(f"\n=== BATALHA {npc_index + 1}/{total_npcs} ===")
    print(f"Seu oponente: {current_npc['name']} (Nível {current_npc['level']})")
    print(f"HP: {current_npc['hp']} | Dano: {current_npc['damage']}")
    print("\nSeus atributos:")
    player_show_func()

def display_victory():
    clear_screen()
    display_logo()
    print("\n=== PARABÉNS AVENTUREIRO! ===")
    print("Você derrotou todos os inimigos e completou sua jornada nas Runas de Avalon!")
    print("Você se tornou uma lenda!")
    print("\nPressione Enter para voltar ao menu principal...")
    input()

def display_defeat(npc_name):
    clear_screen()
    display_logo()
    print("\n=== DERROTA ===")
    print(f"Você foi derrotado por {npc_name}!")
    print("Sua jornada termina aqui... por enquanto.")
    print("\nPressione Enter para voltar ao menu principal...")
    input()