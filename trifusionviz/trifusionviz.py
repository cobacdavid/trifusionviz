# -*- coding: utf-8 -*-
__author__ = "david cobac"
__date__ = 20201211


import graphviz
import math
from .recappels import * 

class Noeud:
    _numero = 0
    _profondeur_max = 0
    _liste_noeuds = []
    _liste_prof_cach = []
    _shape_diviser = "invtrapezium"
    _shape_arreter = "circle"
    _shape_combiner = "trapezium"

    def __init__(self, contenu, profondeur):
        self.numero = Noeud._numero
        self.profondeur = profondeur
        self.forme = None
        #
        Noeud._numero += 1
        #
        self.liste = contenu
        #
        self._de = []
        self._vers = []
        #
        Noeud._liste_noeuds.append(self)

    def visu(self, sousgraphe):
        if not self.forme:
            if len(self.liste) == 1:
                self.forme = Noeud._shape_arreter
            elif self.profondeur <= Noeud._profondeur_max / 2:
                self.forme = Noeud._shape_diviser
            else:
                self.forme = Noeud._shape_combiner
        #
        if self.profondeur not in Noeud._liste_prof_cach:
            etiquette = str(self.liste)
        else:
            etiquette = " " * (len(self.liste)  + 2)
        #
        sousgraphe.node(str(self.numero),
                        label=etiquette,
                        shape=self.forme,
                        fillcolor=str(self.profondeur))


class Arc:
    def __init__(self, noeud1, noeud2):
        self.source = noeud1
        self.destination = noeud2
    
    def visu(self, sousgraphe, tp="s", hp="n"):
        #
        sousgraphe.edge(f"{self.source.numero}:c",
                        f"{self.destination.numero}:c",
                        style="solid",
                        headport=hp,
                        tailport=tp,
                        arrowhead="normal",
                        arrowsize=".5")

def est_plus_petit(element1, element2, fonction=None):
    """Renvoie True ou False selon l'ordre de element1 et element2
    relativement à une fonction (optionnelle)
    """
    
    if not fonction: fonction = lambda a, b: a < b
    return fonction(element1, element2)


def _fusion(gauche, droite, fonction_ordre):
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
        self._graphe = graphviz.Digraph(engine="dot")
        # init classe noeud
        Noeud._liste_noeuds = []
        Noeud._numero = 0
        # 1 en trop car une profondeur manquante : celle de la
        # condtion de terminaison
        self._nb_profondeurs = 1 + 2 * math.ceil(math.log2(len(liste)))
        Noeud._profondeur_max = self._nb_profondeurs
        #
        # attributs publics
        self.fonction_ordre = None
        self.noirblanc = False
        self.profondeurs_cachees = []
        self.forme_diviser = None
        self.forme_combiner = None
        self.forme_arreter = None
        self.style = None
        self.sortie_appels = False
        #
        self._racine = Noeud(liste, 1)

    def sortie(self, nom_fichier, format="pdf"):
        if self.sortie_appels:
            r_appels = Recappels()
        #
        self._tri_fusion(self._racine)
        #
        if self.sortie_appels:
            r_appels.visu(nom_fichier + "_appels", format)
        #
        Noeud._liste_prof_cach = self.profondeurs_cachees
        self._graphe.attr("node", colorscheme=f"rdylgn{self._nb_profondeurs}")
        #
        if not self.style:
            style = "filled,rounded"
            if self.noirblanc:
                style = "rounded"
        else:
            style = self.style
        self._graphe.attr("node", style=style)
        #
        if self.forme_arreter:
            Noeud._shape_arreter = self.forme_arreter
        if self.forme_combiner:
            Noeud._shape_combiner = self.forme_combiner
        if self.forme_diviser:
            Noeud._shape_diviser = self.forme_diviser
        #
        self._trace()
        #
        self._graphe.render(filename=nom_fichier, format=format)

    def _tri_fusion(self, noeud, profondeur=1):
        liste = noeud.liste
        #
        if len(liste) == 1:
            bloc = Bloc(liste, None, None, None, None, None)
            return noeud, bloc
        #
        iMilieu = (len(liste) + 1) // 2
        g = liste[:iMilieu]
        d = liste[iMilieu:]
        og = Noeud(g, profondeur + 1)
        od = Noeud(d, profondeur + 1)
        #
        ng, bloc_ng = self._tri_fusion(og, profondeur + 1)
        nd, bloc_nd = self._tri_fusion(od, profondeur + 1)
        f = _fusion(ng.liste, nd.liste, self.fonction_ordre)
        nf = Noeud(f, self._nb_profondeurs - profondeur + 1)
        #
        og._de.append(noeud.numero)
        od._de.append(noeud.numero)
        ng._vers.append(nf.numero)
        nd._vers.append(nf.numero)
        #
        bloc = Bloc(liste,
                    og.liste, od.liste,
                    ng.liste, nd.liste,
                    nf.liste)
        #
        Bloc.arete(bloc, ":tfg:ne", bloc_ng, ":arg")
        Bloc.arete(bloc, ":tfd:ne", bloc_nd, ":arg")
        sous_id = ":f" if len(ng.liste) !=1 else ":r"
        Bloc.arete(bloc_ng, sous_id, bloc, ":tfg")
        sous_id = ":f" if len(nd.liste) !=1 else ":r"
        Bloc.arete(bloc_nd, sous_id, bloc, ":tfd")
        #
        return nf, bloc

    def _trace(self):
        # clusters des noeuds avec la même profondeur
        liste_singletons = []
        for i in range(1, Noeud._profondeur_max + 1):
            with self._graphe.subgraph(name=str(i)+"sub") as prof:
                prof.attr(rank="same")
                for n in Noeud._liste_noeuds:
                    # on discrimine pour aligner les noeuds de
                    # longueur 1
                    if n.profondeur == i and len(n.liste) != 1:
                        n.visu(prof)
                    elif len(n.liste) == 1:
                        liste_singletons.append(n)
        # les noeuds de longueur 1
        with self._graphe.subgraph(name="seulsub") as prof:
            prof.attr(rank="same")
            for n in liste_singletons:
                n.visu(prof)
        # les arcs
        for n in Noeud._liste_noeuds:
            # a priori chaque liste ci-dessous est vide ou un singleton
            for parent in n._de:
                Arc(Noeud._liste_noeuds[parent], n).visu(self._graphe)
            for enfant in n._vers:
                Arc(n, Noeud._liste_noeuds[enfant]).visu(self._graphe)
