import Util
class Explosion:
    def __init__(self,imagen,centro):
        self.centro = centro
        self.cuadro = 0    
        self.atenuador = 0
        self.alive = True
        #carga la imagen de la explosion
        self.img = imagen.imgExplosion

    def update(self):
        if self.cuadro < 5 :
           if self.atenuador > 1 :
            self.cuadro +=1
            self.atenuador = 0
        else:
           self.alive = False
        self.atenuador += 1
    def getView(self):
        pos_x = self.centro.x -( self.img[self.cuadro].get_width() / 2 )
        pos_y = self.centro.y -( self.img[self.cuadro].get_height() / 2 )
        return [ Util.Imagen(self.img[self.cuadro],Util.Vector(pos_x,pos_y) ) ]
        
class Estrella(Util.Object):
    def __init__(self,pos,vel,imagen,limite):
        Util.Object.__init__(self, limite)
        self.imagen = [imagen.estrella]
        self.posicion= pos
        self.velocidad = vel
        self.alive = True
        self.vista = 0
    def update(self):
        if self.alive :
            self.posicion.x += self.velocidad.x
            self.posicion.y += self.velocidad.y
            if self.posicion.x > self.limite.x or self.posicion.x < 0:
                self.alive = False
            if self.posicion.y > self.limite.y or self.posicion.y < 0:
                self.alive = False
                
    def getView(self):
        if self.alive :
            return [ Util.Imagen(self.imagen[self.vista],self.posicion) ]
        return[]