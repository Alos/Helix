import amara
 
class ArchivoXML:
    def __init__(self,nombre):
        self.nombre = nombre
        
    def creaArchivo(self):
        self.archivo = open ("../../conf/"+self.nombre,"w")
        self.archivo.write("<helixconf>\n")
            
    def agregaTag(self,tag,params,valores):
        if (len(params)==len(valores)):
            self.archivo.write("\t<"+tag+">\n")
            for i in range(len(params)):
                self.archivo.write ("\t\t<"+params[i]+">"+valores[i]+"</"+params[i]+">\n")
            return True
            self.archivo.write("\t</"+tag+">\n")
        else: 
            return False
    def cerrarArchivo(self):
        self.archivo.write("</helixconf>")
        
    
    def leerTag(self,archivo,tag,params):
        i=0
        for fragDom in amara.pushdom(source=archivo, xpatterns=u"/helixconf/"+tag[i]):
            label = fragDom.firstChild
            for j in range(len(params)):
                param = label.xpath('string('+params[j]+')') #obtener el elemento nombre
                print param+"\n"
                
    