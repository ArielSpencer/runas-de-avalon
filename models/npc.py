def create_npc(level):
    return {
        "name": f"NPC #{level}",
        "level": level,
        "damage": 5 * level,
        "hp": 100 * level,
        "hp_max": 100 * level,
        "exp": 7 * level,
    }

def generate_npcs(n_npcs):
    npc_list = []
    for x in range(n_npcs):
        new_npc = create_npc(x + 1)
        npc_list.append(new_npc)
    return npc_list

def reset_npc(npc):
    npc["hp"] = npc["hp_max"]