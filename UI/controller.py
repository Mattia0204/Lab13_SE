import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """""
        self._model.build_weighted_graph()
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Grafo calcolato: {self._model.G.number_of_nodes()} nodi, {self._model.G.number_of_edges()} archi"))
        min_p, max_p = self._model.get_edges_weight_min_max()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Peso min: {min_p:.2f}, Peso max: {max_p:.2f}"))
        self._view.page.update()

    def handle_conta_edges(self, e):
        """ Handler per gestire il conteggio degli archi """""
        try:
            soglia = float(self._view.txt_name.value)
        except:
            self._view.show_alert("Inserisci un numero valido per la soglia.")
            return

        min_p, max_p = self._model.get_edges_weight_min_max()
        if soglia < min_p or soglia > max_p:
            self._view.show_alert(f"Soglia fuori range ({min_p:.2f}-{max_p:.2f})")
            return

        minori, maggiori = self._model.count_edges_by_threshold(soglia)
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(
            ft.Text(f"Archi < {soglia}: {minori}, Archi > {soglia}: {maggiori}"))
        self._view.page.update()

    def handle_ricerca(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """""
        # TODO