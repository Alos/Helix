import Util
import random

                  
#############DROP GENERAL##################
class DropGeneral(Util.Object):
      def __init__(self, img, centro):
        Util.Object.__init__(self)
        self.nombre= None
        self.vista=0
        self.centro= centro
        #TODO manejar mejor la poicion del item pa que no tengas q pasar presisamente en el centro
        self.posicion=centro
        self.cont=0
        self.alive= True
        #segun yo pa q caiga pero nomas no se como
        #va a quedar la logica...se caen?
        self.velocidadDeCaida=Util.Vector(0,3)
      def update(self):
        #print self.cont
        if not self.cont == 100:
            if self.vista == 0:
                #entonces pintamos el otro
                self.vista=1
            else:
                self.vista=0
        else:
            self.alive=False
      def getView(self):
        pos_x = self.centro.x -( self.imagen[self.vista].get_width() / 2 )
        pos_y = self.centro.y -( self.imagen[self.vista].get_height() / 2 )
        self.cont+=1
        return [ Util.Imagen(self.imagen[self.vista],Util.Vector(pos_x,pos_y) ) ]



############Clases de Drops###################
class BlueRayDrop(DropGeneral):
    def __init__(self, img, centro):
        DropGeneral.__init__(self, img, centro)
        self.imagen= img.imgBlueRayDrop
        self.nombre= "BlueRay"
 
        
class LaserDrop(DropGeneral):
    def __init__(self, img, centro):
        DropGeneral.__init__(self, img, centro)
        self.imagen= img.imgLaserDrop 
        self.nombre= "Laser"
        
class PlasmaDrop(DropGeneral):
    def __init__(self, img, centro):
        DropGeneral.__init__(self, img, centro)
        self.imagen= img.imgPlasmaDrop  
        self.nombre= "Plasma" 
        
class EnergiaDrop(DropGeneral):
    def __init__(self, img, centro):
        DropGeneral.__init__(self, img, centro)
        self.imagen= img.imgEnergiaDrop  
        self.nombre= "Energia" 