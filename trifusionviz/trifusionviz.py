# -*- coding: utf-8 -*-
__author__ = "david cobac"
__date__ = 20201211


import graphviz
import math


class Noeud:
    _numero = 0
    _profondeur_max = 0
    _liste_noeuds = []
    _liste_prof_cach = []
    _shape_diviser = "invtrapezium"
    _shape_arret = "circle"
    _shape_combiner = "trapezium"

    def __init__(self, contenu, profondeur):
        self.numero = Noeud._numero
        self.profondeur = profondeur
        #
        Noeud._numero += 1
        #
        self.liste = contenu
        #
        if len(contenu) == 1:
            self._shape = Noeud._shape_arret
        elif profondeur <= Noeud._profondeur_max / 2:
            self._shape = Noeud._shape_diviser
        else:
            self._shape = Noeud._shape_combiner
        #
        self.dico = {"numero": self.numero,
                     "profondeur": profondeur,
                     "de": None,
                     "vers": None}
        #
        Noeud._liste_noeuds.append(self)

    def visu(self, sousgraphe):
        if self.profondeur not in Noeud._liste_prof_cach:
            etiquette = str(self.liste)
        else:
            etiquette = " " * (len(self.liste)  + 2)
        #
        sousgraphe.node(str(self.numero),
                        label=etiquette,
                        shape=self._shape,
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
        Noeud._profondeur_max = self._nb_profondeurs + 1
        #
        # attributs publics
        self.fonction_ordre = None
        self.noirblanc = False
        self.profondeurs_cachees = []
        #
        self._racine = Noeud(liste, 1)

    def sortie(self, nom_fichier, format="pdf"):
        self._tri_fusion(self._racine)
        #
        Noeud._liste_prof_cach = self.profondeurs_cachees
        self._graphe.attr("node", colorscheme=f"rdylgn{self._nb_profondeurs}")
        self._graphe.attr("node", style="rounded")
        if not self.noirblanc:
            self._graphe.attr("node", style="filled")
        #
        self._racine.visu(self._graphe)
        self._trace()
        #
        self._graphe.render(filename=nom_fichier, format=format)

    def _tri_fusion(self, noeud, profondeur=1):
        liste = noeud.liste

        if len(liste) == 1: return noeud

        iMilieu = (len(liste) + 1) // 2
        g = liste[:iMilieu]
        d = liste[iMilieu:]
        og = Noeud(g, profondeur + 1)
        od = Noeud(d, profondeur + 1)

        ng = self._tri_fusion(og, profondeur + 1)
        nd = self._tri_fusion(od, profondeur + 1)
        f = _fusion(ng.liste, nd.liste, self.fonction_ordre)
        nf = Noeud(f, self._nb_profondeurs - profondeur + 1)

        og.dico["de"] = noeud.numero # noeud.dico["numero"]
        od.dico["de"] = noeud.numero # noeud.dico["numero"]
        ng.dico["vers"] = nf.numero # nf.dico["numero"]
        nd.dico["vers"] = nf.numero # nf.dico["numero"]

        return nf

    def _trace(self):
        # clusters des noeuds avec la même profondeur
        for i in range(Noeud._profondeur_max + 1):
            with self._graphe.subgraph(name=str(i)) as prof:
                prof.attr(rank="same")
                for n in Noeud._liste_noeuds:
                    if n.profondeur == i:
                        n.visu(prof)

        # les arcs
        for n in Noeud._liste_noeuds:
            if n.dico['de'] is not None:
                Arc(Noeud._liste_noeuds[n.dico['de']], n).visu(self._graphe)
            if n.dico['vers'] is not None:
                Arc(n, Noeud._liste_noeuds[n.dico['vers']]).visu(self._graphe)

