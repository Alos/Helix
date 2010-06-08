import pygame
import Util
import Naves
class NaveBasica(Naves.Nave):
    def __init__(self,img,pos,vel, sonidos):
        Naves.Nave.__init__(self, img, pos, vel,sonidos)
        self.vista = 4
        self.alive = True
        self.retardo = 0
        self.topeRetardo = 2
        self.movLateral = False
        self.imagen = img.imgNave
        self.acciones = None
        self.radar = None
        self.team = 1 #esto es para diferenciar entre amigo o enemigo
        self.centro= self.getCentro()
    def update(self):
       Naves.Nave.update(self)
       #self.estabilizador.update(self.velocidad)
       #self.aplicarFuerza(self.estabilizador.estabiliza())
       
       self.retardo += 1
       if pygame.K_LEFT in self.acciones:
           self.movLateral = True
           if self.vista > 0:
                   if self.retardo > self.topeRetardo:
                        self.vista = self.vista - 1
                        self.lastre = 0
    
       if pygame.K_RIGHT in self.acciones:
           self.movLateral = True
           if self.vista < 8 :
                   if self.retardo > self.topeRetardo:
                        self.vista = self.vista + 1
                        self.lastre = 0

       if not self.movLateral:
           #self.retardo += 1
           if self.retardo > self.topeRetardo:
                if self.vista < 4:
                     self.vista = self.vista + 1
                     self.retardo = 0
                if self.vista > 4:
                     self.vista = self.vista - 1
                     self.retardo = 0

       self.movLateral = False
       if not self.armas[self.armaActual]  == None:
           self.armas[self.armaActual].update()
    def repair(self):
        self.escudo.repair()
            
    def getPosArma(self):
        inc_x = self.imagen[self.vista].get_width() / 2
        #inc_y = self.imagen[self.vista].get_height() + 2
        inc_y = 5
        return Util.Vector(self.posicion.x + inc_x, self.posicion.y - inc_y)
    def getCentro(self):
        inc_x = self.imagen[self.vista].get_width() / 2
        inc_y = self.imagen[self.vista].get_height() / 2
        return Util.Vector(self.posicion.x + inc_x , self.posicion.y + inc_y )