import Test

class Animal:
    def __init__(self):
        self.habla="quack"

class Perro(Animal):
    def hablador(self):
        print self.habla
 
class OtroPerro(Perro):
    def hablamas(self):
        print self.habla
               
miPerro= Perro()

miPerro.hablador()

otroPerro = OtroPerro()
otroPerro.hablamas()

print Test.Algo.hola