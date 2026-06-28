import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillddstore(self):
        negozi=self._model.getAllStores()
        for n in negozi:
            self._view._ddStore.options.append(ft.dropdown.Option(text=n.store_name, key=n.store_id))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        storeId=self._view._ddStore.value
        if storeId is None:
            self._view.create_alert("Selezionare un negozio dal dd")
            self._view.update_page()
            return
        storeId=int(storeId)
        k=self._view._txtIntK.value
        if k is None:
            self._view.create_alert("Inserire un valore di k")
            self._view.update_page()
            return
        try:
            k=int(k)
        except ValueError:
            self._view.create_alert("Inserire un valore di k valido")
            self._view.update_page()
            return

        self._model.createGraph(storeId,k)

        nodi, archi, archiBest= self._model.getInfoGraph()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato con {nodi} nodi e {archi} archi"))
        self._view.txt_result.controls.append(ft.Text(f"Top 5 archi:"))
        for n in archiBest:
            self._view.txt_result.controls.append(ft.Text(f"{n[0]} - {n[1]} : {n[2]['weight']}"))

        orders=self._model.getOrders()
        self._view._ddNode.disabled = False
        self._view._btnCerca.disabled = False
        self._view._ddNode.options.clear()
        for n in orders:
            self._view._ddNode.options.append(ft.dropdown.Option(n.order_id))
        self._view.update_page()


    def handleCerca(self, e):
        if self._model._graph.nodes is None:
            self._view.create_alert("Creare prima il grafo")
            self._view.update_page()
            return
        node=self._view._ddNode.value
        path=self._model.searchPath(int(node))
        self._view._btnRicorsione.disabled = False

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Percorso più lungo trovato con {len(path)} nodi:"))
        for n in path:
            self._view.txt_result.controls.append(ft.Text(f"{n}"))
        self._view.update_page()



    def handleRicorsione(self, e):
        if self._model._graph.nodes is None:
            self._view.create_alert("Creare prima il grafo")
            self._view.update_page()
            return
        node=self._view._ddNode.value
        path, peso=self._model.handleRicorsione(int(node))

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Percorso più lungo trovato con {len(path)} nodi e {peso} di peso:"))
        for n in path:
            self._view.txt_result.controls.append(ft.Text(f"{n}"))
        self._view.update_page()