#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys

try:
    import scribus
except ImportError, err:
    print "This Python script is written for the Scribus scripting interface."
    print "It can only be run from within Scribus."
    sys.exit(1)

from obra import Cocina

class Punto(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Formato(object):
    # Page formatting
    INTERLINEADO_FIJO = 0
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
        scribus.createCharStyle(
            name="estilo_titulo",
            font="Crimson Text Bold",
            features="bold",
            fontsize=18.0
        )

        scribus.createCharStyle(
            name="estilo_cuerpo",
            font="Lato Regular",
            fontsize=14.0
        )

        scribus.createParagraphStyle(
            name="parrafo_titulo",
            alignment=scribus.ALIGN_LEFT,
            charstyle="estilo_titulo"
        )

        scribus.createParagraphStyle(
            name="parrafo_poema",
            alignment=scribus.ALIGN_LEFT,
            linespacingmode=Formato.INTERLINEADO_FIJO,
            linespacing=22,
            charstyle="estilo_cuerpo"
        )

        scribus.createParagraphStyle(
            name="parrafo_receta",
            alignment=scribus.ALIGN_BLOCK,
            linespacingmode=Formato.INTERLINEADO_FIJO,
            linespacing=22,
            charstyle="estilo_cuerpo"
        )

    @classmethod
    def marginar(cls, punto, dimension):
        p = Punto(punto.x + dimension.x/5, punto.y + dimension.y/6)
        d = Punto(dimension.x - 2*dimension.x/5, dimension.y - 2*dimension.y/6)

        return p, d


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

    @classmethod
    def linea(clscls, inicio, fin):
        scribus.createLine(inicio.x, inicio.y, fin.x, fin.y)

    def cuadro_de_texto(self, posicion, dimension, texto, nombre, estilo = None):
        p, d = Formato.marginar(posicion, dimension)
        scribus.createText(p.x, p.y, d.x, d.y, nombre)
        self.posicionar(nombre)
        scribus.insertText(texto, 0, nombre)
        if estilo is not None:
            long_texto = scribus.getTextLength(nombre)
            scribus.selectText(0, long_texto , nombre)
            scribus.setStyle(estilo, nombre)

    def imagen(self, posicion, dimension, fichero):
        marco_imagen = scribus.createImage(posicion.x, posicion.y, dimension.x, dimension.y)
        self.posicionar(marco_imagen)
        scribus.loadImage(fichero, marco_imagen)


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
    def renglones_para_anotar(cls, base):

        inicio = Punto(base.x, base.y + Dimension.C.y // 3)
        margen_izqdo = Dimension.C.x / 6
        margen_derecho = Dimension.C.x * 5 / 6

        salto = (Dimension.C.y // 3) * 2 / 10

        for i in range(1, 10):
            Espacio.linea(
                Punto(base.x + margen_izqdo, inicio.y + salto * i),
                Punto(base.x + margen_derecho, inicio.y + salto * i)
            )

    @classmethod
    def imagen_anotacion(cls, base):
        inicio = Punto(Dimension.C.x / 6, 50)
        tamanio = Punto(Dimension.C.x * 4 / 6, Dimension.C.y // 3 - 50)
        espacio_imagen = Espacio(base)
        espacio_imagen.imagen(inicio, tamanio, Cocina.imagen_aleatoria())



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
        Impresora.imagen_anotacion(Puntos.P)
        Impresora.renglones_para_anotar(Puntos.P)
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
        Impresora.imagen_anotacion(Puntos.R)
        Impresora.renglones_para_anotar(Puntos.R)
        scribus.closeMasterPage()

    @classmethod
    def rellenar_pasos_receta(cls, receta, page_num):
        espacio_receta = Espacio(Puntos.Q)
        espacio_receta.cuadro_de_texto(
            Punto(Puntos.O.x, Puntos.O.y + 120),
            Punto(Formato.A5.x, 30),
            receta["titulo"],
            "cuadro_titulo_{}".format(page_num),
            "parrafo_titulo"
        )
        espacio_receta.cuadro_de_texto(
            Punto(Puntos.O.x, Puntos.O.y + 50),
            Dimension.A,
            receta["contenido"],
            "cuadro_contenido_{}".format(page_num),
            "parrafo_receta"
        )

    @classmethod
    def rellenar_ingredientes_receta(cls, receta, page_num):
        espacio_receta = Espacio(Puntos.P)
        espacio_receta.cuadro_de_texto(
            Punto(Puntos.O.x, Puntos.O.y + 120),
            Punto(Formato.A5.x, 30),
            receta["titulo"] + "\n\nIngredientes",
            "cuadro_titulo_{}".format(page_num),
            "parrafo_titulo"
        )

        texto_ingredientes = ""
        for ingrediente in receta["ingredientes"]:
            texto_ingredientes += "{} {} de {}\n".format(*ingrediente)

        espacio_receta.cuadro_de_texto(
            Punto(Puntos.O.x, Puntos.O.y + 50),
            Dimension.A,
            texto_ingredientes,
            "cuadro_contenido_{}".format(page_num),
            "parrafo_receta"
        )

    @classmethod
    def rellenar_poema(cls, poema, page_num):
        espacio_receta = Espacio(Puntos.Q)
        espacio_receta.cuadro_de_texto(
            Punto(Puntos.O.x, Puntos.O.y + 120),
            Punto(Formato.A5.x, 30),
            poema["titulo"],
            "cuadro_titulo_{}".format(page_num),
            "parrafo_titulo"
        )
        espacio_receta.cuadro_de_texto(
            Punto(Puntos.O.x, Puntos.O.y + 50),
            Dimension.A,
            poema["contenido"],
            "cuadro_contenido_{}".format(page_num),
            "parrafo_poema"
        )

    @classmethod
    def rellenar_documento(cls):
        i_poema = iter(Cocina.poemas)
        i_receta = iter(Cocina.recetas)
        receta = None
        for page_num in range(1, Cocina.num_paginas + 1):
            scribus.gotoPage(page_num)
            if page_num % 2:
                scribus.applyMasterPage(Cocina.receta_A, page_num)
                if page_num % 8 == 1:
                    receta = i_receta.next()
                    cls.rellenar_pasos_receta(receta, page_num)
                else:
                    cls.rellenar_poema(i_poema.next(), page_num)
            else:
                scribus.applyMasterPage(Cocina.receta_B, page_num)
                if page_num % 8 == 2:
                    cls.rellenar_ingredientes_receta(receta, page_num)

            # Seleccionar cuadro tecnicas
            # meter tecnica
            # Seleccionar cuadro marcapaginas
            # meter algo?
