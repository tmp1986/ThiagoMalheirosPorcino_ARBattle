# -*- coding: latin1 -*-
import db
from contextlib import closing

class carta():
    def __init__(self):
        self.s = db.Session()    
    
    def salva(self):
       self.s.commit()
                    
    def verifica_carta(self,pattern):
        if self.s.query(db.Carta).filter(db.Carta.pattern == pattern).count() > 0:
            return True
        else:
            return False
            
    def atualiza_carta(self,nome,ataque,defesa,classe,pattern,egg,tamanho):
       carta = self.s.query(db.Carta).filter(db.Carta.pattern == pattern).first()
       carta.nome = nome
       carta.ataque = ataque
       carta.defesa = defesa
       carta.classe = classe
       carta.egg = egg 
       carta.tamanho = tamanho
        
    def inclui_carta(self,nome,ataque,defesa,classe,pattern,egg,tamanho):            
        if self.verifica_carta(pattern):
            self.atualiza_carta(nome,ataque,defesa,classe,pattern,egg,tamanho)
        else:
            carta = db.Carta(nome,ataque,defesa,classe,pattern,egg,tamanho)
            self.s.add(carta)
            
    def lista_cartas(self):
        for carta in self.s.query(db.Carta):
            print carta 

c = carta()



c.inclui_carta( 'Elfo Azul', 10, 20, 3, 'E15.patt', 'ELFOAZUL',150)
c.inclui_carta( 'Elfo Negro', 15, 15, 3, 'E95.patt', 'ELFONEGRO',150)
c.inclui_carta( 'Elfo Branco', 8, 50, 3, 'E17.patt', 'ELFOBRANCO',150)

c.inclui_carta( 'Orc Vermelho', 30, 10, 4, 'O42.patt', 'ORCVERMELHO',150)
c.inclui_carta( 'Orc Azul', 50, 20, 4, 'O43.patt', 'ORCAZUL',150)
c.inclui_carta( 'Orc Negro', 40, 50, 4, 'O39.patt', 'ORCNEGRO',150)

c.inclui_carta( 'Cavaleiro Azul', 15, 30, 5, 'C8.patt', 'CAVALEIROAZUL',150)
c.inclui_carta( 'Cavaleiro Vermelho', 30, 10, 5, 'C9.patt', 'CAVALEIROVERMELHO',150)
c.inclui_carta( 'Cavaleiro Negro', 45, 10, 5, 'C83.patt', 'CAVALEIRONEGRO',150)
#Commit no Banco de dados
c.salva()
c.lista_cartas()    