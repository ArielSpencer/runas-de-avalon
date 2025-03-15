from models.player import player
from models.npc import generate_npcs
from models.battle import start_battle

def main():
    print("꧁•⊹٭ ʀᴜɴᴀꜱ ᴅᴇ ᴀᴠᴀʟᴏɴ ٭⊹•꧂")
    npcs = generate_npcs(3)
    if npcs:  
        start_battle(player, npcs[0])

if __name__ == "__main__":
    main()