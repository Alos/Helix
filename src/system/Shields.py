import Util
import random
import HUD

                  
#############DROP GENERAL##################
class Escudo(Util.Object):
    def __init__(self,img):
        Util.Object.__init__(self)
        self.imagen=img.imgEscudo
        self.vista=6
        self.centro = None
        self.atenuador=0
        self.alive=True
        self.energia= 5
        self.hud = HUD.barraDeVida(img,Util.Vector(0,0))
    def update(self,centro):
        self.centro=centro
        if self.vista < 6 :
           if self.atenuador > 1 :
            self.vista +=1
            self.atenuador = 0
        self.atenuador += 1
    
    def getView(self):
        view = []
        if self.vista<6:
            pos_x = self.centro.x -( self.imagen[self.vista].get_width() / 2 )
            pos_y = self.centro.y -( self.imagen[self.vista].get_height() / 2 )
            view = [ Util.Imagen(self.imagen[self.vista],Util.Vector(pos_x,pos_y) ) ]
        view += self.hud.getView()
        return view
    def get_with(self):
        return self.imagen[self.vista].get_width()-10
    def get_height(self):
        return self.imagen[self.vista].get_height()-10
    def getPosicion(self):
        self.posicion = self.centro.resta(Util.Vector((self.get_width()+10)/2,(self.get_height()+10)/2))
        falso = Util.Vector(10,10)
        falso = self.posicion.suma(falso)
        return falso
    def hit(self):
        if not self.energia < 1:
            self.hud.disminuye()
            self.energia -= 1
            self.vista=0
    def repair(self):
        if self.energia < 5:
            self.hud.aumenta()
            self.energia +=1
         