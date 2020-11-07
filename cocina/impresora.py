#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import os
import time

try:
    import scribus
except ImportError as err:
    print("Esto está pensado para ser ejecutado desde Scribus.")
    print("Sin Scribus no hay escrito.")
    sys.exit(1)

import math

from obra import Cocina


class Punto(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def rotar(self, matriz):
        a = self.x * matriz[0].x + self.y * matriz[0].y
        b = self.x * matriz[1].x + self.y * matriz[1].y
        return Punto(a, b)


A3 = Punto(*scribus.PAPER_A3)
A4 = Punto(*scribus.PAPER_A4)
A5 = Punto(*scribus.PAPER_A5)
A6 = Punto(*scribus.PAPER_A6)


class Formato(object):
    INTERLINEADO_FIJO = 0
    INTERLINEADO_AUTOMATICO = 1

    SIN_MARGENES = (0, 0, 0, 0)
    MARGENES_5_7_ANCHO = 5.0 / 7
    MARGENES_2_3_DIAGONAL = 2.0 / 3
    MARGENES_3_4_DIAGONAL = 3.0 / 4
    MARGENES_ISO = 1.0

    DOBLADO_VALLE = scribus.LINE_DASH
    DOBLADO_MONTE = scribus.LINE_DASHDOT

    @classmethod
    def crear_estilos(cls):
        scribus.createCharStyle(
            name="estilo_titulo", font="Crimson Text Bold", fontsize=50.0
        )

        scribus.createCharStyle(
            name="estilo_cuerpo_poema", font="Lato Regular", fontsize=35.0
        )

        scribus.createCharStyle(
            name="estilo_cuerpo_prosa", font="Lato Regular", fontsize=30.0
        )

        scribus.createParagraphStyle(
            name="parrafo_titulo",
            alignment=scribus.ALIGN_LEFT,
            charstyle="estilo_titulo",
            linespacing=80,
        )

        scribus.createParagraphStyle(
            name="parrafo_poema",
            alignment=scribus.ALIGN_LEFT,
            linespacingmode=Formato.INTERLINEADO_FIJO,
            linespacing=70.0,
            charstyle="estilo_cuerpo_poema",
        )

        scribus.createParagraphStyle(
            name="parrafo_receta",
            alignment=scribus.ALIGN_BLOCK,
            linespacingmode=Formato.INTERLINEADO_FIJO,
            linespacing=60,
            charstyle="estilo_cuerpo_prosa",
        )

        scribus.createParagraphStyle(
            name="parrafo_lista",
            alignment=scribus.ALIGN_LEFT,
            linespacingmode=Formato.INTERLINEADO_FIJO,
            linespacing=70.0,
            charstyle="estilo_cuerpo_poema",
        )

    @classmethod
    def marginar(
        cls, punto, dimension, norma=MARGENES_5_7_ANCHO, traslado_x=0.5, traslado_y=0.5
    ):
        alpha = math.atan2(dimension.y, dimension.x)

        if norma == Formato.MARGENES_5_7_ANCHO or norma == Formato.MARGENES_ISO:
            # Conocemos la relación del cateto opuesto
            nuevo_ancho = dimension.x * norma
            nueva_hipo = nuevo_ancho / math.cos(alpha)
        elif (
            norma == Formato.MARGENES_2_3_DIAGONAL
            or norma == Formato.MARGENES_3_4_DIAGONAL
        ):
            # Conocemos la relación de la hipotenusa
            hipo = math.hypot(dimension.x, dimension.y)
            nueva_hipo = hipo * norma
        else:
            raise Exception("Pero qué formato de margen es ese")

        nueva_dimension = Punto(
            math.cos(alpha) * nueva_hipo, math.sin(alpha) * nueva_hipo
        )
        margenes = Punto(
            dimension.x - nueva_dimension.x, dimension.y - nueva_dimension.y
        )

        p = Punto(punto.x + margenes.x * traslado_x, punto.y + margenes.y * traslado_y)

        return p, nueva_dimension


class Dimension(object):
    A = Punto(A5.x, A5.y)
    B = Punto(A4.x - 20, A4.y - A5.y - 20)
    C = Punto(A4.x - A5.x - 20, A5.y)

    D = Punto(A4.y - A5.y - 40, A4.x - 40)
    E = Punto(A4.x - 60, A4.y - A5.y - 80)


class Puntos(object):
    O = Punto(0 + 10, 0 + 10)
    P = Punto(0 + 10, A4.y - A5.y - 10)
    Q = Punto(A4.x - A5.x - 10, A4.y - A5.y - 10)
    R = Punto(A5.x + 10, A4.y - A5.y - 10)
    S = Punto(A4.x - 10, 0 + 10)

    T = Punto(0 + 20, 0 + 20)


#   Puntos obra:
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

#   Puntos portada:
#
#     O--------------P-------Q--+
#     |              |        \ |
#     |              |         \|
#     |----J----K----L----------R
#     |    |    |    |          |
#     |    |    |    |          |
#     |    |    |    |          |
#     |----Z----Y----W----------S
#     |              |         /|
#     |              |        / |
#     |______________V______T___|
#


class PuntosPortada(object):
    O = Punto(0, 0)
    P = Punto(A4.x, 0)
    Q = Punto(A4.x + A5.y / 2, 0)
    R = Punto(A3.y, (A3.x - A5.x) / 2)
    S = Punto(A3.y, A3.x / 2 + A5.x / 2)
    T = Punto(Q.x, A3.x)
    V = Punto(A4.x, A3.x)
    W = Punto(P.x, S.y)
    Y = Punto(W.x - R.y, S.y)
    Z = Punto(Y.x - A5.y / 2, S.y)
    J = Punto(Z.x, R.y)
    K = Punto(Y.x, R.y)
    L = Punto(A4.x, R.y)


#   Puntos lenguetas:
#
#     O---------------+----------+
#     |               |        \ |
#     |     /A-B\/C-D\|         \|
#     |----J----K-----L----------+
#     |    |    |     |          |
#     |    |    |     |          |
#     |    |    |     |          |
#     |----Z----Y-----W----------+
#     |    \E-F/\G-H/ |         /|
#     |_______________+_______/__|
#


class PuntosLenguetas(object):
    W = PuntosPortada.W
    Y = PuntosPortada.Y
    Z = PuntosPortada.Z
    J = PuntosPortada.J
    K = PuntosPortada.K
    L = PuntosPortada.L

    A = Punto(J.x + 10, J.y - 30)
    B = Punto(K.x - 10, A.y)
    C = Punto(K.x + 10, A.y)
    D = Punto(L.x - 10, A.y)
    E = Punto(A.x, Z.y + 30)
    F = Punto(B.x, E.y)
    G = Punto(C.x, E.y)
    H = Punto(D.x, E.y)


class Espacio(object):
    def _genera_matriz(self):
        if not self.rotacion:
            return None

        theta = math.radians(self.rotacion)
        coseno = math.cos(theta)
        seno = math.sin(theta)
        return [Punto(coseno, seno), Punto(-seno, coseno)]

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
    def linea(cls, inicio, fin, estilo=None):
        nombre = scribus.createLine(inicio.x, inicio.y, fin.x, fin.y)
        if estilo:
            scribus.setLineStyle(estilo, nombre)

    @classmethod
    def multi_linea(cls, puntos, estilo=None):
        lista = []
        for punto in puntos:
            lista.append(punto.x)
            lista.append(punto.y)
        nombre = scribus.createPolyLine(lista)
        if estilo:
            scribus.setLineStyle(estilo, nombre)

    def cuadro_de_texto(
        self, posicion, dimension, texto, nombre, estilo=None, marginar=True
    ):
        # Seleccionar tipo de margen según estilo
        if estilo == "parrafo_receta":
            norma_margen = Formato.MARGENES_3_4_DIAGONAL
        else:
            norma_margen = Formato.MARGENES_5_7_ANCHO
        if marginar:
            p, d = Formato.marginar(posicion, dimension, norma_margen)
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
        scribus.setScaleImageToFrame(True, True, marco_imagen)


class Impresora(object):
    cocinar_lento = True

    @classmethod
    def tick(cls, page=None):
        if Impresora.cocinar_lento:
            scribus.redrawAll()
            time.sleep(1)
        if page is not None:
            scribus.gotoPage(page)
            if page > 1:
                scribus.scrollDocument(0, 1207)  # Depende del tamaño de la ventana :(

    @classmethod
    def iniciar_portada(cls):
        scribus.statusMessage("Generando documento de portada")
        portada = scribus.newDocument(
            scribus.PAPER_A3,
            Formato.SIN_MARGENES,
            scribus.LANDSCAPE,
            1,  # firstPageNumber
            scribus.UNIT_POINTS,
            scribus.PAGE_1,  # pagesType
            0,  # firstPageOrder
            1,  # numPage
        )
        scribus.setInfo(Cocina.autor, Cocina.info, Cocina.descripcion)

    @classmethod
    def iniciar_documento(cls):
        scribus.statusMessage("Generando documento para la colección")
        obra = scribus.newDocument(
            scribus.PAPER_A4,
            Formato.SIN_MARGENES,
            scribus.PORTRAIT,
            1,  # firstPageNumber
            scribus.UNIT_MILLIMETERS,
            scribus.PAGE_1,  # pagesType
            0,  # firstPageOrder
            Cocina.num_paginas,  # numPage
        )
        scribus.setInfo(Cocina.autor, Cocina.info, Cocina.descripcion)
        scribus.zoomDocument(-100)
        scribus.setRedraw(True)

    @classmethod
    def renglones_para_anotar(cls, base):
        scribus.statusMessage("Pintando renglones para anotar")
        inicio = Punto(base.x, base.y + Dimension.C.y // 3)
        margen_izqdo = Dimension.C.x / 6
        margen_derecho = Dimension.C.x * 5 / 6

        salto = (Dimension.C.y // 3) * 2 / 10

        for i in range(1, 10):
            Espacio.linea(
                Punto(base.x + margen_izqdo, inicio.y + salto * i),
                Punto(base.x + margen_derecho, inicio.y + salto * i),
            )

    @classmethod
    def imagen_anotacion(cls, base):
        scribus.statusMessage("Colocando imagen")
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
        # Cuadro planificación
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
        # Cuadro planificación
        Espacio.rectangulo(Puntos.O, Dimension.B)
        # Cuadro anotaciones
        Espacio.rectangulo(Puntos.R, Dimension.C)
        Impresora.renglones_para_anotar(Puntos.R)
        scribus.closeMasterPage()

    @classmethod
    def rellena_titulo(cls, titulo, espacio, origen, page_num):
        espacio.cuadro_de_texto(
            Punto(origen.x, origen.y + 70),
            Punto(A5.x, 45),
            titulo,
            "cuadro_titulo_{}".format(page_num),
            "parrafo_titulo",
            True,
        )

    @classmethod
    def rellenar_pasos_receta(cls, receta, page_num):
        scribus.statusMessage("Rellenando pasos de receta")
        espacio_receta = Espacio(Puntos.Q)
        Impresora.rellena_titulo(receta["titulo"], espacio_receta, Puntos.O, page_num)
        espacio_receta.cuadro_de_texto(
            Punto(Puntos.O.x, Puntos.O.y + 50),
            Dimension.A,
            receta["contenido"],
            "cuadro_contenido_{}".format(page_num),
            "parrafo_receta",
        )

    @classmethod
    def rellenar_ingredientes_receta(cls, receta, page_num):
        scribus.statusMessage("Rellenando ingredientes de receta")
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
            "parrafo_receta",
        )

    @classmethod
    def rellenar_poema(cls, poema, page_num):
        scribus.statusMessage("Rellenando poema")
        espacio_poema = Espacio(Puntos.Q)
        Impresora.rellena_titulo(poema["titulo"], espacio_poema, Puntos.O, page_num)

        espacio_poema.cuadro_de_texto(
            Punto(Puntos.O.x, Puntos.O.y + 50),
            Dimension.A,
            poema["contenido"],
            "cuadro_contenido_{}".format(page_num),
            "parrafo_poema",
        )

    @classmethod
    def rellenar_menu(cls, page_num):
        scribus.statusMessage("Rellenando cuadro de técnicas")
        espacio_menu = Espacio(Puntos.O)

        espacio_menu.cuadro_de_texto(
            Punto(Puntos.O.x, Puntos.O.y),
            Dimension.E,
            "Menú Semanal",
            "cuadro_titulo_menu_{}".format(page_num),
            "parrafo_titulo",
            False,
        )

        menu = "\n"
        menu += "Lunes{0}Miércoles{1}Viernes\n".format("\t" * 12, "\t" * 11)
        menu += " Comida:{0} Comida:{0} Comida:\n".format("\t" * 11)
        menu += " Cena:{0} Cena:{0} Cena\n\n".format("\t" * 12)
        menu += "Martes{0}Jueves{0}Sábado\n".format("\t" * 12)
        menu += " Comida:{0} Comida:{0} Comida:\n".format("\t" * 11)
        menu += " Cena:{0} Cena:{0} Cena:".format("\t" * 12)

        espacio_menu.cuadro_de_texto(
            Punto(Puntos.O.x, Puntos.O.y + 20),
            Dimension.E,
            menu,
            "cuadro_menu_{}".format(page_num),
            "parrafo_receta",
            False,
        )

    @classmethod
    def rellenar_lista(cls, page_num):
        espacio_lista = Espacio(Puntos.S, -90)

        texto = "\t\t\tCompra Semanal"

        espacio_lista.cuadro_de_texto(
            Puntos.O,
            Dimension.D,
            texto,
            "cuadro_lista_{}".format(page_num),
            "parrafo_titulo",
            False,
        )

    @classmethod
    def colocar_imagenes_cubierta(cls):
        espacio_imagen = Espacio(PuntosPortada.R, -90)
        espacio_imagen.imagen(PuntosPortada.O, A5, Cocina.cubierta_frontal)

        espacio_imagen = Espacio(PuntosPortada.Z, 90)
        espacio_imagen.imagen(PuntosPortada.O, Punto(A5.x, A5.y / 2), Cocina.cubierta_trasera)

    @classmethod
    def pintar_portada(cls):
        Espacio.multi_linea(
            [
                PuntosPortada.P,
                PuntosPortada.Q,
                PuntosPortada.R,
                PuntosPortada.S,
                PuntosPortada.T,
                PuntosPortada.V,
                PuntosPortada.W,
                PuntosPortada.Y,
                PuntosPortada.Z,
                PuntosPortada.J,
                PuntosPortada.K,
                PuntosPortada.L,
                PuntosPortada.P,
            ]
        )
        Espacio.multi_linea(
            [
                PuntosPortada.R,
                PuntosPortada.L,
                PuntosPortada.W,
                PuntosPortada.S,
            ],
            Formato.DOBLADO_MONTE,
        )
        Espacio.linea(PuntosPortada.K, PuntosPortada.Y, Formato.DOBLADO_MONTE)
        Espacio.multi_linea(
            [
                PuntosLenguetas.J,
                PuntosLenguetas.A,
                PuntosLenguetas.B,
                PuntosLenguetas.K,
                PuntosLenguetas.C,
                PuntosLenguetas.D,
                PuntosLenguetas.L,
            ]
        )
        Espacio.multi_linea(
            [
                PuntosLenguetas.Z,
                PuntosLenguetas.E,
                PuntosLenguetas.F,
                PuntosLenguetas.Y,
                PuntosLenguetas.G,
                PuntosLenguetas.H,
                PuntosLenguetas.W,
            ]
        )
        Impresora.colocar_imagenes_cubierta()

    @classmethod
    def rellenar_documento(cls):
        i_poema = iter(Cocina.poemas)
        i_receta = iter(Cocina.recetas)
        receta = None
        for page_num in range(1, Cocina.num_paginas + 1):
            Impresora.tick(page_num)
            if page_num % 2:
                scribus.applyMasterPage(Cocina.receta_A, page_num)
                Impresora.imagen_anotacion(Puntos.P)
                Impresora.rellenar_menu(page_num)
                if page_num % 8 == 1:
                    receta = i_receta.next()
                    cls.rellenar_pasos_receta(receta, page_num)
                else:
                    cls.rellenar_poema(i_poema.next(), page_num)
            else:
                scribus.applyMasterPage(Cocina.receta_B, page_num)
                Impresora.rellenar_lista(page_num)
                Impresora.imagen_anotacion(Puntos.R)
                if page_num % 8 == 2:
                    cls.rellenar_ingredientes_receta(receta, page_num)
            Impresora.tick()

    @classmethod
    def recolectar_codigo(cls):
        with open(
            os.path.join(os.path.dirname(__file__), "..", "gutemberg.py"), "r"
        ) as fichero:
            codigo = fichero.read()

        ficheros = os.listdir(os.path.join(os.path.dirname(__file__)))
        for nombre in ficheros:
            if nombre.endswith(".py"):
                ruta = os.path.join(os.path.dirname(__file__), nombre)
                codigo += nombre + ":\n" + "-" * len(nombre) + "\n\n"
                with open(ruta, "r") as fichero:
                    codigo += fichero.read()
        return codigo

    @classmethod
    def tomar_consciencia(cls):
        scribus.statusMessage("Soy parte de la obra")

        scribus.newDocument(
            scribus.PAPER_A4,
            Formato.SIN_MARGENES,
            scribus.PORTRAIT,
            1,  # firstPageNumber
            scribus.UNIT_MILLIMETERS,
            scribus.PAGE_1,  # pagesType
            0,  # firstPageOrder
            0,  # numPage
        )

        scribus.createCharStyle(
            name="estilo_cuerpo_codigo", font="Source Code Pro Regular", fontsize=12.0
        )

        scribus.createParagraphStyle(
            name="estilo_codigo",
            alignment=scribus.ALIGN_LEFT,
            linespacingmode=Formato.INTERLINEADO_FIJO,
            linespacing=20,
            charstyle="estilo_cuerpo_codigo",
        )

        codigo = Impresora.recolectar_codigo()
        plegaria = "Este es cáliz número {} de mi sangre"
        pagina = 1
        ruego = codigo

        espacio_infinito = Espacio(Puntos.O)
        espacio_infinito.cuadro_de_texto(
            Puntos.O, A4, ruego, plegaria.format(pagina), estilo="estilo_codigo"
        )

        while scribus.textOverflows(plegaria.format(pagina)) == 1:
            pagina = pagina + 1
            scribus.newPage(-1)
            scribus.gotoPage(pagina)

            espacio_infinito = Espacio(Puntos.O)
            espacio_infinito.cuadro_de_texto(
                Puntos.O, A4, "", plegaria.format(pagina), estilo="estilo_codigo"
            )

            scribus.linkTextFrames(plegaria.format(pagina - 1), plegaria.format(pagina))
