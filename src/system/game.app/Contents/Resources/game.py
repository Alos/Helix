#modulos externos usados dentro del juego
import sys
import pygame
import math
import Armas
import Util
import FXBasico
import HUD
import Niveles
import NPCNaves
import PCNaves
import Resources
import Config
import IA
#vamos por las cosas del archivo de configuracion

miConfig = Config.Config()
print miConfig.width
print miConfig.height
miVector= Util.Vector(miConfig.width , miConfig.height)
print "V:X", miVector.x
print "V:Y", miVector.y
# Init the graphic window
pygame.init()
win = pygame.display.set_mode(( miVector.x , miVector.y ), pygame.FULLSCREEN | pygame.DOUBLEBUF)
pygame.display.set_caption("Helix")
imagenes = Resources.Img(win)
sonidos = Resources.Sound()
miNivel = Niveles.NivelBase(win,imagenes,sonidos, miConfig)
miNave = PCNaves.NaveBasica(imagenes,Util.Vector(miConfig.width/2 , miConfig.height-100),Util.Vector(0,0),sonidos)
miNave.setArma(Armas.Laser(imagenes,sonidos)) 
miNave.setArma(Armas.PlasmaCanon(imagenes,sonidos))
miNave.setRadar(Util.Radar(miNivel))
copiloto= IA.Copiloto(miNave)
miNave.copiloto= copiloto
miNivel.setPC(miNave)
miNivel.inicia()