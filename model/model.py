from itertools import combinations

from networkx.classes import neighbors

from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.best_path = []
        self.best_pesi = []

    def get_years(self):
        return DAO.get_years()

    def get_shape(self, year):
        return DAO.get_shape(year)

    def create_graph(self, year, shape):
        nodi = DAO.get_state()
        self.G.add_nodes_from(nodi)

        diz_avvistamenti = DAO.get_avvistamenti(year, shape)
        neighbors = DAO.get_connection()

        for u, v in neighbors:
            peso_u = diz_avvistamenti.get(u, 0)
            peso_v = diz_avvistamenti.get(v, 0)

            peso_tot = peso_u + peso_v

            self.G.add_edge(u, v, weight=peso_tot)

    def get_graph_details(self):
        lista_pesi = []

        for nodo in self.G.nodes():
            # TRUCCO NETWORKX:
            # .degree(nodo, weight="weight") somma i pesi di tutti gli archi collegati a 'nodo'.
            # "weight" è il nome della chiave che abbiamo usato in add_edge(..., weight=...)
            somma_pesi = self.G.degree(nodo, weight="weight")

            lista_pesi.append((nodo, somma_pesi))

        return lista_pesi

    def n_nodi_archi(self):
        n_nodi = self.G.number_of_nodes()
        n_archi = self.G.number_of_edges()

        return n_nodi, n_archi

    def get_best_set(self):
        self.best_path = []
        self.best_pesi = []

        for nodo_partenza in self.G.nodes():
            # Creo la lista parziale iniziale che contiene SOLO quel nodo
            parziale = [nodo_partenza]
            lista_pesi = []

            # Lancio la ricorsione
            self.ricorsione(parziale, lista_pesi)

        return self.best_path, self.best_pesi

    def ricorsione(self, parziale, lista_pesi):
        # Ho fatto meglio di prima?
        if len(parziale) > len(self.best_path):
            self.best_path = list(parziale)
            self.best_pesi = list(lista_pesi)

        # Verifico i nodi da esplorare

        # mi salvo l'ultimo nodo in modo da... (non vuoto all'inizio in quanto inserito nel metodo pubblico)
        ultimo_nodo = parziale[-1]
        # poter trovare subito i vicini dell'arco da considerare per l'esplorazione
        vicini = self.G.neighbors(ultimo_nodo)

        for v in vicini:
            if v not in parziale:
                # salvo il peso dell'arco per poterlo confrontare
                peso_arco_attuale = self.G[ultimo_nodo][v]["weight"]

                if len(parziale) == 1:
                    parziale.append(v)
                    self.ricorsione(parziale, lista_pesi)
                    parziale.pop()

                else:
                    # Ho già fatto almeno un passo. Devo confrontare con il precedente.
                    penultimo_nodo = parziale[-2]
                    peso_arco_precedente = self.G[penultimo_nodo][ultimo_nodo]['weight']

                    # CONDIZIONE: Peso Crescente
                    if peso_arco_attuale > peso_arco_precedente:
                        parziale.append(v)
                        lista_pesi.append(peso_arco_attuale + peso_arco_precedente)

                        self.ricorsione(parziale, lista_pesi)

                        parziale.pop()
                        lista_pesi.pop()


    def get_distance(self):
        diz_id_coord = DAO.get_lat_long()

        return diz_id_coord



    # trovo lat e long associata ad ogni stato nel dao

    #per ogni coppia associo al primo nodo (stato) i suoi valori... poi per il secondo   (dizionario[stato] = lat, long)

    #calcolo finale della distanza