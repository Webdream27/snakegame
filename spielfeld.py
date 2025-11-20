""" **********************************
Die Klasse fuer das Spielfeld
***********************************""" 
import pygame

class Spielfeld:
    def __init__(self, breite, hoehe):
        # fuer die Punkte
        self.punkte = 0
        # fuer die Zeit
        self.zeit = 0
        # fuer die Richtung
        self.richtung = 0
        # fuer die Breite der Spielfeldbegrenzung
        self.balkenbreite = 25
        # fuer die Breite und Hoehe
        self.breite = breite
        self.hoehe = hoehe
        
        # eine leere Liste fuer die Hindernisse
        self.hindernisse = [] 
        
        # AUFGABE 1 START: Attribut fuer das aktuelle Level
        self.level = 1 
        # AUFGABE 1 ENDE
        
        # das Spielfeld erzeugen
        self.screen = pygame.display.set_mode((breite, hoehe))
        
        # das Spielfeld zeichnen
        self.zeichne_spielfeld()
        
    # die Methode liefert die Zeichenflaeche
    def get_screen(self):
        return self.screen
    
    # die Hilfsfunktion zeichnet Rechtecke und speichert Hindernisse
    def zeichne_rechteck(self, farbe, x, y, laenge, breite, als_hindernis=True):
        rechteck = pygame.draw.rect(self.screen, farbe, [x, y, laenge, breite])
        if als_hindernis:
            self.hindernisse.append(rechteck)
        return rechteck
        
    # Die Spielfeldbegrenzungen zeichnen
    def zeichne_begrenzung(self):
        # die Liste der Hindernisse zuruecksetzen
        self.hindernisse = [] 
        
        # die vier Raender als Hindernisse setzen
        self.zeichne_rechteck("white", 0, 0, self.breite, self.balkenbreite) # Oben
        self.zeichne_rechteck("white", self.breite - self.balkenbreite, 0, self.balkenbreite, self.hoehe) # Rechts
        self.zeichne_rechteck("white", 0, self.hoehe - self.balkenbreite, self.breite, self.balkenbreite) # Unten
        self.zeichne_rechteck("white", 0, 0, self.balkenbreite, self.hoehe) # Links

    # AUFGABE 1 START: Zeichnet Level-spezifische Hindernisse
    def zeichne_level_hindernisse(self, level):
        self.level = level
        
        # Nur die Raender behalten
        self.hindernisse = self.hindernisse[:4] 
        
        if level == 2:
            # Level 2: Zwei vertikale Bloecke
            farbe = (150, 150, 150) 
            breite = 30
            hoehe = 200
            
            # Linker Block
            self.zeichne_rechteck(farbe, 200, (self.hoehe/2) - (hoehe/2), breite, hoehe, als_hindernis=True)
            # Rechter Block
            self.zeichne_rechteck(farbe, 570, (self.hoehe/2) - (hoehe/2), breite, hoehe, als_hindernis=True)

        elif level == 3:
            # Level 3: Ein Rahmen-Hindernis
            farbe = (100, 100, 100) 
            rand = 120 
            balken_dicke = 20
            
            # Vertikale Balken 
            self.zeichne_rechteck(farbe, rand, rand, balken_dicke, self.hoehe - 2 * rand, als_hindernis=True)
            self.zeichne_rechteck(farbe, self.breite - rand - balken_dicke, rand, balken_dicke, self.hoehe - 2 * rand, als_hindernis=True)
            
            # Horizontale Balken 
            self.zeichne_rechteck(farbe, rand, rand, self.breite - 2 * rand, balken_dicke, als_hindernis=True)
            self.zeichne_rechteck(farbe, rand, self.hoehe - rand - balken_dicke, self.breite - 2 * rand, balken_dicke, als_hindernis=True)
    # AUFGABE 1 ENDE
            
    # Das Spielfeld und Hindernisse neu zeichnen
    def zeichne_spielfeld(self):
        self.screen.fill("red")
        
        # Schwarze Spielflaeche
        pygame.draw.rect(self.screen, "black",[0 + self.balkenbreite, 0 + self.balkenbreite, self.breite - 2*self.balkenbreite, self.hoehe - 2*self.balkenbreite])

        # Begrenzung zeichnen
        self.zeichne_begrenzung()
        
        # AUFGABE 1 START: Level-spezifische Hindernisse zeichnen
        self.zeichne_level_hindernisse(self.level)
        # AUFGABE 1 ENDE
        
    # gab es eine Kollision im Spielfeld?
    # uebergeben wird ein Objekt
    def pruefe_kollision(self, objekt):
        # auf Kollision pruefen
        if objekt.collidelist(self.hindernisse) != -1:
            return True
        return False