# -*- coding: latin-1 -*-
from conf import *
from math import *

from pandac.PandaModules import *
from panda3d.core import *
from direct.directbase import DirectStart
from direct.task import Task
from direct.actor import Actor
from direct.gui.OnscreenText import *
from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.DirectObject import DirectObject
from direct.interval.MetaInterval import Sequence
from direct.interval.FunctionInterval import Func,Wait
import cPickle, sys

import db
from carta import Carta
from jogador import Jogador
from display import Display

dbs = db.Session()
display = Display()

class ARToll():
    Pronto = False
    def Start(self):
		#Processa o video da Webcam
		#OBS WebcamVideo no Windows e OpenCVTexture no linux
		base.camLens.setNear(0.1)
		base.cam.node().getDisplayRegion(0).setSort(10)
		#render.setAttrib(CullFaceAttrib.makeReverse())
		#Exibo as opcoes de resolucao da camera
		option = WebcamVideo.getOption(6)
		self.cursor = option.open()
		self.tex = Texture('movie')
		self.cursor.setupTexture(self.tex)
		videoTextureScale = Vec2(option.getSizeX()/float(self.tex.getXSize()), option.getSizeY()/float(self.tex.getYSize()))

		#criar o card que mostra a imagem captada pela webcam
		cardMaker = CardMaker('cardMaker')
		cardMaker.setFrame(-4/3.0,4/3.0,-1,1)
		cardMaker.setUvRange(Point2(videoTextureScale[0],0), Point2(0,videoTextureScale[1]))
		card = render.attachNewNode(cardMaker.generate())
		card.setTexture(self.tex)
		card.setTwoSided(True)
		card.setY(5)
		card.setScale(1.70)
		card.setSx(-card.getSx())
		card.setBin("fixed", -1)
		card.setDepthTest(False)
		card.setDepthWrite(False)

		#Carrega a Configuracao da Camera
		self.ar = ARToolKit.make(base.cam, "./camera_para.dat", 1)
		self.Pronto = True
    
    def attachPattern(self,Pattern3D,Pattern):
        self.ar.attachPattern("Patterns\\"+Pattern, Pattern3D)   
        
class Batalha(DirectObject):
    jogador = []
    cartas = []    
    #lbjogador = None
    #dejogador = None
    backGround = []
    Pronto = False
    BatalhaIniciada = False
    JogadorInicial = None
    musicaMenu = base.loader.loadSfx("sound/menu.ogg")
	
    def __init__(self): 
        self.key()
        #Criacao das Cartas
        for c in dbs.query(db.Carta):
            self.cartas.append(Carta(c.nome, c.ataque, c.defesa, c.classe, c.pattern, c.egg, c.tamanho,c.ativo))

        #Configuracao do Panda
        base.disableMouse()
        #camera.setPosHpr(14.5, -15.4, 14, 45, -14, 0)
        #base.camera.setPos(10,-50,10)
        base.setBackgroundColor( BLACK )
        #Busca Nome do Jogador
        self.Nome()
       #self.setupLights()

    def setupLights(self):                    #Sets up some default lighting
        ambientLight = AmbientLight( "ambientLight" )
        ambientLight.setColor( Vec4(.4, .4, .35, 1) )
        directionalLight = DirectionalLight( "directionalLight" )
        directionalLight.setDirection( Vec3( 0, 8, -2.5 ) )
        directionalLight.setColor( Vec4( 0.9, 0.8, 0.9, 1 ) )
        render.setLight(render.attachNewNode( directionalLight ) )
        render.setLight(render.attachNewNode( ambientLight ) )
        
    def key(self):
        self.accept("escape", sys.exit)
        self.accept("space",  self.NovaBatalha,[0])
        
    def IniciaPartida(self):
        display.Inicia()
        display.AtulizaDisplayPartida("Inicio da partida")
        self.Pronto = True
        self.AtualizaInfoJogador()
        self.musicaMenu.stop()
        musicaBatalha = base.loader.loadSfx("sound/ost.ogg")
        musicaBatalha.setVolume(3.0)
        musicaBatalha.setLoop(True)
        musicaBatalha.play()
        
    def AtualizaInfoJogador(self):    
        for jogador in range(0,NUM_JOGADORES):
            #Verifica se o Jogador possui carta na mesa
            if  self.jogador[jogador].CartaMesa > 0:
                display.AtualizaDisplayJogador(jogador, self.jogador[jogador].nome,self.jogador[jogador].pontos,str(self.cartas[self.jogador[jogador].carta]))

            else:
                display.AtualizaDisplayJogador(jogador, self.jogador[jogador].nome,self.jogador[jogador].pontos,'')
    def configuraNome(self,nomeJogador):
        if nomeJogador == '':
            return 0            
        jgdAtual = len(self.jogador) + 1        
        self.jogador.append(Jogador(nomeJogador,0))
        self.lbjogador.setText('Informe o nome do '+str(jgdAtual+1)+'º Jogador:')
        self.dejogador.focus=1
        self.dejogador.enterText("")        

        
        if jgdAtual >= NUM_JOGADORES:
            self.lbjogador.destroy()
            self.dejogador.destroy()
            self.backGround[0].destroy()

            
    def Nome(self):
        self.backGround.append(OnscreenImage(image = 'texturas/background.png', pos = (0, 0, 0),scale = (1.8,1,1)))
        #self.backGround.append(OnscreenImage(image = 'texturas/bgright.png', pos = (1, 0, 0)))
        fontMenu = loader.loadFont('font1.ttf')
        self.lbjogador = OnscreenText(text = 'Informe o nome do 1º jogador:', font=fontMenu, style=1, fg = (0,0,0,1),shadow = DARKGRAIN , pos=(-0.7,0.1), align = TextNode.ALeft, scale = .09)
        self.dejogador = DirectEntry(text = "" ,scale=.07,focus=1,command=self.configuraNome)
        self.dejogador.setPos(Point3(-0.4,0,-0.05))
        self.musicaMenu.setVolume(3.0)
        self.musicaMenu.setLoop(True)
        self.musicaMenu.play()
     

            
    def JogadorCarta(self,carta,jogador):
        #Verifica se a carta esta disponivel
        if carta.ativo == 1:                        
            CartaIndex = self.cartas.index(carta)
            
            #Verifica se a carta já não foi associada ao jogador
            if not self.jogador[jogador].VerificaCarta(CartaIndex):
               carta.render() #Exibe o boneco vinculado a carta.
               self.jogador[jogador].ApresentaCarta(CartaIndex)
               display.AtulizaDisplayPartida( self.jogador[jogador].nome + ' apresenta '+ str(carta) )
               
			   
            #Verifica se a carta estava com o outro jogador
            for j in range(0,NUM_JOGADORES):
                #Se a carta pertencia a outro jogado, ocorre a desassociação da carta
                if j <> jogador and self.jogador[j].VerificaCarta(CartaIndex):
                    self.jogador[j].RetiraCarta()
                    display.AtulizaDisplayPartida( self.jogador[j].nome + ' fica sem carta na mesa.')
            self.AtualizaInfoJogador()    
            if self.JogadorInicial is None:
                self.JogadorInicial = jogador
        else:
            display.AtulizaDisplayPartida( 'A carta '+ str(carta) +' esta desativada.')
    
    def jogadoresPronto(self):
        for j in range(0,NUM_JOGADORES):
            if not self.jogador[j].CartaMesa:
                    return False
        return True
    
    def JogadorAtaque(self, JogadorAtq, JogadorDef):
    
        if not self.BatalhaIniciada:
            self.BatalhaIniciada = True
            
            cartaAtq = b.cartas[JogadorAtq.carta]
            cartaDef = b.cartas[JogadorDef.carta]
            
            Sequence(   
                cartaAtq.objeto3D.actorInterval('stand_out'),
                cartaAtq.objeto3D.actorInterval('atack_in'),
                cartaAtq.objeto3D.actorInterval('atack_base'),
                #cartaDef.objeto3D.actorInterval('die_in'),
                cartaDef.objeto3D.actorInterval('die_in'),
                cartaDef.objeto3D.actorInterval('die_base'),
                #Func(cartaDef.die),
                cartaAtq.objeto3D.actorInterval('stand_in'),        
                cartaAtq.objeto3D.actorInterval('stand_base'),
                #Func(display.AtulizaDisplayPartida, b.jogador[self.JogadorInicial].nome + ' venceu a partida.'),
                Func(JogadorAtq.IncluiPontuacao, 10),
                Func(JogadorDef.RetiraPontuacao, 5),
                Func(self.AtualizaInfoJogador),
                Func(self.dlgbox,'Retire da mesa as cartas da batalha anterior!',self.NovaBatalha)
                ).start()
            
           

                
    def JogadorEmpate(self, Jogador1, Jogador2):
    
        if not self.BatalhaIniciada:
            self.BatalhaIniciada = True
            
            carta1 = b.cartas[Jogador1.carta]
            carta2 = b.cartas[Jogador2.carta]
            
            Sequence(   
                carta1.objeto3D.actorInterval('stand_out'),
                carta1.objeto3D.actorInterval('atack_in'),
                carta1.objeto3D.actorInterval('atack_base'),
                #carta1.objeto3D.actorInterval('stand_in'),        
                #carta1.objeto3D.actorInterval('stand_base'),
                carta1.objeto3D.actorInterval('die_in'),
                carta1.objeto3D.actorInterval('die_base'),
                Func(Jogador1.RetiraPontuacao, 5),
                ).start()
                
            Sequence(   
                carta2.objeto3D.actorInterval('stand_out'),
                carta2.objeto3D.actorInterval('atack_in'),
                carta2.objeto3D.actorInterval('atack_base'),
               # carta2.objeto3D.actorInterval('stand_in'),        
               # carta2.objeto3D.actorInterval('stand_base'),
                carta2.objeto3D.actorInterval('die_in'),
                carta2.objeto3D.actorInterval('die_base'),
                Func(Jogador2.RetiraPontuacao, 5),
                Func(display.AtulizaDisplayPartida, 'EMPATE - Cartas com o mesmo valor de ataque e defesa.'),
                Func(self.dlgbox,'Retire da mesa as cartas da batalha anterior!',self.NovaBatalha)
                ).start()
                
    
    def NovaBatalha(self,arg):
        
        if self.BatalhaIniciada or not arg:
        
            if arg:
                self.dialogbox.cleanup()
            #display.AtulizaDisplayPartida("Retira da mesa as cartas da batalha anterior.")
            
            #Retira as cartas da mesa.
            for carta in self.cartas:                           
                carta.remrender()
                
            #Desassocia as cartas dos jogadores.
            for j in range(0,NUM_JOGADORES):
                self.jogador[j].RetiraCarta()

            #Flag que indica que a partida já foi iniciada
            self.BatalhaIniciada = False
            
            #Display da partida
            display.AtulizaDisplayPartida("Inicio da nova batalha")
            display.AtulizaDisplayPartida("Apresente novas cartas.")
        
    def dlgbox(self,msg,cmd):
        self.dialogbox = OkDialog(dialogName="Msg", text=msg, command=cmd)
        self.dialogbox.setColorScale(0.96,0.96,0.96,.85)
        
if __name__ == "__main__":
    b = Batalha()
    arToll = ARToll()    
    
    #A partida só será iniciada apos os jogadores informar seus nomes.
    def config(task):        
        if len(b.jogador)== NUM_JOGADORES:
            #Inicia o ArtoolKit
            arToll.Start()
            #Associa as Cartas aos patterns
            for carta in b.cartas:                
                arToll.attachPattern(carta.pattern3D, carta.pattern)
                carta.pattern3D.reparentTo(render)
            #Tudo Pronto já pode Iniciar a partida
            b.IniciaPartida()
            #Finaliza essa tarefa
            return Task.done
        return Task.cont      
    taskMgr.add(config, "config")

    def AudioDeathPlay(cartastr):
        pathIn = "sound/fx/"+cartastr.split(" ")[0]+"/death.ogg"             
        charSound = base.loader.loadSfx(pathIn) 
        charSound.setVolume(9.0)
        charSound.setLoop(False)
        if charSound.status() != charSound.BAD:
            charSound.play()    
        print "Som morte:"+ cartastr
    
    def batalhaTask(task):            
        
        
        #Verifica se a partida já foi iniciada e se os componentes estão prontos para iniciar a Batalha
        if arToll.Pronto and b.Pronto: 
                   
            #Atualiza o ArtollKit
            arToll.cursor.fetchIntoTexture(0, arToll.tex, 0)
            arToll.ar.analyze(arToll.tex)               
            
            #Procura por cartas que estão presente na Tela
            for carta in b.cartas:                           
                if not carta.pattern3D.isHidden():
                    jogador = carta.lado() #retorna a posição da carta lado dir oe esq
                    b.JogadorCarta(carta,jogador)
            
            #se todos estiver com carta na mese inicia a batalha            
            if b.jogadoresPronto() :
            
                carta1 = b.cartas[b.jogador[0].carta]
                carta2 = b.cartas[b.jogador[1].carta]
                
                #TODO - Organizar...
                              
               
                #Regra1 - cartas com ataque diferente
                if (carta1.ataque != carta2.ataque):
                    # verifica a carta na mesa com maior ataque
                    if (carta1.ataque > carta2.ataque):
                        b.JogadorAtaque(b.jogador[0],b.jogador[1])
                    elif (carta1.ataque < carta2.ataque):
                        b.JogadorAtaque(b.jogador[1],b.jogador[0])
                #Regra2 - cartas com ataque igual
                elif carta1.ataque == carta2.ataque:
                    # verifica a carta na mesa com maior defesa
                    if (carta1.defesa > carta2.defesa):
                        b.JogadorAtaque(b.jogador[0],b.jogador[1])
                        #path2 = "sound/fx/"+carta1.nome.split(" ")[0]+"/death.ogg"
                    elif (carta1.defesa < carta2.defesa):
                        b.JogadorAtaque(b.jogador[1],b.jogador[0])  
                        #path2 = "sound/fx/"+carta2.nome.split(" ")[0]+"/death.ogg"
                     #cartas com ataque e defesa igual
                    elif (carta1.defesa == carta2.defesa):
                        b.JogadorEmpate (b.jogador[0],b.jogador[1])
                
        
        return Task.cont      

    taskMgr.add(batalhaTask, "batalha - Task")

    run()
    