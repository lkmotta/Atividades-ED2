"""
Atividade Prática 03 - Remoção & Storage Compaction - Estrutura de Dados 2

Acadêmicos:
    Gabriel Mancuso Bonfim  (2669498)
    Lucas Henrique Motta    (2669730)

Orientador:
    Prof. Dr. Rafael Gomes Mantovani
"""

from os import path

"""
1) Implemente uma função que realiza a remoção de registros em um arquivo de tamanho fixo.
Use os registros de Animes das aulas passadas.
"""
def removeRegistro(arquivo, chave:str) -> bool:
    """
    Remove um registro marcando o registro inválido por *| no início da linha.

    Args:
        arquivo (str): Caminho do arquivo.
        chave (str): Chave do registro a ser removido.
    """
    removeu = False
    try:
        with open(arquivo, "r") as arq:
            linhas = arq.readlines()
        
        with open(arquivo, "w") as arq:
            for linha in linhas:
                if linha.startswith(chave):
                    arq.write("*|" + linha[2:]) # marca com * e delimita campo, depois reescreve o resto da linha
                    removeu = True
                else:
                    arq.write(linha)
        return removeu
    except Exception as erro:
        print(f"Erro ao remover registro: {erro}")
        return False

"""
2) Implemente uma função que realize o processo de Compactação de
Dados (Storage Compaction) de um arquivo. Além disso, elabore uma
função principal para testar as suas funções de remoção de registros e
compactação de dados.
"""
def compactacaoDados(arquivo) -> None:
    """
    Faz a compactação de dados (Storage Compaction) de um arquivo.

    Args:
        arquivo (str): Arquivo a ser compactado
    """
    try:
        with open(arquivo, "r") as arq:
            linhas = arq.readlines()

        # renomeando o novo arquivo (à compactar) para comparar
        base, extensao = path.splitext(arquivo)
        nome_novo_arquivo = f"{base}-compactado{extensao}"
        
        with open(nome_novo_arquivo, "w") as arq:
            for linha in linhas:
                if linha.startswith("*"):
                    continue
                else:
                    arq.write(linha)

        print(f"\nArquivo '{arquivo}' compactado com sucesso!")
        return
    except Exception as erro:
        print(f"Erro ao compactar arquivo: {erro}")

def main():
    arquivo = input("Insira o caminho do arquivo: ").strip()
    chave = input("Insira a chave do registro a ser removido: ").strip()
    if removeRegistro(arquivo, chave):
        print(f"Registro com chave '{chave}' removido.") 
        compactacaoDados(arquivo)
    else:
        print(f"Registro com chave '{chave}' não encontrado.")

if __name__ == "__main__":
    main()