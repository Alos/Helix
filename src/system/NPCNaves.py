import Util
import pygame
import Naves


class Andromeda(Naves.Nave):
    def __init__(self,img,vel,pos,sonidos):
        Naves.Nave.__init__(self, img, pos, vel,sonidos)
        self.imagen = [img.imgEnemigo]
        self.team = 10 #friend or foe       
        self.vista=0
        self.escudo.energia=0
        self.estabilizador.factor =1
    def update(self):
        #TODO cambiar por la posicion de la pantalla despues
        #if self.posicion.y > self.limite.y:
            #self.alive = False
        Naves.Nave.update(self)
        if not self.armas[self.armaActual]  == None:
           self.armas[self.armaActual].update()
        if not self.radar == None:
           self.radar.detectShips()
    def setArma(self,arma): 
            arma.switchHUD()
            arma.constTemp = 60
            arma.velDisp = 20
            self.armas += [arma]
    
    def getPosArma(self):
        inc_x = self.imagen[self.vista].get_width() / 2
        inc_y = self.imagen[self.vista].get_height() -10 
        return Util.Vector(self.posicion.x + inc_x, self.posicion.y + inc_y )

class Boss1(Naves.Nave):
    def __init__(self,img,vel,pos,sonidos):
        Naves.Nave.__init__(self, img, pos, vel,sonidos)
        self.imagen = [img.imgJefe]
        self.team = 10 #friend or foe       
        self.vista=0
        self.escudo.energia=0
        self.estabilizador.factor =1
    def update(self):
        #TODO cambiar por la posicion de la pantalla despues
        #if self.posicion.y > self.limite.y:
            #self.alive = False
        Naves.Nave.update(self)
        if not self.armas[self.armaActual]  == None:
           self.armas[self.armaActual].update()
        if not self.radar == None:
           self.radar.detectShips()
    def setArma(self,arma): 
            arma.switchHUD()
            arma.constTemp = 60
            arma.velDisp = 20
            self.armas += [arma]
    
    def getPosArma(self):
        inc_x = self.imagen[self.vista].get_width() / 2
        inc_y = self.imagen[self.vista].get_height() -10 
        return Util.Vector(self.posicion.x + inc_x, self.posicion.y + inc_y )