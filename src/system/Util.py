import math
import xml.sax.handler
import xml.sax
import pprint

#cambiar por vectores
#La clase Vector realiza algunas operaciones basias que ayudan a la implementacion de 
#algunas de las funciones de distancia y size del juego
class Vector:
    def __init__(self,x,y):
        self.x =x
        self.y =y
    def getUnitario(self):
        div = math.pow(self.x,2) + math.pow(self.y,2)
        div = math.sqrt(div)
        x = self.x / div
        y = self.y / div
        return Vector(x,y)
    def getMagnitud(self):
        magnitud = math.pow(self.x,2) + math.pow(self.y,2)
        magnitud = math.sqrt(magnitud)
        return magnitud
    def resta(self,vec):
        x = self.x -vec.x
        y = self.y -vec.y
        return Vector(x,y)
    def suma(self,vec):
        x = self.x +vec.x
        y = self.y +vec.y
        return Vector(x,y)
    def mulCon(self,constante):
        x = self.x * constante
        y = self.y * constante
        return Vector(x,y)
#comprueba si hay coliciones entre dos objetos
def collision(obj1, obj2): 
    limInf_obj1 = obj1.getPosicion().y + obj1.get_height()
    limSup_obj1 = obj1.getPosicion().y
    limInf_obj2 = obj2.getPosicion().y + obj2.get_height()
    limSup_obj2 = obj2.getPosicion().y

    limDer_obj1 = obj1.getPosicion().x + obj1.get_width()
    limIzq_obj1 = obj1.getPosicion().x

    limDer_obj2 = obj2.getPosicion().x + obj2.get_width()
    limIzq_obj2 = obj2.getPosicion().x

    colision_y = False
    colision_x = False
    if( (limInf_obj2 <= limInf_obj1) and (limInf_obj2 >= limSup_obj1) ):
        colision_y = True
    if( (limSup_obj2 >= limSup_obj1) and (limSup_obj2 <= limInf_obj1) ) :
        colision_y = True
    if( (limDer_obj2 >= limIzq_obj1) and (limDer_obj2 <= limDer_obj1) ) :
        colision_x = True
    if( (limIzq_obj2 >= limIzq_obj1) and (limIzq_obj2 <= limDer_obj1) ):
        colision_x = True
    if (colision_x and colision_y) :
        return True
    else:
        return False
    
class Imagen:
    def __init__(self,img,pos):
        self.sprite = img
        self.x = pos.x
        self.y = pos.y
        self.layer = 0 
#La clase radar interactual con los objetos en pantalla para obtener su posicion y al mismo tiempo
#realiza alguna de la mecanica para obtener cual objeto es mas cercano a la nave actual
class Radar:
    def __init__(self,mundo):
        self.mundo = mundo
        self.ships = []
        self.proj = []
        self.target = None
        self.oldTargets = []
        self.team = 0
        self.currentPos= None
    def setTeam(self,team):
        self.team = team
    def detectShips(self):
        self.ships = self.mundo.getShips()
        if not self.target in self.ships:
            self.target = None
        for objeto in self.oldTargets:
            if not objeto in self.ships:
                self.oldTargets.remove(objeto)
    def detectProjectiles(self):
        self.proj = self.mundo.getProj()
    def getPosTarget(self):
        if not self.target == None:
            return self.target.getCentro()
        return None
    def toggleTarget(self):
        if not self.target == None:
            self.oldTargets += [self.target]
            self.target = None
        enemies = self.getEnemies()
        for objeto in enemies:
            if not objeto in self.oldTargets:
                self.target = objeto
                
        if self.target == None:
            if len(self.oldTargets) > 0:
                self.oldTargets = []
                self.toggleTarget()
                
    def setClosestTarget(self,pos):
        enemies = self.getEnemies()
        closest = None
        distance = 999999 #infinito xD
        for objeto in enemies:
            tmp = self.getDistance(pos,objeto.posicion)
            if  tmp < distance:
                closest = objeto
                distance = tmp            
        self.target = closest
        
        self.oldTargets = [self.target]
    def getEnemies(self):
        enemies = []
        for ship in self.ships:
            if not self.team == ship.team:
                enemies += [ship]
        return enemies
    def getDistance(self,pos1,pos2):
        a = math.pow(pos1.x - pos2.x,2)
        b = math.pow(pos1.x - pos2.x,2)
        a += b
        a = math.sqrt(a)
        return a
class Propulsor:
    def __init__(self):
        self.potencia = 10
    def movRight(self):
        dir = Vector(1,0)
        fuerza = dir.mulCon(self.potencia)
        return fuerza
    def movLeft(self):
        dir = Vector(-1,0)
        fuerza = dir.mulCon(self.potencia)
        return fuerza
    def movUp(self):
        dir = Vector(0,-1)
        fuerza = dir.mulCon(self.potencia)
        return fuerza
    def movDown(self):
        dir = Vector(0,1)
        fuerza = dir.mulCon(self.potencia)
        return fuerza
class Estabilizador:
    def __init__(self):
        self.velocidad = Vector(0,0)
        self.factor = 0.20 
        self.velocidadMaxima = 100
    def estabiliza(self):
        fuerza = Vector(0,0)
        if self.velocidad.getMagnitud() > 0:
            fuerza = self.velocidad.getUnitario()
            fuerza = fuerza.mulCon(-1)
            fuerza = fuerza.mulCon(self.velocidad.getMagnitud()*self.factor)
        return fuerza        
    def update(self,velocidad):
        self.velocidad = velocidad
#clase generica pa los objetos
#en general tods los objetos en el juego que parecen en pantalla deberan tener una velocidad aceleracion
#posicion y un estado de vivos o muertos
class Object:
    def __init__(self):
        self.velocidad=None
        self.aceleracion= Vector(0,0)
        self.posicion= None
        self.masa = 1
        self.alive= None
        self.vista=0
        #estas son las imagenes cargadas del juego
        self.imagenesDelJuego = None
        #estas son imagenes particulares del objeto
        self.imagen = []
        #esta dice que imagen del arreglo es la actual
    def Update(self):
        self.velocidad = self.velocidad.suma(self.aceleracion)
        self.aceleracion = Vector(0,0)
        self.posicion = self.posicion.suma(self.velocidad)
    def aplicarFuerza(self,fuerza):
        self.aceleracion = self.aceleracion.suma(fuerza);
        self.aceleracion = self.aceleracion.mulCon(1/self.masa)
    def getView(self):
        return []
    def getCentro(self):
        inc_x = self.imagen[self.vista].get_width() / 2
        inc_y = self.imagen[self.vista].get_height() / 2
        return Vector(self.posicion.x + inc_x , self.posicion.y + inc_y )
    def get_width(self):
            return self.imagen[self.vista].get_width()
    def get_height(self):
            return self.imagen[self.vista].get_height()
    def getPosicion(self):
        return self.posicion
    
#saca las cosas el archivo de XML
#Algunos de los parametros de configuracion del juego se guardaran en archivos XML
#Esta clase toma el archivo lo parsea y responde con los datos necesarios para que la clase de 
#configuracion los ponga donde se debe
class HelixConfHandler(xml.sax.handler.ContentHandler):
  def __init__(self):
    self.width = 0
    self.height = 0
 
  def startElement(self, name, attributes):
    if name == "window":
      self.width =  attributes.get('width', None)
      self.height = attributes.get('height', None)
      
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces


def parsea():
    # Create a parser
    parser = make_parser()

    # Tell the parser we are not interested in XML namespaces
    parser.setFeature(feature_namespaces, 0)

    # Create the handler
    dh = HelixConfHandler()

    # Tell the parser to use our handler
    parser.setContentHandler(dh)

    # Parse the input
    parser.parse("helixconf.xml")
    return [dh.width, dh.height]