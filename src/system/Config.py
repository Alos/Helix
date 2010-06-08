import Util

#Esra es la clase de configuracion del juego
#Su trabajo es tomar los datos recividos del pareador y agregarlos a su atributos corrspondientes

class Config:
    def __init__(self):
        self.width=0
        self.height=0
        array = Util.parsea()
        self.width = int(array[0])
        print "Este es el with de config", self.width
        self.height = int(array[1])
        print "Este es el height de config", self.height
    

    