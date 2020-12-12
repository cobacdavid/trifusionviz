# -*- coding: utf-8 -*-
__author__ = "david cobac"
__date__ = 20201211


import graphviz
import math


class Noeud:
    numero = 0
    profondeur_max = 0
    dico_noeuds_profondeur = {}

    def __init__(self, contenu, profondeur):
        self.numero = str(Noeud.numero)
        Noeud.numero += 1
        if profondeur in Noeud.dico_noeuds_profondeur:
            Noeud.dico_noeuds_profondeur[profondeur].append(self)
        else:
            Noeud.dico_noeuds_profondeur[profondeur] = [self]
        self.liste = contenu
        self.contenu = str(contenu)
        if len(contenu) == 1:
            self.shape = "circle"
        elif profondeur <= Noeud.profondeur_max / 2:
            self.shape = "invtrapezium"
        else:
            self.shape = "trapezium"
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
    
    def visu(self, sousgraphe, tp="s", hp="n"):
        sousgraphe.edge(self.source.numero, self.destination.numero,
                style="solid",
                headport=hp,
                tailport=tp,
                arrowhead="normal",
                arrowsize=".5")


def est_plus_petit(element1, element2, fonction=None):
    if not fonction: fonction = lambda a, b: a < b
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


class trifusionviz:
    def __init__(self, liste):
        self.graphe = graphviz.Digraph(engine="dot")
        self.nb_couleurs = 1 + 2 * math.ceil(math.log2(len(liste)))
        Noeud.profondeur_max = self.nb_couleurs
        self.fonction_ordre = None
        self.graphe.attr("node", colorscheme=f"rdylgn{self.nb_couleurs}")
        self.graphe.attr("node", style="filled, rounded")
        #
        self.racine = Noeud(liste, 1)
        self.racine.visu(self.graphe)

    def sortie(self, nom_fichier, format="pdf"):
        self._tri_fusion(self.racine)
        #
        # pour régler le rank : ne créer les noeuds qu'après les
        # avoir tous trouvés mais... refonte complète ?? car les
        # arcs doivent aussi être définis après coup !
        #
        # for profondeur in Noeud.dico_noeuds_profondeur:
        #     for noeud in Noeud.dico_noeuds_profondeur[profondeur]:
        #         with self.graphe.subgraph() as s:
        #             s.attr(rank="same")
        #             pass 
        #
        self.graphe.render(filename=nom_fichier, format=format)

    def _tri_fusion(self, noeud, profondeur=1):
        liste = noeud.liste

        if len(liste) == 1: return noeud

        iMilieu = (len(liste) + 1) // 2
        g = liste[:iMilieu]
        d = liste[iMilieu:]

        og = Noeud(g, profondeur + 1)
        od = Noeud(d, profondeur + 1)

        # dv = graphviz.Digraph()
        dv = self.graphe
        og.visu(dv)
        od.visu(dv)
        Arc(noeud, og).visu(dv)
        Arc(noeud, od).visu(dv)
        # self.graphe.subgraph(dv)

        ng = self._tri_fusion(og, profondeur + 1)
        nd = self._tri_fusion(od, profondeur + 1)
        f = fusion(ng.liste, nd.liste, self.fonction_ordre)

        nf = Noeud(f, self.nb_couleurs - profondeur + 1)

        # cb = graphviz.Digraph()
        cb = self.graphe
        nf.visu(cb)
        Arc(ng, nf).visu(cb)
        Arc(nd, nf).visu(cb)
        # self.graphe.subgraph(cb)

        return nf
