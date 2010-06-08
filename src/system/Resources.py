import pygame
# Load images
#imagenes del juego
class Img:
    def __init__(self,win):
        self.fondo = pygame.Surface(win.get_size())
        #print "Desde los resourses: ",win.get_size() 
        self.fondo =  pygame.image.load("../imagenes/Niveles/fondo.png")
        self.estrella = pygame.image.load("../imagenes/FX/estrella.png")
        self.estrellaazul = pygame.image.load("../imagenes/FX/estrellaazul.png")
        self.estrellaroja = pygame.image.load("../imagenes/FX/estrellaroja.png")
        self.estrellaamarilla = pygame.image.load("../imagenes/FX/estrellaamarilla.png")
        self.estrella2 = pygame.image.load("../imagenes/FX/estrella2.png")
        #imagenes FX
        self.imgProy = pygame.image.load("../imagenes/FX/laser.png")
        self.balaenemiga =  pygame.image.load("../imagenes/FX/balaenemiga.png")
        self.imgExplosion = []
        for tmp in range(6):
            self.imgExplosion += [ pygame.image.load("../imagenes/FX/exp"+`tmp`+".png") ]
        #imagenes naves
        self.imgEnemigo = pygame.image.load("../imagenes/Naves/enemigo.gif")
        self.imgJefe = pygame.image.load("../imagenes/Naves/boss1.gif")
        self.imgNave = []
        for tmp in range(9):
            self.imgNave += [ pygame.image.load("../imagenes/Naves/ship_"+ `tmp` +".png") ]
        #carga la imagen de la barra
        self.imgBarra = []
        for tmp in range(6):
            self.imgBarra += [ pygame.image.load("../imagenes/HUD/vida"+`tmp`+".png") ]
        #carga la imagen de las bolas de energia
        self.imgEnergiaDrop = []
        for tmp in range(2):
            self.imgEnergiaDrop += [ pygame.image.load("../imagenes/Items/energia"+ `tmp` +".png") ]
        #carga la imagen de los escudos
        self.imgEscudo = []
        for tmp in range(7):
            self.imgEscudo += [ pygame.image.load("../imagenes/Escudos/shieldt1s"+`tmp`+".png") ]
        #carga la imagen de la mira
        self.imgMira = pygame.image.load("../imagenes/HUD/target.png")
        self.imgMiraCentro = pygame.image.load("../imagenes/HUD/targetCentro.png")
        self.imgMiraTR = pygame.image.load("../imagenes/HUD/targetTopRight.png") 
        self.imgMiraTL = pygame.image.load("../imagenes/HUD/targetTopLeft.png")
        self.imgMiraBR = pygame.image.load("../imagenes/HUD/targetBottomRight.png") 
        self.imgMiraBL = pygame.image.load("../imagenes/HUD/targetBottomLeft.png")   
        #carga las imagenes de los items
        ########LASER#########
        self.imgLaserDrop = []
        for tmp in range(2):
            self.imgLaserDrop += [ pygame.image.load("../imagenes/Items/lasers"+`tmp`+".png") ]
        ########Plasma#########
        self.imgPlasmaDrop = []
        for tmp in range(2):
            self.imgPlasmaDrop += [ pygame.image.load("../imagenes/Items/plasmas"+`tmp`+".png") ]
        #######BlueRay#########
        self.imgBlueRayDrop = []
        for tmp in range(2):
            self.imgBlueRayDrop += [ pygame.image.load("../imagenes/Items/bluerays"+`tmp`+".png") ]  
#Carga de la musica de fondo           
class Sound:
    def __init__(self):
        pygame.mixer.init()
        self.musica = pygame.mixer.music.load('../sonidos/pandemonium.OGG')
        self.gunshot = pygame.mixer.Sound('../sonidos/gunshot.wav')
        self.boom = pygame.mixer.Sound('../sonidos/ex.wav')
        self.plasmashot = pygame.mixer.Sound('../sonidos/plasmasound.wav')
        self.lock = pygame.mixer.Sound('../sonidos/lock.wav')
    #inicia la musica de fondo del juego
    def iniciaMusica(self):
        pygame.mixer.music.play(-1,0.0)
    def playGunshot(self):
        self.gunshot.play()
    def playBoom(self):
        self.boom.play()
    def playPlasmaSound(self):
        self.plasmashot.play()
    def playLock(self):
        self.lock.play()