# --------------------------------------------------------
# --------------------------------------------------------

import os

# --------------------------------------------------------
# --------------------------------------------------------

class indicePrimario:
   
    __arquivoDados = None
    __arquivoIndices = None
    __arrayIndice = list()  
    __tamanhoRegistro = 425  
   
    # ---------------------------------
    # ---------------------------------
    
    def __init__(self, arqDados, arqIndices):
        self.__arquivoDados = open(arqDados, 'r')
       
        if(os.path.isfile(arqIndices)):
            print("O arquivo de indice primario existe")
            
            with open(arqIndices, 'r') as f:
                for linhas in f:
                    chave, RRN = linhas.split()
                    self.__arrayIndice.append((chave, int(RRN)))
            self.ordenaArrayIndicePrimario()
            print(self.__arrayIndice[:10])                
        else:
            print("Não existe o arquivo de indice primário")
            self.__arquivoIndices = open(arqIndices, 'w')
           
            registros = self.__arquivoDados.readlines()
            RRN = 0            
            for r in registros:
                chave = self.criaChaveCanonica(r)
                self.__arrayIndice.append((chave, RRN))
                RRN = RRN + 1
            
            self.ordenaArrayIndicePrimario()
            
            for i in self.__arrayIndice:
                self.__arquivoIndices.write(f'{i[0]} {i[1]}\n')
       
    # ---------------------------------
    # ---------------------------------
    
    def criaChaveCanonica(self, r):
        campos = r.split("|")
        chave = campos[0].upper().replace(' ', '')
        return chave      
   
    # ---------------------------------
    # ---------------------------------
    
    def ordenaArrayIndicePrimario(self):
        self.__arrayIndice.sort(key = lambda tup: tup[0])      

    # ---------------------------------
    # Busca binária
    # ---------------------------------
    def __buscaBinaria(self, chave): 
        # print("CHAVE = ", chave)
        inicio, fim = 0, len(self.__arrayIndice) - 1
        while(inicio <= fim):
            meio = (inicio + fim)//2
            # print("Meio = ", meio)
            tuplaMeio = self.__arrayIndice[meio]
            # print(tuplaMeio)
            if(tuplaMeio[0] == chave):
                RRN = tuplaMeio[1]
                return (True, meio, RRN)
            elif (chave < tuplaMeio[0]):
                fim = meio-1
            else:
                inicio = meio+1
        return (False, None, None)

    # ---------------------------------
    # Método de pesquisa
    #   @Parametros:
    #       - chave: chave canônica do registro que se deseja encontrar 
    #   @Retornos:
    #       - (Achou/NãoAchou, RRN)
    # ---------------------------------
    
    def pesquisa(self, chave):
        # 1. Pesquisar a "chave" na tabela de indices
        #  usando busca binária
        retorno = self.__buscaBinaria(chave=chave)
        return(retorno)
        #[achou/n achou, idTabela, idArquivo/RRN] 
        
    # ---------------------------------
    # Método de remoção
    #   @Parametros:
    #       - chave: chave canônica do registro que se deseja encontrar 
    #   @Retornos:
    #       - True|False: retorna se conseguiu remover ou não
    # ---------------------------------
    
    def removeRegistro(self, chave):
        # 1. Pesquisar a chave na tabela de indices
        [result, idTabela, RRN] = self.pesquisa(chave = chave)
        # 2.a ) não achou _> retorna Falso
        if(not result):
            return (False)
        else: # 2.b ) Achou
        # 3. Invalida o registro no arquivo    
            #   seek para a linha desejada (RRN)
            offset = self.__tamanhoRegistro * RRN
            self.__arquivoDados.seek(offset)
            #   char[0] = *
            #   char[1] = |
            self.__arquivoDados.write("*|")
            # 4. remover o registro da tabela (idTabela)
            #   acessar o arrayIndice e remover o elemento de id idTabela
            self.__arrayIndice.pop(idTabela)
            
 
# --------------------------------------------------------
# --------------------------------------------------------