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
        "ingredientes": "Ingredients",
        "unidad": "unit",
        "menu-semanal": "Weekly Menu",
        "lista-de-la-compra": "Shopping List",
        "lunes": "Monday",
        "martes": "Tuesday",
        "miercoles": "Wednesday",
        "jueves": "Thursday",
        "viernes": "Friday",
        "sabado": "Saturday",
        "domingo": "Sunday",
        "almuerzo": "Lunch",
        "cena": "Dinner",
        "de": "of",
    }

    poemas = [
        {
            "titulo": "Wait",
            "contenido": ""
            """
Use gentle fire
cook slowly.

One thing only
one at a time.

Do not allow rush
to understand the unspoken.
""",
        },
        {
            "titulo": "Sort",
            "contenido": ""
            """
Time is not lost
when we have
a peaceful heart
and a full belly.

From the serenity
of a careful layout
full of emotion
a dish is born.
""",
        },
        {
            "titulo": "Pray",
            "contenido": ""
            """
Silent conversation
at frying pans rhythm.

Sauteing vegetables
the idea takes shape.

No question is asked:
the answer appears.
""",
        },
        {
            "titulo": "Invent",
            "contenido": ""
            """
Following the recipe
will grant
your destination.

Keeping your eyes open
deciding on each step
will make yours the journey.

Living like that,
without measuring:
just smudging and creating.
""",
        },
        {
            "titulo": "Knead",
            "contenido": ""
            """
From the action of our hands
flour and water depart
to bring something new.

The dough already knows
the final form of the bread.

Our strength
our movements
are just elements
of awakening.
""",
        },
        {
            "titulo": "Witness",
            "contenido": ""
            """
Sometimes
our action
is not necessary.

Observing
even without ourselves
is part of the recipe.
""",
        },
        {
            "titulo": "Taste",
            "contenido": ""
            """
Lick 
the wooden spoon
   from 
time to time.

Maybe it was missing salt
or you might realize
after all those years
what was causing you trouble.
""",
        },
        {
            "titulo": "Enjoy",
            "contenido": ""
            """
A stew without delight
it is mere instrument.

Life without pleasure
is just detriment.

The one who eats
just to be fed
asks for punishment.
""",
        },
        {
            "titulo": "Share",
            "contenido": ""
            """
Each instant
in which we live
is not ours.

It belongs
to all the people
with whom we share it.

No matter how big the pot is
if the broth is just for you
it will always be less.
""",
        },
    ]

    recetas = [
        {
            "titulo": "Poached Eggs",
            "ingredientes": [(1, "unit", "egg")],
            "contenido": ""
            """
If the eggs, or the cook, is not in a very good shape: individual moulds, not made of paper, the oven at 180ºC, a spoon of water and one egg per mold for 11 minutes.

For the brave days: a big pot with abundant water at 80ºC, crack the eggs on a skimmer or strainer, place gently into the water. After 4 minutes you will need to rescue them carefully.
""",
        },
        {
            "titulo": "Hollandaise Sauce",
            "ingredientes": [
                (1, "unit", "big egg yolk"),
                (0.5, "spoon", "lemon juice"),
                (1, "pinch", "salt"),
                (75, "grams", "butter"),
            ],
            "contenido": ""
            """
Slowly heat up the butter in a saucepan
until it is completely liquid.

Separate the foam if there is any and set aside.

In a metal or glass bowl mix and beat
the yolks, the water, the lemon and the salt.

Heat a saucepan with water and put the bowl on top.

Whisk constantly
while you add the butter
little by little.

Continue for a while until it is uniform.

Keep doing it a little bit more.

Now it is ready.
""",
        },
        {
            "titulo": "English Muffins",
            "ingredientes": [
                (500, "grams", "flour"),
                (10, "grams", "salt"),
                (4, "grams", "dry yeast"),
                (60, "grams", "butter"),
                (150, "mililiters", "milk"),
                (150, "mililiters", "watter"),
            ],
            "contenido": ""
            "Take the butter out of the fridge. Mix the flour, the dry yeast, the sugar and finally "
            "the salt in a bowl. Heat the water and milk in a saucepan over low heat. Take it off the heat "
            "when you put your finger in and don't feel any difference in temperature. Everywhere will tell you to add "
            "the liquid little by little. Do it as you find more fun. Keep mixing and kneading "
            "with your hands until the dough can be easily removed from your fingers. Add the butter "
            "and keep kneading, beating and rolling, in the same bowl if you don't want to stain too much."
            "\n\n"
            "After much stretching, folding and pressing the dough should be homogeneous and could be lengthened "
            "without breaking too much, then it is ready to be left in the bowl covered with a cloth to rest. "
            "Divide the dough into pieces, six or ten are good numbers. Form balls and flatten them later. "
            "Cook them on both sides in a pan that is already very hot, but lower the heat when you put them in."
            "\n\n"
            "They can also be baked in the oven at 180ºC for a few minutes until they are slightly "
            "brown on top, paying attention not to burn them and turning them halfway cooking time.",
        },
        {
            "titulo": "Eggs Benedict",
            "ingredientes": [
                (1, "unit", "Poached egg"),
                (1, "unit", "English muffin"),
                (30, "mililiters", "Hollandaise sauce"),
            ],
            "contenido": ""
            """
Get some bacon slices into the oven until they start becoming dry and you can't resist the smell in the kitchen. If you like them crunchy wait a little bit more and you will thank yourself.

Open up a muffin and place one bacon slice and one poached egg over one of the halves. Sprinkle with abundant hollandaise sauce. Add some french fries to the side to complete a meal suitable for celebrating life. 
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
