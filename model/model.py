import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.DiGraph()
        self._idMap={}

        self._bestPath = []
        self._maxLength = 0
        self._bestPunteggio=0

    def getAllStores(self):
        return DAO.getAllStores()

    def createGraph(self, storeId, k):
        self._graph.clear()
        self._idMap={}

        nodes=DAO.getOrders(storeId)
        for node in nodes:
            self._idMap[node.order_id]=node
        self._graph.add_nodes_from(nodes)

        self._addEdges(storeId, k)

    def _addEdges(self,storeId, k):
        edges=DAO.getEdges(storeId, k)
        for edge in edges:
            node1=self._idMap[edge[0]]
            node2=self._idMap[edge[1]]
            somma=edge[2]
            giorni=edge[3]

            self._graph.add_edge(node1,node2, weight=somma/giorni)

    def getInfoGraph(self):
        edges=list(self._graph.edges(data=True))
        edges.sort(key=lambda x: x[2]["weight"], reverse=True)
        return len(self._graph.nodes), len(self._graph.edges), edges[:5]
    def getOrders(self):
        return list(self._graph.nodes)

    def searchPath(self, nodeId):
        start_node = self._idMap[nodeId]
        self._bestPath = []
        self._maxLength = 0
        self._dfs(start_node, [start_node])

        return self._bestPath

    def _dfs(self, current_node, parziale):
        if len(parziale) > self._maxLength:
            self._maxLength = len(parziale)
            self._bestPath = copy.deepcopy(parziale)

        for neighbor in self._graph.neighbors(current_node):
            if neighbor not in parziale:
                parziale.append(neighbor)
                self._dfs(neighbor, parziale)
                parziale.pop()

    def handleRicorsione(self, nodeId):
        node=self._idMap[nodeId]
        self._bestPath=[]
        self._bestPunteggio=0

        self._ricorsione([node],9999, 0)

        return  self._bestPath, self._bestPunteggio

    def _ricorsione(self,parziale, arco, punteggio):
        if punteggio>self._bestPunteggio:
            self._bestPunteggio=punteggio
            self._bestPath=copy.deepcopy(parziale)

        for node in self._graph.neighbors(parziale[-1]):
            if node not in parziale:
                new_arco=self._graph[parziale[-1]][node]["weight"]
                if arco>new_arco:
                    new_punteggio=new_arco+punteggio
                    parziale.append(node)
                    self._ricorsione(parziale, new_arco, new_punteggio)
                    parziale.pop()
