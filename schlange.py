""" **********************************
Die Klasse für die Schlange
***********************************""" 

# das Modul importieren
import pygame

class Schlange:
    def __init__(self, screen):
        # für die Zeichenfläche
        self.screen = screen
        
        # eine leere Liste für die Schlangenteile
        self.teile = []
        
    # die Methode zeichnet die Schlange    
    def zeichnen(self):
        for teil in self.teile:
            pygame.draw.rect(self.screen, "red", teil)
    
    # die Methode setzt ein neues Teil vorne in die Liste
    def anhaengen(self, teil):
        self.teile.insert(0, teil)
    
    # die Methode löscht das letzte Teil:
    def loeschen(self):
        self.teile.pop()
        
    # gab es eine Kollision mit einem Schlangenteil?
    # übergeben wird ein Objekt
    def pruefe_kollision(self, schlangenteil):
        # AUFGABE 1 START: Selbstkollision
        # gegen alle Teile ausser dem Kopf pruefen
        for i, teil in enumerate(self.teile):
            if i > 0 and teil.x == schlangenteil.x and teil.y == schlangenteil.y:
                 return True
        return False
        # AUFGABE 1 ENDE
