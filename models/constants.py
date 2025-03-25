PLAYER_CLASSES = {
    "Guerreiro": {
        "hp_max": 120,
        "damage": 20,
        "description": "Forte e resistente, o Guerreiro tem mais HP mas causa menos dano."
    },
    "Mago": {
        "hp_max": 80,
        "damage": 35,
        "description": "Frágil mas poderoso, o Mago causa mais dano mas tem menos HP."
    },
    "Arqueiro": {
        "hp_max": 100,
        "damage": 25,
        "description": "Balanceado, o Arqueiro tem atributos medianos."
    }
}

ITEMS = {
    "Guerreiro": [
        {
            "id": "espada_ferro",
            "name": "Espada de Ferro",
            "description": "Uma espada básica, mas resistente.",
            "rarity": "comum",
            "effects": {
                "damage": 10,
            }
        },
        {
            "id": "escudo_madeira",
            "name": "Escudo de Madeira",
            "description": "Um escudo simples que oferece alguma proteção.",
            "rarity": "comum",
            "effects": {
                "hp_max": 15,
            }
        },
        {
            "id": "espada_afiada",
            "name": "Espada Afiada",
            "description": "Uma espada com lâmina extremamente afiada.",
            "rarity": "incomum",
            "effects": {
                "damage": 18,
            }
        },
        {
            "id": "armadura_placas",
            "name": "Armadura de Placas",
            "description": "Uma armadura robusta que oferece excelente proteção.",
            "rarity": "incomum",
            "effects": {
                "hp_max": 25,
            }
        },
        {
            "id": "machado_guerra",
            "name": "Machado de Guerra",
            "description": "Um machado poderoso que causa dano devastador.",
            "rarity": "raro",
            "effects": {
                "damage": 30,
                "hp_max": -10,
            }
        },
        {
            "id": "espada_avalon",
            "name": "Espada de Avalon",
            "description": "Uma espada lendária imbuída com a magia antiga de Avalon.",
            "rarity": "lendário",
            "effects": {
                "damage": 50,
                "hp_max": 30,
            }
        },
    ],
    "Mago": [
        {
            "id": "cajado_iniciante",
            "name": "Cajado de Iniciante",
            "description": "Um cajado básico para canalizar magia.",
            "rarity": "comum",
            "effects": {
                "damage": 12,
            }
        },
        {
            "id": "amuleto_protetor",
            "name": "Amuleto Protetor",
            "description": "Um amuleto que oferece proteção contra ataques.",
            "rarity": "comum",
            "effects": {
                "hp_max": 10,
            }
        },
        {
            "id": "grimorio_encantamentos",
            "name": "Grimório de Encantamentos",
            "description": "Um livro antigo contendo poderosos encantamentos.",
            "rarity": "incomum",
            "effects": {
                "damage": 20,
            }
        },
        {
            "id": "manto_arcano",
            "name": "Manto Arcano",
            "description": "Um manto imbuído com energia mágica.",
            "rarity": "incomum",
            "effects": {
                "hp_max": 15,
                "damage": 8,
            }
        },
        {
            "id": "orbe_poder",
            "name": "Orbe de Poder",
            "description": "Um orbe que amplifica o poder mágico.",
            "rarity": "raro",
            "effects": {
                "damage": 35,
                "hp_max": -5,
            }
        },
        {
            "id": "cajado_runas",
            "name": "Cajado das Runas",
            "description": "Um cajado lendário inscrito com as runas antigas de Avalon.",
            "rarity": "lendário",
            "effects": {
                "damage": 60,
                "hp_max": 20,
            }
        },
    ],
    "Arqueiro": [
        {
            "id": "arco_madeira",
            "name": "Arco de Madeira",
            "description": "Um arco simples, mas preciso.",
            "rarity": "comum",
            "effects": {
                "damage": 11,
            }
        },
        {
            "id": "arco_composto",
            "name": "Arco Composto",
            "description": "Um arco aprimorado com maior poder de penetração.",
            "rarity": "incomum",
            "effects": {
                "damage": 19,
            }
        },
        {
            "id": "aljava_reforçada",
            "name": "Aljava Reforçada",
            "description": "Uma aljava que permite carregar mais flechas e oferece proteção.",
            "rarity": "incomum",
            "effects": {
                "hp_max": 18,
                "damage": 5,
            }
        },
        {
            "id": "flechas_elficas",
            "name": "Flechas Élficas",
            "description": "Flechas feitas pelos elfos, extremamente letais.",
            "rarity": "raro",
            "effects": {
                "damage": 32,
            }
        },
        {
            "id": "arco_vento",
            "name": "Arco do Vento",
            "description": "Um arco lendário que dispara flechas com a velocidade do vento.",
            "rarity": "lendário",
            "effects": {
                "damage": 55,
                "hp_max": 25,
            }
        },
    ],
    "Universal": [
        {
            "id": "pocao_cura_pequena",
            "name": "Poção de Cura Pequena",
            "description": "Restaura 50 pontos de HP.",
            "rarity": "comum",
            "effects": {
                "heal": 50,
            },
            "consumable": True
        },
        {
            "id": "pocao_cura_media",
            "name": "Poção de Cura Média",
            "description": "Restaura 100 pontos de HP.",
            "rarity": "incomum",
            "effects": {
                "heal": 50,
            },
            "consumable": True
        },
        {
            "id": "pocao_cura_grande",
            "name": "Poção de Cura Grande",
            "description": "Restaura 200 pontos de HP.",
            "rarity": "raro",
            "effects": {
                "heal": 50,
            },
            "consumable": True
        },
        {
            "id": "pocao_forca",
            "name": "Poção de Força",
            "description": "Aumenta temporariamente o dano em 15 pontos.",
            "rarity": "incomum",
            "effects": {
                "damage_temp": 15,
            },
            "consumable": True,
            "duration": 3
        },
        {
            "id": "amuleto_sorte",
            "name": "Amuleto da Sorte",
            "description": "Aumenta suas chances de encontrar itens raros.",
            "rarity": "raro",
            "effects": {
                "drop_chance": 1.5,
            "consumable": True,
            "duration": 3
            }
        },
        {
            "id": "pedra_runica",
            "name": "Pedra Rúnica de Avalon",
            "description": "Uma pedra mística com o poder das antigas runas.",
            "rarity": "lendário",
            "effects": {
                "hp_max": 20,
                "damage": 20,
            "consumable": True,
            "duration": 3
            }
        },
    ]
}

DROP_CHANCES = {
    "comum": 0.3,
    "incomum": 0.15,
    "raro": 0.05,
    "lendário": 0.01
}