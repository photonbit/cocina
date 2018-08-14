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


class Cocina(object):
    # Document Information
    autor = "Daniel Moreno Medina"
    info = ""
    descripcion = ""
    num_recetas = 4
    num_poemas = 9
    num_paginas = (num_recetas + num_poemas) * 2

    # Master pages
    receta_A = "recetaDelante"
    receta_B = "recetaDetras"


class Formato(object):
    # Page formatting
    SIN_MARGENES = (0, 0, 0, 0)
    A3 = Punto(*scribus.PAPER_A3)
    A4 = Punto(*scribus.PAPER_A4)
    A5 = Punto(*scribus.PAPER_A5)


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


class Impresora(object):
    def crear_documento(self):
        obra = scribus.newDocument(
            scribus.PAPER_A4,  # size
            Formato.SIN_MARGENES,  # margins
            scribus.PORTRAIT,  # orientation
            1,  # firstPageNumber
            scribus.UNIT_MILLIMETERS,  # unit
            scribus.PAGE_1,  # pagesType
            0,  # firstPageOrder
            Cocina.num_paginas  # numPage
        )
        scribus.setInfo(Cocina.autor, Cocina.info, Cocina.descripcion)

    def pagina_maestra_impares(self):
        scribus.createMasterPage(Cocina.receta_A)
        scribus.editMasterPage(Cocina.receta_A)
        # Cuadro receta
        scribus.createRect(
            Cocina.A4.x - Cocina.A5.x,
            Cocina.A4.y - Cocina.A5.y,
            Cocina.A5.x,
            Cocina.A5.y
        )
        # Cuadro tecnica
        scribus.createRect(
            0,
            0,
            Cocina.A4.x,
            Cocina.A4.y - Cocina.A5.y
        )
        # Cuadro anotaciones
        scribus.createRect(
            0,
            Cocina.A4.y - Cocina.A5.y,
            Cocina.A4.x - Cocina.A5.x,
            Cocina.A5.y
        )
        scribus.closeMasterPage()

    def pagina_maestra_pares(self):
        scribus.createMasterPage(Cocina.receta_B)
        scribus.editMasterPage(Cocina.receta_B)
        # Cuadro receta
        scribus.createRect(
            0,
            Cocina.A4.y - Cocina.A5.y,
            Cocina.A5.x,
            Cocina.A5.y
        )
        # Cuadro tecnica
        scribus.createRect(
            0,
            0,
            Cocina.A4.x,
            Cocina.A4.y - Cocina.A5.y
        )
        # Cuadro anotaciones
        scribus.createRect(
            Cocina.A5.x,
            Cocina.A4.y - Cocina.A5.y,
            Cocina.A4.x - Cocina.A5.x,
            Cocina.A5.y
        )

        scribus.closeMasterPage()
