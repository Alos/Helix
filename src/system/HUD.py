import pygame
import Util
import math

#La clase de mira seleciona el target mas cercano usando su radar y lo pinta
class mira:
    def __init__(self,imagen):
        self.centro = None
        self.alive = True
        #carga la imagen de la explosion
        self.imagenDeMira = imagen.imgMira
        self.imagenMiraCentro = imagen.imgMiraCentro
        self.imagenMiraTR = imagen.imgMiraTR
        self.imagenMiraTL = imagen.imgMiraTL
        self.imagenMiraBR = imagen.imgMiraBR
        self.imagenMiraBL = imagen.imgMiraBL
        
    def update(self):
        x=0

    def setCentro(self, object):
        self.centro= object.posicion
       
    def getView(self):
        posx= self.centro.x 
        posy= self.centro.y 
        return [Util.Imagen(self.imagenDeMira,Util.Vector(posx,posy))] 

#TODO Terminar la barra de vida
class barraDeVida:
    def __init__(self,imagen,posicion):
        self.imagen = imagen.imgBarra
        self.posicion = posicion
        self.estado=5
        self.alive=True
    def getView(self):
        return [Util.Imagen(self.imagen[self.estado],self.posicion)]
    def disminuye(self):
        if self.estado > 0:
            self.estado -= 1
            if self.estado == 0:
                self.alive = False
        
    def aumenta(self):
        if self.estado < 5:
            self.estado +=1
            