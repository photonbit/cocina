#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys

from collections import namedtuple

try:
    import scribus
except ImportError, err:
    print "This Python script is written for the Scribus scripting interface."
    print "It can only be run from within Scribus."
    sys.exit(1)

from obra import Cocina, poemas

class Punto(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Formato(object):
    # Page formatting
    SIN_MARGENES = (0, 0, 0, 0)
    A3 = Punto(*scribus.PAPER_A3)
    A4 = Punto(*scribus.PAPER_A4)
    A5 = Punto(*scribus.PAPER_A5)
    A6 = Punto(*scribus.PAPER_A6)

    X = (
        0,
        A4.x - A5.x,
        A5.x,
        A4.x
    )

    Y = (
        0,
        A4.y - A5.y,
        A5.y,
        A4.y
    )

    @classmethod
    def crear_estilos(cls):
        estilo_titulo = scribus.createCharStyle(
            name="estilo_titulo",
            features="bold",
            fontsize=18.0
        )

        estilo_cuerpo = scribus.createCharStyle(
            name="estilo_cuerpo",
            fontsize=12.0
        )

        parrafo_titulo = scribus.createParagraphStyle(
            name="parrafo_titulo",
            linespacing=2,
            alignment=scribus.ALIGN_LEFT,
            charstyle="estilo_titulo"
        )

        parrafo_poema = scribus.createParagraphStyle(
            name="parrafo_poema",
            linespacing=1.5,
            alignment=scribus.ALIGN_LEFT,
            charstyle="estilo_cuerpo"
        )
        parrafo_receta = scribus.createParagraphStyle(
            name="parrafo_receta",
            linespacing=1,
            alignment=scribus.ALIGN_BLOCK,
            charstyle="estilo_cuerpo"
        )


class Dimension(object):
    A = Punto(Formato.X[2], Formato.Y[2])
    B = Punto(Formato.X[3], Formato.Y[1])
    C = Punto(Formato.X[1], Formato.Y[2])


class Puntos(object):
    O = Punto(Formato.X[0], Formato.Y[0])
    P = Punto(Formato.X[0], Formato.Y[1])
    Q = Punto(Formato.X[1], Formato.Y[1])
    R = Punto(Formato.X[2], Formato.Y[1])


class Espacio(object):

    def __init__(self, origen, rotacion = 0):
        self.origen = origen
        self.rotacion = rotacion

    def posicionar(self, nombre):
        scribus.moveObject(self.origen.x, self.origen.y, nombre)
        if self.rotacion is not 0:
            scribus.rotateObject(self.rotacion, nombre)

    @classmethod
    def rectangulo(cls, posicion, dimension):
        scribus.createRect(posicion.x, posicion.y, dimension.x, dimension.y)

    def cuadro_de_texto(self, posicion, dimension, texto, nombre, estilo = None):
        scribus.createText(posicion.x, posicion.y, dimension.x, dimension.y, nombre)
        self.posicionar(nombre)
        scribus.insertText(texto, 0, nombre)
        if estilo is not None:
            scribus.selectText(0, len(texto) - 1 , nombre)
            scribus.setStyle(estilo, nombre)

    def imagen(self, posicion, dimension, fichero):
        scribus.createImage(posicion.x, posicion.y, dimension.x, dimension.y)
        self.posicionar()
        scribus.loadImage(fichero)


class Impresora(object):
    @classmethod
    def iniciar_portada(cls):
        portada = scribus.newDocument(
            scribus.PAPER_A3,  # size
            Formato.SIN_MARGENES,  # margins
            scribus.LANDSCAPE,  # orientation
            1,  # firstPageNumber
            scribus.UNIT_MILLIMETERS,  # unit
            scribus.PAGE_1,  # pagesType
            0,  # firstPageOrder
            1  # numPage
        )
        scribus.setInfo(Cocina.autor, Cocina.info, Cocina.descripcion)

    @classmethod
    def iniciar_documento(cls):
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

    @classmethod
    def pagina_maestra_impares(cls):
        scribus.createMasterPage(Cocina.receta_A)
        scribus.editMasterPage(Cocina.receta_A)
        # Cuadro receta
        Espacio.rectangulo(Puntos.Q, Dimension.A)
        # Cuadro tecnica
        Espacio.rectangulo(Puntos.O, Dimension.B)
        # Cuadro anotaciones
        Espacio.rectangulo(Puntos.P, Dimension.C)
        scribus.closeMasterPage()

    @classmethod
    def pagina_maestra_pares(self):
        scribus.createMasterPage(Cocina.receta_B)
        scribus.editMasterPage(Cocina.receta_B)
        # Cuadro receta
        Espacio.rectangulo(Puntos.P, Dimension.A)
        # Cuadro tecnica
        Espacio.rectangulo(Puntos.O, Dimension.B)
        # Cuadro anotaciones
        Espacio.rectangulo(Puntos.R, Dimension.C)

        scribus.closeMasterPage()

    @classmethod
    def rellenar_documento(cls):
        for page_num in range(1, Cocina.num_paginas + 1):
            scribus.gotoPage(page_num)
            if page_num % 2:
                scribus.applyMasterPage(Cocina.receta_A, page_num)
                # Seleccionar cuadro para poema
                # meterlo poema
                page_num_str = str(page_num)
                poema_num = page_num // 2
                if poema_num < len(poemas):
                    espacio_receta = Espacio(Puntos.Q)
                    espacio_receta.cuadro_de_texto(
                        Puntos.O,
                        Dimension.A,
                        poemas[poema_num]["contenido"],
                        "cuadro_contenido_{}".format(page_num)
                    )
            else:
                scribus.applyMasterPage(Cocina.receta_B, page_num)
                # Seleccionar cuadro contenido
                # meter ingredientes si estamos en receta

            # Seleccionar cuadro tecnicas
            # meter tecnica
            # Seleccionar cuadro marcapaginas
            # meter algo?
