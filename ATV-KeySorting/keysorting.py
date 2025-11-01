""" 
Atividade Prática 2- Keysorting - Estrutura de Dados 2
Acadêmico:
    Lucas Henrique Motta (2669730)
Orientador:
    Prof. Dr. Rafael Gomes Mantovani
"""
from sys import argv

class Heroi:
    def __init__(
            self, key, Name, Alignment, Gender, EyeColor, Race, HairColor,
            Publisher, SkinColor, Height, Weight, Intelligence, Strength,
            Speed, Durability, Power, Combat, Total
        ):
        self.key = key
        self.Name = Name
        self.Alignment = Alignment
        self.Gender = Gender
        self.EyeColor = EyeColor
        self.Race = Race
        self.HairColor = HairColor
        self.Publisher = Publisher
        self.SkinColor = SkinColor
        self.Height = Height
        self.Weight = Weight
        self.Intelligence = Intelligence
        self.Strength = Strength
        self.Speed = Speed
        self.Durability = Durability
        self.Power = Power
        self.Combat = Combat
        self.Total = Total




def le_header(arquivo) -> dict:
    """
    Lê o cabeçalho do arquivo metadado e retorna um dicionário com os metadados.
    Metadados válidos:
    - SORT: {Q, M, H, I} (Quick, Merge, Heap, Insertion)
    - ORDER: {C, D} (Crescente, Decrescente)
    Args:
        arquivo (str): caminho para o arquivo com estrutura de cabeçalhos (metadados)
    Returns:
        dict: dicionário com os valores do cabeçalho
    """
    try:
        with open(arquivo, 'r') as arq:
            header = arq.readline().strip()
            header_dicionario = {}
            chaves_aceitas = ['SORT', 'ORDER']
            
            # dividndo a linha pelo delimitador |
            for item in header.split('|'):
                chave, valor = item.split('=') # chave fica com o valor antes de '=' e valor com o depois
                if chave in chaves_aceitas:
                    header_dicionario[chave] = int(valor) # registrando no dicionario a retornar
                else:
                    print(f"\nERRO: Chave inválida no header do arquivo encontrada: '{chave}'.")
                    return {}
            
            return header_dicionario
    except Exception as erro:
        print(f"Erro ao ler cabeçalho do arquivo metadado: {erro}")
        return {}


def keysorting(arquivo_entrada, arquivo_saida) -> None:
    try:
        # lendo header
        header = le_header(arquivo_entrada)
        if not header:
            print(f"\033[1;91mERRO\033[1;30m\nNão foi possível ler o cabeçalho do arquivo '{arquivo_entrada}'.\033[m")
            return
        
        with open(arquivo_entrada, 'r') as arq:
            linhas = arq.readlines()

        # verificando se o arquivo está vazio
        if not linhas.strip():
            print(f"\033[1;91mERRO\033[1;30m\nO arquivo '{arquivo_entrada}' está vazio.\033[m")
            return
            
        # verificando modos e algoritmo a ser usado
        algoritmo = header['SORT']
        modo = header['ORDER']

        if algoritmo not in ['Q', 'M', 'H', 'I']:
            print(f"\033[1;91mERRO\033[m: Algoritmo {algoritmo} não é válido. Use 'Q', 'M', 'H' ou 'I'.")
            return
        
        if modo not in ['C', 'D']:
            print(f"\033[1;91mERRO\033[m: Modo {modo} não é válido. Use 'C' ou 'D'.")
            return
        
        # lendo dados e criando o vetor de herois
        herois = []
        for pos, linha in enumerate(linhas):
            if pos == 0: continue
            
            if linha.strip() and len(linha.split('|')) == 17:
                herois.append(Heroi(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6], linha[7], linha[8], linha[9], linha[10], linha[11], linha[12], linha[13], linha[14], linha[15], linha[16]))
            else:
                print(f"Linha {pos} não possui 17 campos válidos.")
        

        # ... IMPLEMENTE O RESTO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    except Exception as erro:
        print(f"Erro ao ler arquivo de entrada: {erro}")



    """
    # escrevendo no arquivo de saida
        with open(arq_saida, "w") as arq:
            for nome, lista_ord, comp, tempo in resultados:
                cabecalho = f"{nome:<15} |   {lista_ord}   | {comp:>5} -> Comp | {tempo:>5.3f}ms"
                linha = "=" * (len(cabecalho))
                arq.write(linha + "\n")
                arq.write(cabecalho + "\n")
            arq.write(linha + "\n")
    """

def main():
    if len(argv) != 3:
        print("\033[1;91mERRO\033[1;30m\nO comando de execução deve ser\033[m: python main.py <arq_entrada> <arq_saida>")
        return

    arq_entrada = argv[1]
    arq_saida = argv[2]
    
    keysorting(arq_entrada, arq_saida)


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
            while k >= 0:
                if not (aux < lista[k]):
                    break
                lista[k+1] = lista[k]
                k -= 1
        else:
            while k >= 0:
                if not (aux > lista[k]):
                    break
                lista[k+1] = lista[k]
                k -= 1

        lista[k+1] = aux


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
    Returns:
        int: indice do pivo
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
    
    tamanho_heap = len(lista)

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