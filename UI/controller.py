import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self, e):
        self._model.buildGraph()

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view._txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.get_numnodi()}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.get_numarchi()}"))
        self.fillDropdown()
        self._view.update_page()

    def handleStampaInfo(self,e):
        self._view._txt_result.controls.clear()
        art, grad = self._model.get_nodo_grado_max()
        art2, val = self._model.get_nodo_somma_pesi_max()
        self._view._txt_result.controls.append(ft.Text(f"il nodo con grado massimo è l'artista {art} con grado {grad}"))
        self._view._txt_result.controls.append(ft.Text(f"il nodo con somma dei pesi incidenti maggiore è {art2} con somma {val}"))
        archi10 = self._model.get_top10_archi()
        self._view._txt_result.controls.append(ft.Text(f"i dieci archi ordinati per peso decrescente sono:"))
        for a in archi10:
            self._view._txt_result.controls.append(ft.Text(f"{a[0]}------>{a[1]}, peso: {a[2]["weight"]}"))
        self._view.update_page()

    def handleSelezione(self,e):
        self._view._txt_result.controls.clear()
        soglia = self._view._txtInN.value
        art = self._view._ddArtista.value
        if soglia is None or art is None:
            self._view._txt_result.controls.append(ft.Text(f"riempire entrambe i campi richiesti!!!", color= "red"))
            self._view.update()
            return

        try:
            soglia = int(soglia)
        except (ValueError, TypeError):
            self._view._txt_result.controls.append(
                ft.Text("Inserire un numero intero valido!", color="red"))
            self._view.update()
            return

        if soglia > len(self._model._grafo.nodes()):
            self._view._txt_result.controls.append(
                ft.Text(f"inserire numero minore dei nodi presenti nel grafo!!!", color="red"))
            self._view.update()
            return



        lista, score = self._model.getSottoinsiemeOttimo(soglia,art)
        self._view._txt_result.controls.append(ft.Text(f"la lista di candidati ottimi ha score {score} è composta da: "))
        somma = 0
        for a in lista:
            self._view._txt_result.controls.append(
                ft.Text(f"{a}, con numero di brani: {len(a.brani)} e compare in {len(a.playlist)} playlist"))
            somma += len(a.brani)
        self._view._txt_result.controls.append(
            ft.Text(f"il numero totale di brani della soluzione è {somma}"))


        self._view.update_page()

    def fillDropdown(self):
        valori = self._model.getNodes()
        for v in valori:
            self._view._ddArtista.options.append(ft.dropdown.Option(key = v.ArtistId , text = v.Name))  # key=text=v (valore puro)

        self._view.update_page()