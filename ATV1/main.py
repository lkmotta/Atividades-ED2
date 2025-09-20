import sys
from time import time
from random import randint as rdi

def main():
    if len(sys.argv) != 3:
        print("\033[1;91mERRO\033[1;30m\nO comando de execução deve ser\033[m: python main.py <arq_entrada> <arq_saida>")
        return

    arq_input = sys.argv[1]
    arq_output = sys.argv[2]

    try:
        with open(arq_input, 'r') as arq:
            data = arq.read()

        # verificando se o arquivo está vazio
        if not data.strip():
            print(f"\033[1;91mERRO\033[1;30m\nO arquivo '{arq_input}' está vazio.\033[m")
            return
        
        # verificando se a primeira linha contém um número válido
        linhas = data.splitlines()
        if(not linhas[0].isdigit()):
            print(f"\033[1;91mERRO\033[1;30m\nA primeira linha do arquivo '{arq_input}' deve conter um número inteiro válido.\033[m")
            return
        
        n = int(linhas[0])
        if n <= 0:
            print(f"\033[1;91mERRO\033[1;30m\nO número de elementos deve ser maior que zero.\033[m")
            return
        
        # lendo a letra do modo
        if len(linhas) < 2:
            print(f"\033[1;91mERRO\033[1;30m\nA segunda linha do arquivo '{arq_input}' deve conter uma letra válida: C, D ou R.\033[m")
            return
        
        letra_modo = linhas[1].strip().upper()
            
        # gerando a lista de números
        if letra_modo in ['C', 'c']:
            lista = list(range(1, n+1))
        elif letra_modo in ['D', 'd']:
            lista = list(range(n, 0, -1))
        elif letra_modo in ['R', 'r']:
            lista = [rdi(0, 32000) for _ in range(n)] # _ é uma variável descartável
        else:
            print(f"\033[1;91mERRO\033[1;30m\nA segunda linha do arquivo '{arq_input}' deve conter uma letra válida: C, D ou R.\033[m")
            return
        
        print(f"\nLista inicial ({letra_modo}): {lista}\n")

        with open(arq_output, 'w') as outfile:
            outfile.write(lista.__str__() + '\n')

    except Exception as e:
        print(f"\033[1;91mERRO\033[1;30m\n{e}\033[m")


# Algoritmos de Ordenação

def bubble_sort(lista:list, modo:bool=True) -> None:
    """Algoritmo de ordenação por bolha

    Args:
        lista (list): lista a ser ordenada
        modo (bool, opcional): crescente = True | decrescente = False. True por padrão.
    """
    i = 0
    j = len(lista)-1
    troca = True

    while troca:
        troca = False
        while i < j:
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

def selection_sort(lista:list, modo:bool=True) -> None:
    """Algoritmo de ordenação por seleção

    Args:
        lista (list): lista a ser ordenada
        modo (bool, opcional): crescente = True | decrescente = False. True por padrão.
    """
    size = len(lista)
    
    for i in range(0, size-1):
        aux = i # menor ou maior (indice)
        for j in range(i+1, size):
            if modo:
                if lista[j] < lista[aux]: aux = j
            else:
                if lista[j] > lista[aux]: aux = j
                
        lista[i], lista[aux] = lista[aux], lista[i]

def insertion_sort(lista:list, modo:bool=True) -> None:
    """Algoritmo de ordenação por inserção

    Args:
        lista (list): lista a ser ordenada
        modo (bool, opcional): crescente = True | decrescente = False. True por padrão.
    """
    size = len(lista)
    
    for i in range(1, size):
        aux = lista[i]
        k = i-1

        if modo:
            while (k >= 0) and (aux < lista[k]):
                lista[k+1] = lista[k]
                k-=1
        else:
            while (k >= 0) and (aux > lista[k]):
                lista[k+1] = lista[k]
                k-=1

        lista[k+1] = aux

# Algoritmos de Ordenação recursivos

def merge_sort(lista:list, inicio:int, fim:int, modo:bool=True) -> None:
    """Algoritmo de ordenação por mistura

    Args:
        lista (list): lista a ser ordenada
        inicio (int): indice inicial
        fim (int): indice final
        modo (bool, opcional): crescente = True | decrescente = False. True por padrão.
    """
    if inicio < fim:
        meio = (inicio + fim)//2
        
        merge_sort(lista, inicio, meio, modo)
        merge_sort(lista, meio+1, fim, modo)
        
        merge(lista, inicio, meio, fim, modo)

def merge(vetor:list, inicio:int, meio:int, fim:int, modo:bool) -> None:
    """Auxiliar do merge_sort

    Args:
        vetor (list): lista pra dividir e conquistar
        inicio (int): indice inicial
        meio (int): indice do meio
        fim (int): indice final
        modo (bool): herda o modo da merge_sort.
    """
    v_aux = []
    p1 = inicio
    p2 = meio+1
    
    # definindo uma função lambda pra comparação dependendo do modo
    compara = lambda x,y: x < y if modo else x > y
    
    while (p1 <= meio) and (p2 <= fim):
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


def quick_sort(lista:list, inicio:int, fim:int, modo:bool=True) -> None:
    """Algoritmo de ordenação rápida (pivotamento)

    Args:
        lista (list): lista a ser ordenada
        inicio (int): indice inicial
        fim (int): indice final
        modo (bool, opcional): crescente = True | decrescente = False. True por padrão.
    """
    if inicio < fim:
        pivo = particiona(lista, inicio, fim, modo) # pivo para separar os dados
        quick_sort(lista, inicio, pivo-1, modo) # subparte da esquerda
        quick_sort(lista, pivo+1, fim, modo) # subparte da direita

def particiona(lista, inicio, fim, modo=True) -> int:
    """Auxiliar do quick_sort

    Args:
        vetor (list): lista pra dividir e conquistar
        inicio (int): indice inicial
        fim (int): indice final
        modo (bool): herda o modo da quick_sort.
    """
    esquerda = inicio
    direita = fim
    pivo = lista[inicio]

    while esquerda < direita:
        if modo:
            while esquerda <= fim and lista[esquerda] <= pivo:
                esquerda += 1
            while direita > inicio and lista[direita] > pivo:
                direita -= 1
        else:
            while esquerda <= direita and lista[esquerda] >= pivo:
                esquerda += 1
            while direita >= esquerda and lista[direita] < pivo:
                direita -= 1

        if esquerda > direita:
            break
        
        lista[esquerda], lista[direita] = lista[direita], lista[esquerda]

    lista[inicio], lista[direita] = lista[direita], lista[inicio]
    return direita


def heap_sort(lista:list, modo:bool=True) -> None:
    """Algoritmo de ordenação por heap\n
    Ordena o heap usando heap auxiliar.\n
    1 -> 2,3\n
    2 -> 4,5\n
    i -> 2i, 2i+1

    Args:
        lista (list): lista a ser ordenada
        modo (bool, opcional): crescente = True | decrescente = False. True por padrão.
    """
    build_max_heap(lista, modo)
    
    tamanho_heap = len(lista)-1

    for i in range(len(lista)-1, 0, -1):
        # removendo o elemento da primeira posição
        lista[0], lista[i] = lista[i], lista[0]
        tamanho_heap-=1
        
        # reconstruindo o heap
        max_heapify(lista, 0, tamanho_heap, modo)

def max_heapify(lista:list, inicio:int, tamanho_heap:int, modo:bool) -> None:
    """Auxiliar do heap_sort\n
    Mantém a propriedade do heap

    Args:
        lista (list): heap a ser mantido
        inicio (int): indice inicial
        tamanho_heap (int): autoexplicativo
        modo (bool): herda do heap_sort.
    """
    e = 2*inicio + 1 # esquerda
    d = 2*inicio + 2 # direita
    maior = inicio
    
    if(modo):
        # determinando qual filho é maior (r ou l)
        if (e < tamanho_heap) and (lista[e] > lista[maior]):
            maior = e
        if (d < tamanho_heap) and (lista[d] > lista[maior]):
            maior = d
    else:
        # determinando qual filho é menor (r ou l)
        if (e < tamanho_heap) and (lista[e] < lista[maior]):
            maior = e
        if (d < tamanho_heap) and (lista[d] < lista[maior]):
            maior = d
        
    if maior != inicio:
        lista[inicio], lista[maior] = lista[maior], lista[inicio]
        max_heapify(lista, maior, tamanho_heap, modo)

def build_max_heap(lista:list, modo:bool) -> None:
    """Auxiliar do heap_sort\n
    Constrói o heap inicial

    Args:
        lista (list): heap a ser construído
        modo (bool): herda do heap_sort.
    """
    tamanho = len(lista)

    # criando um heap de máximo "de baixo pra cima"
    for i in range((tamanho//2)-1, -1, -1):
        max_heapify(lista, i, tamanho, modo)


if __name__ == "__main__":
    main()