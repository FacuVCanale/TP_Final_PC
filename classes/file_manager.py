class File:
    def __init__(self,archivo,modo) -> None:
        self.archivo = archivo
    def agregar(self,text,mode=a):
        if (text != int) and (text != float) and (text!=str)
            return "Actualmente, este método no admite ese tipo de objeto."
        else:
            with open(self.archivo,mode) as file:
                file.write(text)
    def escribir(self,text):
        if (text != int) and (text != float) and (text!=str)
            return "Actualmente, este método no admite ese tipo de objeto."
        else:
            with open(self.archivo,"w") as file:
                file.write(text)
    def leer(self,text):
        with open(self.archivo,"r") as file:
            return file.read()
    def __str__(self):
        pass