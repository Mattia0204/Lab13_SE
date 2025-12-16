import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.peso_min = -1
        self.peso_max = -1
        self.minori = 0
        self.maggiori = 0
        self.lista_archi = []
        self.lista_duplicati = []
        self.G = nx.Graph()

    def build_weighted_graph(self):  # costruisce il grafo pesato e orientato
        self.G = nx.Graph()
        dict_interazione = DAO.get_interazione()
        dict_gene = DAO.get_gene()
        for interazione in dict_interazione.values():
            cromosoma1 = 0
            cromosoma2 = 0
            peso = float(interazione.correlazione)
            for gene in dict_gene.values():
                if gene.id == interazione.id_gene1:
                    cromosoma1 = gene.cromosoma
                if gene.id == interazione.id_gene2:
                    cromosoma2 = gene.cromosoma
                if cromosoma1 != cromosoma2:
                    if (cromosoma1, cromosoma2) not in self.G:
                        self.G.add_edge(cromosoma1, cromosoma2, peso=peso)
                    else:
                        peso_estratto=float(self.G[cromosoma1][cromosoma2]['peso'])
                        peso = peso + peso_estratto
                        self.G.remove_edge(cromosoma1, cromosoma2)
                        self.G.add_edge(cromosoma1, cromosoma2, peso=peso)

        return self.G

    def get_edges_weight_min_max(self):  # restituisce peso minimo e massimo degli archi
        pesi = [data["peso"] for _, _, data in self.G.edges(data=True)]  # lista dei pesi degli archi
        for peso in pesi:
            peso = float(peso)
            if self.peso_min == -1:
                self.peso_min = peso
            if self.peso_max == -1:
                self.peso_max = peso
            if self.peso_max < peso:
                self.peso_max = peso
            if self.peso_min > peso:
                self.peso_min = peso
        return self.peso_min, self.peso_max

    def count_edges_by_threshold(self, soglia):  # conta archi minori e maggiori della soglia
        pesi = [data["peso"] for _, _, data in self.G.edges(data=True)]  # lista dei pesi degli archi
        for peso in pesi:
            peso = float(peso)
            if peso < soglia:
                self.minori += 1  # incrementa il contatore minori
            elif peso > soglia:
                self.maggiori += 1  # incrementa il contatore maggiori
        return self.minori, self.maggiori
    """
    def nodi_consecutivi(self):  # costruisce dizionario dei vicini diretti dal DB
        dic_nodi = {}
        dict_rifugi = DAO.get_rifugio()
        for rifugio in dict_rifugi.values():
            dic_nodi[rifugio.nome] = []
        dict_connessioni = DAO.get_connessione()
        for connessione in dict_connessioni.values():
            rifugio1 = ""
            rifugio2 = ""
            id1 = connessione.id_rifugio1
            id2 = connessione.id_rifugio2
            for rifugio in dict_rifugi.values():  # cerca i nomi corrispondenti agli id
                if rifugio.id == id1:
                    rifugio1 = rifugio.nome
                if rifugio.id == id2:
                    rifugio2 = rifugio.nome
            if rifugio1 and rifugio2:  # se entrambi i nomi sono presenti
                dic_nodi[rifugio1].append(rifugio2)
                dic_nodi[rifugio2].append(rifugio1)
        return dic_nodi

    def cerca_cammino_minimo(self, soglia):  # ricerca cammino minimo con Dijkstra e filtri
        soglia = float(soglia)
        cammini_validi = []
        G_soglia = nx.Graph()  # sotto-grafo che conterrà solo archi con peso > soglia
        for u, v, data in self.G.edges(data=True):
            if data["peso"] > soglia:
                G_soglia.add_edge(u, v, peso=data["peso"])
        for nodo_inizio in G_soglia.nodes:
            lengths, paths = nx.single_source_dijkstra(G_soglia, source=nodo_inizio, weight="peso")  # Dijkstra da nodo_inizio
            for nodo_fine, peso_totale in lengths.items():  # per ogni nodo raggiungibile prendo lunghezze e percorsi
                path = paths[nodo_fine]
                if len(path) >= 3:  # controllo che il percorso abbia almeno 3 nodi (2 archi)
                    coppia = tuple(
                        sorted([path[0], path[-1]]))  # normalizza coppia estremi per evitare duplicati inversi
                    cammini_validi.append((coppia[0], coppia[1], path, peso_totale))
        unici = set()
        cammini_unici = []
        for c in cammini_validi:  # rimuove duplicati approssimativi basati su estremi e peso
            key = (c[0], c[1], round(c[3], 6))
            if key not in unici:
                unici.add(key)
                cammini_unici.append(c)
        if not cammini_unici:
            return []
        min_peso = min(cammini_unici, key=lambda x: x[3])[3]  # trova il peso minimo tra i cammini unici
        cammini_minimi = [c for c in cammini_unici if c[3] == min_peso]  # filtra solo i cammini con peso minimo
        percorsi_finali = []
        for start, end, path, _ in cammini_minimi:
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                peso_arco = G_soglia[u][v]['peso']
                percorsi_finali.append((u, v, peso_arco))
        return percorsi_finali
    """