""" 
Entregável 11 - Busca Binária em Arquivos - Estrutura de Dados 2
Acadêmico:
    Lucas Henrique Motta (2669730)
Orientador:
    Prof. Dr. Rafael Gomes Mantovani
"""

def numeroRegistros(arquivo) -> int:
    valor_registros = 0
    try:
        with open(arquivo, "r") as arq:
            linhas = arq.readlines()
        
        if not linhas: return 0
        
        for linha in linhas:
            if linha.strip(): valor_registros += 1
        
        return valor_registros
    except Exception as erro:
        print(f"\nErro ao extrair numero de registros: {erro}")
        return 0

def lerRegistroComRNN(arquivo, RNN) -> str:
    try:
        with open(arquivo, 'r') as arq:
            linhas = arq.readlines()
        
        return str(linhas[RNN])
    except IndexError:
        print(f"\nErro: RNN maior que o número de registros.")
        return None
    except Exception as erro:
        print(f"\nErro ler registro com RNN: {erro}")
        return None

def buscaBinaria(arq, chave : str, registro : str='') -> bool: 
    """ Função para busca binária em arquivos 
    Args:
        arq: arquivo com os registros já ordenados 
        chave: a chave do registro que procuramos
        registro: objeto para retornar o registro encontrado
    Returns:
        true: se encontrar o registro e salvar o conteúdo corretamente em reg 
        false: se não encontrar o registro, e der algum erro durante o processo de leitura 
    """  
    inicio = 0  
    fim = numeroRegistros(arq) - 1
    
    if fim < 0: return False
    
    while inicio <= fim:
        meio = (inicio + fim) // 2 
        registro = lerRegistroComRNN(arq, meio)
        if not registro: return False # deu erro na hora de ler o registro c/ rnn
        
        chave_atual = registro.split('|')[0]
        if chave_atual == chave:
            return True
        
        if chave_atual < chave: 
            inicio = meio + 1
            
        else: fim = meio - 1
        
    return False

def main() -> None:
    # testando
    arquivo = input("Insira o caminho do arquivo: ").strip()
    chave = input("Insira a chave a ser buscada: ").strip()
    encontrado = buscaBinaria(arquivo, chave)
    
    if encontrado: print(f"Registro encontrado.") 
    else: print("Registro não encontrado.")    

if __name__ == "__main__":
    main()