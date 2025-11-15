"""
Entregável 12 - Indice Primário: Construtor e Pesquisa - Estrutura de Dados II
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

    def __init__(self, arquivo_dados, arquivo_indices):
        self.arq_dados = open(arquivo_dados, 'r')
        self.array_indices = []                                                 

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
            rrn = 0
            for reg in registros:
                chave = self.cria_chave(reg) # cria chave canonica
                self.array_indices.append((chave, rrn)) # insere no vetor de tuplas
                rrn += 1
            
            self.ordena_indices() # depois de inserir tudo, ordena pra pesquisa
        
        with open(arquivo_indices, 'w') as self.arq_ind:
            for indice in self.array_indices:
                self.arq_ind.write(f'{indice[0]} {indice[1]}\n') # escreve/atualiza no arquivo

            print(f'Arquivo de indices "{arquivo_indices}" criado/atualizado com sucesso!')


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

def main() -> None:
    arq_dados = "arquivoDadosRegistrosFixos.txt"
    arq_indices = "indice.txt"
      
    array_indices = Indice_primario(arq_dados, arq_indices)

    teste1 = array_indices.pesquisa(chave="YU-GI-OH!")
    print(teste1)
    teste2 = array_indices.pesquisa(chave="JOJO'SBIZARREADVENTURE")
    print(teste2)
    teste3 = array_indices.pesquisa(chave="ONEPIECE")
    print(teste3)


if __name__ == "__main__":
    main()