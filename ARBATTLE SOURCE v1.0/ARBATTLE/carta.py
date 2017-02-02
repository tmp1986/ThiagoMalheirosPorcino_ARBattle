# -*- coding: latin1 -*-
from conf import *
from direct.actor import Actor
from direct.interval.MetaInterval import Sequence
from direct.interval.FunctionInterval import Func,Wait
from math import *


class Carta:

    def __init__(self, nome, ataque, defesa, classe, pattern, egg, tamanho, ativo):
        self.nome = nome
        self.ataque = ataque
        self.defesa = defesa
        self.classe = classe
        self.pattern = pattern
        self.egg = egg
        self.ativo = ativo
        
        self.tamanho = tamanho
        
        #self.pattern3D = render.attachNewNode(PandaNode("floor"))
        self.pattern3D = loader.loadModel('yup-axis')
        self.pattern3D.setScale(0.01)
        self.pattern3D.setBin("fixed", 0)
        
        #Cria o OBjeto 3D
        self.objeto3D = Actor.Actor("Eggs//"+egg,{"atack":"Eggs//"+egg+"-atack_base",
                                                "atack_out":"Eggs//"+egg+"-atack_out",
                                                "atack_in":"Eggs//"+egg+"-atack_in",
                                                "die_base":"Eggs//"+egg+"-die_base",
                                                "die_in":"Eggs//"+egg+"-die_in",
                                                "stand_base":"Eggs//"+egg+"-stand_base",
                                                "stand_in":"Eggs//"+egg+"-stand_in",
                                                "stand_out":"Eggs//"+egg+"-stand_out"})
        self.objeto3D.reparentTo(render)
        #self.objeto3D.setScale(tamanho)
        self.objeto3D.setBin("fixed", 0)
       
        #animacao  
        self.objeto3D.attack = Sequence(   
        self.objeto3D.actorInterval('stand_out'),
        self.objeto3D.actorInterval('atack_in'),
        self.objeto3D.actorInterval('atack_base')
        )

        self.objeto3D.stand_base = Sequence(
        self.objeto3D.actorInterval('stand_base',
        ))
        
        self.objeto3D.stand = Sequence(
        self.objeto3D.actorInterval('stand_in'),        
        self.objeto3D.actorInterval('stand_base'),
        Func(self.stand)        )
        
        self.objeto3D.die = Sequence(
        self.objeto3D.actorInterval('die_in'))

       
        
    def __repr__(self):
        return "%s \n(A=%i, D=%i, C=%i)" % (self.nome, self.ataque, self.defesa, self.classe)
    
    def render(self):
        
        self.objeto3D.setScale(self.pattern3D.getScale()*self.tamanho)
        self.objeto3D.setPos(self.pattern3D.getPos())
 
        self.PlayInAudio();
 
        if self.lado() == 0:
            if (fabs(self.pattern3D.getP()) < fabs(self.pattern3D.getR())):
                self.objeto3D.setHpr (90, fabs(self.pattern3D.getP())*-1,fabs(self.pattern3D.getR())*-1)
            else:
                self.objeto3D.setHpr (90, fabs(self.pattern3D.getR())*-1,fabs(self.pattern3D.getP())*-1)
        else:
            if (fabs(self.pattern3D.getP()) < fabs(self.pattern3D.getR())):
                self.objeto3D.setHpr (-90, fabs(self.pattern3D.getP()),fabs(self.pattern3D.getR()))
            else:
                self.objeto3D.setHpr (-90, fabs(self.pattern3D.getR()),fabs(self.pattern3D.getP()))                            
        self.objeto3D.reparentTo(render)
        #self.objeto3D.stand.start()
        #self.objeto3D.stand_base.loop()
        self.objeto3D.loop("stand_base")
        self.objAnimName = "stand"
        self.objeto3D.show()

        
        if DEBUG:
            print self.nome
            print 'Hpr | PT  = (%.2f,%.2f,%.2f) / BC = (%.2f,%.2f,%.2f)' %(self.pattern3D.getH(),self.pattern3D.getP(),self.pattern3D.getR(),
                                                                           self.objeto3D.getH(),self.objeto3D.getP(),self.objeto3D.getR())
            print 'Pos | PT  = (%.2f,%.2f,%.2f) / BC = (%.2f,%.2f,%.2f)' %(self.pattern3D.getX(),self.pattern3D.getY(),self.pattern3D.getZ(),
                                                                        self.objeto3D.getX(),self.objeto3D.getY(),self.objeto3D.getZ())
    def remrender(self):   
        #self.objeto3D.destroy()
        self.objeto3D.hide() 
    
    def lado(self):                                                                      
        x, y, z = self.pattern3D.getPos() 
        #Verifica a qual lado a carta está posicionada direito ou esquerdo 
        if x > 0:
            lado = 1
        else:
            lado = 0

        return lado
        
    def setAnim(self,animName):       
    
        self.objAnimName = animName 
        #Anim = self.objeto3D.actorInterval(self.objAnimName,playRate=5)
        #Anim.start()
        self.objeto3D.play(self.objAnimName)
        self.objeto3D.stop()
        #self.objeto3D.play('stand')
        #attack1 = carta.objeto3D.actorInterval("atack",playRate=5)
        
    def getCurrentAnim(self):
        return self.objAnimName
        
    def atack(self):    
        if not self.objeto3D.attack.isPlaying() and self.getCurrentAnim() != "attack":  
            self.objAnimName = 'attack'
            self.objeto3D.attack.start()
            
        #self.setAnim('stand')
        #carta.objeto3D.loop("atack")
        #self.eve.actorInterval("walk", playRate = 2).loop()
        
    def die(self):
        self.objeto3D.stand.stop()
        self.objeto3D.die_in.loop()
        
    def stand(self):
        #if not self.objeto3D.stand_base.isPlaying() and self.getCurrentAnim() != "stand":
        self.objAnimName = 'stand'     
        self.objeto3D.stand_base.loop()
        

    def PlayInAudio(self):
        pathIn = "sound/fx/"+self.nome.split(" ")[0]+"/in.ogg"             
        charSound = base.loader.loadSfx(pathIn) 
        charSound.setVolume(9.0)
        charSound.setLoop(False)
        if charSound.status() != charSound.BAD:
            charSound.play()    
        print str(charSound.status())
    
