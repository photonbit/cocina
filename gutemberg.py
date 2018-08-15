#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys

try:
    import scribus
except ImportError, err:
    print "Esto está escrito para ser ejecutado desde Scribus."
    print "Sin Scribus no hay escrito."
    sys.exit(1)

from cocina.impresora import Impresora, Formato

def main(argv):
    Impresora.iniciar_portada()
    Impresora.iniciar_documento()
    Impresora.pagina_maestra_impares()
    Impresora.pagina_maestra_pares()
    Formato.crear_estilos()
    Impresora.rellenar_documento()


def envoltorio(argv):
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
    envoltorio(sys.argv)
