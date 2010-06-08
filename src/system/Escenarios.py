import Util
import Resources
import random

class Estrella(Util.Object):
    def __init__(self,img, pos, size):
        Util.Object.__init__(self)
        self.size=size
        self.nombre= None
        if size == 0: 
            dados= random.randint(1,2)
            if dados == 1:
                self.imagen=img.estrella
                self.nombre="estrella"
            if dados == 2:
                self.imagen=img.estrella2
                self.nombre="estrella2"
        else:
            if size == 1:
                self.imagen=img.estrella2
            if size == 2:
                self.imagen=img.estrella2
            if size == 3:
                self.imagen=img.estrellaazul
                self.nombre="estrellaazul"
            if size == 4:
                self.imagen=img.estrellaamarilla
                self.nombre="estrellaamarilla"
            if size == 5:
                self.imagen=img.estrellaroja
                self.nombre="estrellaroja"
        self.posicion=pos
        self.vista=0
        self.alive=True
    def update(self):
        if self.size==0:
            self.posicion.y += 10
        else:
            self.posicion.y += 3
        
        
    def getView(self):
        return [Util.Imagen(self.imagen,self.posicion)]
    
    