import Util
import Resources
import Proyectiles
import HUD


#Esta es la clase generica de las armas, tambien hereda de Object
class Arma(Util.Object):
    def __init__(self,img,sound):
        Util.Object.__init__(self)
        self.tempArma = 0
        self.velDisp = None
        self.imgProy = None
        self.sound = sound
        self.targetable=False
        self.mira = None
        self.hudon = False
        self.imagenesDelJuego = img
    def setVelDisparo(self,vel):
        self.velDisp = vel
    
    def update(self):
        if self.tempArma > 0:
            self.tempArma -= 1
    
    def getView(self):
        if not self.mira == None and self.hudon:
            return self.mira.getView()
        else:
            return []
    
    def setTarget(self,target):
        if not target == None:
            self.target=target
            self.mira= HUD.mira(self.img)
        else:
            self.target = None
            self.mira = None
    
    def switchHUD(self):
        if not self.hudon:
            self.hudon = True
        else:
            self.hudon = False


###########################Implementacion de armas########################
class Laser(Arma):
    def __init__(self,img,sound):
        Arma.__init__(self, img, sound)
        self.tempArma = 0
        self.constTemp = 7
        self.velDisp = 40
        self.targetable=False
        self.imgProy = img.imgProy
        
    def dispara(self,pos):
        if self.tempArma == 0:
            #ignora olimpicamente la direccion que le dieron
            #falta componer la logica de esta arma para cuando es usada
            #por un enemigo
            dir = Util.Vector(0,-1)
            vel = dir.mulCon(self.velDisp)
            self.tempArma = self.constTemp
            #self.sound.playPlasmaSound()
            return Proyectiles.RayoLaser(pos,vel,self.imgProy)
    def update(self):
        if self.tempArma > 0:
            self.tempArma -= 1
    def setTarget(self,meh):
        #nada
        x=0;
            

class PlasmaCanon(Arma):
    def __init__(self,img,sound):
        Arma.__init__(self, img, sound)
        self.velDisp = 40
        self.targetable=True
        self.target=None
        self.mira = None
        self.hudon = True
        self.imgProy = img.balaenemiga
        self.constTemp = 20
        self.sonidos=sound
    def update(self):
        if self.tempArma > 0:
            self.tempArma -= 1
        if not self.target == None:
            if not self.target.alive:
                self.target= None    
        if not self.target == None:
            #self.mira.setCentro(self.target.posicion)
            self.mira.setCentro(self.target)
        else:
            self.mira = None
    def dispara(self,pos):
           if self.tempArma == 0:
                if not self.target == None:
                   dir=self.target.getCentro().resta(pos)
                   dir=dir.getUnitario()
                else:
                    dir=Util.Vector(0,-1)
                vel= dir.mulCon(self.velDisp)
                self.tempArma= self.constTemp
                self.sound.playPlasmaSound()
                return Proyectiles.Plasma(pos,vel,self.imgProy)
    def getView(self):
        if not self.mira == None and self.hudon:
            return self.mira.getView()
        else:
            return []
    def setTarget(self,target):
        if not target == None:
            self.target=target
            self.mira= HUD.mira(self.imagenesDelJuego)
        else:
            self.target = None
            self.mira = None
            