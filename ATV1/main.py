"""
Atividade Prática 01 - Algoritmos de Ordenação - Estrutura de Dados 2

Acadêmicos:
    Gabriel Mancuso Bonfim  (2669498)
    Lucas Henrique Motta    (2669730)

Orientador:
    Prof. Dr. Rafael Gomes Mantovani
"""

from sys import argv
from time import time
from random import randint as rdi

def main():
    if len(argv) != 3:
        print("\033[1;91mERRO\033[1;30m\nO comando de execução deve ser\033[m: python main.py <arq_entrada> <arq_saida>")
        return

    arq_entrada = argv[1]
    arq_saida = argv[2]

    try:
        with open(arq_entrada, 'r') as arq:
            data = arq.read()

        # verificando se o arquivo está vazio
        if not data.strip():
            print(f"\033[1;91mERRO\033[1;30m\nO arquivo '{arq_entrada}' está vazio.\033[m")
            return
        
        linhas = data.splitlines()

        # verificando padrão do arquivo de entrada        
        if(len(linhas) > 2): 
            print(f"\033[1;91mERRO\033[1;30m\nO arquivo '{arq_entrada}' possui mais de duas linhas (Arquivo fora do padrão).\033[m")
            return

        if len(linhas) < 2:
            print(f"\033[1;91mERRO\033[1;30m\nA segunda linha do arquivo '{arq_entrada}' deve conter uma letra válida: C, D ou R.\033[m")
            return
        
        # verificando se a primeira linha contém um numero válido
        try:
            primeira = linhas[0].strip()
            n = int(primeira)
        except (IndexError, ValueError):
            print(f"\033[1;91mERRO\033[1;30m\nA primeira linha do arquivo '{arq_entrada}' deve conter um número inteiro válido.\033[m")
            return
        
        # verificando se o valor de elementos da lista é <= 0
        if n <= 0:
            print(f"\033[1;91mERRO\033[1;30m\nO número de elementos deve ser maior que zero.\033[m")
            return
        
        # verificado a letra do modo
        modo = linhas[1].strip().upper()
        if len(modo) != 1 or modo not in ('C','D','R'):
            print(f"\033[1;91mERRO\033[1;30m\nA segunda linha do arquivo '{arq_entrada}' deve conter uma letra válida: C, D ou R.\033[m")
            return
        letra_modo = modo
        
        # gerando a lista de números
        if letra_modo == 'C':
            lista = list(range(1, n+1))
        elif letra_modo == 'D':
            lista = list(range(n, 0, -1))
        else: # só sobra modo 'R'
            lista = [rdi(0, 32000) for _ in range(n)] # _ é uma variável descartável
        
        print(f"\nLista inicial ({letra_modo}): {lista}\n")

        metodos = [
            ("Bubble Sort", bubble_sort),
            ("Selection Sort", selection_sort),
            ("Insertion Sort", insertion_sort),
            ("Merge Sort", merge_sort),
            ("Quick Sort", quick_sort),
            ("Heap Sort", heap_sort),
            ("Radix Sort",radix_sort)
        ]

        resultados = []

        # percorrendo lista de métodos e colocando as respostas
        for nome, funcao in metodos:
            lista_copia = lista.copy()
            t0 = time()
            if nome == "Merge Sort" or nome == "Quick Sort":
                comparacoes = funcao(lista_copia, 0, len(lista_copia)-1, True)
            else:
                comparacoes = funcao(lista_copia, True)
            t1 = time()
            tempo = (t1 - t0) * 1000
            resultados.append((nome, lista_copia, comparacoes, tempo))

        # escrevendo no arquivo de saida
        with open(arq_saida, "w") as arq:
            for nome, lista_ord, comp, tempo in resultados:
                cabecalho = f"{nome:<15} |   {lista_ord}   | {comp:>5} -> Comp | {tempo:>5.3f}ms"
                linha = "=" * (len(cabecalho))
                arq.write(linha + "\n")
                arq.write(cabecalho + "\n")
            arq.write(linha + "\n")

        print(f"\033[1;92mSUCESSO\033[1;30m\nResultados salvos em '{arq_saida}'.\033[m")

    except Exception as e:
        print(f"\033[1;91mERRO\033[1;30m\n{e}\033[m")


# Algoritmos de Ordenação

def bubble_sort(lista:list, modo:bool=True) -> int:
    """Algoritmo de ordenação por bolha

    Args:
        lista (list): lista a ser ordenada
        modo (bool, opcional): crescente = True | decrescente = False. True por padrão.
    Returns:
        int: numero de comparações feitas 
    """
    i = 0
    j = len(lista)-1
    troca = True
    comps = 0

    while troca:
        troca = False
        while i < j:
            comps+=1
            if not modo:
                if lista[i] < lista[i+1]:
                    lista[i], lista[i+1] = lista[i+1], lista[i]
                    troca = True
            else:
                if lista[i] > lista[i+1]:
                    lista[i], lista[i+1] = lista[i+1], lista[i]
                    troca = True
            i+=1
        i=0
        j-=1
    return comps

def selection_sort(lista:list, modo:bool=True) -> int:
    """Algoritmo de ordenação por seleção

    Args:
        lista (list): lista a ser ordenada
        modo (bool, opcional): crescente = True | decrescente = False. True por padrão.
    Returns:
        int: numero de comparações feitas
    """
    size = len(lista)
    comps = 0
    
    for i in range(0, size-1):
        aux = i # menor ou maior (indice)
        for j in range(i+1, size):
            comps+=1
            if modo:
                if lista[j] < lista[aux]: aux = j
            else:
                if lista[j] > lista[aux]: aux = j
                
        lista[i], lista[aux] = lista[aux], lista[i]
    
    return comps

def insertion_sort(lista:list, modo:bool=True) -> int:
    """Algoritmo de ordenação por inserção

    Args:
        lista (list): lista a ser ordenada
        modo (bool, opcional): crescente = True | decrescente = False. True por padrão.
    Returns:
        int: numero de comparações feitas
    """
    size = len(lista)
    comps = 0
    
    for i in range(1, size):
        aux = lista[i]
        k = i-1

        if modo:
            while k >= 0:
                comps += 1
                if not (aux < lista[k]):
                    break
                lista[k+1] = lista[k]
                k -= 1
        else:
            while k >= 0:
                comps += 1
                if not (aux > lista[k]):
                    break
                lista[k+1] = lista[k]
                k -= 1

        lista[k+1] = aux

    return comps

# Algoritmos de Ordenação Recursivos

def merge_sort(lista:list, inicio:int, fim:int, modo:bool=True) -> int:
    """Algoritmo de ordenação por mistura

    Args:
        lista (list): lista a ser ordenada
        inicio (int): indice inicial
        fim (int): indice final
        modo (bool, opcional): crescente = True | decrescente = False. True por padrão.
    Returns:
        int: numero de comparações feitas
    """
    comps = 0
    if inicio < fim:
        meio = (inicio + fim)//2
        
        comps += merge_sort(lista, inicio, meio, modo)
        comps += merge_sort(lista, meio+1, fim, modo)
        
        comps += merge(lista, inicio, meio, fim, modo)

    return comps

def merge(vetor:list, inicio:int, meio:int, fim:int, modo:bool) -> int:
    """Auxiliar do merge_sort

    Args:
        vetor (list): lista pra dividir e conquistar
        inicio (int): indice inicial
        meio (int): indice do meio
        fim (int): indice final
        modo (bool): herda o modo da merge_sort.
    Returns:
        int: numero de comparações feitas 
    """
    v_aux = []
    p1 = inicio
    p2 = meio+1
    comps = 0
    
    # definindo uma função lambda pra comparação dependendo do modo
    compara = lambda x,y: x < y if modo else x > y
    
    while (p1 <= meio) and (p2 <= fim):
        comps+=1
        if compara(vetor[p1], vetor[p2]):
            v_aux.append(vetor[p1])
            p1+=1
        else:
            v_aux.append(vetor[p2])
            p2+=1

    while p1 <= meio:
        v_aux.append(vetor[p1])
        p1 += 1
    
    while p2 <= fim:
        v_aux.append(vetor[p2])
        p2 += 1

    # copiando os valores do v_aux de volta para vetor
    for idx, val in enumerate(v_aux):
        vetor[inicio + idx] = val
    
    return comps


def quick_sort(lista:list, inicio:int, fim:int, modo:bool=True) -> int:
    """Algoritmo de ordenação rápida (pivotamento)

    Args:
        lista (list): lista a ser ordenada
        inicio (int): indice inicial
        fim (int): indice final
        modo (bool, opcional): crescente = True | decrescente = False. True por padrão.
    Returns:
        int: numero de comparações feitas
    """
    comps = 0
    if inicio < fim:
        pivo, comparacoes = particiona(lista, inicio, fim, modo) # pivo para separar os dados
        comps += comparacoes
        comps += quick_sort(lista, inicio, pivo-1, modo) # subparte da esquerda
        comps += quick_sort(lista, pivo+1, fim, modo) # subparte da direita

    return comps

def particiona(lista, inicio, fim, modo=True) -> tuple:
    """Auxiliar do quick_sort

    Args:
        vetor (list): lista pra dividir e conquistar
        inicio (int): indice inicial
        fim (int): indice final
        modo (bool): herda o modo da quick_sort.
    Returns:
        tuple: (indice do pivo, numero de comparações)
    """
    esquerda = inicio
    direita = fim
    pivo = lista[inicio]
    comps = 0

    while esquerda < direita:
        if modo:
            while esquerda <= fim and lista[esquerda] <= pivo:
                comps+=1
                esquerda += 1
            while direita > inicio and lista[direita] > pivo:
                comps+=1
                direita -= 1
        else:
            while esquerda <= direita and lista[esquerda] >= pivo:
                comps+=1
                esquerda += 1
            while direita >= esquerda and lista[direita] < pivo:
                comps+=1
                direita -= 1

        if esquerda > direita:
            break
        
        lista[esquerda], lista[direita] = lista[direita], lista[esquerda]

    lista[inicio], lista[direita] = lista[direita], lista[inicio]
    
    return direita, comps


def heap_sort(lista:list, modo:bool=True) -> int:
    """Algoritmo de ordenação por heap\n
    Ordena o heap usando heap auxiliar.\n
    1 -> 2,3\n
    2 -> 4,5\n
    i -> 2i, 2i+1

    Args:
        lista (list): lista a ser ordenada
        modo (bool, opcional): crescente = True | decrescente = False. True por padrão.
    Returns:
        int: numero de comparações feitas
    """
    comps = build_max_heap(lista, modo)
    
    tamanho_heap = len(lista)

    for i in range(len(lista)-1, 0, -1):
        # removendo o elemento da primeira posição
        lista[0], lista[i] = lista[i], lista[0]
        tamanho_heap-=1
        
        # reconstruindo o heap
        comps += max_heapify(lista, 0, tamanho_heap, modo)

    return comps

def max_heapify(lista:list, inicio:int, tamanho_heap:int, modo:bool) -> int:
    """Auxiliar do heap_sort\n
    Mantém a propriedade do heap

    Args:
        lista (list): heap a ser mantido
        inicio (int): indice inicial
        tamanho_heap (int): autoexplicativo
        modo (bool): herda do heap_sort.
    Returns:
        int: numero de comparações feitas
    """
    e = 2*inicio + 1 # esquerda
    d = 2*inicio + 2 # direita
    maior = inicio
    comps = 0

    if(modo):
        # determinando qual filho é maior (r ou l)
        if (e < tamanho_heap) and (lista[e] > lista[maior]):
            comps+=1
            maior = e
        if (d < tamanho_heap) and (lista[d] > lista[maior]):
            comps+=1
            maior = d
    else:
        # determinando qual filho é menor (r ou l)
        if (e < tamanho_heap) and (lista[e] < lista[maior]):
            comps+=1
            maior = e
        if (d < tamanho_heap) and (lista[d] < lista[maior]):
            comps+=1
            maior = d
        
    if maior != inicio:
        lista[inicio], lista[maior] = lista[maior], lista[inicio]
        comps += max_heapify(lista, maior, tamanho_heap, modo)

    return comps

def build_max_heap(lista:list, modo:bool) -> int:
    """Auxiliar do heap_sort\n
    Constrói o heap inicial

    Args:
        lista (list): heap a ser construído
        modo (bool): herda do heap_sort.
    Returns:
        int: numero de comparações feitas
    """
    tamanho = len(lista)
    comps = 0

    # criando um heap de máximo "de baixo pra cima"
    for i in range((tamanho//2)-1, -1, -1):
        comps += max_heapify(lista, i, tamanho, modo)
    
    return comps

# Algoritmo Extra [Radix sort]

def radix_sort(lista, mode=True) -> int:
    """Algoritmo de ordenação Radix Sort

    Args:
        lista (list): Lista de números inteiros a ser ordenada
        mode (bool, opcional): Ignorado neste algoritmo. Mantido para compatibilidade
    Returns:
        int: Retorna 0, pois o Radix Sort não realiza comparações diretas entre elementos
    """

    # maior numero da lista para saber qnts digitos precisa
    maximo = max(lista) 

    # inicia expoente na casa da unidade
    exp = 1

    # continua enquanto tievr digitos a serem processados
    while maximo // exp > 0:         # para apos o mais signif do max
        ordenacao_por_contagem(lista, exp)
        # multiplica expoente por 10 -> passa pra proxima unidade
        exp *= 10

    return 0    # não faz comparações

def ordenacao_por_contagem(lista, exp) -> None:
    """Auxiliar do Radix Sort: ordenação por contagem de dígitos

    Args:
        lista (list): Lista de números inteiros a ser ordenada parcialmente
        exp (int): Expoente que indica a casa decimal atual (unidade, dezena, centena, etc.)
    """

    n = len(lista)

    # criando lista de saída temporária com o mesmo tamanho da original.
    saida = [0] * n

    # criando lista de ocorrencia de (0 - 9)
    contagem = [0] * 10

    # percorrendo a lista e conta a ocorrência de cada dígito 
    for i in range(n):
        indice = (lista[i] // exp)          # descarta os digitos na direta do exp
        contagem[int(indice % 10)] += 1     # pega o resto da divisao (% 10) para pegar o digito a direita

    # contagem vai ser uma lista que cada posição tem o digito final dele
    # a partir do segundo elemento, cada um é a soma dele e o anterior 
    for i in range(1, 10):
        contagem[i] += contagem[i-1]
    
    # percorrendo a lista de entrada de tras pra frente para manter a estabilidade
    i = n - 1
    while i >= 0:
        indice = (lista[i] // exp)
        # colocando o numero na posição correta na saida
        saida[contagem[int(indice % 10)] - 1] = lista[i]
        # decrementando contagem para o próximo número com o mesmo dígito
        contagem[int(indice % 10)] -= 1
        i -= 1

    # copiando a lista de saida para a lista original
    for i in range(n):
        lista[i] = saida[i]

if __name__ == "__main__":
    main()
