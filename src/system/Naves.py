import pygame
import Util
import Shields

class Nave(Util.Object):
        def __init__(self,img,pos,vel,sonidos):
            Util.Object.__init__(self)
            self.vista = 4
            self.retardo = 0
            self.topeRetardo = 2
            self.movLateral = False
            self.armas = []
            self.armaActual = 0
            #self.imgNave = img.imgNave
            self.acciones = None
            self.radar = None
            self.team = None #esto es para diferenciar entre amigo o enemigo
            self.posicion=pos
            self.velocidad=vel
            self.copiloto= None
            self.alive=True
            self.sonidos = sonidos
            self.oldtarget= None #esta va por ahora para ver cuando se selecciono algo nuevo en el target(sonido)
            self.cambiandoArma=False 
            self.cambiandoTarget=False
            self.escudo= Shields.Escudo(img)
            self.propulsor = Util.Propulsor()
            self.estabilizador = Util.Estabilizador()
        def setArma(self,arma): 
            self.armas += [arma]
        def shiftArma(self):
            self.armaActual += 1
            if not self.armaActual < len(self.armas):
                self.armaActual = 0                
        def switchArma(self,num):
            self.armaActual = num
        def setRadar(self,radar):
            self.radar = radar
            self.radar.setTeam(self.team)
            self.radar.CurrentPos=self.posicion
        def mover(self,acciones):
            self.acciones = self.copiloto.getAcciones(acciones)
            proyectiles = []
            if not pygame.K_TAB in acciones:
                self.cambiandoTarget=False 
            if not pygame.K_w in acciones:
                self.cambiandoArma=False  
            for accion in self.acciones:     
                if accion == pygame.K_LEFT:
                    self.movLateral = True
                    self.aplicarFuerza(self.propulsor.movLeft())
                if accion == pygame.K_RIGHT:
                    self.movLateral = True
                    self.aplicarFuerza(self.propulsor.movRight())
                if accion == pygame.K_UP:
                    self.aplicarFuerza(self.propulsor.movUp())
                if accion == pygame.K_DOWN:
                    self.aplicarFuerza(self.propulsor.movDown())
                #la opcion de default es la de disparar con la tecla "d"
                if accion == pygame.K_d:
                    proy = self.dispara()
                    if not proy == None :
                        proyectiles += [proy]
                #con w cambiamos de armas en caso de que la nave contenga varias 
                if accion == pygame.K_w:
                    if not self.cambiandoArma:
                        self.cambiandoArma=True
                        self.shiftArma()
                #dependiend de la arma, ser apocible que el jugador seleccione el enemigo mas cercano con "C"
                if accion == pygame.K_c:
                    self.radar.detectShips()
                    self.radar.setClosestTarget(self.posicion)
                    self.armas[self.armaActual].setTarget(self.radar.target)
#Esta lineas de abajo q hacen el sonido del target deberan estar mejor en el radar
                    if self.team==1 and not self.oldtarget==self.radar.target:
                        self.sonidos.playLock()
                        self.oldtarget=self.radar.target
                if accion == pygame.K_TAB:
                    if not self.cambiandoTarget:
                        self.cambiandoTarget= True
                        self.radar.detectShips()
                        self.radar.toggleTarget()
                        self.armas[self.armaActual].setTarget(self.radar.target)
            
            return proyectiles
    
        def update(self):
           #actualiza la posicion del radar
           Util.Object.Update(self)
           self.estabilizador.update(self.velocidad)
           self.aplicarFuerza(self.estabilizador.estabiliza())
           if not self.armas[self.armaActual]  == None:
               self.armas[self.armaActual].update()
           self.centro = self.getCentro()
           self.escudo.update(self.centro)
        def getView(self):
            imagenes = [Util.Imagen(self.imagen[self.vista],self.posicion)]
            if not self.armas[self.armaActual]  == None:
                imagenes += self.armas[self.armaActual].getView()
            if not self.escudo == None:
                imagenes += self.escudo.getView()
            return imagenes
        def getPosArma(self):
            inc_x = self.imgNave[self.vista].get_width() / 2
            inc_y = self.imgNave[self.vista].get_height() - 10
            return Util.Vector(self.posicion.x + inc_x, self.posicion.y - inc_y)
       
        def dispara(self):
            if not (self.armas[self.armaActual] == None and self.radar == None):
                return self.armas[self.armaActual].dispara(self.getPosArma())
            return None
        def get_with(self):
            if self.escudo.energia > 0:
                return self.escudo.get_with()
            else:
                return self.imagen[self.vista].get_with()
        def get_height(self):
            if self.escudo.energia > 0:
                return self.escudo.get_height()
            else:
                return self.imagen[self.vista].get_height()
        def getPosicion(self):
            if self.escudo.energia > 0:
                return self.escudo.getPosicion()
            else:
                return self.posicion
        def hit(self, vector):
            self.escudo.hit()
            
            