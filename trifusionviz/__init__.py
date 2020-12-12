# -*- coding: utf-8 -*-
from .trifusionviz import *

version = '0.1'

if __name__ == "__main__":
    import random


    liste = list(range(13))
    random.shuffle(liste)

    t = trifusionviz(liste)
    t.sortie("exemple_sortie")

    u = trifusionviz(liste)
    u.fonction_ordre = lambda x, y: str(x) < str(y)
    u.sortie("exemple_sortie_lexico", "png")

