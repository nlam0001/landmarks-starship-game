
import pygame
import random

# Configuración de pantalla
ANCHO, ALTO = 800, 600
BLANCO = (255, 255, 255)
AZUL_NEON = (0, 255, 255)
ROJO = (255, 50, 50)
AMARILLO = (255, 255, 0)

class SpaceGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((ANCHO, ALTO))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        
        # Jugador
        self.nave_rect = pygame.Rect(100, 300, 50, 40)
        self.energia = 100
        self.puntos = 0
        self.estado = "NORMAL" # NORMAL, ESCUDO, CARGANDO
        
        # Obstáculos y Balas
        self.asteroides = []
        self.balas = []
        self.ultimo_disparo = 0
        
    def crear_asteroide(self):
        if random.randint(1, 30) == 1:
            y_pos = random.randint(0, ALTO - 40)
            self.asteroides.append(pygame.Rect(ANCHO, y_pos, 40, 40))

    def actualizar(self, gesto):
        # 1. Movimiento básico con POINTING_UP
        if gesto == "Pointing_Up":
            self.nave_rect.y -= 7
        else:
            self.nave_rect.y += 3 # Gravedad simple
            
        # 2. Lógica de Gestos
        self.estado = "NORMAL"
        
        if gesto == "Open_Palm":
            self.estado = "ESCUDO" # Inmune a choques
        
        elif gesto == "Closed_Fist":
            self.estado = "CARGANDO"
            if self.energia < 100: self.energia += 0.5
            
        elif gesto == "Victory": # Disparar
            ahora = pygame.time.get_ticks()
            if ahora - self.ultimo_disparo > 300: # Ráfaga cada 300ms
                self.balas.append(pygame.Rect(self.nave_rect.right, self.nave_rect.centery, 10, 5))
                self.ultimo_disparo = ahora
        
        elif gesto == "ILoveYou": # Limpiar pantalla (Cuesta 50 de energía)
            if self.energia >= 50:
                self.asteroides = []
                self.energia -= 50

        # Limitar movimiento
        self.nave_rect.clamp_ip(pygame.Rect(0, 0, ANCHO, ALTO))

        # 3. Mover Asteroides y Balas
        for a in self.asteroides[:]:
            a.x -= 5
            if a.x < -40: self.asteroides.remove(a)
            
            # Colisión con nave
            if self.nave_rect.colliderect(a):
                if self.estado != "ESCUDO":
                    self.energia -= 1
                self.asteroides.remove(a)

        for b in self.balas[:]:
            b.x += 10
            if b.x > ANCHO: self.balas.remove(b)
            
            # Colisión bala con asteroide
            for a in self.asteroides[:]:
                if b.colliderect(a):
                    if a in self.asteroides: self.asteroides.remove(a)
                    if b in self.balas: self.balas.remove(b)
                    self.puntos += 10

        self.crear_asteroide()

    def dibujar(self):
        # Fondo y HUD
        self.screen.fill((10, 10, 30)) # Azul muy oscuro
        
        # Dibujar Nave según estado
        color_nave = AZUL_NEON
        if self.estado == "ESCUDO": 
            color_nave = AMARILLO
            pygame.draw.circle(self.screen, (100, 100, 255), self.nave_rect.center, 40, 2)
        elif self.estado == "CARGANDO": 
            color_nave = (100, 255, 100)

        pygame.draw.rect(self.screen, color_nave, self.nave_rect, border_radius=5)
        
        # Dibujar Asteroides
        for a in self.asteroides:
            pygame.draw.ellipse(self.screen, (150, 150, 150), a)

        # Dibujar Balas
        for b in self.balas:
            pygame.draw.rect(self.screen, ROJO, b)

        # Interfaz (HUD)
        txt_gesto = self.font.render(f"COMANDO: {self.estado}", True, BLANCO)
        txt_puntos = self.font.render(f"PUNTOS: {self.puntos}", True, BLANCO)
        self.screen.blit(txt_gesto, (20, 20))
        self.screen.blit(txt_puntos, (ANCHO - 200, 20))
        
        # Barra de Energía
        pygame.draw.rect(self.screen, ROJO, (20, 50, 100, 10))
        pygame.draw.rect(self.screen, (0, 255, 0), (20, 50, self.energia, 10))

        pygame.display.flip()
        self.clock.tick(60)