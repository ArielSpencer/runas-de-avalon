import random
from models.constants import DIFFICULTY_SETTINGS

NPC_TYPES = {
    "Bandido": {
        "damage_multiplier": 1.0,
        "hp_multiplier": 0.9,
        "exp_multiplier": 1.0,
        "names": ["Bandido Renegado", "Saqueador", "Ladino das Sombras", "Bandoleiro"]
    },
    "Orc": {
        "damage_multiplier": 1.2,
        "hp_multiplier": 1.1,
        "exp_multiplier": 1.1,
        "names": ["Orc Guerreiro", "Orc Berserker", "Orc Chefe", "Orc Brutal"]
    },
    "Esqueleto": {
        "damage_multiplier": 0.8,
        "hp_multiplier": 0.7,
        "exp_multiplier": 0.9,
        "names": ["Esqueleto Guerreiro", "Esqueleto Arqueiro", "Esqueleto Mago", "Ossos Sombrios"]
    },
    "Goblin": {
        "damage_multiplier": 0.7,
        "hp_multiplier": 0.6,
        "exp_multiplier": 0.8,
        "names": ["Goblin Ladino", "Goblin Xamã", "Goblin Chefe", "Goblin Assassino"]
    },
    "Troll": {
        "damage_multiplier": 1.5,
        "hp_multiplier": 1.4,
        "exp_multiplier": 1.3,
        "names": ["Troll das Montanhas", "Troll de Pedra", "Troll Gigante", "Troll Ancestral"]
    },
    "Demônio": {
        "damage_multiplier": 1.3,
        "hp_multiplier": 1.2,
        "exp_multiplier": 1.4,
        "names": ["Demônio Menor", "Demônio de Fogo", "Demônio das Trevas", "Lorde Demônio"]
    }
}

BOSS_TYPES = {
    "Dragão": {
        "damage_multiplier": 2.0,
        "hp_multiplier": 2.5,
        "exp_multiplier": 3.0,
        "names": ["Dragão de Fogo", "Dragão de Gelo", "Dragão das Sombras", "Dragão Ancião"]
    },
    "Lich": {
        "damage_multiplier": 1.8,
        "hp_multiplier": 1.5,
        "exp_multiplier": 2.5,
        "names": ["Lich Supremo", "Necromante Sombrio", "Senhor dos Mortos", "Lich Eterno"]
    },
    "Titã": {
        "damage_multiplier": 2.2,
        "hp_multiplier": 3.0,
        "exp_multiplier": 3.5,
        "names": ["Titã de Ferro", "Titã de Rocha", "Titã Celestial", "Titã Primordial"]
    }
}

def create_npc(level, difficulty="Normal", npc_type=None, is_boss=False):
    difficulty_modifiers = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["Normal"])
    
    if is_boss:
        if not npc_type:
            npc_type = random.choice(list(BOSS_TYPES.keys()))
        type_data = BOSS_TYPES[npc_type]
        name = random.choice(type_data["names"])
    else:
        if not npc_type:
            npc_type = random.choice(list(NPC_TYPES.keys()))
        type_data = NPC_TYPES[npc_type]
        name = random.choice(type_data["names"])
    
    base_damage = int(5 * level * type_data["damage_multiplier"])
    base_hp = int(90 * level * type_data["hp_multiplier"])
    base_exp = int(12 * level * type_data["exp_multiplier"])
    
    final_damage = int(base_damage * difficulty_modifiers["enemy_damage_multiplier"])
    final_hp = int(base_hp * difficulty_modifiers["enemy_hp_multiplier"])
    
    if is_boss:
        name = f"💀 {name} (BOSS)"
    
    return {
        "name": name,
        "type": npc_type,
        "level": level,
        "damage": final_damage,
        "hp": final_hp,
        "hp_max": final_hp,
        "exp": base_exp,
        "is_boss": is_boss,
        "difficulty": difficulty,
    }

def generate_npcs(n_npcs, difficulty="Normal"):
    npc_list = []
    boss_positions = [4, 9, 14, 19]
    
    for x in range(n_npcs):
        npc_level = (x // 2) + 1
        
        is_boss = (x + 1) in boss_positions
        
        if is_boss:
            new_npc = create_npc(npc_level + 2, difficulty, is_boss=True)
        else:
            new_npc = create_npc(npc_level, difficulty)
        
        new_npc["encounter_number"] = x + 1
        npc_list.append(new_npc)
    
    return npc_list

def reset_npc(npc):
    npc["hp"] = npc["hp_max"]

def get_npc_description(npc):
    descriptions = {
        "Bandido": "Um fora-da-lei perigoso que vive de saques e pilhagem.",
        "Orc": "Uma criatura brutal e selvagem, conhecida por sua força descomunal.",
        "Esqueleto": "Um morto-vivo reanimado, resistente mas não muito forte.",
        "Goblin": "Uma criatura pequena mas astuta, frequentemente subestimada.",
        "Troll": "Um gigante primitivo com força devastadora e pele resistente.",
        "Demônio": "Uma entidade maligna de outro plano, poderosa e perigosa.",
        "Dragão": "A criatura mais temível de todas, com poder ancestral.",
        "Lich": "Um mago morto-vivo de poder imensurável.",
        "Titã": "Um ser colossal de poder primordial."
    }
    
    return descriptions.get(npc.get("type", ""), "Uma criatura misteriosa.")

def generate_random_encounter():
    encounter_types = [
        {
            "name": "Caravana Perdida",
            "description": "Você encontra uma caravana abandonada.",
            "reward_type": "coins",
            "reward_value": random.randint(20, 50)
        },
        {
            "name": "Baú Esquecido",
            "description": "Um baú antigo aparece no seu caminho.",
            "reward_type": "coins",
            "reward_value": random.randint(30, 80)
        },
        {
            "name": "Comerciante Viajante",
            "description": "Um comerciante oferece suas mercadorias.",
            "reward_type": "shop_discount",
            "reward_value": 0.2
        },
        {
            "name": "Fonte Mágica",
            "description": "Uma fonte misteriosa restaura suas energias.",
            "reward_type": "heal",
            "reward_value": 0.5
        },
        {
            "name": "Templo Abandonado",
            "description": "Um templo antigo concede uma bênção temporária.",
            "reward_type": "blessing",
            "reward_value": "damage_boost"
        }
    ]
    
    return random.choice(encounter_types)