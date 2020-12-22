# -*- coding: utf-8 -*-
from .trifusionviz import *

version = '0.7'

if __name__ == "__main__":
    import random


    liste = list(range(13))
    random.shuffle(liste)

    t = tfv.trifusionviz(liste)
    # sortie pdf
    t.sortie_appels = True
    t.sortie("exemple_sortie")

    u = tfv.trifusionviz(liste)
    u.fonction_ordre = lambda x, y: str(x) < str(y)
    u.noirblanc = True
    u.profondeurs_cachees = range(2, 2 + 7)
    u.forme_diviser, u.forme_arreter, u.forme_combiner = \
        "invhouse", "rectangle", "house"
    # sortie png
    u.sortie("exemple_sortie_lexico", "png")

    v = tfv.trifusionviz(liste)
    v.style = "invis"
    # sortie png
    v.sortie("exemple_invisible", "png")
