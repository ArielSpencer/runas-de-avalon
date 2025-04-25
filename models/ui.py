import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_logo():
    print("╔═══════════════════════════════════════╗")
    print("║       ꧁•⊹٭ ʀᴜɴᴀꜱ ᴅᴇ ᴀᴠᴀʟᴏɴ ٭⊹•꧂       ║")
    print("║       ⭐ A Jornada Legendária ⭐      ║")
    print("╚═══════════════════════════════════════╝")

def display_animated_logo():
    import time
    frames = [
        "✨ A Jornada Legendária ✨",
        "🌟 A Jornada Legendária 🌟",
        "⭐ A Jornada Legendária ⭐"
    ]
    
    for frame in frames:
        clear_screen()
        print("╔═══════════════════════════════════════╗")
        print("║       ꧁•⊹٭ ʀᴜɴᴀꜱ ᴅᴇ ᴀᴠᴀʟᴏɴ ٭⊹•꧂       ║")
        print(f"║    {frame:^31}  ║")
        print("╚═══════════════════════════════════════╝")
        time.sleep(0.3)

def display_how_to_play():
    clear_screen()
    display_logo()
    print("\n🎮 === COMO JOGAR === 🎮")
    print("\nRunas de Avalon é um RPG de texto épico onde você enfrenta criaturas em batalhas intensas!")
    
    print("\n🏗️ CRIAÇÃO DE PERSONAGEM:")
    print("• Escolha entre 5 classes únicas: Guerreiro, Mago, Arqueiro, Assassino e Paladino")
    print("• Selecione o nível de dificuldade (Fácil, Normal, Difícil, Insano)")
    print("• Cada classe tem atributos e habilidades especiais diferentes")
    
    print("\n⚔️ SISTEMA DE BATALHA:")
    print("• Batalhas em turnos com sistema de dano crítico")
    print("• Cada classe tem chance diferente de causar críticos")
    print("• Enfrente 20 inimigos para completar sua jornada")
    print("• Alguns inimigos são BOSSES muito mais poderosos!")
    
    print("\n📈 PROGRESSÃO:")
    print("• Ganhe experiência derrotando inimigos")
    print("• Suba de nível para melhorar seus atributos")
    print("• Colete moedas para comprar itens na loja")
    print("• Equipe até 3 itens simultaneamente")
    
    print("\n🎒 SISTEMA DE ITENS:")
    print("• Itens têm 4 raridades: Comum, Incomum, Raro e Lendário")
    print("• Itens consumíveis oferecem efeitos temporários")
    print("• Bosses têm maior chance de dropar itens raros")
    
    print("\n📊 DIFICULDADES:")
    print("• Fácil: Mais experiência e moedas, inimigos mais fracos")
    print("• Normal: Experiência balanceada")
    print("• Difícil: Menos recompensas, inimigos mais fortes")
    print("• Insano: Desafio extremo para verdadeiros mestres!")
    
    print("\n🏆 ESTATÍSTICAS:")
    print("• Acompanhe suas vitórias, críticos e maior dano causado")
    print("• Complete o jogo para ver suas estatísticas finais")
    
    print("\nPressione Enter para voltar ao menu principal...")
    input()

def display_about():
    clear_screen()
    display_logo()
    print("\n📜 === SOBRE === 📜")
    print("\nRunas de Avalon é um jogo de RPG de texto desenvolvido em Python.")
    print("\nNeste mundo místico e perigoso, você é um aventureiro corajoso")
    print("em busca das lendárias Runas de Avalon, artefatos de poder incomensurável")
    print("espalhados pelas terras sombrias do reino.")
    
    print("\n🌟 FEATS DA VERSÃO ATUAL:")
    print("• 5 classes jogáveis com habilidades únicas")
    print("• Sistema de crítico aprimorado")
    print("• 4 níveis de dificuldade")
    print("• Tipos variados de inimigos e bosses épicos")
    print("• Sistema de itens consumíveis")
    print("• Estatísticas detalhadas de progressão")
    print("• Interface visual melhorada")
    
    print("\n🎭 HISTÓRIA:")
    print("Há muito tempo, as Runas de Avalon mantinham a paz no reino.")
    print("Quando foram espalhadas por criaturas malignas, o caos se instaurou.")
    print("Agora, apenas um herói corajoso pode reunir as runas")
    print("e restaurar a ordem no mundo!")
    
    print("\n⚡ Enfrente inimigos cada vez mais poderosos!")
    print("⚡ Evolua seu personagem nesta jornada épica!")
    print("⚡ Torne-se uma lenda de Avalon!")
    
    print("\nPressione Enter para voltar ao menu principal...")
    input()

def display_credits():
    clear_screen()
    display_logo()
    print("\n👨‍💻 === CRÉDITOS === 👨‍💻")
    print("\n🎯 Desenvolvido por: Ariel Spencer")
    print("🌐 GitHub: https://github.com/ArielSpencer/runas-de-avalon")
    print("📧 Contato: github.com/arielspencer")
    
    print("\n🛠️ TECNOLOGIAS UTILIZADAS:")
    print("• Python 3.x")
    print("• Programação orientada a objetos")
    print("• Sistema modular de arquivos")
    
    print("\n🎨 DESIGN & DESENVOLVIMENTO:")
    print("• Sistema de classes balanceado")
    print("• Mecânicas de RPG tradicionais")
    print("• Interface de texto otimizada")
    print("• Sistema de progressão envolvente")
    
    print("\nObrigado por jogar Runas de Avalon!")
    print("Pressione Enter para voltar ao menu principal...")
    input()

def display_battle_header(npc_index, total_npcs, current_npc, player_show_func):
    clear_screen()
    display_logo()
    
    encounter_num = npc_index + 1
    
    if current_npc.get("is_boss", False):
        print(f"\n💀 === BATALHA ÉPICA {encounter_num}/{total_npcs} === 💀")
        print("🔥 ATENÇÃO: BOSS DETECTADO! 🔥")
    else:
        print(f"\n⚔️ === BATALHA {encounter_num}/{total_npcs} === ⚔️")
    
    print(f"\n🎯 Seu oponente: {current_npc['name']}")
    print(f"📊 Nível {current_npc['level']} | Tipo: {current_npc.get('type', 'Desconhecido')}")
    print(f"❤️ HP: {current_npc['hp']} | ⚔️ Dano: {current_npc['damage']}")
    
    if current_npc.get("is_boss", False):
        print("💰 Bosses garantem recompensas especiais!")
    
    from models.npc import get_npc_description
    description = get_npc_description(current_npc)
    print(f"\n📝 {description}")
    
    print("\n👤 Seus atributos:")
    player_show_func()

def display_victory():
    clear_screen()
    display_animated_logo()
    
    print("\n🎉 === PARABÉNS, LENDA DE AVALON! === 🎉")
    print("\n🏆 Você derrotou todos os inimigos e completou sua jornada épica!")
    print("⭐ As Runas de Avalon foram reunidas e a paz foi restaurada!")
    print("🌟 Você se tornou uma lenda imortal!")
    
    victory_messages = [
        "🔥 Sua coragem ecoará pelos séculos!",
        "⚔️ Nenhum inimigo pôde resistir à sua força!",
        "✨ As runas antigas reconhecem sua grandeza!",
        "🛡️ Você é digno do título de Herói de Avalon!"
    ]
    
    import random
    print(f"\n{random.choice(victory_messages)}")
    
    print("\n" + "═" * 50)
    print("║          🏅 MISSÃO CUMPRIDA 🏅           ║")
    print("═" * 50)
    
    print("\nPressione Enter para ver suas estatísticas finais...")
    input()

def display_defeat(npc_name):
    clear_screen()
    display_logo()
    print("\n💀 === DERROTA === 💀")
    print(f"\n⚰️ Você foi derrotado por {npc_name}!")
    print("🌑 Sua jornada termina aqui... por enquanto.")
    print("\n💪 Mas todo herói enfrenta desafios!")
    print("🔄 Aprenda com esta experiência e tente novamente!")
    print("⚡ A próxima aventura pode ser a vitoriosa!")
    
    defeat_tips = [
        "💡 Dica: Experimente uma classe diferente!",
        "💡 Dica: Tente uma dificuldade menor!",
        "💡 Dica: Use mais itens consumíveis!",
        "💡 Dica: Equipe melhor seus itens!"
    ]
    
    import random
    print(f"\n{random.choice(defeat_tips)}")
    
    print("\nPressione Enter para voltar ao menu principal...")
    input()

def display_loading_screen(message="Carregando"):
    import time
    
    clear_screen()
    display_logo()
    print(f"\n{message}", end="")
    
    for i in range(3):
        print(".", end="", flush=True)
        time.sleep(0.5)
    
    print(" ✅")
    time.sleep(0.5)

def display_level_up_animation():
    import time
    
    clear_screen()
    
    frames = [
        "⭐ LEVEL UP! ⭐",
        "🌟 LEVEL UP! 🌟", 
        "✨ LEVEL UP! ✨",
        "💫 LEVEL UP! 💫"
    ]
    
    for frame in frames:
        clear_screen()
        display_logo()
        print("\n" + "═" * 20)
        print(f"   {frame}")
        print("═" * 20)
        time.sleep(0.3)

def display_progress_bar(current, total, description="Progresso"):
    percentage = (current / total) * 100
    filled_length = int(20 * current // total)
    bar = "█" * filled_length + "░" * (20 - filled_length)
    
    print(f"\n{description}: [{bar}] {percentage:.1f}% ({current}/{total})")

def display_rarity_color(rarity):
    rarity_symbols = {
        "comum": "⚪",
        "incomum": "🟢", 
        "raro": "🔵",
        "lendário": "🟡"
    }
    return rarity_symbols.get(rarity, "⚪")

def display_class_icon(player_class):
    class_icons = {
        "Guerreiro": "⚔️",
        "Mago": "🧙‍♂️",
        "Arqueiro": "🏹",
        "Assassino": "🗡️",
        "Paladino": "🛡️"
    }
    return class_icons.get(player_class, "⚔️")