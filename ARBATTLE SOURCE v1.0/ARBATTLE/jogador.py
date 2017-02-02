# -*- coding: latin1 -*-
class Jogador:

    def __init__(self, nome, pontos):
        self.nome = nome
        self.pontos = pontos
        self.CartaMesa = False
        self.carta = None
        
    def ApresentaCarta(self, carta):    
        self.carta = carta
        self.CartaMesa = True
        
    def RetiraCarta(self):    
        self.carta = None
        self.CartaMesa = False 

    def VerificaCarta(self,carta):        
        if self.carta == carta and self.CartaMesa:
            return True
        else:
            return False
            
    def CartaMesa(self,carta):        
        return self.carta
        
    def IncluiPontuacao(self,ponto):
        self.pontos += ponto
        
    def RetiraPontuacao(self,ponto):
        self.pontos -= ponto    
        
    def __repr__(self):
        return "%s (%i)" % (self.nome, self.pontos)
    