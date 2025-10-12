"""
Atividade Prática 02 - Busca Sequencial e Acesso Direto (Função grep) - Estrutura de Dados 2

Acadêmicos:
    Gabriel Mancuso Bonfim  (2669498)
    Lucas Henrique Motta    (2669730)

Orientador:
    Prof. Dr. Rafael Gomes Mantovani
"""
def readRecordByRRN(file, RNN:int) -> str:
    """
    3. Escreva uma função para leitura de registros de tamanho variável usando RRN (Relative Record Number - Número de Registro Relativo),
    que retorna um registro baseado em sua posição no arquivo. Por exemplo: se for solicitado para recuperar o 50º registro do arquivo,
    a função deve se deslocar por 49 registros e retornar/imprimir apenas o conteúdo do 50º registro.
    """
    if(RNN < 0):
        print("\nInsira um valor de RNN válido!")
        exit(1)
    try:
        # identificando o maior registro do dataset
        with open(file, "r", encoding="utf-8") as arq:
            maior_linha = max(arq.readlines(), key=len) # max com key=len retorna a maior linha
            maior = len(maior_linha) # len retorna o tamanho da maior linha
            
        # verificando se o RNN solicitado e maior que o maior RNN do dataset
        if(RNN > maior):
            print("\nO RNN solicitado e maior que o maior RNN do dataset.")
            exit(1)

        with open(file, "r", encoding="utf-8") as arq:
            for pos, linha in enumerate(arq):
                if(pos == RNN):
                    if(len(linha) < maior):
                        linha = linha.strip() + "*" * (maior - len(linha))
                    return linha.strip()
            
    except FileNotFoundError:
        print(f"Arquivo {file} não encontrado.")
        exit(1)

def main() -> None:
    arquivo = input("Insira o caminho do arquivo: ").strip()
    RNN = int(input("Insira o RNN do registro a ser lido: ").strip())
    registro = readRecordByRRN(arquivo, RNN)
    print(f"Registro {RNN}: {registro}")

if __name__ == "__main__":
    main()