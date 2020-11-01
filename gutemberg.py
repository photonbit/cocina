#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys

try:
    import scribus
except ImportError as err:
    print("Esto está pensado para ser ejecutado desde Scribus.")
    print("Sin Scribus no hay escrito.")
    sys.exit(1)

from cocina.impresora import Impresora, Formato

def main(argv):
    lento = scribus.messageBox('Poco a poco', '¿Quieres cocinar a fuego lento?',
                        scribus.ICON_WARNING, scribus.BUTTON_YES,
                                scribus.BUTTON_NO)
    if lento == scribus.BUTTON_YES:
        Impresora.cocinar_lento = True
    else:
        Impresora.cocinar_lento = False
    Impresora.iniciar_portada()
    Impresora.pintar_portada()
    Impresora.iniciar_documento()
    Impresora.pagina_maestra_impares()
    Impresora.pagina_maestra_pares()
    Formato.crear_estilos()
    Impresora.rellenar_documento()
    Impresora.tomar_consciencia()


def envoltorio(argv):
    try:
        scribus.statusMessage("Calentando los fogones...")
        main(argv)
    finally:
        if scribus.haveDoc():
            scribus.setRedraw(True)
        scribus.statusMessage("")
        scribus.progressReset()


if __name__ == '__main__':
    envoltorio(sys.argv)
