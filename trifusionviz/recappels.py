import graphviz



class Bloc:
    _numero = 1
    _liste_bloc = []
    _liste_lien = []

    def arete(bloc1, sous_id_bloc1, bloc2, sous_id_bloc2):
        de = str(bloc1.numero) + sous_id_bloc1
        vers = str(bloc2.numero) + sous_id_bloc2
        Bloc._liste_lien.append([de, vers])

    def __init__(self, arg, g, d, tfg, tfd, f):
        self.numero = Bloc._numero
        Bloc._numero += 1
        self._dico = {"arg": arg,
                      "g": g, "d": d,
                      "tfg": tfg, "tfd": tfd,
                      "f": f}
        Bloc._liste_bloc.append(self)
        
    def visu(self, graphe):
        if len(self._dico['arg']) >1:
            graphe.node(str(self.numero),
                        label=f"""<arg>{self._dico['arg']}
                        |g ← {self._dico['g']}
                        |d  ← {self._dico['d']}
                        |<tfg>tf(g) = {self._dico['tfg']}
                        |<tfd>tf(d) =  {self._dico['tfd']}
                        |<f>fusion(tf(g), tf(d)) = {self._dico['f']}""")
        else:
            graphe.node(str(self.numero),
                        label=f"<arg>{self._dico['arg']}|<r>{self._dico['arg']}")

class Recappels:
    def __init__(self):
        Bloc._numero = 0
        Bloc._liste_bloc = []
        Bloc._liste_lien = []
        self._graphe = graphviz.Digraph(engine="dot")
        self._graphe.graph_attr["rankdir"] = "LR"
        self._graphe.attr("node", shape="record")
        self._graphe.attr("edge", arrowhead="open", arrowsize=".5")

    def visu(self, nom_fichier, format):
        # les premiers sont les derniers : parcours en profondeur
        for b in Bloc._liste_bloc[::-1]:
            b.visu(self._graphe)
        for de, vers in Bloc._liste_lien:
            self._graphe.edge(de, vers)
        self._graphe.render(filename=nom_fichier, format=format)
