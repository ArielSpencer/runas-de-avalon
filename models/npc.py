def create_npc(level):
    return {
        "name": f"NPC #{level}",
        "level": level,
        "damage": 4 * level,
        "hp": 80 * level,
        "hp_max": 80 * level,
        "exp": 9 * level,
    }

def generate_npcs(n_npcs):
    npc_list = []
    for x in range(n_npcs):
        npc_level = (x // 2) + 1
        new_npc = create_npc(npc_level)
        new_npc["name"] = f"NPC #{x + 1}"
        npc_list.append(new_npc)
    return npc_list

def reset_npc(npc):
    npc["hp"] = npc["hp_max"]