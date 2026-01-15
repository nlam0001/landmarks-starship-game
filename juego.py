import pygame
import random
import sys

# Colores Sci-Fi
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 255)
DEEP_SPACE = (5, 5, 25)
WHITE = (255, 255, 255)
DARK_GREY = (35, 35, 50)
YELLOW = (255, 255, 0)
ORANGE = (255, 140, 0)
GREEN = (0, 255, 100)
RED = (255, 0, 0)

class SpaceGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        
        # Carga de imágenes con manejo de errores
        try:
            self.img_nave = pygame.image.load("nave.png").convert_alpha()
            self.img_nave = pygame.transform.scale(self.img_nave, (55, 45))
            self.img_asteroide = pygame.image.load("asteroide.png").convert_alpha()
            self.img_asteroide = pygame.transform.scale(self.img_asteroide, (40, 40))
        except:
            self.img_nave = None
            self.img_asteroide = None

        self.font_main = pygame.font.SysFont("Consolas", 14, bold=True)
        self.font_emoji = pygame.font.SysFont("Segoe UI Emoji", 32)
        self.font_big = pygame.font.SysFont("Consolas", 60, bold=True)
        
        self.ultimo_disparo = 0
        self.pausado = False
        self.reset_game()

    def reset_game(self):
        self.stars = [[random.randint(0, 800), random.randint(0, 500), random.random() * 2] for _ in range(60)]
        self.nave_rect = pygame.Rect(100, 250, 50, 40)
        self.puntos = 0
        self.energia = 100
        self.vidas = 3 # Iniciamos con 3
        self.estado = "None"
        self.asteroides = []
        self.balas = []
        self.playing = True
        self.msg_alerta = ""
        self.msg_timer = 0

        self.hud_items = [
            ("Pointing_Up", "SUBIR", "☝️", NEON_BLUE),
            ("Open_Palm", "ESCUDO", "✋", NEON_PINK),
            ("Closed_Fist", "CARGAR", "✊", GREEN),
            ("Victory", "FUEGO", "✌️", NEON_BLUE),
            ("Thumb_Up", "SUPER", "👍", YELLOW),
            ("Thumb_Down", "BAJAR", "👎", ORANGE),
            ("ILoveYou", "BOMBA", "🤟", NEON_PINK),
            ("OK_Sign", "PAUSA", "👌", WHITE),
            ("Rock_ON", "RAFAGA", "🤘", NEON_BLUE)
        ]

    def show_game_over(self):
        esperando = True
        while esperando:
            self.screen.fill((10, 10, 20))
            msg = self.font_big.render("MISION FALLIDA", True, RED)
            score = self.font_main.render(f"PUNTOS FINALES: {self.puntos}", True, WHITE)
            instr = self.font_main.render("PRESIONA 'R' PARA REINTENTAR O 'Q' PARA SALIR", True, GREEN)
            
            self.screen.blit(msg, (400 - msg.get_width()//2, 200))
            self.screen.blit(score, (400 - score.get_width()//2, 300))
            self.screen.blit(instr, (400 - instr.get_width()//2, 400))
            
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: return True
                    if event.key == pygame.K_q: return False
                if event.type == pygame.QUIT: return False

    def actualizar(self, gesto):
        if not self.playing: return
        self.estado = gesto
        ahora = pygame.time.get_ticks()

        # 1. GESTO DE PAUSA (OK_Sign)
        if gesto == "OK_Sign":
            self.pausado = True
            return
        else:
            self.pausado = False

        # 2. MOVIMIENTO
        if gesto == "Pointing_Up": self.nave_rect.y -= 9
        elif gesto == "Thumb_Down": self.nave_rect.y += 10
        else: self.nave_rect.y += 3 # Gravedad
        
        self.nave_rect.clamp_ip(pygame.Rect(0, 0, 800, 510))

        # 3. ATAQUE
        if gesto == "Victory" and ahora - self.ultimo_disparo > 250:
            self.balas.append(pygame.Rect(self.nave_rect.right, self.nave_rect.centery, 15, 5))
            self.ultimo_disparo = ahora
        
        if gesto == "Rock_ON" and ahora - self.ultimo_disparo > 500:
            for dy in [-20, 0, 20]:
                self.balas.append(pygame.Rect(self.nave_rect.right, self.nave_rect.centery + dy, 15, 5))
            self.ultimo_disparo = ahora

        # 4. ENERGIA Y BOMBA
        if gesto == "Closed_Fist" and self.energia < 100: self.energia += 0.5
        if gesto == "Thumb_Up" and self.energia < 100: self.energia += 1.5
        if gesto == "ILoveYou" and self.energia > 80:
            self.asteroides = []; self.energia -= 80
            self.msg_alerta = "¡BOMBA ACTIVADA!"; self.msg_timer = ahora

        # 5. LOGICA DE OBJETOS
        if random.randint(1, 30) == 1:
            self.asteroides.append(pygame.Rect(800, random.randint(0, 470), 40, 40))

        for a in self.asteroides[:]:
            a.x -= 7
            if self.nave_rect.colliderect(a):
                if gesto != "Open_Palm":
                    self.energia -= 34 # Tres choques y mueres si no cargas
                self.asteroides.remove(a)
            elif a.x < -50: self.asteroides.remove(a)

        for b in self.balas[:]:
            b.x += 15
            if b.x > 800: self.balas.remove(b)
            for a in self.asteroides[:]:
                if b.colliderect(a):
                    self.asteroides.remove(a); self.balas.remove(b)
                    self.puntos += 10; break

        # 6. REVISAR VIDAS (REPARADO)
        if self.energia <= 0:
            self.vidas -= 1
            self.energia = 100
            self.msg_alerta = f"¡VIDA PERDIDA! QUEDAN {self.vidas}"
            self.msg_timer = ahora
            if self.vidas == 0: # Cuando llega a 0 exactamente
                self.playing = False

    def dibujar(self):
        # Si ya no estamos jugando, ir a pantalla Game Over
        if not self.playing:
            if self.show_game_over(): 
                self.reset_game()
            else: 
                pygame.quit(); sys.exit()

        self.screen.fill(DEEP_SPACE)
        # Estrellas
        for s in self.stars:
            s[0] -= s[2]
            if s[0] < 0: s[0] = 800
            pygame.draw.circle(self.screen, (100, 100, 150), (int(s[0]), int(s[1])), 1)

        # Nave e Imagen
        if self.img_nave:
            self.screen.blit(self.img_nave, self.nave_rect)
        else:
            pygame.draw.polygon(self.screen, NEON_BLUE, [self.nave_rect.topleft, self.nave_rect.bottomleft, self.nave_rect.midright])

        # Escudo
        if self.estado == "Open_Palm":
            pygame.draw.circle(self.screen, NEON_PINK, self.nave_rect.center, 55, 2)

        # Asteroides
        for a in self.asteroides:
            if self.img_asteroide: self.screen.blit(self.img_asteroide, a)
            else: pygame.draw.rect(self.screen, (120, 120, 130), a, border_radius=5)

        # Balas
        for b in self.balas: pygame.draw.rect(self.screen, YELLOW, b)

        # HUD Superior
        txt_score = self.font_main.render(f"PUNTOS: {self.puntos} | VIDAS: {self.vidas}", True, WHITE)
        self.screen.blit(txt_score, (15, 15))
        pygame.draw.rect(self.screen, RED, (15, 40, 100, 10))
        pygame.draw.rect(self.screen, GREEN, (15, 40, max(0, self.energia), 10))

        if self.pausado:
            p_txt = self.font_big.render("PAUSA", True, WHITE)
            self.screen.blit(p_txt, (400 - p_txt.get_width()//2, 250))

        self.draw_hud_visual()
        pygame.display.flip()
        self.clock.tick(60)

    def draw_hud_visual(self):
        pygame.draw.rect(self.screen, (15, 15, 35), (0, 510, 800, 90))
        item_w = 800 // len(self.hud_items)
        for i, (gesto_id, label, emoji, col) in enumerate(self.hud_items):
            x = i * item_w
            active = self.estado == gesto_id
            rect = pygame.Rect(x + 4, 520, item_w - 8, 75)
            if active:
                pygame.draw.rect(self.screen, (col[0]//4, col[1]//4, col[2]//4), rect, border_radius=10)
                pygame.draw.rect(self.screen, col, rect, 2, border_radius=10)
            emo_surf = self.font_emoji.render(emoji, True, WHITE)
            self.screen.blit(emo_surf, (rect.centerx - emo_surf.get_width()//2, rect.y + 5))
            txt_surf = self.font_main.render(label, True, col if active else (100, 100, 120))
            self.screen.blit(txt_surf, (rect.centerx - txt_surf.get_width()//2, rect.bottom - 20))
