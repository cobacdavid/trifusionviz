__author__ = "david cobac"
__date__ = 20201211


import graphviz
import math

class maliste:
    numero = 0

    def __init__(self, contenu):
        self.numero = str(maliste.numero)
        maliste.numero += 1
        self.contenu = str(contenu)


def fusion(gauche, droite):
    lG = len(gauche)
    lD = len(droite)
    iG, iD = 0, 0
    resultat = []

    while iG < lG and iD < lD:
        if gauche[iG] < droite[iD]:
            resultat.append(gauche[iG])
            iG += 1
        elif gauche[iG] > droite[iD]:
            resultat.append(droite[iD])
            iD += 1
        else:
            resultat.append(gauche[iG])
            resultat.append(droite[iD])
            iG += 1
            iD += 1

    if iG != lG:
        resultat += gauche[iG:]

    if iD != lD:
        resultat += droite[iD:]

    return resultat


def tri_fusion(liste, graphe, numero, nb_couleurs, profondeur=1):
    if len(liste) == 1: return liste, numero

    iMilieu = (len(liste)+1) // 2
    g = liste[:iMilieu]
    d = liste[iMilieu:]

    og = maliste(g)
    od = maliste(d)

    if len(g) == 1:
        shapeg = "circle"
    else:
        shapeg = "invtrapezium"
    if len(d) == 1:
        shaped = "circle"
    else:
        shaped = "invtrapezium"
    

    dv = graphviz.Digraph()
    
    dv.node(og.numero,
                label=og.contenu,
                shape=shapeg,
                fillcolor=str(profondeur+1))
    dv.node(od.numero,
                label=od.contenu,
                shape=shaped,
                fillcolor=str(profondeur+1))
    
    dv.edge(numero, og.numero,
                style="solid",
                headport="n",
                tailport="s",
                arrowhead="normal",
                arrowsize=".5")
    dv.edge(numero, od.numero,
                style="solid",
                shape=shaped,
                headport="n",
                tailport="s",
                arrowhead="normal",
                arrowsize=".5")

    graphe.subgraph(dv)

    fg, ng = tri_fusion(g, graphe, og.numero, nb_couleurs, profondeur + 1)
    fd, nd = tri_fusion(d, graphe, od.numero, nb_couleurs, profondeur + 1)
    f = fusion(fg, fd)
    mlf = maliste(f)

    cb = graphviz.Digraph()
    
    cb.node(mlf.numero, label=mlf.contenu,
                shape="trapezium",
                fillcolor=str(nb_couleurs - profondeur + 1))
    cb.node(mlf.numero, label=mlf.contenu,
                shape="trapezium",
                fillcolor=str(nb_couleurs - profondeur + 1))

    cb.edge(ng, mlf.numero,
                headport="n",
                tailport="s",
                arrowhead="normal",
                arrowsize=".5")
    cb.edge(nd, mlf.numero,
                headport="n",
                tailport="s",
                arrowhead="normal",
                arrowsize=".5")

    graphe.subgraph(cb)

    return f, mlf.numero


def tri_visu(liste):
    g = graphviz.Digraph(filename="trifusionviz", format="pdf", engine="dot")
    nb_couleurs = 1 + 2 * math.ceil(math.log2(len(liste)))
    g.attr("node", colorscheme=f"rdylgn{nb_couleurs}")
    g.attr("node", style="filled, rounded")
    if len(liste) == 1:
        shape = "circle"
    else:
        shape = "invtrapezium"
    
    racine = maliste(liste)

    g.node(racine.numero, label=racine.contenu,
           shape=shape,
           fillcolor="1")
        
    tri_fusion(liste, g, racine.numero, nb_couleurs)
    g.render()


if __name__ == "__main__":
    import random

    
    liste = list(range(20))
    random.shuffle(liste)

    tri_visu(liste)
