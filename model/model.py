import copy

import networkx as nx
from mysql.connector.constants import flag_is_set

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._nodes = []
        self._idMap = {}

    def getNodes(self):
        return self._nodes

    def get_numnodi(self):
        return len(self._grafo.nodes())

    def get_numarchi(self):
        return len(self._grafo.edges())

    def buildGraph(self):
        self._grafo.clear()
        self._idMap.clear()

        self._nodes = DAO.getAllNodes()
        for n in self._nodes:
            self._grafo.add_node(n)
            self._idMap[n.ArtistId] = n
        for art in self._grafo.nodes():
            art.brani.extend(DAO.getAllBrani(art.ArtistId))
            art.playlist.extend(DAO.getAllPlaylist(art.ArtistId))

        self.addEdgesPesati()

    def addEdgesPesati(self):
        for e in DAO.getAllEdges():
            n1 = self._idMap.get(e[0])
            n2 = self._idMap.get(e[1])
            if n1 is None or n2 is None:
                continue
            self._grafo.add_edge(n1, n2, weight=e[2])

    def get_nodo_grado_max(self):
        nodo = max(self._grafo.nodes(), key=lambda n: self._grafo.degree(n))
        return nodo, self._grafo.degree(nodo)

    def get_nodo_somma_pesi_max(self):
        nodo = max(self._grafo.nodes(), key=lambda n: self._grafo.degree(n, weight="weight"))
        return nodo, self._grafo.degree(nodo, weight="weight")

    def get_top10_archi(self):
        archi = list(self._grafo.edges(data=True))
        archi_ordinati = sorted(
            archi,
            key=lambda e: (-e[2]['weight'], e[0].Name, e[1].Name)
        )
        return archi_ordinati[:10]

    def getSottoinsiemeOttimo(self, soglia,art):
        self._bestScore = 0  # <------- float("inf") se MINIMIZZI
        self._optList = []
        candidati = [n for n in self._grafo.nodes()
                     if n is not art]  # <------- PRE-FILTRO intrinseco (se assente: tutti i nodi)
        self._ricorsione_sub(candidati, soglia, [art], 0)
        return self._optList, self._bestScore

    def _ricorsione_sub(self, candidati, soglia, parziale, index):
        if len(parziale) == soglia:  # CASO BASE: raggiunti K elementi
            if self._getScoreSoluzione(parziale) > self._bestScore:  # <------- < se MINIMIZZI
                self._bestScore = self._getScoreSoluzione(parziale)
                self._optList = copy.deepcopy(parziale)  # <------- deepcopy: NON togliere
            return
        if index >= len(candidati):  # CASO BASE: candidati finiti
            return
        if len(candidati) - index < soglia - len(parziale):  # POTATURA: rimasti < mancanti
            return

        self._ricorsione_sub(candidati, soglia, parziale, index + 1)  # SCELTA A: ESCLUDO candidati[index]

        if self.compatibile(candidati[index],
                            parziale):  # <------- COMPATIBILITA (se assente: togli l'if e rientra il blocco)
            parziale.append(candidati[index])  # SCELTA B: INCLUDO candidati[index]
            self._ricorsione_sub(candidati, soglia, parziale, index + 1)
            parziale.pop()

    def _getScoreSoluzione(self, listaElems):
        score = 0
        for el in listaElems:
            score += len(el.brani)
        return score

    def compatibile(self, nodo, parziale):
        almeno_un_vicino = False
        for n in parziale:
            if self._grafo.has_edge(nodo, n):
                almeno_un_vicino = True
                if self._grafo.get_edge_data(nodo, n)['weight'] == 1:
                    return False  # <-- veto immediato: niente early-exit sul controllo "almeno uno"
        return almeno_un_vicino














