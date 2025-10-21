"""
Atividade Prática 04 - Remoção & Inserção com Reuso - Estrutura de Dados 2

Acadêmico:
    Lucas Henrique Motta (2669730)

Orientador:
    Prof. Dr. Rafael Gomes Mantovani
"""

def le_header(arquivo) -> dict:
    """
    Lê o cabeçalho do arquivo e retorna um dicionário com os metadados.
    
    Args:
        arquivo (str): caminho para o arquivo com estrutura de cabeçalhos (metadados)
    Returns:
        dict: dicionário com os valores do cabeçalho
    """
    try:
        with open(arquivo, 'r') as arq:
            header = arq.readline().strip()
            header_dicionario = {}
            chaves_aceitas = ['tam', 'cont', 'recente']
            
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
        print(f"Erro ao ler cabeçalho: {erro}")
        return {}
    

def atualiza_header(arquivo, header_atualizado:dict) -> bool:
    """
    Faz a nova linha de header com base no header atualizado.
    
    Args:
        arquivo (str): caminho para o arquivo com estrutura de cabeçalhos (metadados)
        header_atualizado (dict): dicionário com os novos valores do header
    """
    try:
        with open(arquivo, "r") as arq:
            linhas = arq.readlines()

        header_linha = str()
        for chave, valor in header_atualizado.items():
            header_linha += f"{chave}={valor}|"

        header_linha = header_linha.rstrip('|') # removendo o ultimo '|'
        
        linhas[0] = header_linha + '\n'

        with open(arquivo, "r+") as arq:
            arq.writelines(linhas)
        
        return True
    except Exception as erro:
        print(f"Erro ao atualizar header: {erro}")
        return False


def remocaoComReuso(arquivo, chave) -> bool:
    """
    Remove o registro marcando-o como inválido e atualiza o header.

    Args;
        arquivo (str): caminho para o arquivo com estrutura de cabeçalhos (metadados)
        chave (str): chave do registro a ser removido
    """
    removeu = True

    # extraindo header do arquivo
    header = le_header(arquivo)
    if(header == {}):
        print(f"\nERRO: Arquivo '{arquivo}' não possui header ou é inválido.")
        return False

    try:
        with open(arquivo, "r+") as arq:
            linhas = arq.readlines()
            arq.seek(0) # voltando ao inicio do arquivo

            for pos, linha in enumerate(linhas):
                if linha.startswith(chave):
                    # invalida registro com *, marca o recente (pilha lógica) e delimita campo, depois reescreve o resto da linha
                    arq.write(f"*{header['recente']}|{linha[len(str(header['recente'])) + 2:]}") # +2 por causa do '*' e '|'
                    header['recente'] = pos
                    header['cont'] -= 1
                    removeu = True
                else:
                    arq.write(linha)

        if not atualiza_header(arquivo, header): print("\nDeu ruim ao atualizar header!")
            
        return removeu
    except Exception as erro:
        print(f"Erro ao remover registro: {erro}")
        return False


def insercaoComReuso(arquivo, registro) -> bool:
    """
    Insere um registro em um arquivo de metadados (estrutura de cabeçalho) com reuso em pilha lógica.

    Args;
        arquivo (str): caminho para o arquivo com estrutura de cabeçalho (metadados)
        registro (str): registro a ser inserido com reuso
    """
    header = le_header(arquivo)
    if(header == {}):
        print(f"\nERRO: Arquivo '{arquivo}' não possui header ou é inválido.")
        return False
    
    # verificando se a chave do registro ja está no arquivo
    try:
        campos_registro = registro.split('|')
        chave_registro = campos_registro[0]   # primeiro campo é a chave
        with open(arquivo, "r") as arq:
            for linha in arq.readlines():
                if linha.startswith(chave_registro):
                    print("\nChave do registro ({chave}) já existe no arquivo.")
                    return False

    except Exception as erro:
        print(f"\nERRO (extraindo chave do registro): {erro}")
        return False
    
    # caso a chave não exista no arquivo, vamos inserir o registro
    try:
        """
        - verificar se header['recentes'] é -1
            -> caso seja, vamos inserir por append
        - se não for:
            -> iniciar pilha lógica pelo header:
                ~ verificar qual é o recente, e pegar o registro dele;
                ~ verificar qual é o proximo RRN invalidado no registro e atualizar header;
                ~ inserir registro nesta linha.
            
        - atualizar header
        fim
        """
        if header['recente'] == -1:
            # inserir registro por append (final do arquivo)
            with open(arquivo, "a") as arq:
                arq.write(registro + '\n')
                header['cont'] += 1
        else:
            with open(arquivo, "r+") as arq:
                linhas = arq.readlines();
                pos_insercao = header['recente']
                linha_invalida = linhas[pos_insercao]

                # verificando se realmente o registro está invalidado
                if linha_invalida.startswith('*'):
                    # extraindo o próximo recente do registro inválido
                    campos_invalido = linha_invalida[1:].split('|') # removendo o '*' e dividindo pelos campos
                    proximo_recente = int(campos_invalido[0]) # o próximo recente
                    header['recente'] = proximo_recente
                    header['cont'] += 1
                    linhas[pos_insercao] = registro + '\n' # reescrevendo registro

                else:
                    print(f"\nERRO: registro apontado no valor da chave 'recente' não está invalidado.")
                    return False

                # escrevendo mudanças
                arq.seek(0)
                arq.writelines(linhas)

        if not atualiza_header(arquivo, header): print("\nDeu ruim ao atualizar header!")
        return True
    
    except Exception as erro:
        print(f"\nErro ao inserir registro: {erro}")
        return False


def main():
    # testando
    arquivo = input("Insira o caminho do arquivo: ").strip()
    chave = input("Insira a chave do registro a ser removido: ").strip()
    
    if remocaoComReuso(arquivo, chave):
        print(f"Registro com chave '{chave}' removido.") 
    
    registro = input("Insira o registro a ser inserido: ").strip()
    if insercaoComReuso(arquivo, registro):
        print("Registro inserido com sucesso!")


if __name__ == "__main__":
    main()