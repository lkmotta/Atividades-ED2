"""
Atividade Prática 02 - Busca Sequencial e Acesso Direto (Função grep) - Estrutura de Dados 2

Acadêmicos:
    Gabriel Mancuso Bonfim  (2669498)
    Lucas Henrique Motta    (2669730)

Orientador:
    Prof. Dr. Rafael Gomes Mantovani
"""

def grep(arquivo, string:str) -> tuple:
    """
    1. Implemente uma função que simula o comando grep do Unix.
    
    Args:
        arquivo: um arquivo texto com registros codificados usando \\n como delimitador de de registros,
        e | como delimitador de campos;
        string: uma string de consulta que deseja-se verificar sua existência e ocorrências no arquivo;
    
    Returns:
        tuple: Um tupla contendo todos os registros onde a informação foi encontrada no arquivo texto.
    """
    registros = ()
    try:
        with open(arquivo, "r", encoding="utf-8") as arq:
            for linha in arq.readlines():
                if string in linha:
                    registros += (linha.strip(),)
    except FileNotFoundError:
        print(f"Arquivo {arquivo} não encontrado.")
        exit(1)

    return registros

def main():
    arquivo = input("Insira o caminho do arquivo: ").strip()
    string = input("Insira a string a ser buscada: ").strip()
    
    resultado = grep(arquivo, string)
    print(f"A string '{string}' foi encontrada {len(resultado)} vezes nos registros:")
    for reg in resultado:
        print(reg)

if __name__ == "__main__": 
    main()