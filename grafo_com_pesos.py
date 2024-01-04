#Feito por: Alan W. S. Corrêa

import sys

class Grafo:
    def __init__(self):
        self.num_vertices = 0
        self.arestas = []

    def leitura_arquivo_grafo(self, nome_arquivo):
        with open(nome_arquivo, 'r') as arquivo:
            self.num_vertices = int(arquivo.readline().strip())
            for linha in arquivo:
                inicia, fim = map(int, linha.strip().split())
                self.arestas.append((inicia, fim))
    
    def leitura_arquivo_grafo_com_pesos(self, nome_arquivo):
        with open(nome_arquivo, 'r') as arquivo:
            self.num_vertices = int(arquivo.readline().strip())
            for linha in arquivo:
                inicia, fim, peso = map(float, linha.strip().split())
                self.arestas.append((int(inicia), int(fim), peso))

    def distancia_caminho_minimo(self, origem, destino):
        if origem < 1 or origem > self.num_vertices or destino < 1 or destino > self.num_vertices:
            return 'Vértices de origem ou destino inválidos.'

        pai, distancia = self.busca_caminho_minimo(origem - 1)

        caminho = self.construir_caminho(origem - 1, destino - 1, pai)

        if caminho:
            return f'Caminho mínimo de {origem} para {destino}: {caminho}, Distância mínima: {distancia[destino - 1]}'
        else:
            return f'Não há caminho de {origem} para {destino}.'

    def distancia_caminho_minimo_todos(self, origem):
        if origem < 1 or origem > self.num_vertices:
            return 'Vértice de origem inválido.'

        pai, distancia = self.busca_caminho_minimo(origem - 1)

        result = []
        for destino in range(1, self.num_vertices + 1):
            if origem != destino:
                caminho = self.construir_caminho(origem - 1, destino - 1, pai)
                if caminho:
                    result.append(f'Caminho mínimo de {origem} para {destino}: {caminho}, Distância mínima: {distancia[destino - 1]}')
                else:
                    result.append(f'Não há caminho de {origem} para {destino}.')

        return result
   
    def busca_caminho_minimo(self, origem):
        if not self.tem_pesos_negativos():
            return self.busca_largura(origem)
        else:
            return self.dijkstra(origem)

    def tem_pesos_negativos(self):
        for aresta in self.arestas:
            if len(aresta) == 3 and aresta[2] < 0:
                return True
        return False
  
    def dijkstra(self, origem):
        distancia = [sys.maxsize] * self.num_verticesmin_index
        pai = [-1] * self.num_vertices
        visitado = [False] * self.num_vertices
        distancia[origem] = 0

        for _ in range(self.num_vertices - 1):
            u = self.min_distancia(distancia, visitado)
            visitado[u] = True

            for v in range(self.num_vertices):
                if not visitado[v] and distancia[v] > distancia[u] + self.peso(u, v):
                    distancia[v] = distancia[u] + self.peso(u, v)
                    pai[v] = u

        return pai, distancia

    def min_distancia(self, distancia, visitado):
        min_dist = sys.maxsize
        min_index = -1

        for v in range(self.num_vertices):
            if not visitado[v] and distancia[v] < min_dist:
                min_dist = distancia[v]
                min_index = v

        return min_index

    def peso(self, u, v):
        for aresta in self.arestas:
            if len(aresta) == 3 and aresta[0] == u and aresta[1] == v:
                return aresta[2]
        return sys.maxsize

    def construir_caminho(self, origem, destino, pai):
        caminho = []
        if pai[destino] == -1:
            return None
        atual = destino
        while atual != origem:
            caminho.insert(0, atual + 1)
            atual = pai[atual]
        caminho.insert(0, origem + 1)
        return caminho

    def kruskal(self):
        arestas_ordenadas = sorted(self.arestas, key=lambda x: x[2] if len(x) == 3 else 0)
        arvore_geradora = []
        conjunto = [i for i in range(self.num_vertices)]

        for aresta in arestas_ordenadas:
            inicio, fim, peso = aresta
            if conjunto[inicio - 1] != conjunto[fim - 1]:
                arvore_geradora.append((inicio, fim, peso))
                antigo_conjunto, novo_conjunto = conjunto[inicio - 1], conjunto[fim - 1]
                for i in range(self.num_vertices):
                    if conjunto[i] == antigo_conjunto:
                        conjunto[i] = novo_conjunto

        return arvore_geradora
    
    def desenhar_arvore_geradora(self, arvore_geradora, arquivo_saida):
        with open(arquivo_saida, 'w') as arquivo:
            arquivo.write(f'Arvore Geradora Minima:\n')
            peso_total = 0
            for aresta in arvore_geradora:
                inicio, fim, peso = aresta
                arquivo.write(f'  {inicio} -> {fim} ["Peso = {peso}"];\n')
                peso_total += peso
            arquivo.write('}\n')
            arquivo.write(f'Peso total: {peso_total:.2f}\n')

    def calcula_grau(self):
        grau = {}
        for aresta in self.arestas:
            for vertice in aresta:
                if vertice in grau:
                    grau[vertice] += 1
                else:
                    grau[vertice] = 1

        total_vertices = self.num_vertices
        distribui_grau = {k: v / total_vertices for k, v in grau.items()}
        return distribui_grau

    def escreve_info_grafo(self, saida_arquivo):
        distribui_grau = self.calcula_grau()
        total_arestas = len(self.arestas)
        media_grau = (2 * total_arestas) / self.num_vertices

        with open(saida_arquivo, 'w') as arquivo:
            arquivo.write(f'1 - Numero Vertices = {self.num_vertices}\n')
            arquivo.write(f'2 - Numero Arestas = {total_arestas}\n')
            arquivo.write(f'3 - Grau Medio = {media_grau:.1f}\n\n')
            for vertice, frequencia in sorted(distribui_grau.items()):
                arquivo.write(f'{vertice} {frequencia:.2f}\n')

    def cria_matriz_adjacencia(self):
        matriz_adjacencia = [[0] * self.num_vertices for _ in range(self.num_vertices)]
        for aresta in self.arestas:
            inicia, fim = aresta
            matriz_adjacencia[inicia - 1][fim - 1] = 1 

        return matriz_adjacencia

    def cria_lista_adjacencia(self):
        lista_adjacencia = [[] for i in range(self.num_vertices)]
        for aresta in self.arestas:
            inicia, fim = aresta
            lista_adjacencia[inicia - 1].append(fim - 1)
            lista_adjacencia[fim - 1].append(inicia - 1)

        return lista_adjacencia

    def busca_largura(self, inicia_vertice):
        visitado = [False] * self.num_vertices
        pai = [-1] * self.num_vertices
        nivel = [-1] * self.num_vertices

        fila = []
        fila.append(inicia_vertice)
        visitado[inicia_vertice] = True
        nivel[inicia_vertice] = 0

        while fila:
            vertice_atual = fila.pop(0)
            for vizinho in self.cria_lista_adjacencia()[vertice_atual]:
                if not visitado[vizinho]:
                    fila.append(vizinho)
                    visitado[vizinho] = True
                    pai[vizinho] = vertice_atual
                    nivel[vizinho] = nivel[vertice_atual] + 1

        return pai, nivel

    def busca_profunda(self, inicia_vertice):
        visitado = [False] * self.num_vertices
        pai = [-1] * self.num_vertices
        nivel = [-1] * self.num_vertices

        def busca_profunda_util(vertice_atual):
            visitado[vertice_atual] = True
            for vizinho in self.cria_lista_adjacencia()[vertice_atual]:
                if not visitado[vizinho]:
                    pai[vizinho] = vertice_atual
                    nivel[vizinho] = nivel[vertice_atual] + 1
                    busca_profunda_util(vizinho)

        busca_profunda_util(inicia_vertice)
        return pai, nivel

    def escreve_info_arvore(self, saida_arquivo, pai, nivel):
        with open(saida_arquivo, 'w') as arquivo:
            arquivo.write(f'# Numero de Vertices = {self.num_vertices}\n')
            for vertice in range(self.num_vertices):
                arquivo.write(f'Vertices {vertice + 1}, Pai:{pai[vertice] + 1 if pai[vertice] != -1 else "Nenhum"}, Nivel: {nivel[vertice] + 1}\n')

    def componentes_conexos(self):
        visitado = [False] * self.num_vertices
        componentes = []

        def busca_componente(vertice):
            componente = []
            fila = [vertice]

            while fila:
                vertice_atual = fila.pop()
                if not visitado[vertice_atual]:
                    componente.append(vertice_atual)
                    visitado[vertice_atual] = True
                    for vizinho in self.cria_lista_adjacencia()[vertice_atual]:
                        if not visitado[vizinho]:
                            fila.append(vizinho)

            return componente

        for vertice in range(self.num_vertices):
            if not visitado[vertice]:
                componente = busca_componente(vertice)
                if componente:
                    componentes.append(componente)
        componentes.sort(key=lambda x: len(x), reverse=True)

        return componentes
    
if __name__ == '__main__':

    entrada_grafo = 'entrada_grafos.txt'
    saida_busca_largura = 'saida_busca_largura.txt'
    saida_busca_profunda = 'saida_busca_profunda.txt'
    saida_grafo = 'saida_grafos.txt'
    entrada_grafo_com_pesos = 'entrada_grafos_com_pesos.txt' 

    grafo = Grafo()
    grafo_com_pesos = Grafo() 
    grafo.leitura_arquivo_grafo(entrada_grafo)
    grafo_com_pesos.leitura_arquivo_grafo_com_pesos(entrada_grafo_com_pesos)

    inicia_vertice = int(input('Escolha o vértice inicial: '))

    pai_busca_largura, nivel_busca_largura = grafo.busca_largura(inicia_vertice - 1)
    pai_busca_profunda, nivel_busca_profunda = grafo.busca_profunda(inicia_vertice - 1)
    grafo.escreve_info_grafo(saida_grafo)
    grafo.escreve_info_arvore(saida_busca_largura, pai_busca_largura, nivel_busca_largura)
    grafo.escreve_info_arvore(saida_busca_profunda, pai_busca_profunda, nivel_busca_profunda)
    componentes = grafo.componentes_conexos()

    escolha_representação = input('Escolha a representação (1 - Matriz de Adjacência, 2 - Lista de Adjacência): ')

    if escolha_representação == '1':
        matriz_adjacencia = grafo.cria_matriz_adjacencia()
        print('Matriz de Adjacência:')
        for linha in matriz_adjacencia:
            print(linha)

    elif escolha_representação == '2':
        lista_adjacencia = grafo.cria_lista_adjacencia()
        print('Lista de Adjacência:')
        for i, vizinho in enumerate(lista_adjacencia):
            print(f'{i + 1}: {vizinho}')
    else:
        print('Escolha uma opção válida para representação (1 ou 2)')
    
    print(f'Número de Componentes Conexos: {len(componentes)}')
    for i, componente in enumerate(componentes, start=1):
        print(f'Componente {i}: Tamanho = {len(componente)}, Vértices = {componente}')

    
    origem = int(input('Escolha o vértice de origem: '))

    
    if not grafo.tem_pesos_negativos():
        tipo_algoritmo = 'busca_largura'
    else:
        tipo_algoritmo = 'Dijkstra'

    if tipo_algoritmo == 'busca_largura':
        pai, nivel = grafo.busca_largura(origem - 1)
    else:
        pai, distancia = grafo.dijkstra(origem - 1)

    print(f'Distância mínima e caminho mínimo de {origem} para todos os outros vértices:')
    for destino in range(1, grafo.num_vertices + 1):
        if origem != destino:
            caminho = grafo.construir_caminho(origem - 1, destino - 1, pai)
            if tipo_algoritmo == 'busca_largura':
                print(f'Caminho mínimo de {origem} para {destino}: {caminho}, Distância mínima: {nivel[destino - 1]}')
            else:
                print(f'Caminho mínimo de {origem} para {destino}: {caminho}, Distância mínima: {distancia[destino - 1]}')

    arvore_geradora = grafo_com_pesos.kruskal()

    grafo_com_pesos.desenhar_arvore_geradora(arvore_geradora, 'arvore_geradora.txt')

    print('Árvore Geradora Mínima (Kruskal):')
    for aresta in arvore_geradora:
        print(aresta)
    