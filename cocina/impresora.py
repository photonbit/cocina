#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys

try:
    import scribus
except ImportError, err:
    print "This Python script is written for the Scribus scripting interface."
    print "It can only be run from within Scribus."
    sys.exit(1)


class Punto(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Espacio(object):
    def __init__(self, origen, rotacion = 0):
        self.origen = origen
        self.rotacion = rotacion

    def posicionar(self):
        scribus.moveObject(self.origen.x, self.origen.y)
        if self.rotacion is not 0:
            scribus.rotateObject(self.rotacion)

    def cuadro_de_texto(self, posicion, dimension, texto, estilo = None):
        scribus.createText(posicion.x, posicion.y, dimension.x, dimension.y)
        self.posicionar()
        scribus.insertText(texto, 0)
        if estilo is not None:
            scribus.selectText(0, len(texto))
            scribus.setStyle(estilo)

    def imagen(self, posicion, dimension, fichero):
        scribus.createImage(posicion.x, posicion.y, dimension.x, dimension.y)
        self.posicionar()
        scribus.loadImage(fichero)
