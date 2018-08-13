#!/usr/bin/env python2
# -*- coding: utf-8 -*-

class Ingrediente(object):
    def __init__(self, cantidad, unidad, nombre):
        self.cantidad = cantidad
        self.unidad = unidad
        self.nombre = nombre

class Receta(object):
    def __init__(self, nombre, ingredientes, pasos):
        self.nombre = nombre
        self.ingredientes = ingredientes
        self.pases = pasos
