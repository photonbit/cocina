import os
import random


class Cocina(object):
    # Document Information
    autor = "Daniel Moreno Medina"
    info = ""
    descripcion = ""

    # Master pages
    receta_A = "recetaDelante"
    receta_B = "recetaDetras"

    traduce = {
        "ingredientes": "Ingredientes",
        "unidad": "unidad",
        "menu-semanal": "Menu semanal",
        "lista-de-la-compra": "Lista de la compra",
        "lunes": "Lunes",
        "martes": "Martes",
        "miercoles": "Miércoles",
        "jueves": "Jueves",
        "viernes": "Viernes",
        "sabado": "Sábado",
        "domingo": "Domingo",
        "almuerzo": "Almuerzo",
        "cena": "Cena",
        "de": "de",
    }

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
""",
        },
        {
            "titulo": "Ordena",
            "contenido": ""
            """
No es perdido
el tiempo si está
el corazón tranquilo
y la panza llena.

Del reposo y color
de la disposición
nace un plato
lleno de emoción.
""",
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
""",
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
""",
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
solo la hacen
despertar.
""",
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
""",
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
""",
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
""",
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
""",
        },
    ]

    recetas = [
        {
            "titulo": "Huevos Pochados",
            "ingredientes": [(1, "unidad", "huevo")],
            "contenido": ""
            """
Si los huevos, o quien los cocine, no están muy frescos: moldes, no de papel, el horno a 180ºC, una cucharada de agua y un huevo por molde durante 11 minutos.

Para los días valientes: una olla grande con abundante agua a 80ºC, huevos cascados sobre una espumadera o colador, depositados suavemente en el agua. A los 4 minutos habrá que pescarlos con cuidado.
""",
        },
        {
            "titulo": "Salsa Holandesa",
            "ingredientes": [
                (1, "unidad", "yema grande"),
                (0.5, "cucharada", "zumo de limón"),
                (1, "pizca", "sal"),
                (75, "gramos", "mantequilla"),
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
""",
        },
        {
            "titulo": "Muffins Ingleses",
            "ingredientes": [
                (500, "gramos", "harina"),
                (10, "gramos", "sal"),
                (4, "gramos", "levadura en polvo"),
                (60, "gramos", "mantequilla"),
                (150, "mililitros", "leche"),
                (150, "mililitros", "agua"),
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
            "tostado por arriba, sin que se lleguen a quemar, dándoles la vuelta a mitad de cocción.",
        },
        {
            "titulo": "Huevos Benedict",
            "ingredientes": [
                (1, "unidad", "Huevo pochado"),
                (1, "unidad", "Muffin inglés"),
                (30, "mililitros", "Salsa holandesa"),
                (2, "unidad", "huevos"),
            ],
            "contenido": ""
            """
Pon unas tiras de bacon en el horno hasta que empiecen a estar secas y no puedas resistir el olor en la cocina. Si te gusta crujiente espera un poco más y te lo agradecerás.

Abre un muffin y sobre una mitad coloca una loncha de bacon, un huevo pochado y riega con abundante salsa holandesa. Unas patatas fritas al lado completan una comida para celebrar.
""",
        },
    ]

    imagenes = os.listdir(os.path.join(os.path.dirname(__file__), "..", "imagenes"))

    cubierta_frontal = os.path.join(os.path.dirname(__file__), "..", "cubierta", "frontal.png")
    cubierta_trasera = os.path.join(os.path.dirname(__file__), "..", "cubierta", "trasera.png")

    @classmethod
    def imagen_aleatoria(cls):
        return os.path.join(
            os.path.dirname(__file__), "..", "imagenes", random.choice(cls.imagenes)
        )

    num_recetas = len(recetas)
    num_poemas = len(poemas)
    num_paginas = (num_recetas + num_poemas) * 2
