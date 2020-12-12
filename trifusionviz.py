__author__ = "david cobac"
__date__ = 20201211


import graphviz
import math

class Noeud:
    numero = 0

    def __init__(self, contenu, profondeur):
        self.numero = str(Noeud.numero)
        Noeud.numero += 1
        self.liste = contenu
        self.contenu = str(contenu)
        self.shape = "circle" if len(contenu) == 1 else "invtrapezium"
        self.couleur = str(profondeur)

    def visu(self, sousgraphe):
        sousgraphe.node(self.numero,
                        label=self.contenu,
                        shape=self.shape,
                        fillcolor=self.couleur)


class Arc:
    def __init__(self, noeud1, noeud2):
        self.source = noeud1
        self.destination = noeud2
    
    def visu(self, sousgraphe):
        sousgraphe.edge(self.source.numero, self.destination.numero,
                style="solid",
                headport="n",
                tailport="s",
                arrowhead="normal",
                arrowsize=".5")

    
def est_plus_petit(element1, element2, fonction=None):
    if not fonction: fonction= lambda a, b: a < b
    return fonction(element1, element2)


def fusion(gauche, droite, fonction_ordre):
    lG = len(gauche)
    lD = len(droite)
    iG, iD = 0, 0
    resultat = []

    while iG < lG and iD < lD:
        if est_plus_petit(gauche[iG], droite[iD], fonction_ordre):
            resultat.append(gauche[iG])
            iG += 1
        elif est_plus_petit(droite[iD], gauche[iG], fonction_ordre):
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


def tri_fusion(noeud, graphe, nb_couleurs, fonction_ordre, profondeur=1):
    liste = noeud.liste
    
    if len(liste) == 1: return noeud

    iMilieu = (len(liste)+1) // 2
    g = liste[:iMilieu]
    d = liste[iMilieu:]

    og = Noeud(g, profondeur + 1)
    od = Noeud(d, profondeur + 1)

    dv = graphviz.Digraph()
    og.visu(dv)
    od.visu(dv)
    Arc(noeud, og).visu(dv)
    Arc(noeud, od).visu(dv)
    graphe.subgraph(dv)

    ng = tri_fusion(og, graphe, nb_couleurs, fonction_ordre, profondeur + 1)
    nd = tri_fusion(od, graphe, nb_couleurs, fonction_ordre, profondeur + 1)
    f = fusion(ng.liste, nd.liste, fonction_ordre)

    nf = Noeud(f, nb_couleurs - profondeur + 1)

    cb = graphviz.Digraph()
    nf.visu(cb)
    Arc(ng, nf).visu(cb)
    Arc(nd, nf).visu(cb)
    graphe.subgraph(cb)

    return nf


def tri_visu(liste, fonction_ordre=None, fichier_sortie=None, format=None):
    if not fichier_sortie: fichier_sortie = "trifusionviz"
    if not format: format = "pdf"
    
    g = graphviz.Digraph(filename=fichier_sortie, format=format, engine="dot")
    nb_couleurs = 1 + 2 * math.ceil(math.log2(len(liste)))
    g.attr("node", colorscheme=f"rdylgn{nb_couleurs}")
    g.attr("node", style="filled, rounded")

    noeud_racine = Noeud(liste, 1)
    noeud_racine.visu(g)
        
    tri_fusion(noeud_racine, g, nb_couleurs, fonction_ordre=fonction_ordre)
    g.render()


if __name__ == "__main__":
    import random

    
    liste = list(range(30))
    random.shuffle(liste)

    tri_visu(liste, lambda x, y: str(x) < str(y), "ordrelexico", "png")
    tri_visu(liste)
