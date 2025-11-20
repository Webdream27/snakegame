""" **********************************
SNAKE FINAL PERFORMANCE EDITION
***********************************""" 
import asyncio
import pygame
import sys
import random
import pygame.freetype
import os

# --- KONFIGURATION ---
GRID_SIZE = 20 
GAME_WIDTH = 900
GAME_HEIGHT = 700
UI_HEIGHT = 280 
WINDOW_WIDTH = GAME_WIDTH
WINDOW_HEIGHT = GAME_HEIGHT + UI_HEIGHT

# --- KLASSE APFEL ---
class Apfel:
    def __init__(self, screen, breite, hoehe, neu, spielfeld_instanz):
        self.screen = screen
        self.spielfeld = spielfeld_instanz 
        self.groesse = 10 
        
        while True:
            if (neu == True):
                rand_min = self.spielfeld.balkenbreite + self.groesse
                rand_max_x = breite - self.spielfeld.balkenbreite - self.groesse
                rand_max_y = hoehe - self.spielfeld.balkenbreite - self.groesse
                
                self.pos_x = random.randint(rand_min, rand_max_x)
                self.pos_y = random.randint(rand_min, rand_max_y)
            else:
                self.pos_x = 200
                self.pos_y = 200
            
            temp_rect = pygame.Rect(self.pos_x - self.groesse, self.pos_y - self.groesse, self.groesse * 2, self.groesse * 2)
            if not self.spielfeld.pruefe_kollision(temp_rect):
                break 
        
        self.rechteck = None 
        self.zeichnen()
            
    def zeichnen(self):    
        self.rechteck = pygame.draw.circle(self.screen, "green", (self.pos_x, self.pos_y), self.groesse)
            
    def pruefe_kollision(self, objekt):
        if self.rechteck and objekt.colliderect(self.rechteck):
            return True
        return False

# --- KLASSE SCHLANGE ---
class Schlange:
    def __init__(self, screen):
        self.screen = screen
        self.teile = []
        
    def zeichnen(self):
        for teil in self.teile:
            pygame.draw.rect(self.screen, "red", teil)
    
    def anhaengen(self, teil):
        self.teile.insert(0, teil)
    
    def loeschen(self):
        self.teile.pop()
        
    def pruefe_kollision(self, schlangenteil):
        for i, teil in enumerate(self.teile):
            if i > 0 and teil.x == schlangenteil.x and teil.y == schlangenteil.y:
                 return True
        return False

# --- KLASSE SPIELFELD ---
class Spielfeld:
    def __init__(self, breite, hoehe):
        self.balkenbreite = 20 
        self.breite = breite
        self.hoehe = hoehe
        self.hindernisse = [] 
        self.level = 1 
        
        self.screen = pygame.display.get_surface()
        self.zeichne_spielfeld()
        
    def get_screen(self):
        return self.screen
    
    def zeichne_rechteck(self, farbe, x, y, laenge, breite, als_hindernis=True):
        rechteck = pygame.draw.rect(self.screen, farbe, [x, y, laenge, breite])
        if als_hindernis:
            self.hindernisse.append(rechteck)
        return rechteck
        
    def zeichne_begrenzung(self):
        self.hindernisse = [] 
        self.zeichne_rechteck("white", 0, 0, self.breite, self.balkenbreite) 
        self.zeichne_rechteck("white", self.breite - self.balkenbreite, 0, self.balkenbreite, self.hoehe) 
        self.zeichne_rechteck("white", 0, self.hoehe - self.balkenbreite, self.breite, self.balkenbreite) 
        self.zeichne_rechteck("white", 0, 0, self.balkenbreite, self.hoehe) 

    def zeichne_level_hindernisse(self, level):
        self.level = level
        self.hindernisse = self.hindernisse[:4] 
        
        if level == 2:
            farbe = (150, 150, 150) 
            breite = 40 
            hoehe = 200
            self.zeichne_rechteck(farbe, 200, (self.hoehe/2) - (hoehe/2), breite, hoehe, als_hindernis=True)
            self.zeichne_rechteck(farbe, 560, (self.hoehe/2) - (hoehe/2), breite, hoehe, als_hindernis=True)

        elif level == 3:
            farbe = (100, 100, 100) 
            rand = 120 
            balken_dicke = 20 
            self.zeichne_rechteck(farbe, rand, rand, balken_dicke, self.hoehe - 2 * rand, als_hindernis=True)
            self.zeichne_rechteck(farbe, self.breite - rand - balken_dicke, rand, balken_dicke, self.hoehe - 2 * rand, als_hindernis=True)
            self.zeichne_rechteck(farbe, rand, rand, self.breite - 2 * rand, balken_dicke, als_hindernis=True)
            self.zeichne_rechteck(farbe, rand, self.hoehe - rand - balken_dicke, self.breite - 2 * rand, balken_dicke, als_hindernis=True)
            
    def zeichne_spielfeld(self):
        pygame.draw.rect(self.screen, "red", [0, 0, self.breite, self.hoehe])
        pygame.draw.rect(self.screen, "black",[0 + self.balkenbreite, 0 + self.balkenbreite, self.breite - 2*self.balkenbreite, self.hoehe - 2*self.balkenbreite])
        self.zeichne_begrenzung()
        self.zeichne_level_hindernisse(self.level)
        
    def pruefe_kollision(self, objekt):
        if objekt.collidelist(self.hindernisse) != -1:
            return True
        return False

# --- BUTTONS & LAYOUT ---
BTN_SIZE = 90  
GAP_X = 70     
GAP_Y = 15     
CTRL_CENTER_X = WINDOW_WIDTH * 0.75 
CTRL_START_Y = GAME_HEIGHT + 30

btn_up = pygame.Rect(CTRL_CENTER_X - BTN_SIZE//2, CTRL_START_Y, BTN_SIZE, BTN_SIZE)
btn_down = pygame.Rect(CTRL_CENTER_X - BTN_SIZE//2, CTRL_START_Y + BTN_SIZE + GAP_Y, BTN_SIZE, BTN_SIZE)
btn_left = pygame.Rect(CTRL_CENTER_X - BTN_SIZE//2 - BTN_SIZE - 10, CTRL_START_Y + BTN_SIZE + GAP_Y, BTN_SIZE, BTN_SIZE)
btn_right = pygame.Rect(CTRL_CENTER_X - BTN_SIZE//2 + BTN_SIZE + 10, CTRL_START_Y + BTN_SIZE + GAP_Y, BTN_SIZE, BTN_SIZE)

btn_neustart = pygame.Rect(50, GAME_HEIGHT + 80, 200, 80)

def draw_text(screen, text, x, y, size=30, color="white"):
    font = pygame.font.Font(None, size)
    surf = font.render(str(text), True, color)
    screen.blit(surf, (x, y))
    return surf.get_rect(topleft=(x,y))

def zeichne_interface(screen):
    pygame.draw.rect(screen, (20, 20, 20), [0, GAME_HEIGHT, WINDOW_WIDTH, UI_HEIGHT])
    pygame.draw.line(screen, "white", (0, GAME_HEIGHT), (WINDOW_WIDTH, GAME_HEIGHT), 3)

    for btn, direction in [(btn_up, 0), (btn_down, 180), (btn_left, 90), (btn_right, 270)]:
        pygame.draw.rect(screen, (60, 60, 60), btn, border_radius=15)
        pygame.draw.rect(screen, "white", btn, 2, border_radius=15)
        shape_surf = pygame.Surface((BTN_SIZE, BTN_SIZE), pygame.SRCALPHA)
        mid = BTN_SIZE // 2
        pygame.draw.polygon(shape_surf, "white", [(mid, 15), (15, BTN_SIZE-15), (BTN_SIZE-15, BTN_SIZE-15)])
        rotated_surf = pygame.transform.rotate(shape_surf, direction)
        rot_rect = rotated_surf.get_rect(center=btn.center)
        screen.blit(rotated_surf, rot_rect)

    # BLAUER BUTTON
    pygame.draw.rect(screen, (0, 180, 255), btn_neustart, border_radius=10)
    pygame.draw.rect(screen, "white", btn_neustart, 2, border_radius=10)
    font = pygame.font.Font(None, 40)
    text_surf = font.render("NEUSTART", True, "white")
    text_rect = text_surf.get_rect(center=btn_neustart.center)
    screen.blit(text_surf, text_rect)

def check_mobile_input(pos, aktuelle_richtung):
    x, y = pos
    if btn_up.collidepoint(x, y) and aktuelle_richtung != 1: return 0
    elif btn_down.collidepoint(x, y) and aktuelle_richtung != 0: return 1
    elif btn_right.collidepoint(x, y) and aktuelle_richtung != 3: return 2
    elif btn_left.collidepoint(x, y) and aktuelle_richtung != 2: return 3
    return aktuelle_richtung

# --- SOUND GLOBAL ---
crunch_sound = None 

async def meldung_zeigen_interaktiv(screen, text, wartezeit_ms=3000):
    start_ticks = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_ticks < wartezeit_ms:
        overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        screen.blit(overlay, (0,0))
        font = pygame.font.Font(None, 70)
        surf = font.render(text, True, "white")
        rect = surf.get_rect(center=(GAME_WIDTH//2, GAME_HEIGHT//2))
        screen.blit(surf, rect)
        zeichne_interface(screen)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_neustart.collidepoint(event.pos): return True 
                else: return False 
        await asyncio.sleep(0)
    return False

async def game_over(screen, text):
    await meldung_zeigen_interaktiv(screen, text, wartezeit_ms=3000)

async def start_game(screen):
    pygame.event.clear() 
    
    schwierigkeitsgrade = {
        pygame.K_1: {"text": "1: EINFACH", "frames": 15, "punkte_pro_apfel": 1},
        pygame.K_2: {"text": "2: NORMAL", "frames": 20, "punkte_pro_apfel": 2},
        pygame.K_3: {"text": "3: SCHWER", "frames": 25, "punkte_pro_apfel": 3},
        pygame.K_4: {"text": "4: EXTREM", "frames": 30, "punkte_pro_apfel": 4}
    }
    
    selected_difficulty = None
    bg_image = None
    
    # LÄDT JETZT JPG
    try:
        if os.path.exists("assets/start.jpg"):
            loaded_img = pygame.image.load("assets/start.jpg")
            bg_image = pygame.transform.scale(loaded_img, (GAME_WIDTH, GAME_HEIGHT))
        else:
            # Fallback falls JPG fehlt
            pass
    except:
        bg_image = None
    
    rects = {} 
    
    while selected_difficulty is None:
        screen.fill("black") 
        if bg_image:
            screen.blit(bg_image, (0,0))
        else:
             pygame.draw.rect(screen, (0,0,50), [0,0,GAME_WIDTH,GAME_HEIGHT])

        pygame.draw.rect(screen, (20, 20, 20), [0, GAME_HEIGHT, WINDOW_WIDTH, UI_HEIGHT])
        draw_text(screen, "SNAKE", 380, 80, 80, "white")
        draw_text(screen, "SCHWIERIGKEIT WÄHLEN:", 280, 180, 40, "yellow")
        
        y_offset = 260
        rects = {} 
        for key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
            val = schwierigkeitsgrade[key]
            button_rect = pygame.Rect(250, y_offset, 400, 50)
            pygame.draw.rect(screen, (80, 80, 80), button_rect, border_radius=10)
            pygame.draw.rect(screen, "white", button_rect, 2, border_radius=10)
            font = pygame.font.Font(None, 40)
            surf = font.render(val["text"], True, "white")
            text_rect = surf.get_rect(center=button_rect.center)
            screen.blit(surf, text_rect)
            rects[key] = button_rect
            y_offset += 70
            
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in schwierigkeitsgrade:
                    selected_difficulty = event.key
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # AUDIO WAKE UP
                if crunch_sound:
                    crunch_sound.play() 
                    crunch_sound.stop() 

                x, y = event.pos
                for key, rect in rects.items():
                    if rect.collidepoint(x, y):
                        selected_difficulty = key

        await asyncio.sleep(0)
    
    return schwierigkeitsgrade[selected_difficulty]

def initialisiere_schlange(screen):
    position_x = 100
    position_y = 100
    schlangenkopf = pygame.rect.Rect([position_x, position_y, 20, 20])
    schlange = Schlange(screen)
    schlange.anhaengen(schlangenkopf)
    richtung = 2 
    return schlange, position_x, position_y, richtung

async def main():
    # AUDIO PRE-INIT
    try:
        pygame.mixer.pre_init(22050, -16, 2, 512) 
    except:
        pass
    pygame.init()
    try:
        pygame.mixer.init()
    except:
        pass

    # LÄDT JETZT WAV 
    global crunch_sound
    try:
        if os.path.exists("assets/grumpf.wav"):
            crunch_sound = pygame.mixer.Sound("assets/grumpf.wav")
            crunch_sound.set_volume(0.6)
        else:
            crunch_sound = None
    except:
        crunch_sound = None

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Online Deluxe")
    
    while True:
        schwierigkeit = await start_game(screen)
        
        frames = schwierigkeit["frames"]             
        punkte_pro_apfel = schwierigkeit["punkte_pro_apfel"] 

        spielfeld = Spielfeld(GAME_WIDTH, GAME_HEIGHT)
        clock = pygame.time.Clock()
        skip_collision_frame = False
        running = True
        level = 1
        level_up_score = 5 
        level_maximum = 3 
        schlange, position_x, position_y, richtung = initialisiere_schlange(screen)
        bewegung = 20 
        apfel = Apfel(screen, GAME_WIDTH, GAME_HEIGHT, True, spielfeld)
        punkte = 0

        while running:
            if punkte >= level_up_score * level and level < level_maximum:
                level += 1
                spielfeld.level = level 
                await meldung_zeigen_interaktiv(screen, f"LEVEL {level} STARTET...", 3000)
                spielfeld.zeichne_spielfeld()
                schlange, position_x, position_y, richtung = initialisiere_schlange(screen)
                skip_collision_frame = True 
                apfel = Apfel(screen, GAME_WIDTH, GAME_HEIGHT, True, spielfeld)
            elif punkte >= level_up_score * level_maximum:
                await meldung_zeigen_interaktiv(screen, "SIE HABEN GEWONNEN!", 5000)
                running = False
                break

            spielfeld.zeichne_spielfeld()
            schlange.zeichnen()
            apfel.zeichnen()
            zeichne_interface(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and richtung != 1: richtung = 0
                    elif event.key == pygame.K_DOWN and richtung != 0: richtung = 1
                    elif event.key == pygame.K_RIGHT and richtung != 3: richtung = 2
                    elif event.key == pygame.K_LEFT and richtung != 2: richtung = 3
                if event.type == pygame.MOUSEBUTTONDOWN:
                    richtung = check_mobile_input(event.pos, richtung)
                    if btn_neustart.collidepoint(event.pos):
                        running = False 

            if richtung == 0: position_y -= bewegung
            elif richtung == 1: position_y += bewegung
            elif richtung == 2: position_x += bewegung
            elif richtung == 3: position_x -= bewegung
                
            schlangenteil = pygame.rect.Rect([position_x, position_y, 20, 20])
            
            if skip_collision_frame:
                skip_collision_frame = False 
            else:
                if spielfeld.pruefe_kollision(schlangenteil):
                    await game_over(screen, "GAME OVER")
                    running = False 
                if schlange.pruefe_kollision(schlangenteil):
                    await game_over(screen, "GAME OVER")
                    running = False 
            
            if running:
                schlange.anhaengen(schlangenteil)
                if apfel.pruefe_kollision(schlangenteil):
                    if crunch_sound:
                        crunch_sound.play() 
                    punkte += punkte_pro_apfel 
                    apfel = Apfel(screen, GAME_WIDTH, GAME_HEIGHT, True, spielfeld)
                    if punkte % 10 == 0 and frames < 50: frames += 5
                else:
                    schlange.loeschen()     
            
            draw_text(screen, "Punkte: " + str(punkte), 750, 30, 30, "white")
            pygame.display.flip()
            clock.tick(frames)
            await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())