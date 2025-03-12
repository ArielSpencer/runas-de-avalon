from random import randint

lista_npcs = []

def criar_npc():
  level = randint(0, 50)
  
  novo_npc = {
    "nome": f"NPC #{level}",
    "level": level,
    "dano": 5 * level,
    "hp": 100 * level,
  }
  
  return novo_npc

def gerar_npcs(n_npcs):
    for x in range(n_npcs):
        novo_npc = criar_npc()
        lista_npcs.append(novo_npc)
        

def exibir_npcs():
    for npc in lista_npcs:
        print(
          f"Nome: {npc['nome']} // Level: {npc['level']} // Dano: {npc['dano']} // HP: {npc['hp']}"
        )

gerar_npcs(10)
exibir_npcs()

