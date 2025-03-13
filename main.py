from random import randint

lista_npcs = []

player = {
  "nome": "Player",
  "level": 1,
  "exp": 0,
  "exp_max": 50,
  "hp": 100,
  "hp_max": 100,
  "dano": 25,
}

def criar_npc(level):
  
  novo_npc = {
    "nome": f"NPC #{level}",
    "level": level,
    "dano": 5 * level,
    "hp": 100 * level,
    "hp_max": 100 * level,
    "exp": 7 * level,
  }
  
  return novo_npc

def gerar_npcs(n_npcs):
    for x in range(n_npcs):
        novo_npc = criar_npc(x + 1)
        lista_npcs.append(novo_npc)
        

def exibir_npcs():
    for npc in lista_npcs:
        exibir_npc(npc)
        
def exibir_npc(npc):
    print(
          f"Nome: {npc['nome']} // Level: {npc['level']} // Dano: {npc['dano']} // HP: {npc['hp']} // Exp: {npc['exp']}"
    )
    
def exibir_player():
    print(
          f"Nome: {player['nome']} // Level: {player['level']} // Dano: {player['dano']} // HP: {player['hp']}/{player['hp_max']} // Exp: {player['exp']}/{player['exp_max']}"
    )

def iniciar_batalha(npc):
    while player["hp"] > 0 and npc["hp"] > 0:
      atacar_npc(npc)
      atacar_player(npc)
      exibir_info_batalha(npc)
      
    if player["hp"] > 0:
      print(f"Player venceu! + {npc['exp']} de EXP")
      player["exp"] += npc["exp"]
      exibir_player()
    else:
      print(f"{npc['nome']} venceu! Game Over")
      exibir_npc(npc)

def atacar_npc(npc):
    npc["hp"] -= player["dano"]
    
def atacar_player(npc):
    player["hp"] -= npc["dano"]

def exibir_info_batalha(npc):
    print(f"Player: {player['hp']}/{player['hp_max']}")
    print(f"{npc['nome']}: {npc['hp']}/{npc['hp_max']}")
    print("-----------------------------\n")

gerar_npcs(3)
# exibir_npcs()

npc_selecionado = lista_npcs[0]
iniciar_batalha(npc_selecionado)