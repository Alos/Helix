import Util

#Estas son la cosas que las armas disparan
#Las posiciones de x y de y estan invertidos 
class RayoLaser(Util.Object):
    def __init__(self,pos,vel,img):
        Util.Object.__init__(self)
        self.velocidad = vel
        self.posicion = pos
        self.alive = True
        self.imagen = [img]
        
    def update(self):
        if self.alive :
            self.posicion.x += self.velocidad.x
            self.posicion.y += self.velocidad.y
            #if self.posicion.x > self.limite.x or self.posicion.x < 0:
             #   self.alive = False
            #if self.posicion.y > self.limite.y or self.posicion.y < 0:
            #    self.alive = False
                
    def getView(self):
        if self.alive :
            return [ Util.Imagen(self.imagen[self.vista],self.posicion) ]
        return[]
    
    

class Plasma(Util.Object):
    def __init__(self,pos,vel,img):
        Util.Object.__init__(self)
        #print "x", self.maxx
        #print "y", self.maxy
        self.velocidad = vel
        self.posicion = pos
        self.alive = True
        self.imagen = [img]
    def update(self):
        if self.alive :
            self.posicion.x += self.velocidad.x
            self.posicion.y += self.velocidad.y
            #if self.posicion.x > self.limite.x or self.posicion.x < 0:
             #   self.alive = False
            #if self.posicion.y > self.limite.y or self.posicion.y < 0:
             #   self.alive = False
                
    def getView(self):
        if self.alive :
            return [ Util.Imagen(self.imagen[self.vista],self.posicion) ]
        return[]
    
   