#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Escrito por Jaime Vargas

#--------------------------------
# Inportacion de Modulos
#--------------------------------

import pygame
from pygame.locals import *
import os
import sys

# -----------
# Constantes
# -----------

ANCHO = 640
ALTO = 480
NEGRO = (0,0,0)
BLANCO = (255,255,255)

# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------

# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------

class jugador():
    def __init__(self, player):
        self.dimension = [10, 100] #tamaño de los sprites
        pos_vertical = ALTO / 2 - self.dimension[1] / 2
        
        if player == 1: # posicion del jugador 1
            self.pos = [25, pos_vertical] 
        elif player == 2: # posicion del jugador 2
            self.pos = [ANCHO - self.dimension[0] - 25, pos_vertical]
        
        self.velocidad = 0
        self.aceleracion = 2
    
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


def main():
    pygame.init()

    #creacion de los jugadores
    jugador1 = jugador(1)
    jugador2 = jugador(2)
    
    #creacion de la ventana
    windows = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("PyPONG")

    #loop Principal
    while True:

        # Fondo
        windows.fill(NEGRO)
        # Dibujar Jugadores
        jugador1.dibujar(windows)
        jugador2.dibujar(windows)

        # Entradas del teclado y mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
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
            
            elif event.type == pygame.KEYUP: # Cuando se deja de Presionar las teclas
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    jugador1.mover("no")
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    jugador2.mover("no")
        
        jugador1.actualizar()
        jugador2.actualizar()
        pygame.display.update()


if __name__ == "__main__":
    main()