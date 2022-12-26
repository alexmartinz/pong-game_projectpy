'''
CONTROLES JUGADOR 1: MOVER ARRIBA: W, MOVER ABAJO: S.
CONTROLES JUGADOR 2: MOVER ARRIBA: TECLA-UP, MOVER ABAJO TECLA-DOWN.
'''
import pygame, sys, time, random
from pygame import Rect

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
sizeScreen = (800, 600)
background = BLACK
ballScale = [20, 20]
playerWidth = 20
playerHeight = 90
SOCORE_FONT = pygame.font.SysFont("couriernew", 50, False, False)
leftScore = 0
rightScore = 0

class Pelota(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites/ball.png")
        self.image = pygame.transform.scale(self.image, ballScale) 
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.speedX = 0
        self.speedY = 0

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites/racket.png")
        self.image = pygame.transform.scale(self.image, (playerWidth, playerHeight))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.speed = 0

screen = pygame.display.set_mode(sizeScreen)
clock = pygame.time.Clock()
pygame.display.set_caption("PONG")
icon = pygame.image.load("img/icono.ico")
pygame.display.set_icon(icon)
soundGol = pygame.mixer.Sound('sounds/gol.mp3')
soundRebot = pygame.mixer.Sound('sounds/rebote.mp3')
pygame.mixer.music.load('sounds/loop.mp3')
pygame.mixer.music.play(50)

#CONTIENE TODOS LOS SPRITES A DIBUJAR
allSpriteList = pygame.sprite.Group()
#COORDENADAS Y VELOCIDAD -> PELOTA
spriteBall = Pelota()
spriteBall.rect.x = 400
spriteBall.rect.y = 300
spriteBall.speedX = 3
spriteBall.speedY = 3
#COORDENADAS INICIALES -> PLAYER 1
spritePlayer1 = Jugador()
spritePlayer1.rect.x = 50
spritePlayer1.rect.y = int(300 - (playerHeight / 2))
#COORDENADAS INICIALES -> PLAYER 2
spritePlayer2 = Jugador()
spritePlayer2.rect.x = 750 - playerWidth
spritePlayer2.rect.y = int(300 - (playerHeight / 2))
allSpriteList.add(spriteBall)
allSpriteList.add(spritePlayer1)
allSpriteList.add(spritePlayer2)

game_over = False
FPS = 60

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN: #ACTIVE
            # PLAYER 1
            if event.key == pygame.K_w:
                spritePlayer1.speed = -3
            if event.key == pygame.K_s:
                spritePlayer1.speed = 3
            # PLAYER 2
            if event.key == pygame.K_UP:
                spritePlayer2.speed = -3
            if event.key == pygame.K_DOWN:
                spritePlayer2.speed = 3
        if event.type == pygame.KEYUP: #INACTIVE
            # PLAYER 1
            if event.key == pygame.K_w:
                spritePlayer1.speed = 0
            if event.key == pygame.K_s:
                spritePlayer1.speed = 0
            # PLAYER 2
            if event.key == pygame.K_UP:
                spritePlayer2.speed = 0
            if event.key == pygame.K_DOWN:
                spritePlayer2.speed = 0

    ''' LOGIC CODE '''
    #CONTADOR DE PUNTOS PARA LOS JUGADORES
    if spriteBall.rect.x < 0:
        rightScore +=1
    elif spriteBall.rect.x > 800:
        leftScore += 1
    leftScoreText = SOCORE_FONT.render(f"{leftScore}",1,WHITE, None)
    rightScoreText = SOCORE_FONT.render(f"{rightScore}",1,WHITE, None)
    #HACE QUE LA PELOTA REBOTE SI GOLPEA ARRIBA O ABAJO DE LA PANTALLA
    if spriteBall.rect.y > 590 or spriteBall.rect.y < 10:
        spriteBall.speedY *= -1
        soundRebot.play()
    #REVISA SI LA PELOTA SALE DEL LADO DERECHO / IZQUIERDO
    if spriteBall.rect.x > 800 or spriteBall.rect.x < 0:
        soundGol.play()
        spriteBall.rect.x = 400
        spriteBall.rect.y = 300
        #SI SALE DE LA PANTALLA INVIERTE DIRECCION
        spriteBall.speedX *= -1 
        spriteBall.speedY *= -1
    #MODIFICA LAS COORDENADAS PARA DAR MOVIMIENTO A LOS JUGADORES / PELOTA
    spritePlayer1.rect.y += spritePlayer1.speed
    spritePlayer2.rect.y += spritePlayer2.speed
    spriteBall.rect.x += spriteBall.speedX
    spriteBall.rect.y += spriteBall.speedY
    ''' LOGIC CODE '''

    screen.fill(background)

    ''' DRAW CODE '''
    screen.blit(leftScoreText, (200, 20))
    screen.blit(rightScoreText, (600, 20))
    allSpriteList.draw(screen)
    line = pygame.draw.line(screen, WHITE, (400, 0), (400, 600), 1)
    ''' DRAW CODE '''

    ''' EVENTS CODE '''
    if spriteBall.rect.colliderect(spritePlayer1) or spriteBall.rect.colliderect(spritePlayer2):
        spriteBall.speedX *= -1
        soundRebot.play()
    ''' EVENTS CODE '''

    pygame.display.flip()
    clock.tick(FPS)        
pygame.quit()
