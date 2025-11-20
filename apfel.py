""" **********************************
Die Klasse fuer die Aepfel
***********************************""" 
# das Modul importieren
import pygame
# fuer die zufaelligen Zahlen
from random import randint

class Apfel:
    # AUFGABE 1 START: spielfeld_instanz fuer die Hindernispruefung hinzufuegen
    def __init__(self, screen, breite, hoehe, neu, spielfeld_instanz):
        # fuer die Zeichenflaeche
        self.screen = screen
        self.spielfeld = spielfeld_instanz 
        self.groesse = 10 
        
        # AUFGABE 1 START: Schleife zur Generierung einer Position, die NICHT mit Hindernissen kollidiert
        while True:
            # fuer die Position
            if (neu == True):
                # eine zufaellige Position ermitteln
                rand_min = self.spielfeld.balkenbreite + self.groesse + 5
                rand_max_x = breite - self.spielfeld.balkenbreite - self.groesse - 5
                rand_max_y = hoehe - self.spielfeld.balkenbreite - self.groesse - 5
                
                self.pos_x = randint(rand_min, rand_max_x)
                self.pos_y = randint(rand_min, rand_max_y)
            else:
                # eine feste Position setzen
                self.pos_x = 200
                self.pos_y = 200
            
            # Temporaeres Rechteck fuer die Kollisionspruefung erstellen
            # Groesse * 2, da der Apfelradius 10 ist (Apfelgroesse ist 20x20)
            temp_rect = pygame.Rect(self.pos_x - self.groesse, self.pos_y - self.groesse, self.groesse * 2, self.groesse * 2)
            
            # Pruefen, ob der Apfel mit einem Hindernis kollidiert
            if not self.spielfeld.pruefe_kollision(temp_rect):
                break # Position ist gueltig
        # AUFGABE 1 ENDE
        
        self.rechteck = None 
        self.zeichnen()
            
    # die Methode zeichnet einen Apfel
    def zeichnen(self):    
        # den Apfel zeichnen
        self.rechteck = pygame.draw.circle(self.screen, "green", (self.pos_x, self.pos_y), self.groesse)
            
    # gab es eine Kollision mit einem Apfel?
    # uebergeben wird ein Objekt
    def pruefe_kollision(self, objekt):
        # auf Kollision pruefen
        if objekt.colliderect(self.rechteck):
            return True
        return False