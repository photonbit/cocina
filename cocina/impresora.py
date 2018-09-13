#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys

try:
    import scribus
except ImportError, err:
    print "Esto está pensado para ser ejecutado desde Scribus."
    print "Sin Scribus no hay escrito."
    sys.exit(1)

import math

from obra import Cocina


class Punto(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def rotar(self, matriz):
        return Punto(
            self.x * matriz[0].x + self.y * matriz[0].y,
            self.x * matriz[1].x + self.y * matriz[1].y
        )


class Formato(object):
    INTERLINEADO_FIJO = 0
    INTERLINEADO_AUTOMATICO = 1

    SIN_MARGENES = (0, 0, 0, 0)
    MARGENES_5_7_ANCHO = 5.0 / 7
    MARGENES_2_3_DIAGONAL = 2.0 / 3
    MARGENES_3_4_DIAGONAL = 3.0 / 4
    MARGENES_ISO = 1.0

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
            fontsize=50.0
        )

        scribus.createCharStyle(
            name="estilo_cuerpo_poema",
            font="Lato Regular",
            fontsize=35.0
        )

        scribus.createCharStyle(
            name="estilo_cuerpo_prosa",
            font="Lato Regular",
            fontsize=30.0
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
            linespacing=70.0,
            charstyle="estilo_cuerpo_poema"
        )

        scribus.createParagraphStyle(
            name="parrafo_receta",
            alignment=scribus.ALIGN_BLOCK,
            linespacingmode=Formato.INTERLINEADO_FIJO,
            linespacing=60,
            charstyle="estilo_cuerpo_prosa"
        )

    @classmethod
    def marginar(cls, punto, dimension, norma=MARGENES_5_7_ANCHO, traslado_x=0.5, traslado_y=0.5):
        alpha = math.atan2(dimension.y, dimension.x)

        if norma == Formato.MARGENES_5_7_ANCHO or norma == Formato.MARGENES_ISO:
            nuevo_ancho = dimension.x * norma
            nueva_hipo = nuevo_ancho / math.cos(alpha)
        elif norma == Formato.MARGENES_2_3_DIAGONAL or norma == Formato.MARGENES_3_4_DIAGONAL:
            hipo = math.hypot(dimension.x, dimension.y)
            nueva_hipo = hipo * norma
        else:
            raise Exception("Pero qué formato de margen es ese")

        nueva_dimension = Punto(math.cos(alpha) * nueva_hipo, math.sin(alpha) * nueva_hipo)
        margenes = Punto(dimension.x - nueva_dimension.x, dimension.y - nueva_dimension.y)

        p = Punto(punto.x + margenes.x * traslado_x, punto.y + margenes.y * traslado_y)

        return p, nueva_dimension


class Dimension(object):
    A = Punto(Formato.X[2], Formato.Y[2])
    B = Punto(Formato.X[3], Formato.Y[1])
    C = Punto(Formato.X[1], Formato.Y[2])
    D = Punto(Formato.Y[1], Formato.X[3])


class Puntos(object):
    O = Punto(Formato.X[0], Formato.Y[0])
    P = Punto(Formato.X[0], Formato.Y[1])
    Q = Punto(Formato.X[1], Formato.Y[1])
    R = Punto(Formato.X[2], Formato.Y[1])
    S = Punto(Formato.X[3], Formato.Y[0])


#   Puntos:
#
#     O------------S   O------------S
#     |            |   |            |
#     |            |   |            |
#     P---Q--------|   P--------R---|
#     |   |        |   |        |   |
#     |   |        |   |        |   |
#     |   |        |   |        |   |
#     |   |        |   |        |   |
#     |   |        |   |        |   |
#     |   |        |   |        |   |
#     |___|________|   |________|___|
#


class Espacio(object):

    def _genera_matriz(self):
        if not self.rotacion:
            return None

        theta = math.radians(self.rotacion)
        coseno = math.cos(theta)
        seno = math.sin(theta)
        return [Punto(coseno, -seno), Punto(seno, coseno)]

    def __init__(self, origen, rotacion=0):
        self.origen = origen
        self.rotacion = rotacion
        self.matriz_rotacion = self._genera_matriz()

    def posicionar(self, nombre, punto):
        if self.rotacion is not 0:
            scribus.rotateObject(self.rotacion, nombre)
            punto = punto.rotar(self.matriz_rotacion)
        punto = Punto(punto.x + self.origen.x, punto.y + self.origen.y)
        scribus.moveObject(punto.x, punto.y, nombre)

    @classmethod
    def rectangulo(cls, posicion, dimension):
        scribus.createRect(posicion.x, posicion.y, dimension.x, dimension.y)

    @classmethod
    def linea(clscls, inicio, fin):
        scribus.createLine(inicio.x, inicio.y, fin.x, fin.y)

    def cuadro_de_texto(self, posicion, dimension, texto, nombre, estilo=None, marginar=True):
        if marginar:
            p, d = Formato.marginar(posicion, dimension)
        else:
            p, d = posicion, dimension
        scribus.createText(0, 0, d.x, d.y, nombre)
        self.posicionar(nombre, p)
        scribus.insertText(texto, 0, nombre)
        if estilo is not None:
            long_texto = scribus.getTextLength(nombre)
            scribus.selectText(0, long_texto, nombre)
            scribus.setStyle(estilo, nombre)

    def imagen(self, posicion, dimension, fichero):
        marco_imagen = scribus.createImage(0, 0, dimension.x, dimension.y)
        self.posicionar(marco_imagen, posicion)
        scribus.loadImage(fichero, marco_imagen)
        scribus.setScaleImageToFrame(True, False, marco_imagen)
        scaleX, scaleY = scribus.getImageScale(marco_imagen)
        scribus.setScaleImageToFrame(False, False, marco_imagen)
        scale = scaleY
        if scaleY > scaleX:
            scale = scaleX
        scribus.setImageScale(scale, scale, marco_imagen)


class Impresora(object):
    @classmethod
    def iniciar_portada(cls):
        portada = scribus.newDocument(
            scribus.PAPER_A3,
            Formato.SIN_MARGENES,
            scribus.LANDSCAPE,
            1,  # firstPageNumber
            scribus.UNIT_MILLIMETERS,
            scribus.PAGE_1,  # pagesType
            0,  # firstPageOrder
            1  # numPage
        )
        scribus.setInfo(Cocina.autor, Cocina.info, Cocina.descripcion)

    @classmethod
    def iniciar_documento(cls):
        obra = scribus.newDocument(
            scribus.PAPER_A4,
            Formato.SIN_MARGENES,
            scribus.PORTRAIT,
            1,  # firstPageNumber
            scribus.UNIT_MILLIMETERS,
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
        Impresora.renglones_para_anotar(Puntos.R)
        scribus.closeMasterPage()

    @classmethod
    def rellena_titulo(cls, titulo, espacio, origen, page_num):
        espacio.cuadro_de_texto(
            Punto(origen.x, origen.y + 100),
            Punto(Formato.A5.x, 50),
            titulo,
            "cuadro_titulo_{}".format(page_num),
            "parrafo_titulo",
            True
        )

    @classmethod
    def rellenar_pasos_receta(cls, receta, page_num):
        espacio_receta = Espacio(Puntos.Q)
        Impresora.rellena_titulo(receta["titulo"], espacio_receta, Puntos.O, page_num)
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
        Impresora.rellena_titulo("Ingredientes", espacio_receta, Puntos.O, page_num)

        texto_ingredientes = ""
        for ingrediente in receta["ingredientes"]:
            cantidad, unidad, nombre = ingrediente
            if unidad == "unidad":
                texto_ingredientes += "{} {}\n".format(cantidad, nombre)
            else:
                if not isinstance(cantidad, int):
                    cantidad = "{}/{}".format(*cantidad.as_integer_ratio())
                texto_ingredientes += "{} {} de {}\n".format(cantidad, unidad, nombre)

        espacio_receta.cuadro_de_texto(
            Punto(Puntos.O.x, Puntos.O.y + 50),
            Dimension.A,
            texto_ingredientes,
            "cuadro_contenido_{}".format(page_num),
            "parrafo_receta"
        )

    @classmethod
    def rellenar_poema(cls, poema, page_num):
        espacio_poema = Espacio(Puntos.Q)
        Impresora.rellena_titulo(poema["titulo"], espacio_poema, Puntos.O, page_num)

        espacio_poema.cuadro_de_texto(
            Punto(Puntos.O.x, Puntos.O.y + 50),
            Dimension.A,
            poema["contenido"],
            "cuadro_contenido_{}".format(page_num),
            "parrafo_poema"
        )

    @classmethod
    def rellenar_tecnica(cls, page_num):
        if page_num % 2:
            espacio_tecnica = Espacio(Puntos.S, -90)
        else:
            espacio_tecnica = Espacio(Puntos.P, 90)

        texto = Cocina.tecnicas[0]["nombre"] + "\n\n\n"
        for tecnica, nombre in Cocina.tecnicas[0]["compendio"].iteritems():
            texto += nombre + "\n"
            texto += tecnica + "\n\n"

        espacio_tecnica.cuadro_de_texto(
            Puntos.O,
            Dimension.D,
            texto,
            "cuadro_tecnicas_{}".format(page_num),
            "parrafo_receta",
            False
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
                Impresora.imagen_anotacion(Puntos.P)
                if page_num % 8 == 1:
                    receta = i_receta.next()
                    cls.rellenar_pasos_receta(receta, page_num)
                else:
                    cls.rellenar_poema(i_poema.next(), page_num)
            else:
                scribus.applyMasterPage(Cocina.receta_B, page_num)
                Impresora.imagen_anotacion(Puntos.R)
                if page_num % 8 == 2:
                    cls.rellenar_ingredientes_receta(receta, page_num)

            cls.rellenar_tecnica(page_num)
