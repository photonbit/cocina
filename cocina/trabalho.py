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
        "unidad": "unidade",
        "menu-semanal": "Menu semanal",
        "lista-de-la-compra": "Lista de compras",
        "lunes": "Segunda",
        "martes": "Terça",
        "miercoles": "Quarta",
        "jueves": "Quinta",
        "viernes": "Sexta",
        "sabado": "Sábado",
        "domingo": "Domingo",
        "almuerzo": "Almoço",
        "cena": "Jantar",
        "de": "de",
    }

    poemas = [
        {
            "titulo": "Espera",
            "contenido": """
Coloca o lume baixo,
cozinha devagar.

Faz uma única coisa,
cada vez uma.

Não permitas que a pressa
perceba o não dito.
""",
        },
        {
            "titulo": "Ordena",
            "contenido": """
Não é perdido
o tempo se o
coração está tranquilo
e a barriga cheia.

Do repouso e da cor
da disposição
nasce um prato
repleto de emoção.
""",
        },
        {
            "titulo": "Reza",
            "contenido": """
Diálogo silencioso
ao ritmo das frigideiras.

Salteando legumes
a ideia ganha forma.

Sem formular pergunta
a resposta surge.
""",
        },
        {
            "titulo": "Inventa",
            "contenido": """
Seguindo a receita
chegarás sem dúvida
ao teu destino.

Olhar em frente
e a cada passo decidir
fará teu o caminho.

Viver assim,
sem medir:
apenas difundir e criar.
""",
        },
        {
            "titulo": "Amasa",
            "contenido": """
Da ação das mãos
farinha e água caminham
para nos trazer algo novo.

A massa já sabe
que forma terá o pão.

A nossa força,
os nossos movimentos
apenas a fazem
despertar.
""",
        },
        {
            "titulo": "Mira",
            "contenido": """
Às vezes
a nossa ação
não é necessária.

Observar,
mesmo sem nós,
é parte da receita.
""",
        },
        {
            "titulo": "Prueba",
            "contenido": """
Chupa a colher
   de pau de
vez em quando.

Talvez lhe falte sal
ou apercebas-te,
com os anos,
o que te fazia mal.
""",
        },
        {
            "titulo": "Disfruta",
            "contenido": """
Um guisado sem deleite
é mero instrumento.

A vida, sem prazeres,
é apenas sofrimento.

Quem come só para se alimentar
precisa de um castigamento.
""",
        },
        {
            "titulo": "Comparte",
            "contenido": """
Cada instante
em que vivemos
não é nosso.

Pertence
às pessoas
com quem o partilhamos.

Por maior que seja a panela,
se o caldo for só para ti,
sempre será menos.
""",
        },
    ]

    recetas = [
        {
            "titulo": "Ovos Escalfados",
            "ingredientes": [(1, "unidade", "ovo")],
            "contenido": """
Se os ovos, ou quem os cozinhe, não estiverem muito frescos: formas, não de papel, forno a 180ºC, uma colher de sopa de água e um ovo por forma durante 11 minutos.

Para os dias de coragem: um tacho grande com bastante água a 80ºC, ovos partidos sobre uma escumadeira ou coador, depositados suavemente na água. Aos 4 minutos será preciso pescá-los com cuidado.
""",
        },
        {
            "titulo": "Molho Holandês",
            "ingredientes": [
                (1, "unidade", "gema grande"),
                (0.5, "colher de sopa", "sumo de limão"),
                (1, "pitada", "sal"),
                (75, "gramas", "manteiga"),
            ],
            "contenido": """
Aquece a manteiga num tacho
até ficar líquida.

Retira a espuma que formar e reserva.

Numa tigela de metal ou vidro mistura e bate
as gemas, a água, o sumo de limão e a sal.

Aquece um tacho com água e coloca a tigela por cima.

Bate com varas
enquanto adicionas a manteiga.

Continua um pouco até ficar bem ligado.

Siga um pouco mais.

Está pronto.
""",
        },
        {
            "titulo": "Muffins Ingleses",
            "ingredientes": [
                (500, "gramas", "farinha"),
                (10, "gramas", "sal"),
                (4, "gramas", "fermento em pó"),
                (60, "gramas", "manteiga"),
                (150, "mililitros", "leite"),
                (150, "mililitros", "água"),
            ],
            "contenido": "Tira a manteiga do frigorífico. Mistura a farinha, o fermento, o açúcar e por último a sal num recipiente. Aquece a água e o leite num tacho em lume brando. Retira do lume quando, ao introduzir o dedo, não sintas nada. Em todo o lado te dirão para verter o líquido aos poucos. Faz como te for mais divertido. Continua a misturar e amassar com as mãos até que a massa quase se descole facilmente dos dedos. Acrescenta a manteiga e segue a amassar, a bater e a enrolar, no mesmo recipiente se não quiseres sujar muito.\n\nQuando, depois de muito esticar, dobrar e apertar, a massa estiver homogénea e puder alongar-se sem partir demasiado, estará pronta para descansar no recipiente, tapada com um pano. Divide a massa em pedaços; seis ou dez são bons números. Forma bolas e achata-as depois. Cozinha-as de ambos os lados numa frigideira bem quente, baixando o lume ao colocá-las.\n\nTambém podes fazer no forno a 180ºC durante alguns minutos até ficarem com cor tostada por cima, sem que queimem, virando-as a meio da cozedura.",
        },
        {
            "titulo": "Ovos Benedict",
            "ingredientes": [
                (1, "unidade", "ovo escalfado"),
                (1, "unidade", "muffin inglês"),
                (30, "mililitros", "molho holandês"),
                (2, "unidade", "ovos"),
            ],
            "contenido": """
Coloca umas tiras de bacon no forno até começarem a ficar secas e não conseguires resistir ao cheiro na cozinha. Se gostas crocante, espera mais um pouco e agradecer-te-ás.

Abre um muffin e sobre uma metade coloca uma fatia de bacon, um ovo escalfado e rega com abundante molho holandês. Algumas batatas fritas ao lado completam uma refeição de celebração.
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
