from indicePrimario import * 

if __name__ == '__main__':
    
    arqDados = "arquivoDadosRegistrosFixos.txt"
    arqIndices = "indice.txt"
   
    # criando o indice primario    
    arrayIndices = indicePrimario(arqDados=arqDados, 
                                  arqIndices=arqIndices)
    
    # destruir
    # inserir
    # remover
    
    # pesquisar
    # Achar!
    ret1 = arrayIndices.pesquisa(chave="GINTAMA")
    print(ret1)
    ret2 = arrayIndices.pesquisa(chave="DRAGONBALLSUPER")
    print(ret2)
    ret3 = arrayIndices.pesquisa(chave="FULLMETALALCHEMIST")
    print(ret3)
         
  