# -*- coding: latin1 -*-
from pandac.PandaModules import *
from direct.gui.OnscreenText import *
from direct.gui.DirectGui import *
from conf import *

class Display:
	displayJogador = []
	displayPontos = []
	displayPartida = []
	displayInfo = []
	displayCarta = []

	
	#font = loader.loadFont('arial.egg')
	def DisplayInfo(self):
		#for i in range(0, MAX_LINHAS_INF):
		self.displayInfo.append(OnscreenImage(image = 'texturas/bggametop.png', pos = (0, 0,0.8),scale = (1.8,0.2,0.2)))
		#self.displayInfo.append ( OnscreenText( text = 'ESC: Sair',style=2, pos = (LIMITX[0]-0.3, LIMITY[0]-.05), fg=(1,1,1,1), align = TextNode.ALeft, scale = .05, wordwrap=15))
			
	def DisplayPartida(self):
		for i in range(0, MAX_LINHAS_PARTIDA):
			fontMenu = loader.loadFont('font1.ttf')
			self.displayPartida.append ( OnscreenText( pos = (LIMITX[1], LIMITY[0]-.062*i), fg=(0,0,0,1),font=fontMenu, align = TextNode.ALeft, scale = .03))

	def DisplayJogador(self):
		self.displayInfo.append(OnscreenImage(image = 'texturas/bggamebottom.png', pos = (0, 0,-0.8),scale = (1.8,0.2,0.2)))
		for i in range(0,NUM_JOGADORES):
			if i == 0:
				posx = LIMITX[1] + 0.10
			else:
				posx = LIMITX[0] - 0.95 
			
			fontMenu = loader.loadFont('font1.ttf')
			
			self.displayJogador.append (OnscreenText(text = 'Nome: ', style=1,font=fontMenu, pos=(posx,LIMITY[1] +.22 ), fg=(0,0,0,1), align = TextNode.ALeft, scale = .09))
			self.displayPontos.append(OnscreenText(text = 'Pontos: ', style=1, font=fontMenu, pos=(posx,LIMITY[1]+.13), fg=(0,0,0,1), align = TextNode.ALeft, scale = .09))
			self.displayCarta.append(OnscreenText(text = '', style=1, font=fontMenu, pos=(posx,LIMITY[1]+.07), fg=(0,0,0,1), align = TextNode.ALeft, scale = .06))

	def AtulizaDisplayPartida(self, text):
		for i in range(0, MAX_LINHAS_PARTIDA-1):
			self.displayPartida[i].setText(self.displayPartida[i+1].getText())

		self.displayPartida[MAX_LINHAS_PARTIDA-1].setText(text)

	def AtualizaDisplayJogador(self,Jogador,Nome,Pontos,Carta):
		if len(self.displayPontos)==0:
			self.DisplayJogador()

		self.displayJogador[Jogador].setText('Nome: '+ Nome)
		self.displayPontos[Jogador].setText('Pontos: '+ str(Pontos))
		self.displayCarta[Jogador].setText(''+ Carta)
		
		
	def Coordenadas_XY(self):
		for i in range(-20,20):
			OnscreenText(text = '.'+ '%.1f' % (i/float(10)), pos = (0, i/float(10)), scale = 0.05, fg=(1,1,1,1))
		for i in range(-20,20):
			OnscreenText(text = '.' , pos = (i/float(10), 0), scale = 0.05, fg=(1,1,1,1))
			if i <> 0:
				OnscreenText(text = '%.1f' % (i/float(10)) , pos = (i/float(10),0.05), scale = 0.05, fg=(1,1,1,1))
			
		OnscreenText(text = 'X', pos = (LIMITX[0]-.03, .1), scale = 0, fg=(1,1,1,1))
		OnscreenText(text = 'Y', pos = (.1, LIMITY[0]-.03), scale = 0, fg=(1,1,1,1))           
		  

	def Inicia(self):
		if DEBUG:
			self.Coordenadas_XY()
		self.DisplayInfo()
		self.DisplayPartida()
		
		
		