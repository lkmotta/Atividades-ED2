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
    2. Crie uma nova função baseada no exercício anterior e retorne agora todos os
    registros e índices das linhas onde existe a string consultada
    
    Args:
        arquivo: O caminho do arquivo a ser lido. Possui os registros codificados usando \\n como delimitador de registros, e | como delimitador de campos.
        string: A string a ser buscada para contar ocorrências no arquivo.
    
    Returns:
        tuple: Uma tupla contendo duas tuplas:
            - tuple[int]: Índices das linhas onde a string foi encontrada.
            - tuple[str]: Registros (linhas) onde a string foi encontrada.
    """
    posicoes, registros = (),()
    
    try:
        with open(arquivo, "r", encoding="utf-8") as arq:
            for pos, linha in enumerate(arq):
                if string in linha:
                    registros += (linha.strip(), )
                    posicoes += (pos, )
    except FileNotFoundError:
        print(f"Arquivo {arquivo} não encontrado.")
        exit(1)

    return (posicoes, registros)
    
def main():
    arquivo = input("Insira o caminho do arquivo: ").strip()
    string = input("Insira a string a ser buscada: ").strip()

    resultado = grep(arquivo, string)
    print(f"A string '{string}' foi encontrada em:\n")
    for i in range(len(resultado[0])):
        print(f"Linha {resultado[0][i]}: {resultado[1][i]}")

if __name__ == "__main__": 
    main()