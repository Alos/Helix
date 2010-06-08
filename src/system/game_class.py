#Version 0.2

import sys
import pygame
import random
import math

#tamano de la ventana
WIDTH     = 800
HEIGHT    = 600

# Init the graphic window
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT), True)
pygame.display.set_caption("Helix")

# Load images
fondo = pygame.Surface(win.get_size())
fondo =  pygame.image.load("fondo.png")

estrellas = pygame.Surface(win.get_size())
estrellas =  pygame.image.load("estrellas.png")

estrellas2 = pygame.Surface(win.get_size())
estrellas2 =  pygame.image.load("estrellas.png")

imgProy = pygame.image.load("laser.png")

imgEnemigo = pygame.image.load("enemigo1.png")

balaenemiga =  pygame.image.load("balaenemiga.png")

#carga la imagen de la nave
imgNave = []
for tmp in range(9):
    imgNave += [ pygame.image.load("n"+ `tmp` +".png") ]

#carga la imagen de la explosion
imgExplosion = []
for tmp in range(6):
    imgExplosion += [ pygame.image.load("exp"+`tmp`+".png") ]

#carga la imagen de la barra
imgBarra = []
for tmp in range(6):
    imgBarra += [ pygame.image.load("vida"+`tmp`+".png") ]

fin = False
npcDisparos = []
pcDisparos = []
npcEnemigos = []
acciones = []

#funcion para cargar los sonidos
def load_sound(name):
    try:
        sound = pygame.mixer.Sound(name)
        sound.play()
    except pygame.error, message:
        print "Couldn't load sound",ogg
    return None

#inicia la musica de fondo del juego
pygame.mixer.init()
musica = pygame.mixer.music.load('pandemonium.OGG')
pygame.mixer.music.play(-1,0.0)


class velocidad:
    def __init__(self,xp,yp):
        self.x = xp
        self.y = yp

class posicion:
    def __init__(self,xp,yp):
        self.x = xp
        self.y = yp

class proyectil:
    def __init__(self,pos,vel, tipo):
        self.velocidad = vel
        self.posicion = pos
        self.alive = True
        self.tipo = tipo
    def update(self):
       if self.alive :
        self.posicion.x += self.velocidad.x
        self.posicion.y += self.velocidad.y
        if self.posicion.x > win.get_width() or self.posicion.x < 0:
           self.alive = False
        if self.posicion.y > win.get_height() or self.posicion.y < 0:
           self.alive = False

    def paint(self):
       if self.alive :
        win.blit (self.tipo, (self.posicion.x, self.posicion.y))
    
    def get_centro(self):
                inc_x = imgProy.get_width() / 2
                inc_y = imgProy.get_height() / 2
                return posicion(self.posicion.x + inc_x , self.posicion.y + inc_y )    
    
    def get_width(self):
       return imgProy.get_width()
    
    def get_height(self):
       return imgProy.get_height()

#esta es la clase que contiene todo lo demas
class mundo:
    def __init__(self,ia):
        self.nuevoplaneta= True
        #las posiciones del fondo negro
        self.y=-600
        #posiciones del bg
        self.y1=0
        #la posicion de estrellas uno
        self.y2 = 0
        #la posicion de estrellas dos
        self.y3 = -600
        self.ia = ia
        self.golpes = 0
        self.puntos = 0
        self.explosiones = []
        self.barra = barra_vida(posicion(800-imgBarra[0].get_width(),20))
    #el ciclo es lo q hace el juego cada "turno"
    def ciclo(self):
        self.update()
        self.paint()
        self.ia.update()
        self.eliminaMuertos(npcDisparos)
        self.eliminaMuertos(pcDisparos)
        self.eliminaMuertos(npcEnemigos)
        self.eliminaMuertos(self.explosiones)
        #checar si sigue con vida y repintar
        for objeto in npcDisparos:
           if self.collision(miNave,objeto) or self.collision(objeto,miNave):
            self.golpes += 1
            load_sound('ex.wav')
            objeto.alive = False
            self.barra.disminuye()
            self.explosiones += [ explosion(objeto.get_centro()) ]
            #print self.golpes
        miNave.update()
        miNave.paint()

        #checar si se mato algo
        for npcObjeto in npcEnemigos:
           for pcObjeto in pcDisparos:
            if self.collision(npcObjeto,pcObjeto) or self.collision(pcObjeto,npcObjeto):
               self.puntos += 1234
               load_sound('ex.wav')
               npcObjeto.alive = False
               self.ia.murioEnemigo()
               pcObjeto.alive = False
               self.explosiones += [ explosion(npcObjeto.get_centro()) ]
               print self.puntos
        
        self.repinta(npcDisparos)
        self.repinta(pcDisparos)
        self.repinta(npcEnemigos)
        self.barra.paint()
        self.repinta(self.explosiones)

    def update(self):
        if self.nuevoplaneta == True:
            #elige un tipo de planeta (nomas hay 4 por el momento)
            dios = random.randint(1,4)    
            self.planeta =  pygame.image.load("planeta"+`dios`+".png")
            #posicion del planeta
            self.posmin= 0-self.planeta.get_height()
            self.yplaneta = random.randint(-400, self.posmin)
            self.posx = random.randint(-100, 900)
            self.nuevoplaneta = False
            #print "Planeta elegido: " + `dios`+ "Pos X: "+`self.posx`+ "Pos Y: "+`self.yplaneta`
        
        self.y2 += 5
        self.y3 += 5
        self.y1 += 2
        self.y  += 2
        self.yplaneta += 1
        
        #si las estrellitas se salen de la pantalla se mueven 
        #otras estrellista para que se vea una animacion continua
        if self.y2 > 600:
            self.y2 = 0
            self.y3 = -600
    
        if self.yplaneta > 600:
            #print "Nuevo planeta necesitado"
            self.nuevoplaneta = True
    
    def paint(self):    
        win.blit(fondo, (0,0))
        win.blit(self.planeta, (self.posx,self.yplaneta))
        win.blit(estrellas, (0,self.y2))
        win.blit(estrellas2, (0,self.y3))
#comprueba si hay coliciones entre dos objetos
    def collision(self,obj1, obj2): 
        limInf_obj1 = obj1.posicion.y + obj1.get_height()
        limSup_obj1 = obj1.posicion.y

        limInf_obj2 = obj2.posicion.y + obj2.get_height()
        limSup_obj2 = obj2.posicion.y

        limDer_obj1 = obj1.posicion.x + obj1.get_width()
        limIzq_obj1 = obj1.posicion.x

        limDer_obj2 = obj2.posicion.x + obj2.get_width()
        limIzq_obj2 = obj2.posicion.x

        colision_y = False
        colision_x = False
        if( (limInf_obj2 <= limInf_obj1) and (limInf_obj2 >= limSup_obj1) ):
           colision_y = True
        if( (limSup_obj2 >= limSup_obj1) and (limSup_obj2 <= limInf_obj1) ) :
           colision_y = True
        if( (limDer_obj1 >= limIzq_obj2) and (limDer_obj1 <= limDer_obj2) ) :
           colision_x = True
        if( (limIzq_obj1 >= limIzq_obj2) and (limIzq_obj1 <= limDer_obj2) ):
                   colision_x = True
        if (colision_x and colision_y) :
           return True
        else:
           return False
    def eliminaMuertos(self,lista):
        i=0
        while( i < len(lista) ):
            tmp = lista[i]
            if not tmp.alive:
                del lista[i]
            else:
                i = i+1
    def repinta(self,lista):
        for objeto in lista:
                        objeto.update()
                        objeto.paint()

            
class nave:
    def __init__(self, pos,vel):
        self.vista = 4
        self.posicion = pos
        self.alive = True
        self.velocidad = vel
        self.lastre = 0
        self.resorte = 2
        self.movLateral = False
        self.tempArma = 0

    def mover(self,dir):
       if dir == pygame.K_LEFT:
        self.movLateral = True
        if self.posicion.x > 0 :
            self.posicion.x = self.posicion.x - self.velocidad.x
       if dir == pygame.K_RIGHT:
        self.movLateral = True
        if self.posicion.x < 800 - imgNave[self.vista].get_width():
                        self.posicion.x = self.posicion.x + self.velocidad.x
       if dir == pygame.K_UP:
        if self.posicion.y > 0:
            self.posicion.y = self.posicion.y - self.velocidad.y

       if dir == pygame.K_DOWN:
        if self.posicion.y < 600 -imgNave[self.vista].get_height():
            self.posicion.y = self.posicion.y + self.velocidad.y

    def update(self):
       self.lastre += 1
       if pygame.K_LEFT in acciones:
        self.movLateral = True
        if self.vista > 0:
                   if self.lastre > self.resorte:
                        self.vista = self.vista - 1
                        self.lastre = 0
    
       if pygame.K_RIGHT in acciones:
        self.movLateral = True
        if self.vista < 8 :
                   if self.lastre > self.resorte:
                        self.vista = self.vista + 1
                        self.lastre = 0

        if not self.movLateral:
            self.lastre = self.lastre + self.lastre +1
            if self.lastre > self.resorte:
                   if self.vista < 4:
                     self.vista = self.vista + 1
                     self.lastre = 0
            if self.vista > 4:
                     self.vista = self.vista - 1
                     self.lastre = 0

       self.movLateral = False 
       if self.tempArma > 0:
        self.tempArma -= 1
    
    def paint(self):
        win.blit (imgNave[self.vista], (self.posicion.x, self.posicion.y))
    def get_punta(self):
        inc_x = imgNave[self.vista].get_width() / 2
        inc_y = imgNave[self.vista].get_height() +10
        return posicion(self.posicion.x + inc_x, self.posicion.y - inc_y)
    def get_centro(self):
        inc_x = imgNave[self.vista].get_width() / 2
        inc_y = imgNave[self.vista].get_height() / 2
        return posicion(self.posicion.x + inc_x , self.posicion.y + inc_y )
    def dispara(self,sp):
        if self.tempArma == 0:
            sp += [ proyectil(self.get_punta(),velocidad(0,-20), imgProy) ]
            self.tempArma = 5
            load_sound('gunshot.wav')
    def get_width(self):
        return imgNave[self.vista].get_width()
    def get_height(self):
           return imgNave[self.vista].get_height()

class enemigo:
    def __init__(self,pos,vel,sp,ia):
        self.posicion = pos
        self.velocidad = vel
        self.velDisparo = 17
        self.alive = True
        self.tempArma = 0
        self.sprites = sp
        self.ia = ia
    
    def update(self):
        self.posicion.x = self.posicion.x + self.velocidad.x
        self.posicion.y = self.posicion.y + self.velocidad.y
        self.dispara()
        self.tempArma -= 1
        if self.posicion.y > 600 :
            self.alive = False
            self.ia.termine()

    def paint(self):
        win.blit (imgEnemigo, (self.posicion.x, self.posicion.y))
    def get_punta(self):
        inc_x = imgEnemigo.get_width() / 2
        inc_y = imgEnemigo.get_height() -10 
        return posicion(self.posicion.x + inc_x, self.posicion.y + inc_y )
    def dispara(self):
                if self.tempArma == 0:
                        vel = self.calculaDisparo()            
                        self.sprites += [ proyectil(self.get_punta(),self.calculaDisparo(), balaenemiga) ]
                        self.tempArma = 19
    def calculaDisparo(self):
        a = miNave.get_centro().x - self.get_punta().x 
        b = miNave.get_centro().y - self.get_punta().y
        dividendo = math.pow(a,2) + math.pow(b,2)
        dividendo = math.sqrt(dividendo)
        a = a / dividendo
        b = b / dividendo
        resultado = velocidad(a * self.velDisparo, b * self.velDisparo)
        return resultado
    def get_centro(self):
                inc_x = imgEnemigo.get_width() / 2
                inc_y = imgEnemigo.get_height() / 2
                return posicion(self.posicion.x + inc_x , self.posicion.y + inc_y )

    def get_width(self):
        return imgEnemigo.get_width()
    def get_height(self):
           return imgEnemigo.get_height()



class IA:
    def __init__(self,sprites,spDisparo):
        self.maxEnemigos = 20
        self.dificultad = 20
        self.enemiActual = 0
        self.recursos = self.dificultad
        self.sprites = sprites
        self.spDisparo = spDisparo

    def update(self):
        if self.recursos > self.dificultad and self.enemiActual < self.maxEnemigos:
            self.sueltaEnemigo()
            self.enemiActual += 1
            self.recursos = 0
        self.recursos += 1
    
    def sueltaEnemigo(self):
        posx = random.randint(0 +imgEnemigo.get_width(), 800-imgEnemigo.get_width())
        posy = 0 - imgEnemigo.get_height()
        nuevoEnemigo = enemigo( posicion(posx,posy),velocidad(0,random.randint(10,15)),self.spDisparo,self)
        self.sprites +=[nuevoEnemigo]
    def murioEnemigo(self):
        self.enemiActual -=1
    
    def termine(self):
        self.enemiActual -= 1
class explosion:
    def __init__(self,centro):
        self.centro = centro
        self.cuadro = 0    
        self.atenuador = 0
        self.alive = True
    def update(self):
        if self.cuadro < 5 :
           if self.atenuador > 2 :
            self.cuadro +=1
            self.atenuador = 0
        else:
           self.alive = False
        self.atenuador += 1
    def paint(self):
        pos_x = self.centro.x -( imgExplosion[self.cuadro].get_width() / 2 )
        pos_y = self.centro.y -( imgExplosion[self.cuadro].get_height() / 2 )
        win.blit (imgExplosion[self.cuadro], (pos_x, pos_y))
        
        
class barra_vida:
    def __init__(self, pos):
        self.pos=pos
        self.estado=5
        self.alive=True
    def paint(self):
        win.blit (imgBarra[self.estado], (self.pos.x, self.pos.y))
    def disminuye(self):
        if self.estado > 0:
            self.estado -= 1
            if self.estado == 0:
                self.alive = False
        
miNave = nave(posicion (400,500),velocidad(15,15))
miIA = IA(npcEnemigos,npcDisparos)
miMundo = mundo(miIA)
################## Main loop

#Variables para el menu
selecciono = False
pressed = False
last_key = None
Inicio= True
pantalla_inicio = pygame.image.load("intro_inicio.png")
pantalla_salir = pygame.image.load("intro_salir.png")
win.blit(pantalla_inicio, (0,0))
pygame.display.flip()
#while del menu principal
while not selecciono:  
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
            selecciono = True
        if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_q:
            selecciono = True

           if event.key == pygame.K_UP:
            #print "UP"
            Inicio = True
            win.blit(pantalla_inicio, (0,0))
            pygame.display.flip()

           if event.key == pygame.K_DOWN:
            #print "DOWN"
            Inicio= False
            win.blit(pantalla_salir, (0,0))
            pygame.display.flip()
           elif event.key == pygame.K_s:
            if Inicio == False:
                print "Adios!"
                selecciono = True
                fin = True
            if Inicio == True:
                print "Nos Atacan!!"
                selecciono = True
                    
while not fin:
        
    if pygame.K_RIGHT in acciones:
       miNave.mover(pygame.K_RIGHT)
    if pygame.K_LEFT in acciones:
       miNave.mover(pygame.K_LEFT)
    if pygame.K_UP in acciones:
       miNave.mover(pygame.K_UP)
    if pygame.K_DOWN in acciones:
       miNave.mover(pygame.K_DOWN)
    if pygame.K_d in acciones:
       miNave.dispara(pcDisparos)
    #faltan if para las demas acciones permitidas

    # Draw the scene
    miMundo.ciclo()
    if not miMundo.barra.alive:
        fin= True
    pygame.display.flip()


    # For each event..
    for event in pygame.event.get():
      if event.type is pygame.KEYUP:
          i=0
          while( i < len(acciones) ):
           if acciones[i] == event.key:
              del acciones[i]
           else:
              i = i+1

      if event.type is pygame.KEYDOWN:
        if event.key not in acciones:
            acciones += [ event.key ]
        if event.key == pygame.K_q:
            fin = True
salio = False
go = pygame.image.load("gameover.png")
win.blit(go, (0,0))
pygame.display.flip()

while not salio:
    for event in pygame.event.get():
        if event.type is pygame.KEYDOWN:
            if event.key == pygame.K_q:
                salio = True