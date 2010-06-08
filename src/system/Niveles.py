import Util
import random
import pygame
import Armas
import IA
import NPCNaves
import FXBasico
import Naves
import Items
import Shields
import Escenarios
class NivelBase:
    def __init__(self,win,img,sonidos,conf):
        self.conf= conf
        self.nuevoplaneta= True
        self.pausado = False
        self.inicio = True
        #posiciones del bg
        sonidos.iniciaMusica()
        self.fondo = pygame.Surface(win.get_size())
        self.fondo = self.fondo.convert()
        self.fondo.fill((0,0,0))
        self.win = win
        self.img = img
        self.sonidos = sonidos
        self.pc = []
        self.npc =[]
        self.pcProy = []
        self.npcProy = []
        self.FX = []
        self.drop= []
        #self.ia = ia
        self.acciones=None
        self.golpes = 0
        self.puntos = 0
        self.hb = Guion()
        self.estrellas= []
        self.posicionestrella=0
        for tmp in range(20):
            self.posicionestrella= Util.Vector(random.randint(0, win.get_width()), random.randint(0, win.get_height())) 
            self.estrellas += [ Escenarios.Estrella(self.img,self.posicionestrella, 0) ]
        
        self.estrellitas= []
        self.posicionestrella2=0
        for tmp in range(300):
            self.posicionestrella2= Util.Vector(random.randint(0, win.get_width()), random.randint(0, win.get_height()))
            self.dados = random.randint(1,4) 
            self.estrellitas += [ Escenarios.Estrella(self.img,self.posicionestrella2, self.dados) ]
        
        self.estrellasrojas= []
        self.posicionestrella2=0
        for tmp in range(100):
            self.posicionestrella2= Util.Vector(random.randint(0, win.get_width()/2), random.randint(0, win.get_height()/2))
            self.dados = random.randint(1,4) 
            self.estrellasrojas += [ Escenarios.Estrella(self.img,self.posicionestrella2, 5) ]
            
            
    def inicia(self):
        acciones = []
        self.fin = False
        clock = pygame.time.Clock()
        FPS = 25        
        while not self.fin:
            dt = clock.tick(FPS)
            if not self.pausado:
                for objeto in self.pc:
                    proy = objeto.mover(acciones)
                    for objeto in proy:
                        self.addPCProy(objeto)
                for objeto in self.npc:
                    proy = objeto.mover([])
                    for objeto in proy:
                        self.addNPCProy(objeto)
                # Draw the scene
                self.ciclo(acciones)
                pygame.display.flip()
                if self.inicio :
                    self.pausado = True
                    self.inicio = False
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
                        self.fin = True
                    if event.key == pygame.K_p:
                        if self.pausado:
                            self.pausado = False
                        else:
                            self.pausado = True
                    if event.key == pygame.K_r:
                        self.hb.estado = 0
    def setPC(self,pc):
        self.pc += [pc]       
    def addNPC(self,npc):
        self.npc += npc
    def addPCProy(self,proy):
        self.pcProy += [proy]        
    def addNPCProy(self,proy):
        self.npcProy += [proy]
        
    def getShips(self):
        return self.npc + self.pc
    def getProj(self):
        return self.npcProy + self.pcProy
        
    def ciclo(self,acciones):
        self.acciones = acciones
        self.update()        
        #self.ia.update()
        #se checan y eliminan elementos fuera de la pantalla
        #proyectiles
        for objeto in self.npcProy:
            if objeto.posicion.x > self.win.get_width() or objeto.posicion.x < 0:
                objeto.alive = False
            if objeto.posicion.y > self.win.get_height() or objeto.posicion.y < 0:
                objeto.alive = False
        for objeto in self.pcProy:
            if objeto.posicion.x > self.win.get_width() or objeto.posicion.x < 0:
                objeto.alive = False
            if objeto.posicion.y > self.win.get_height() or objeto.posicion.y < 0:
                objeto.alive = False
        #naves npc
        for objeto in self.npc:
            if objeto.posicion.y > self.win.get_height():
                objeto.alive = False
        self.eliminaMuertos(self.npcProy)
        self.eliminaMuertos(self.pcProy)
        self.eliminaMuertos(self.npc)
        self.eliminaMuertos(self.FX)
        self.eliminaMuertos(self.drop)
        #checar si sigue con vida y repintar
        for objeto in self.npcProy:
            if Util.collision(self.pc[0],objeto) or Util.collision(objeto,self.pc[0]):
                self.golpes += 1
                self.sonidos.playBoom()
                objeto.alive = False
                
                #self.barra.disminuye()
                if self.pc[0].escudo.energia < 1:
                    self.fin = True
                self.pc[0].hit(Util.Vector(0,0))
                
                #self.FX += [ FXBasico.Explosion(self.img,objeto.get_centro()) ]
               # print self.golpes
        
        #Rutina que chica si hay colicion con alguno de los items en la pantalla
        for objeto in self.drop:
            if Util.collision(self.pc[0],objeto) or Util.collision(objeto,self.pc[0]):
                #ponerle un sonidito pa cuando lo recupere y hacerle algo al 
                #estatus de la nave                
                #self.sonidos.playBoom()
                objeto.alive = False
                self.pc[0].repair()
                print "Recibimos un drop de tipo"
                print objeto.nombre
                
               
        #checar si se mato algo
        for npcObjeto in self.npc:
            for pcObjeto in self.pcProy:
                if Util.collision(npcObjeto,pcObjeto) or Util.collision(pcObjeto,npcObjeto):
                    #le sumamos los puntos y tocamos un boom
                    self.puntos += 123
                    if npcObjeto.escudo.energia < 1:
                        npcObjeto.alive = False
                        self.sonidos.playBoom()
                        self.FX += [ FXBasico.Explosion(self.img,pcObjeto.getCentro()) ]
                        #sacamos un drop
                        #self.drop += [Items.BlueRayDrop(self.img,pcObjeto.get_centro())]
                        #cuando ocure la muerte de una nave se elige un nuevo drop, se cambia el estado de 
                        #currentDrop por el item selecionado y tambien se debera cambiar la imagen a la adecuada
                        dios = random.randint(0,15)#ajustar esta probabilidad con algo pensado
                        if dios == 1 or dios ==2 or dios==3:
                            self.drop += [Items.EnergiaDrop(self.img,pcObjeto.getCentro())]
                    else:
                        npcObjeto.hit(Util.Vector(0,0))
                    pcObjeto.alive = False                    
                    print self.puntos
        #if len(self.npc) < 3:
        self.creaNPC() #esto alguien mas lo tiene que hacer
        self.paint()
        #print self.pcProy
    def eliminaMuertos(self,lista):
        i=0
        while( i < len(lista) ):
            tmp = lista[i]
            if not tmp.alive:
                del lista[i]
            else:
                i = i+1
    
    def update(self):
        if self.nuevoplaneta == True:
            #elige un tipo de planeta (nomas hay 4 por el momento)
            dios = random.randint(1,4)    
            self.planeta =  pygame.image.load("../imagenes/Niveles/planeta"+`dios`+".png")
            #posicion del planeta
            self.posmin= 0-self.planeta.get_height()
            self.yplaneta = random.randint(-400, self.posmin)
            self.posx = random.randint(-100, self.conf.width +100 )
            self.nuevoplaneta = False
        self.yplaneta += 1
        
     
    
        if self.yplaneta > self.conf.height:
            #print "Nuevo planeta necesitado"
            self.nuevoplaneta = True
        #se actualizan todos los componentes del nivel
        for objeto in self.pc:
            objeto.update()
        for objeto in self.npcProy:
            objeto.update()
        for objeto in self.pcProy:
            objeto.update()
        for objeto in self.npc:
            objeto.update()
        #self.barra.paint()
        for objeto in self.FX:
            objeto.update()
        for objeto in self.drop:
            objeto.update()
        for objeto in self.estrellas:
            objeto.update()
        for objeto in self.estrellitas:
            objeto.update()
        for objeto in self.estrellasrojas:
            objeto.update()
        self.checaestrellas(self.estrellas)
        self.checaestrellas(self.estrellasrojas)
        self.checaestrellas(self.estrellitas)                       
    def paint(self):
        #pintado de cosas propias del nivel  
        self.win.blit(self.fondo, (0,0))
        self.repinta(self.estrellitas)
        self.repinta(self.estrellasrojas)
        self.win.blit(self.planeta, (self.posx,self.yplaneta))
        self.repinta(self.estrellas)
      
        #se pintan todos los objetos que se contienen en el nivel        
        self.repinta(self.npcProy)
        self.repinta(self.pcProy)
        self.repinta(self.npc)
        self.repinta(self.pc)
        #se pintan los efectos especiales
        self.repinta(self.FX)
        #se pintan las coas del HUD
        self.repinta(self.drop)
      
        
        
    def repinta(self,lista):
        for objeto in lista:
            imagenes = objeto.getView()
            for imagen in imagenes :
                self.win.blit(imagen.sprite,(imagen.x,imagen.y))
                
    def checaestrellas(self,lista):
         for objeto in lista:
            if objeto.posicion.y > self.win.get_height():
                if not objeto.nombre=="esrtellaroja":
                    objeto.posicion= Util.Vector(random.randint(0, self.win.get_width()), -1)
                else:
                    objeto.posicion= Util.Vector(random.randint(0, self.win.get_width()), -objeto.imagen.get_hight()-50)
            
        
    def creaNPC(self):
        #steve = random.randint(1,3) 
        #componer el tamanyo
        #kamisama= random.randint(-100,900)
        #npc = NPCNaves.Andromeda(self.img,Util.Vector(10,10),Util.Vector(kamisama,-50),self.sonidos)
        #arma = Armas.PlasmaCanon(self.img,self.sonidos)
        #radar = Util.Radar(self)
        #if steve == 1:
        #    ia = IA.Pidgeons(npc)
        #if steve == 2:
        #    ia = IA.Snake(npc)
        #if steve == 3:
        #    ia = IA.Alcon(npc)
        #npc.setArma(arma)
        #npc.setRadar(radar)
        #npc.copiloto=ia
        #self.addNPC(npc)
        self.addNPC(self.hb.update(len(self.npc), self))
        
class Guion:
    def __init__(self):
        self.estado = 0
        self.legion = 0
        self.oleada = 0
        self.finOleada = False
        self.contador = 0
        self.npc = []
    def update(self,numNpc,mundo):
        self.npc = []
        if self.estado == 0:
            if self.oleada < 5 :
                if numNpc == 0 :
                    self.oleada +=1
                    self.finOleada = False
                if numNpc < 4 and not self.finOleada:
                    kamisama= random.randint(-100,900)
                    npc = NPCNaves.Andromeda(mundo.img,Util.Vector(10,10),Util.Vector(kamisama,-50),mundo.sonidos)
                    arma = Armas.PlasmaCanon(mundo.img,mundo.sonidos)
                    radar = Util.Radar(mundo)
                    ia = IA.Pidgeons(npc)
                    npc.setArma(arma)
                    npc.setRadar(radar)
                    npc.copiloto=ia
                    self.npc += [npc]
                else:
                    self.finOleada = True
            else:
                self.oleada = 0
                self.contador = 0
                self.estado = 1
        if self.estado == 1:
            if self.contador < 100:
                self.contador+=1
            else:
                self.contador = 0
                self.estado = 2
        if self.estado == 2:
            if self.oleada < 5 :
                if numNpc == 0 :
                    self.oleada +=1
                    self.finOleada = False
                if numNpc < 4 and not self.finOleada:
                    kamisama= random.randint(-100,900)
                    npc = NPCNaves.Andromeda(mundo.img,Util.Vector(10,10),Util.Vector(kamisama,-50),mundo.sonidos)
                    arma = Armas.PlasmaCanon(mundo.img,mundo.sonidos)
                    radar = Util.Radar(mundo)
                    ia = IA.Snake(npc)
                    npc.setArma(arma)
                    npc.setRadar(radar)
                    npc.copiloto=ia
                    self.npc += [npc]
                else:
                    self.finOleada = True
            else:
                self.oleada = 0
                self.contador = 0
                self.estado = 3
        if self.estado == 3:
            if self.contador < 30:
                self.contador+=1
            else:
                self.estado = 4
        if self.estado == 4:
            if self.oleada < 1:
                kamisama= random.randint(-100,900)
                npc = NPCNaves.Andromeda(mundo.img,Util.Vector(10,10),Util.Vector(kamisama,-50),mundo.sonidos)
                arma = Armas.PlasmaCanon(mundo.img,mundo.sonidos)
                radar = Util.Radar(mundo)
                ia = IA.Alcon(npc)
                npc.setArma(arma)
                npc.setRadar(radar)
                npc.copiloto=ia
                npc.escudo.energia= 6
                self.npc += [npc]
                self.oleada += 1
            else:
                if numNpc < 1:
                    self.oleada = 0
                    self.legion = 0
                    self.contador = 0
                    self.estado = 5
        if self.estado == 5:
            if self.oleada < 5 :
                if numNpc == 0 :
                    self.oleada +=1
                    self.finOleada = False
                if numNpc < 4 and not self.finOleada:
                    steve = random.randint(1,2)
                    kamisama= random.randint(-100,900)
                    npc = NPCNaves.Andromeda(mundo.img,Util.Vector(10,10),Util.Vector(kamisama,-50),mundo.sonidos)
                    arma = Armas.PlasmaCanon(mundo.img,mundo.sonidos)
                    radar = Util.Radar(mundo)
                    if steve == 1:
                        ia = IA.Pidgeons(npc)
                    if steve == 2:
                        ia = IA.Snake(npc)
                    npc.setArma(arma)
                    npc.setRadar(radar)
                    npc.copiloto=ia
                    self.npc += [npc]
                else:
                    self.finOleada = True
            else:
                self.oleada = 0
                self.contador = 0
                self.estado = 6
        if self.estado == 6:
            if self.oleada < 1:
                kamisama= random.randint(-100,900)
                npc = NPCNaves.Boss1(mundo.img,Util.Vector(10,10),Util.Vector(kamisama,0),mundo.sonidos)
                arma = Armas.PlasmaCanon(mundo.img,mundo.sonidos)
                radar = Util.Radar(mundo)
                ia = IA.BossIA(npc)
                npc.setArma(arma)
                arma.constTemp = 0
                npc.setRadar(radar)
                npc.copiloto=ia
                npc.escudo.energia= 100
                self.npc += [npc]
                self.oleada += 1
            else:
                if numNpc < 1:
                    self.oleada = 0
                    self.legion = 0
                    self.contador = 0
                    self.estado = 7
        return self.npc    