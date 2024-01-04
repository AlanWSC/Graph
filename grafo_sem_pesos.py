#Feito por: Alan W.S. Corrêa

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


    grafo = Grafo()
    grafo.leitura_arquivo_grafo(entrada_grafo)

    inicia_vertice = int(input('Escolha o vértice inicial: '))

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

    pai_busca_largura, nivel_busca_largura = grafo.busca_largura(inicia_vertice - 1)
    pai_busca_profunda, nivel_busca_profunda = grafo.busca_profunda(inicia_vertice - 1)

    grafo.escreve_info_grafo(saida_grafo)

    grafo.escreve_info_arvore(saida_busca_largura, pai_busca_largura, nivel_busca_largura)

    grafo.escreve_info_arvore(saida_busca_profunda, pai_busca_profunda, nivel_busca_profunda)

    componentes = grafo.componentes_conexos()

    print(f'Número de Componentes Conexos: {len(componentes)}')

    for i, componente in enumerate(componentes, start=1):
        print(f'Componente {i}: Tamanho = {len(componente)}, Vértices = {componente}')