import random

def ler_entrada(arquivo):
    """
    Lê a entrada do arquivo e retorna a capacidade, o número de itens e os tamanhos dos itens.

    Parâmetros:
    arquivo (str): Nome do arquivo de entrada.

    Retorna:
    tuple: Capacidade, número de itens e lista dos tamanhos dos itens.
    """
    with open(arquivo, 'r') as file:
        capacidade = int(file.readline().strip())
        num_itens = int(file.readline().strip())
        tamanhos_itens = list(map(int, file.readline().strip().split()))
    return capacidade, num_itens, tamanhos_itens

def solucao_gulosa(capacidade, tamanhos_itens):
    """
    Gera uma solução inicial utilizando um algoritmo guloso.

    Parâmetros:
    capacidade (int): Capacidade de cada recipiente.
    tamanhos_itens (list): Lista dos tamanhos dos itens.

    Retorna:
    list: Lista de recipientes com os itens alocados.
    """
    random.shuffle(tamanhos_itens)  # Embaralha os itens para garantir aleatoriedade
    recipientes = []  # Lista de recipientes
    
    for item in tamanhos_itens:
        alocado = False
        for recipiente in recipientes:
            if sum(recipiente) + item <= capacidade:  # Verifica se o item cabe no recipiente
                recipiente.append(item)
                alocado = True
                break
        if not alocado:  # Se o item não couber em nenhum recipiente existente, cria um novo
            recipientes.append([item])
    
    return recipientes

def calcular_custo(solucao):
    """
    Calcula o custo da solução (número de recipientes utilizados).

    Parâmetros:
    solucao (list): Lista de recipientes.

    Retorna:
    int: Número de recipientes utilizados.
    """
    return len(solucao)

def gerar_vizinho(solucao, capacidade):
    """
    Gera uma solução vizinha movendo um item para outro recipiente.

    Parâmetros:
    solucao (list): Lista de recipientes.
    capacidade (int): Capacidade de cada recipiente.

    Retorna:
    list: Nova solução vizinha.
    """
    nova_solucao = [recipiente[:] for recipiente in solucao]  # Cria uma cópia profunda da solução
    item_mover = random.choice([item for sublist in nova_solucao for item in sublist])  # Seleciona um item aleatório
    
    for recipiente in nova_solucao:
        if item_mover in recipiente:  # Remove o item do recipiente atual
            recipiente.remove(item_mover)
            break

    for recipiente in nova_solucao:
        if sum(recipiente) + item_mover <= capacidade:  # Tenta colocar o item em outro recipiente
            recipiente.append(item_mover)
            return nova_solucao

    nova_solucao.append([item_mover])  # Se não couber em nenhum recipiente, cria um novo
    return nova_solucao

def busca_tabu(capacidade, tamanhos_itens, iteracoes=1000, tamanho_tabu=20):
    """
    Aplica a Busca Tabu para encontrar uma melhor solução.

    Parâmetros:
    capacidade (int): Capacidade de cada recipiente.
    tamanhos_itens (list): Lista dos tamanhos dos itens.
    iteracoes (int): Número de iterações.
    tamanho_tabu (int): Tamanho da lista tabu.

    Retorna:
    list: Melhor solução encontrada.
    """
    solucao_atual = solucao_gulosa(capacidade, tamanhos_itens)
    melhor_solucao = solucao_atual
    lista_tabu = []
    
    for _ in range(iteracoes):
        vizinho = gerar_vizinho(solucao_atual, capacidade)
        custo_vizinho = calcular_custo(vizinho)
        
        if vizinho not in lista_tabu and custo_vizinho < calcular_custo(melhor_solucao):
            melhor_solucao = vizinho

        solucao_atual = vizinho
        lista_tabu.append(vizinho)
        if len(lista_tabu) > tamanho_tabu:
            lista_tabu.pop(0)
    
    return melhor_solucao

def processar_arquivos(arquivos):
    """
    Processa uma lista de arquivos de entrada e exibe as soluções.

    Parâmetros:
    arquivos (list): Lista de nomes de arquivos.
    """
    for arquivo in arquivos:
        print(f"\nProcessando {arquivo}...\n")
        capacidade, num_itens, tamanhos_itens = ler_entrada(arquivo)
        solucao_inicial = solucao_gulosa(capacidade, tamanhos_itens)
        print(f"Solução inicial (gulosa): {solucao_inicial}\n")
        print(f"Número de recipientes: {len(solucao_inicial)}\n")
        
        melhor_solucao = busca_tabu(capacidade, tamanhos_itens)
        print(f"Melhor solução (Busca Tabu): {melhor_solucao}\n")
        print(f"Número de recipientes: {len(melhor_solucao)}\n")

if __name__ == "__main__":
    arquivos = ['PEU1.txt', 'PEU2.txt', 'PEU3.txt', 'PEU4.txt', 'PEU5.txt']
    processar_arquivos(arquivos)
