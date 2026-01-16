import flet as ft
from geopy import distance

from database.dao import DAO


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        years = self._model.get_years()

        for year in years:
            self._view.dd_year.options.append(ft.dropdown.Option(year))

        self._view.update()

    def change_option_year(self, e):
        # Handler di dd_year associato all'evento "on_change"
        self.populate_dd_shape()

    def populate_dd_shape(self):
        year = self._view.dd_year.value

        shapes = self._model.get_shape(year)

        for s in shapes:
            self._view.dd_shape.options.append(ft.dropdown.Option(s))

        self._view.update()

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        year = self._view.dd_year.value
        shape = self._view.dd_shape.value

        self._model.create_graph(year, shape)

        self._view.lista_visualizzazione_1.controls.clear()

        #Visualizzare nella GUI, per ogni stato, la somma dei pesi degli archi adiacenti.
        #la somma dei pesi degli archi adiacenti li recupero nel model

        lista_pesi = self._model.get_graph_details()
        n_nodi, n_archi = self._model.n_nodi_archi()

        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Numero di vertici: {n_nodi}, numero di archi: {n_archi}"))

        for (nodo, peso) in lista_pesi:
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Nodo {nodo}, somma dei pesi: {peso}"))

        self._view.update()


    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        best_path, best_pesi = self._model.get_best_set()
        diz_id_coord = self._model.get_distance()
        peso_tot = 0

        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Cammino trovato con {len(best_path)} nodi:"))

        # 3. CICLO PER STAMPARE GLI ARCHI (u --> v)
        # Uso range fino a len-1 perché l'ultimo nodo non ha un successivo
        for i in range(len(best_path) - 1):
            u = best_path[i]
            v = best_path[i + 1]

            (lat_u, long_u) = diz_id_coord.get(u, 0)
            (lat_v, long_v) = diz_id_coord.get(v, 0)

            d = distance.geodesic((lat_u, long_u), (lat_v, long_v)).km

            # Recupero il peso direttamente dal Grafo
            peso = self._model.G[u][v]['weight']
            peso_tot += peso

            self._view.lista_visualizzazione_2.controls.append(ft.Text(f"{u} --> {v}: weight {peso}, distance: {d}"))

        self._view.update()