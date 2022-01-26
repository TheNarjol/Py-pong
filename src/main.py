#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Escrito por Jaime Vargas

#--------------------------------
# Inportacion de Modulos
#--------------------------------

import os
import sys
import random
import pygame
from pygame.locals import *


# -----------
# Constantes
# -----------

ANCHO = 640
ALTO = 480
CENTRO_IZQ = ANCHO * 0.25
CENTRO_DER = ANCHO * 0.75
FPS = 60
NEGRO = (0,0,0)
BLANCO = (255,255,255)
GRIS = (100, 100, 100)

# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------

class jugador():
    def __init__(self, player): # el parametro player indica cual de los dos jugadores es
        self.dimension = [10, 100] #tamaño de los sprites
        pos_vertical = ALTO / 2 - self.dimension[1] / 2
        
        if player == 1: # posicion del jugador 1
            self.pos = [25, pos_vertical] 
        elif player == 2: # posicion del jugador 2
            self.pos = [ANCHO - self.dimension[0] - 25, pos_vertical]
        
        self.velocidad = 0
        self.aceleracion = 4
        self.puntaje = 0
    
    def mover(self, direccion): # define el movimiento hacia arriba y abajo
        if direccion == "no":
            self.velocidad = 0
        elif direccion == "arriba":
            self.velocidad = -self.aceleracion
        elif direccion == "abajo":
            self.velocidad = self.aceleracion

    def actualizar(self): # actualiza la posicion del jugador
        self.pos[1] += self.velocidad
        if self.pos[1] < 10:
            self.pos[1] = 10
        elif self.pos[1] + self.dimension[1] > ALTO - 10:
            self.pos[1] = ALTO - self.dimension[1] - 10

    def dibujar(self, window): # dibujar la barra del jugador
        pygame.draw.rect(window, BLANCO,[self.pos, self.dimension])
    
    def posicion(self):
        return [self.pos[1], self.pos[1] + self.dimension[1]]
    
    def act_puntuacion(self, punto):
        self.puntaje += punto

class pelota():
    def __init__(self):
        self.radius = 8
        self.posicion = [ANCHO / 2, ALTO / 2]
        self.velocidad = [4, random.randrange(1, 9)]
    
    def dibujar(self, windows):
        pygame.draw.circle(windows, BLANCO, self.posicion, self.radius)
    
    def actualizar(self, player1, player2):
        self.posicion[0] += self.velocidad[0]
        self.posicion[1] += self.velocidad[1]

        #rebote velticar
        if self.posicion[1] > ALTO - 10 - self.radius or self.posicion[1] < 10 + self.radius :
            self.velocidad[1] *= -1
        
        #rebote horizontal
        if self.posicion[0] < 35 + self.radius:
            if self.posicion[1] > player1.posicion()[0] and self.posicion[1] < player1.posicion()[1]: 
                # si la pelota esta tocando la barra del player 1 rebota
                self.velocidad[0] *= -1
            else:
                # en caso contrario gana el player 2
                player2.act_puntuacion(1)
                self.reinicio(1)
        elif self.posicion[0] > ANCHO - 35 - self.radius:
            if self.posicion[1] > player2.posicion()[0] and self.posicion[1] < player2.posicion()[1]:
                # si la pelota esta tocando la barra del player 2 rebota
                self.velocidad[0] *= -1
            else:
                # en caso contrario gana el player 1
                player1.act_puntuacion(1)
                self.reinicio(2)

    def reinicio(self, gana):
        self.posicion = [ANCHO / 2, ALTO / 2]
        self.velocidad = [4, random.randrange(1, 9)]
        if gana == 1:
            self.velocidad[0] *= -1

def separador(window):
    altura =(ALTO - 20) / 8
    i = 10
    while i <= ALTO - 10:
        pygame.draw.rect(window, GRIS, ([ANCHO / 2, i],[5, altura]))
        i += altura + 10

def puntuacione(window, fuente, jugador, position1):
    puntuacion = jugador.puntaje
    text = str(puntuacion)
    textRender = fuente.render(text, True, BLANCO)
    cajaText = textRender.get_rect()
    cajaText.centerx = int(position1)
    cajaText.centery = 100
    window.blit(textRender, cajaText)

def main():
    pygame.init()

    ARIAL30 = pygame.font.SysFont("Arial", 30)

    #creacion de objetos
    jugador1 = jugador(1)
    jugador2 = jugador(2)
    pelota1 = pelota()
    
    #creacion de la ventana
    windows = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("PyPONG")
    
    #loop Principal
    run = True
    clock = pygame.time.Clock()
    
    while run:
        # Fondo
        windows.fill(NEGRO)
        separador(windows)
        puntuacione(windows, ARIAL30, jugador1, CENTRO_IZQ)
        puntuacione(windows, ARIAL30, jugador2, CENTRO_DER)

        # dibujo de Sprites
        jugador1.dibujar(windows)
        jugador2.dibujar(windows)
        pelota1.dibujar(windows)


        # Eventos
        for event in pygame.event.get():
            # Quitar juego
            if event.type == pygame.QUIT:
                run = False 
            
            #controles
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    jugador1.mover("arriba")
                if event.key == pygame.K_s:
                    jugador1.mover("abajo")
                if event.key == pygame.K_UP:
                    jugador2.mover("arriba")
                if event.key == pygame.K_DOWN:
                    jugador2.mover("abajo")
            
            elif event.type == pygame.KEYUP: 
                # Cuando se deja de Presionar las teclas
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    jugador1.mover("no")
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    jugador2.mover("no")
        # actualizaciones de sprites
        jugador1.actualizar()
        jugador2.actualizar()
        pelota1.actualizar(jugador1, jugador2)
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()