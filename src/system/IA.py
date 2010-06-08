import pygame
import Config
import random
import Util
class Copiloto:
    def __init__(self, nave):
        self.nave=nave
        
    def getAcciones(self, acciones):
        if not self.nave.posicion.x > 0 :
            self.nave.velocidad.x = 0
        if not self.nave.posicion.x < self.nave.radar.mundo.win.get_width() - self.nave.imagen[self.nave.vista].get_width():
            self.nave.velocidad.x = 0
        if not self.nave.posicion.y > 0:
            self.nave.velocidad.y = 0
        if not self.nave.posicion.y + self.nave.imagen[self.nave.vista].get_height()+15 < self.nave.radar.mundo.win.get_height():
            self.nave.velocidad.y = 0            
        for accion in acciones:
            if accion == pygame.K_LEFT: 
                if not self.nave.posicion.x > 0 :                   
                    acciones.remove(accion)
            if accion == pygame.K_RIGHT:
                if not self.nave.posicion.x < self.nave.radar.mundo.win.get_width() - self.nave.imagen[self.nave.vista].get_width():
                    acciones.remove(accion)
            if accion == pygame.K_UP:
                if not self.nave.posicion.y > 0:
                    acciones.remove(accion)
            if accion == pygame.K_DOWN:
                if not self.nave.posicion.y + self.nave.imagen[self.nave.vista].get_height()+15 < self.nave.radar.mundo.win.get_height():
                    acciones.remove(accion)           
                
        return acciones
    
class Pidgeons(Copiloto):
    def __init__(self, nave):
        self.nave=nave 
    def getAcciones(self,acciones):
        acciones= [pygame.K_DOWN, pygame.K_c, pygame.K_d]
        return acciones
    
class Snake(Copiloto):
    def __init__(self, nave):
        self.nave=nave 
        self.dios =  random.randint(-100,600)
        self.limiteX1=self.dios
        self.buda =  random.randint(100,500) 
        self.limiteX2=self.limiteX1+self.buda
        self.direccion=False
        self.nave.velocidad.y=5
    def getAcciones(self,acciones):
        if self.direccion==True:
            acciones= [pygame.K_DOWN, pygame.K_c, pygame.K_d, pygame.K_RIGHT]            
            if self.nave.posicion.x > self.limiteX2:
                self.direccion = False
        else:
            acciones= [pygame.K_DOWN, pygame.K_c, pygame.K_d, pygame.K_LEFT]
            if self.nave.posicion.x < self.limiteX1:
                self.direccion = True
        
        return acciones
    
class Alcon:
    def __init__(self, nave):
        self.nave=nave
        self.nave.estabilizador.factor = 0
        self.nuevaVelocidad= 7
        self.velocidadDeCaza=Util.Vector(0,3)
    def getAcciones(self,acciones):
        acciones= [pygame.K_c, pygame.K_d]
        if not self.nave.radar.target== None:
            if self.nave.radar.getDistance(self.nave.radar.target.posicion, self.nave.posicion) < 300:
                dir=self.nave.radar.target.posicion.resta(self.nave.posicion)
                dir= dir.getUnitario()
                self.nave.velocidad=dir.mulCon(self.nuevaVelocidad)
                self.nave.posicion = self.nave.velocidad.suma(self.nave.posicion)
            else:
                self.velocidadDeCaza=Util.Vector(0,self.nave.radar.getDistance(self.nave.radar.target.posicion, self.nave.posicion)/100)
                dir=self.nave.radar.target.posicion.resta(self.nave.posicion)
                dir= dir.getUnitario()
                self.nave.velocidad=dir.mulCon(self.nuevaVelocidad).suma(self.velocidadDeCaza)
                self.nave.posicion = self.nave.velocidad.suma(self.nave.posicion)
        return acciones
class BossIA:
    def __init__(self, nave):
        self.nave=nave 
        self.limiteX1=100
        self.limiteX2=700
        self.direccion=False
        self.nave.velocidad.y=5
        self.longRafaga = 30
        self.espera = self.longRafaga + 20
        self.contador = 0
    def getAcciones(self,acciones):
        if self.direccion==True:
            acciones= [pygame.K_c,pygame.K_RIGHT]
            if self.nave.posicion.x > self.limiteX2:
                self.direccion = False
        else:
            acciones= [pygame.K_c,pygame.K_LEFT]
            if self.nave.posicion.x < self.limiteX1:
                self.direccion = True
        if self.contador < self.longRafaga:
            acciones +=[pygame.K_d]
        if self.contador > self.espera:
            self.contador = 0
        self.contador += 1
        return acciones
    