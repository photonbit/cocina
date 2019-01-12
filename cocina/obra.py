#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import random

class Tecnica(object):
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

class Coccion(Tecnica):
    def __init__(self, nombre, descripcion):
        super(Coccion, self).__init__(nombre, descripcion)

class CorteVerdura(Tecnica):
    def __init__(self, nombre, descripcion):
        super(CorteVerdura, self).__init__(nombre, descripcion)

class CorteCarne(Tecnica):
    def __init__(self, nombre, descripcion,  grasa, entrevetado, textura, sabor, cocciones=None):
        self.nombre = "El nombre del corte"
        self.grasa = "Cantidad de grasa"
        self.entrevetado = "Presentación de la grasa"
        self.textura = "Cómo se comporta al tacto"
        self.sabor = "Cómo se comporta al paladar"

        if cocciones is None:
            self.cocciones = []  # List[Coccion]
        else:
            self.cocciones = cocciones

        super(CorteCarne, self).__init__(nombre, descripcion)


class Cocina(object):
    # Document Information
    autor = "Daniel Moreno Medina"
    info = ""
    descripcion = ""

    # Master pages
    receta_A = "recetaDelante"
    receta_B = "recetaDetras"

    poemas = [
        {
            "titulo": "Espera",
            "contenido": ""
"""
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
            "contenido":  ""
"""
No es perdido
el tiempo si está
el corazón tranquilo
y la panza llena.

Del resposo y color
de una cuidada
disposición
nace sin dolor
un plato lleno
de emoción.
"""
        },
        {
            "titulo": "Reza",
            "contenido": ""
"""
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
            "contenido": ""
"""
De seguir la receta
llegarás sin duda
a tu destino.

Mirar hacia delante
y a cada paso decidir
hará tuyo el camino.

Vivir así,
sin medir:
solo difuminar y crear.
"""
        },
        {
            "titulo": "Amasa",
            "contenido": ""
"""
De la acción de las manos
harina y agua marchan          
para traernos algo nuevo.

La masa ya conoce        
qué forma tendrá el pan.

Nuestra fuerza,
nuestros movimientos
únicamente la hacen
despertar.
"""
        },
        {
            "titulo": "Mira",
            "contenido": ""
"""
A veces
nuestra acción
no es necesaria.

Observar,
incluso sin nosotros,
es parte de la receta.
"""
        },
        {
            "titulo": "Prueba",
            "contenido": ""
"""
Chupa la cuchara
de palo de
cuando en cuando.

Quizás le falte sal
o te des cuenta,
con los años,
qué te sentaba mal.
"""
        },
        {
            "titulo": "Disfruta",
            "contenido": ""
"""
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
            "contenido": ""
"""
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
    ]

    recetas = [
        {
            "titulo": "Huevos Pochados",
            "ingredientes": [
                (1, "unidad", "huevo")
            ],
            "contenido": ""
"""
Si los huevos, o quien los cocine, no están muy frescos: moldes, no de papel, el horno a 180ºC, una cucharada de agua y un huevo por molde durante 11 minutos.

Para los días valientes: una olla grande con abundante agua a 80ºC, huevos cascados sobre una espumadera o colador, depositados suavemente en el agua. A los 4 minutos habrá que pescarlos con cuidado.
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
            "contenido": ""
"""
Calienta la mantequilla en un cazo
hasta que esté líquida.

Separa la espuma que tenga y aparta.

En un bol de metal o cristal mezcla y bate 
las yemas, el agua, el limón y la sal.

Calienta un cazo con agua y pon el bol encima.

Bate con varillas
mientras vas añadiendo la mantequilla.

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
            "contenido": ""
"Saca la mantequilla de la nevera. Mezcla la harina, la levadura, el azúcar y por último " 
"la sal en un bol. Calienta el agua y la leche en un cazo a fuego lento. Sácalo del fuego "
"cuando al introducir el dedo no sientas nada. En todas partes te dirán que eches "
"el líquido poco a poco. Hazlo como te resulte más divertido. Sigue mezclando y amasando " 
"con las manos hasta que casi se pueda despegar fácilmente de los dedos. Añade la mantequilla " 
"y sigue amasando, golpeando y enrollando, en el mismo bol si no quieres manchar mucho. "
"\n\n"
"Cuando después de mucho estirar, doblar y apretar la masa sea homogénea y se pueda alargar " 
"sin que se rompa demasiado, ya está lista para reposar en el bol tapado con un trapo. "
"Divide la masa en pedazos, seis o diez son buenos números. Forma bolas y aplástalas después. " 
"Cuécelos por las dos caras en una sartén ya bien caliente, pero bajando el fuego al ponerlos. "
"\n\n"
"También se pueden hacer en el horno a 180ºC durante unos minutos hasta que queden de color "
"tostado por arriba, sin que se lleguen a quemar, dándoles la vuelta a mitad de cocción."
        },
        {
            "titulo": "Huevos Benedict",
            "ingredientes": [
            ],
            "contenido": ""
"""
Pon unas tiras de bacon en el horno hasta que empiecen a estar secas y no puedas resistir el olor en la cocina. Si te gusta crujiente espera un poco más y te lo agradecerás.

Abre un muffin y sobre una mitad coloca una loncha de bacon, un huevo pochado y riega con abundante salsa holandesa. Unas patatas fritas al lado completan una comida para celebrar.
"""
        }
    ]

    tecnicas = [
        {
            "nombre": "preparaciones",
            "compendio": {
                "cocer": "El comodín que puede ser cualquiera de las demás, aunque normalmente pensemos únicamente en hervir",
                "asar": "Calor indirecto y seco",
                "freír": "Hundir en aceite o grasa hirviendo",
                "sofreír": "Planchar a fuego lento en aceite",
                "rehogar": "Sofreír rápidamente",
                "planchar": "Poner en metal caliente",
                "hornear": "Asar, al papillote (envuelto en aluminio), a la sal",
                "confitar": "Introducir en líquido normalmente aceitoso a poca temperatura (60 grados)",
                "macerar": "Líquido normalmente cítrico frío o golpes para ablandar, extraer sabores y líquidos",
                "hervir": "Hundir en agua u otro líquido no aceitoso hirviendo",
                "fermentar": "Permitir una podredumbre controlada",
                "secar": "Eliminar la humedad",
                "baño maría": "",
                "escalfar": "",
                "saltear": "",
                "guisar": "Hasta que cubra. Los guisos van sofritos, suelen llevar agua o vino, pueden hacerse a olla abierta",
                "estofar": "A fuego lento. Los estofados se cocinan en su jugo, a olla cerrada siempre, "
                           "se puede añadir algo de vino, tomate o un poquito de algo más, pero no que cubra"
            }
        },
        {
            "nombre": "cortes",
            "verdura": {
                "juliana": "",
                "dados": "",
                "rodajas": "",
                "finito": ""
            },
            "vaca": {
                "entrecot": "",
                "falda": ""
            },
            "cerdo": {
                "lomo": "",
                "carrilleras": ""
            }
        }
    ]

    imagenes = os.listdir(os.path.join(os.path.dirname(__file__), "..", "imagenes"))

    @classmethod
    def imagen_aleatoria(cls):
        return os.path.join(os.path.dirname(__file__), "..", "imagenes", random.choice(cls.imagenes))


    # Relación entre cortes y cocciones
    # Todos los cortes de carne son buenos,
    # solo hay que saber cocinarlos.

    num_recetas = len(recetas)
    num_poemas = len(poemas)
    num_paginas = (num_recetas + num_poemas) * 2