PLAYER_CLASSES = {
    "Guerreiro": {
        "hp_max": 140,
        "damage": 22,
        "critical_chance": 0.15,
        "description": "Forte e resistente, o Guerreiro tem mais HP e chance de crítico moderada."
    },
    "Mago": {
        "hp_max": 90,
        "damage": 38,
        "critical_chance": 0.25,
        "description": "Frágil mas poderoso, o Mago causa mais dano e tem alta chance de crítico."
    },
    "Arqueiro": {
        "hp_max": 110,
        "damage": 28,
        "critical_chance": 0.20,
        "description": "Balanceado, o Arqueiro tem atributos equilibrados e boa precisão."
    },
    "Assassino": {
        "hp_max": 85,
        "damage": 32,
        "critical_chance": 0.35,
        "description": "Extremamente letal, o Assassino tem a maior chance de crítico mas é frágil."
    },
    "Paladino": {
        "hp_max": 160,
        "damage": 18,
        "critical_chance": 0.10,
        "description": "Defensor sagrado, o Paladino tem muito HP mas dano baixo."
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
                "damage": 12,
            }
        },
        {
            "id": "escudo_madeira",
            "name": "Escudo de Madeira",
            "description": "Um escudo simples que oferece alguma proteção.",
            "rarity": "comum",
            "effects": {
                "hp_max": 18,
            }
        },
        {
            "id": "espada_afiada",
            "name": "Espada Afiada",
            "description": "Uma espada com lâmina extremamente afiada.",
            "rarity": "incomum",
            "effects": {
                "damage": 22,
            }
        },
        {
            "id": "armadura_placas",
            "name": "Armadura de Placas",
            "description": "Uma armadura robusta que oferece excelente proteção.",
            "rarity": "incomum",
            "effects": {
                "hp_max": 30,
                "critical_chance": 0.05,
            }
        },
        {
            "id": "machado_guerra",
            "name": "Machado de Guerra",
            "description": "Um machado poderoso que causa dano devastador.",
            "rarity": "raro",
            "effects": {
                "damage": 35,
                "critical_chance": 0.10,
                "hp_max": -8,
            }
        },
        {
            "id": "martelo_trovao",
            "name": "Martelo do Trovão",
            "description": "Um martelo que ecoa com o poder dos trovões.",
            "rarity": "raro",
            "effects": {
                "damage": 28,
                "hp_max": 15,
                "critical_chance": 0.08,
            }
        },
        {
            "id": "espada_avalon",
            "name": "Espada de Avalon",
            "description": "Uma espada lendária imbuída com a magia antiga de Avalon.",
            "rarity": "lendário",
            "effects": {
                "damage": 55,
                "hp_max": 35,
                "critical_chance": 0.15,
            }
        },
        {
            "id": "escudo_dragao",
            "name": "Escudo do Dragão",
            "description": "Forjado com escamas de dragão ancestral.",
            "rarity": "lendário",
            "effects": {
                "hp_max": 60,
                "damage": 10,
                "critical_chance": 0.05,
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
                "damage": 15,
            }
        },
        {
            "id": "amuleto_protetor",
            "name": "Amuleto Protetor",
            "description": "Um amuleto que oferece proteção contra ataques.",
            "rarity": "comum",
            "effects": {
                "hp_max": 12,
                "critical_chance": 0.03,
            }
        },
        {
            "id": "grimorio_encantamentos",
            "name": "Grimório de Encantamentos",
            "description": "Um livro antigo contendo poderosos encantamentos.",
            "rarity": "incomum",
            "effects": {
                "damage": 25,
                "critical_chance": 0.08,
            }
        },
        {
            "id": "manto_arcano",
            "name": "Manto Arcano",
            "description": "Um manto imbuído com energia mágica.",
            "rarity": "incomum",
            "effects": {
                "hp_max": 18,
                "damage": 12,
                "critical_chance": 0.05,
            }
        },
        {
            "id": "orbe_poder",
            "name": "Orbe de Poder",
            "description": "Um orbe que amplifica o poder mágico drasticamente.",
            "rarity": "raro",
            "effects": {
                "damage": 42,
                "critical_chance": 0.12,
                "hp_max": -5,
            }
        },
        {
            "id": "varinha_fogo",
            "name": "Varinha de Fogo Eterno",
            "description": "Uma varinha que nunca perde sua chama interior.",
            "rarity": "raro",
            "effects": {
                "damage": 32,
                "hp_max": 8,
                "critical_chance": 0.10,
            }
        },
        {
            "id": "cajado_runas",
            "name": "Cajado das Runas",
            "description": "Um cajado lendário inscrito com as runas antigas de Avalon.",
            "rarity": "lendário",
            "effects": {
                "damage": 68,
                "hp_max": 25,
                "critical_chance": 0.20,
            }
        },
        {
            "id": "coroa_arcanos",
            "name": "Coroa dos Arcanos",
            "description": "Uma coroa que amplifica todos os poderes mágicos.",
            "rarity": "lendário",
            "effects": {
                "damage": 45,
                "hp_max": 30,
                "critical_chance": 0.25,
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
                "damage": 13,
                "critical_chance": 0.05,
            }
        },
        {
            "id": "arco_composto",
            "name": "Arco Composto",
            "description": "Um arco aprimorado com maior poder de penetração.",
            "rarity": "incomum",
            "effects": {
                "damage": 23,
                "critical_chance": 0.08,
            }
        },
        {
            "id": "aljava_reforçada",
            "name": "Aljava Reforçada",
            "description": "Uma aljava que permite carregar mais flechas e oferece proteção.",
            "rarity": "incomum",
            "effects": {
                "hp_max": 22,
                "damage": 8,
                "critical_chance": 0.05,
            }
        },
        {
            "id": "besta_repeticao",
            "name": "Besta de Repetição",
            "description": "Uma besta que pode disparar múltiplos projéteis.",
            "rarity": "raro",
            "effects": {
                "damage": 28,
                "critical_chance": 0.15,
                "hp_max": 5,
            }
        },
        {
            "id": "flechas_elficas",
            "name": "Flechas Élficas",
            "description": "Flechas feitas pelos elfos, extremamente letais.",
            "rarity": "raro",
            "effects": {
                "damage": 38,
                "critical_chance": 0.12,
            }
        },
        {
            "id": "arco_vento",
            "name": "Arco do Vento",
            "description": "Um arco lendário que dispara flechas com a velocidade do vento.",
            "rarity": "lendário",
            "effects": {
                "damage": 62,
                "hp_max": 28,
                "critical_chance": 0.25,
            }
        },
        {
            "id": "corda_infinita",
            "name": "Corda do Infinito",
            "description": "Uma corda de arco que nunca se rompe e sempre acerta.",
            "rarity": "lendário",
            "effects": {
                "damage": 40,
                "hp_max": 20,
                "critical_chance": 0.30,
            }
        },
    ],
    "Assassino": [
        {
            "id": "adaga_simples",
            "name": "Adaga Simples",
            "description": "Uma adaga básica, rápida e silenciosa.",
            "rarity": "comum",
            "effects": {
                "damage": 14,
                "critical_chance": 0.10,
            }
        },
        {
            "id": "capa_sombras",
            "name": "Capa das Sombras",
            "description": "Uma capa que oferece proteção e furtividade.",
            "rarity": "comum",
            "effects": {
                "hp_max": 10,
                "critical_chance": 0.08,
            }
        },
        {
            "id": "laminas_gemeas",
            "name": "Lâminas Gêmeas",
            "description": "Duas adagas perfeitamente balanceadas.",
            "rarity": "incomum",
            "effects": {
                "damage": 20,
                "critical_chance": 0.15,
            }
        },
        {
            "id": "mascara_morte",
            "name": "Máscara da Morte",
            "description": "Uma máscara que instila terror nos inimigos.",
            "rarity": "raro",
            "effects": {
                "damage": 25,
                "critical_chance": 0.20,
                "hp_max": -5,
            }
        },
        {
            "id": "punhal_veneno",
            "name": "Punhal Envenenado",
            "description": "Uma lâmina impregnada com veneno letal.",
            "rarity": "raro",
            "effects": {
                "damage": 30,
                "critical_chance": 0.18,
            }
        },
        {
            "id": "katana_sombria",
            "name": "Katana Sombria",
            "description": "Uma katana forjada nas profundezas das sombras.",
            "rarity": "lendário",
            "effects": {
                "damage": 50,
                "critical_chance": 0.35,
                "hp_max": 15,
            }
        },
    ],
    "Paladino": [
        {
            "id": "martelo_luz",
            "name": "Martelo da Luz",
            "description": "Um martelo sagrado que brilha com luz divina.",
            "rarity": "comum",
            "effects": {
                "damage": 10,
                "hp_max": 20,
            }
        },
        {
            "id": "armadura_sagrada",
            "name": "Armadura Sagrada",
            "description": "Uma armadura abençoada pelos deuses.",
            "rarity": "incomum",
            "effects": {
                "hp_max": 35,
                "critical_chance": 0.03,
            }
        },
        {
            "id": "escudo_divino",
            "name": "Escudo Divino",
            "description": "Um escudo imbuído com proteção divina.",
            "rarity": "raro",
            "effects": {
                "hp_max": 50,
                "damage": 8,
                "critical_chance": 0.05,
            }
        },
        {
            "id": "espada_justicia",
            "name": "Espada da Justiça",
            "description": "Uma espada que nunca erra quando luta pela justiça.",
            "rarity": "lendário",
            "effects": {
                "damage": 35,
                "hp_max": 45,
                "critical_chance": 0.15,
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
                "heal": 100,
            },
            "consumable": True
        },
        {
            "id": "pocao_cura_grande",
            "name": "Poção de Cura Grande",
            "description": "Restaura 200 pontos de HP.",
            "rarity": "raro",
            "effects": {
                "heal": 200,
            },
            "consumable": True
        },
        {
            "id": "pocao_forca",
            "name": "Poção de Força",
            "description": "Aumenta temporariamente o dano em 20 pontos.",
            "rarity": "incomum",
            "effects": {
                "damage_temp": 20,
            },
            "consumable": True,
            "duration": 3
        },
        {
            "id": "pocao_velocidade",
            "name": "Poção de Velocidade",
            "description": "Aumenta temporariamente a chance de crítico em 15%.",
            "rarity": "raro",
            "effects": {
                "critical_chance_temp": 0.15,
            },
            "consumable": True,
            "duration": 4
        },
        {
            "id": "amuleto_sorte",
            "name": "Amuleto da Sorte",
            "description": "Aumenta suas chances de encontrar itens raros.",
            "rarity": "raro",
            "effects": {
                "drop_chance": 1.5,
            },
            "consumable": True,
            "duration": 5
        },
        {
            "id": "elixir_experiencia",
            "name": "Elixir da Experiência",
            "description": "Dobra a experiência ganha por 3 batalhas.",
            "rarity": "raro",
            "effects": {
                "exp_multiplier": 2.0,
            },
            "consumable": True,
            "duration": 3
        },
        {
            "id": "pedra_runica",
            "name": "Pedra Rúnica de Avalon",
            "description": "Uma pedra mística com o poder das antigas runas.",
            "rarity": "lendário",
            "effects": {
                "hp_max": 25,
                "damage": 25,
                "critical_chance": 0.10,
            },
            "consumable": True,
            "duration": 5
        },
        {
            "id": "cristal_poder",
            "name": "Cristal do Poder Supremo",
            "description": "Um cristal que amplifica todas as habilidades.",
            "rarity": "lendário",
            "effects": {
                "hp_max": 30,
                "damage": 30,
                "critical_chance": 0.15,
            },
            "consumable": True,
            "duration": 3
        },
    ]
}

DROP_CHANCES = {
    "comum": 0.35,
    "incomum": 0.20,
    "raro": 0.08,
    "lendário": 0.02
}

DIFFICULTY_SETTINGS = {
    "Fácil": {
        "exp_multiplier": 1.5,
        "coin_multiplier": 1.3,
        "enemy_hp_multiplier": 0.8,
        "enemy_damage_multiplier": 0.7,
        "drop_chance_multiplier": 1.2
    },
    "Normal": {
        "exp_multiplier": 1.0,
        "coin_multiplier": 1.0,
        "enemy_hp_multiplier": 1.0,
        "enemy_damage_multiplier": 1.0,
        "drop_chance_multiplier": 1.0
    },
    "Difícil": {
        "exp_multiplier": 0.8,
        "coin_multiplier": 0.9,
        "enemy_hp_multiplier": 1.3,
        "enemy_damage_multiplier": 1.4,
        "drop_chance_multiplier": 0.8
    },
    "Insano": {
        "exp_multiplier": 0.6,
        "coin_multiplier": 0.7,
        "enemy_hp_multiplier": 1.8,
        "enemy_damage_multiplier": 2.0,
        "drop_chance_multiplier": 0.6
    }
}