"""
Entregável 13 - Indice Primário: Inserção, Remoção e Destrutor - Estrutura de Dados II
Acadêmicos:
    Lucas Henrique Motta
    Gabriel Mancuso Bonfim
Orientador:
    Prof. Dr. Rafael Gomes Mantovani
"""
import os

class Indice_primario:
    arq_dados = None
    arq_ind = None
    array_indices = [] # guarda as tuplas de (chave, rrn)
    rrns_reutilizaveis = [] 

    # construtor
    def __init__(self, arquivo_dados, arquivo_indices):
        self.arq_dados = open(arquivo_dados, 'r+')
        self.array_indices = []      
        self.nome_arq_dados = arquivo_dados                                            

        if os.path.isfile(arquivo_indices):
            print("\narquivo já existe\n")
            # ler o arquivo de índices (não abrir em 'w' antes)
            with open(arquivo_indices, 'r') as arq:
                for linhas in arq:
                    partes = linhas.strip().split()  # separa por espaço/whitespace
                    if not partes:
                        continue
                    chave = partes[0]
                    RRN = int(partes[1]) if len(partes) > 1 else 0
                    self.array_indices.append((chave, RRN))
            self.ordena_indices()
        else:
            print("\narquivo não existe\n")
            registros = self.arq_dados.readlines()
            if len(registros) > 0:
                registros_dados = registros[1:] # Ignora header na indexacao
            else:
                registros_dados = []
            rrn = 0
            for reg in registros_dados:
                chave = self.cria_chave(reg) # cria chave canonica
                self.array_indices.append((chave, rrn)) # insere no vetor de tuplas
                rrn += 1
            
            self.ordena_indices() # depois de inserir tudo, ordena pra pesquisa
        
        with open(arquivo_indices, 'w') as self.arq_ind:
            for indice in self.array_indices:
                self.arq_ind.write(f'{indice[0]} {indice[1]}\n') # escreve/atualiza no arquivo

            print(f'Arquivo de indices "{arquivo_indices}" criado/atualizado com sucesso!')

    # destrutor
    def __del__(self):
        # se mecheu no arquivo
        if self.arq_ind:
            # arq_ind lembra o nome do arquivo msm fechado
            nome_do_arquivo = self.arq_ind.name 
            
            # salvar
            with open(nome_do_arquivo, 'w') as arq:
                for chave, rrn in self.array_indices:
                    arq.write(f"{chave} {rrn}\n")
            print("Indices salvos com sucesso!")
        

    def ordena_indices(self):
        self.array_indices.sort(key = lambda tupla: tupla[0]) # genial isso aqui bicho


    def cria_chave(self, reg):
        campos = reg.split("|")
         # upper pra evitar case sensitive e tira espacos unindo tudo
        chave = campos[0].strip().upper().replace(' ', '')
        return chave


    def busca_binaria(self, chave):
        """
        Busca binária (vetor de indices já ordenado)
        Args:
            chave (str): chave canonica

        Returns:
            (Achou/NãoAchou, RRN)
        """
        # busca tendo em vista que o vetor tá ordenado
        # divide no meio, pega o valor do meio e verifica se =, > ou <
        inicio, fim = 0, len(self.array_indices) - 1
        while(inicio <= fim):
            meio = (inicio + fim)//2
            meio_tupla = self.array_indices[meio]

            if(meio_tupla[0] == chave):
                rrn = meio_tupla[1]
                return (True, meio, rrn)
            elif(chave < meio_tupla[0]):
                fim = meio - 1
            else:
                inicio = meio + 1

        return (False, None, None)


    def pesquisa(self, chave:str) -> tuple:
        """
        Pesquisa no vetor de indices a chave canonica.

        Args:
            chave (str): chave canonica

        Returns:
            (achou/n achou, idTabela, idArquivo/RRN)
        """
        resultado = self.busca_binaria(chave)
        return resultado
    
    def remocao(self, chave:str) -> bool:
        # verificar se chave existe na tabela
        achou, indice_tabela, rrn = self.pesquisa(chave)

        # se não achou, finaliza
        if not achou:
            print(f"[AVISO] Chave '{chave}' não encontrada para remoção.")
            return False
        
        # achou: [True, RRN]
        # -> invalidar usando reuso e deslocar no arquivo
        self.arq_dados.seek(0)
        linhas = self.arq_dados.readlines()

        if not linhas:
            return False

        # ler Header atual 
        partes_header = linhas[0].strip().split()
        size_atual = int(partes_header[0].split('=')[1])
        n_atual = int(partes_header[1].split('=')[1])
        recente_atual = int(partes_header[2].split('=')[1])

        # +1 pelo cabecalho
        indice_linha_arquivo = rrn + 1

        conteudo_original = linhas[indice_linha_arquivo].strip()
        
        # -> Invalidar registro e att a pilha
        novo_conteudo = f"*|{recente_atual}|{conteudo_original}\n"
        
        # att o size
        if len(novo_conteudo) - 1 > size_atual: # -1 por conta do \n
            size_atual = len(novo_conteudo) - 1

        # att a linha no buffer
        linhas[indice_linha_arquivo] = novo_conteudo

        # -> decrementar Contadores e att recente
        n_atual -= 1
        novo_topo_pilha = rrn 
        
        # att a linha do cabecalho
        linhas[0] = f"SIZE={size_atual} N={n_atual} RECENTE={novo_topo_pilha}\n"

        # reescreve o arquivo atualizado
        self.arq_dados.seek(0)
        self.arq_dados.writelines(linhas)
        self.arq_dados.truncate() # limpeza se diminuir

        # -> remover da tabela lista de indices o registro (chave, RRN)
        self.array_indices.pop(indice_tabela)

        print(f"[INFO] Registro '{chave}' removido com sucesso (RRN: {rrn}).")
        return True

    def insercao(self, reg:str) -> bool:
        # criar chave Canônica do Registro
        chave = self.cria_chave(reg)

        # pesquisar se chave existe na tabela:
        achou, _, _ = self.pesquisa(chave)

        # se achou: não faz nada
        if achou:
            print(f"[ERRO] Chave '{chave}' já existe.")
            return False
        
        # se não achou:
        self.arq_dados.seek(0)
        linhas = self.arq_dados.readlines()
        if not linhas: 
            return False

        # ler Header
        partes_header = linhas[0].strip().split()
        size = int(partes_header[0].split('=')[1])
        n = int(partes_header[1].split('=')[1])
        recente = int(partes_header[2].split('=')[1])

        rrn_final = -1

        # verificar no Header se existe posição para reuso
        if recente != -1:
            # insere na posição do recente
            rrn_final = recente
            indice_linha = rrn_final + 1 # compensa header

            # pega o proximo da pilha
            linha_reuso = linhas[indice_linha]
            partes_reuso = linha_reuso.split("|")
            
            # segundo campo é o proximo da pilha
            proximo_recente = int(partes_reuso[1])

            # Atualiza pilha 
            recente = proximo_recente
            
            # substitui linha
            linhas[indice_linha] = reg + "\n"
            print(f"[INFO] Inserção com REUSO no RRN {rrn_final}")

        else:
            # vai p/ fim arquivo, append (RRN)
            # rnn = tot - 1 da header
            rrn_final = len(linhas) - 1 
            linhas.append(reg + "\n")
            print(f"[INFO] Inserção com APPEND no RRN {rrn_final}")
        
        # att size
        if len(reg) > size:
            size = len(reg)

        # incrementa o n 
        n += 1 
        
        # att Header
        linhas[0] = f"SIZE={size} N={n} RECENTE={recente}\n"

        # salva no disco
        self.arq_dados.seek(0)
        self.arq_dados.writelines(linhas)
        self.arq_dados.truncate()

        # criar tupla (Chave, RRN)
        nova_tupla = (chave, rrn_final)

        # add a tupla na tabela
        self.array_indices.append(nova_tupla)

        # ordenar a tabela
        self.ordena_indices()

        return True
      

def main() -> None:
    arq_dados = "arquivoDadosRegistrosFixos.txt"
    arq_indices = "indice.txt"
    
      
    array_indices = Indice_primario(arq_dados, arq_indices)

    print("--- Teste de Pesquisa ---")
    print(array_indices.pesquisa(chave="YU-GI-OH!"))     # deve achar
    print(array_indices.pesquisa(chave="DRAGONBALL"))    # n deve achar

    print("\n--- Teste de Inserção ---")
    array_indices.insercao("JOJOSBIZARREADVENTURE|Anime|Stand")
    print(array_indices.pesquisa(chave="JOJOSBIZARREADVENTURE"))

    print("\n--- Teste de Remoção ---")
    array_indices.remocao("ONEPIECE")
    print(array_indices.pesquisa(chave="ONEPIECE"))      # n deve achar mais


if __name__ == "__main__":
    main()