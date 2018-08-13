#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys

try:
    import scribus
except ImportError, err:
    print "This Python script is written for the Scribus scripting interface."
    print "It can only be run from within Scribus."
    sys.exit(1)

import time
from collections import namedtuple

poemas = [
    {
        "titulo": "Espera",
        "contenido": """
        Pon el fuego suave,
        cocina depacio.
        
        Haz una sola una cosa,
        una cada vez.
        
        No permitas que la prisa
        entienda lo no hablado.
        """
    },
    {
        "titulo": "Ordena",
        "contenido": """
        No es perdido
        el tiempo
        si deja
        el corazón tranquilo
        y la panza llena.
        
        Del contento y color
        de una cuidada
        disposición
        nace sin dolor
        un plato lleno
        de emoción.
        """
    },
    {
        "titulo": "Reza",
        "contenido": """
        Diálogo silencioso
        al ritmo de las sartenes.

        Salteando verdura
        la idea se forma.

        Sin formular pregunta
        la respuesta aparece.
        """
    },
    {
        "titulo": "Inventa",
        "contenido": """
        De seguir la receta
        llegarás sin duda
        a tu destino.
        
        Mirar hacia delante
        a cada paso
        hará tuyo el camino.
        
        Vivir así,
        sin medir:
        solo difuminar y crear.
        """
    },
    {
        "titulo": "Amasa",
        "contenido": """
        Carne, masa, materia.

        De la acción de las manos,      
        los ingredientes transmutan        
        y nos traen algo nuevo.

        La masa ya conoce        
        qué forma tendrá el pan.
        
        Nuestra fuerza,
        nuestros movimientos
        únicamente hacen la masa
        despertar.
        """
    },
    {
        "titulo": "Mira",
        "contenido": """
        Vemos a veces
        cómo los ingredientes
        se vuelven comida,
        
        que nuestra acción
        no es necesaria.
        
        A veces,
        
           observar,
        
        incluso sin nosotros,
        
          es parte de la receta.
        """
    },
    {
        "titulo": "Disfruta",
        "contenido": """
        Un guiso sin deleite
        es mero instrumento.
        
        La vida, sin placeres,
        es solo sufrimiento.
        
        Quien come para alimentarse
        necesita un escarmiento.
    """
    },
    {
        "titulo": "Comparte",
        "contenido": """
        Cada instante
        en el que vivimos
        no es nuestro.
        
        Pertenece
        a las personas
        con quienes lo compartimos.
        
        Por grande que sea la olla,
        si el caldo es solo para ti,
        siempre será menos.
    """
    },
    {
        "titulo": "Vive",
        "contenido": """
        Sin olvidarte,
        sin ocuparlo todo.
        Una vez masticada
        la comida
        pensar en la siguiente.
        
        Cuidando que llegue
        cada momento
        siempre en el presente.
    """
    },
]

recetas = [
    {
        "titulo": "Huevos Pochados",
        "ingredientes": [
        ],
        "contenido": """
        Si los huevos, o quien los cocine, no están muy frescos: moldes, no de papel, 
        el horno a 180ºC, una cucharada de agua y un huevo por molde durante 11 minutos.

        Para los días valientes: una olla grande con abundante agua a 80ºC,
        huevos cascados sobre una espumadera o colador, depositados suavemente en el agua.
        A los 4 minutos habrá que pescarlos con cuidado.
        """
    },
    {
        "titulo": "Salsa Holandesa",
        "ingredientes": [
            (1, "unidad", "yema grande"),
            (0.5, "cucharada", "zumo de limón"),
            (1, "pizca", "sal"),
            (75, "gramos", "mantequilla")
        ],
        "contenido": """
        Calienta la mantequilla en un cazo hasta que esté líquida.

        Separa la espuma que tenga y aparta.
        
        En un bol de metal o cristal mezcla y bate las yemas, el agua, el limón y la sal.
        
        Calienta un cazo con agua y pon el bol encima.
        
        Bate con varillas, mientras vas añadiendo la mantequilla.
        
        Sigue un rato hasta que esté bien ligado.
        
        Sigue un poco más.
        
        Ya está listo.
        """
    },
    {
        "titulo": "Muffins Ingleses",
        "ingredientes": [
            (500, "gramos", "harina"),
            (10, "gramos", "sal"),
            (4, "gramos", "levadura en polvo"),
            (60, "gramos", "mantequilla"),
            (150, "mililitros", "leche"),
            (150, "mililitros", "agua")
        ],
        "contenido": """
        Saca la mantequilla de la nevera. Mezcla la harina, la levadura, el azúcar y por último 
        la sal en un bol. Calienta el agua y la leche en un cazo a fuego lento. Sácalo del fuego 
        cuando al introducir el dedo no sientas nada. En todas partes te dirán que eches 
        el líquido poco a poco. Hazlo como te resulte más divertido. Sigue mezclando y amasando 
        con las manos hasta que casi se pueda despegar fácilmente de los dedos. Añade la mantequilla 
        y sigue amasando, golpeando y enrollando, en el mismo bol si no quieres manchar mucho. 
        Cuando después de mucho estirar, doblar y apretar la masa sea homogénea y se pueda alargar 
        sin que se rompa demasiado, ya está lista para reposar en el bol tapado con un trapo. 
        Divide la masa en pedazos, seis o diez son un buenos números. Haz bolas y aplástalas después. 
        Hazlos en la sartén ya bien caliente, pero bajando el fuego al ponerlos o en el horno 
        a 180ºC durante unos minutos hasta que queden de color tostado por arriba, sin que se 
        lleguen a quemar, dándoles la vuelta a mitad de cocción.
        """
    },
    {
        "titulo": "Huevos Benedict",
        "ingredientes": [
        ],
        "contenido": """
        Pon unas tiras de bacon en el horno hasta que empiecen a estar secas y no puedas resistir 
        el olor en la cocina. Si te gusta crujiente espera un poco más y te lo agradecerás.
        
        Abre un muffin y sobre una mitad coloca una loncha de bacon, un huevo pochado y riega con abundante 
        salsa holandesa. Unas patatas fritas al lado completan una comida para celebrar.
        """
    }
]

class Cocina(object):
    # Document Information
    autor = "Daniel Moreno Medina"
    info = ""
    descripcion = ""
    num_recetas = 4
    num_poemas = 9
    num_paginas = (num_recetas + num_poemas) * 2

    # Page formatting
    SIN_MARGENES = (0, 0, 0, 0)
    Papel = namedtuple("Papel", ["x", "y"])
    A3 = Papel(*scribus.PAPER_A3)
    A4 = Papel(*scribus.PAPER_A4)
    A5 = Papel(*scribus.PAPER_A5)

    # Master pages
    receta_A = "recetaDelante"
    receta_B = "recetaDetras"


def main(argv):
    portada = scribus.newDocument(
        scribus.PAPER_A3,  # size
        Cocina.SIN_MARGENES,  # margins
        scribus.LANDSCAPE,  # orientation
        1,  # firstPageNumber
        scribus.UNIT_MILLIMETERS,  # unit
        scribus.PAGE_1,  # pagesType
        0,  # firstPageOrder
        1  # numPage
    )
    scribus.setInfo(Cocina.autor, Cocina.info, Cocina.descripcion)
    obra = scribus.newDocument(
        scribus.PAPER_A4,  # size
        Cocina.SIN_MARGENES,  # margins
        scribus.PORTRAIT,  # orientation
        1,  # firstPageNumber
        scribus.UNIT_MILLIMETERS,  # unit
        scribus.PAGE_1,  # pagesType
        0,  # firstPageOrder
        Cocina.num_paginas  # numPage
    )
    scribus.setInfo(Cocina.autor, Cocina.info, Cocina.descripcion)

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

    for page_num in range(1, Cocina.num_paginas + 1):
        scribus.gotoPage(page_num)
        if page_num % 2:
            scribus.applyMasterPage(Cocina.receta_A, page_num)
        else:
            scribus.applyMasterPage(Cocina.receta_B, page_num)
        # Seleccionar cuadro para poema
        # meterlo poema
        scribus.createText(0, 0, 100, 50, "cuadro_titulo_"+page_num)
        scribus.insertText(poemas[page_num]["titulo"], 0, "cuadro_titulo_"+page_num)
        scribus.createText(100, 0, 500, 500, "cuadro_contenido_"+page_num)
        scribus.insertText(poemas[page_num]["contenido"], 0, "cuadro_contenido_"+page_num)
        # Seleccionar cuadro tecnicas
        # meter tecnica
        # Seleccionar cuadro marcapaginas
        # meter algo?


def main_wrapper(argv):
    try:
        scribus.statusMessage("Calentando los fogones...")
        scribus.progressReset()
        main(argv)
    finally:
        if scribus.haveDoc():
            scribus.setRedraw(True)
        scribus.statusMessage("")
        scribus.progressReset()


if __name__ == '__main__':
    main_wrapper(sys.argv)
