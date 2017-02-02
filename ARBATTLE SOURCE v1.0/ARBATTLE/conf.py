# -*- coding: latin1 -*-
from panda3d.core import ConfigVariableString
from panda3d.core import ConfigVariableBool

#PROJECT
PROJECT_NAME    = 'ARBattle'
VERSION         =  '1.0'
DEBUG           = False
TRACELEVEL      = 0

#GAME
MAX_LINHAS_PARTIDA  = 4
MAX_LINHAS_INF  = 1
NUM_JOGADORES   = 2 #Não
NUM_PARTIDAS    = 3

#Tela
FULLSCREEN      = True
WINSIZE         = [1280,720] #800,600 #1280,720 #1920,1080

if  float(WINSIZE[1])/float(WINSIZE[0])   ==  0.75:
    LIMITX      = [1.3, -1.3]   #4:3 
else:  
    LIMITX      = [1.75, -1.75] #16:9
LIMITY          = [.95, -.95]

#Cores 
LIGHTBLUE       = (0.27,0.51,0.71,1)
DODGEBLUE       = (0.11,0.53,0.93,1)
DARKGRAIN       = (0.5,0.5,0.5,0.5)
OLIVE           = (0.33,0.42,0.18,1)
YELLOWGREEN     = (0.60,0.80,0.20,1)
KHAKI           = (0.74,0.72,0.42,1)
FIREBRICK       = (0.70,0.13,0.13,1)
MARRON          = (0.69,0.19,0.38,1)
VIOLET          = (0.78,0.08,0.52,1)
BROWN           = (0.55,0.27,0.07,1)
SNOW            = (0.55,0.27,0.07,1)
GOLD            = (1,0.84,0,1)
RED             = (1,0,0,1)
GREEN           = (0,1,0,1)
BLUE            = (0,0,1,1)
BLACK           = (0,0,0,1)
WHITE           = (1,1,1,1)


#PANDA
#www.panda3d.org/manual/index.php/List_of_all_config_variables
ConfigVariableString("window-title",'Panda').setStringValue(PROJECT_NAME +' - '+VERSION )

ConfigVariableBool  ('fullscreen', 0).setValue(FULLSCREEN)
ConfigVariableString('win-size', '640 480').setValue(str(WINSIZE[0])+' '+str(WINSIZE[1]))
ConfigVariableBool  ('show-frame-rate-meter', '').setValue(DEBUG)

#ConfigVariableString('load-display', 'pandagl').setValue('pandagl') #pandagl, pandadx9, pandadx8, tinydisplay 
#ConfigVariableString ('aux-display', 'pandagl').setValue('pandagl')  #pandagl, pandadx9, pandadx8, tinydisplay 
#ConfigVariableBool  ('undecorated', '').setValue(True)

   
   
   

