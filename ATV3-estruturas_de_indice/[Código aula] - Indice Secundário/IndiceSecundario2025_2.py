# Exemplo de import usando classes e herança
#from IndicePrimario import *
#class IndiceSecundario(IndicePrimario):
class IndiceSecundario:

    #atributos
    __tabelaIndicePrimario = []
    __tabelaIndiceSecundario = []
    __arquivoDados = None
    __arquivoIndicePrimario = None
    __arquivoIndiceSecundario = None 
    
    # opcionais
    __tamanhoRegistro = 100
    __nroRegistrosValidos = 0
    __nroTotalRegistros   = 0    
    __totalOperacoes = 0
    __arquivosAtualizados = False
    
    # Parametros:
    #  - campo: nome do campo que será definido o indice secundário
    def __init__(self, campo):
        pass
    
    def __del__(self):
        pass
    
    # Parametros:
    # - registro: registro com a informacao completa
    def inserir(self, registro):
        pass
    
    # Parametros:
    # - chaveP: chave primaria
    # - chaveS: chave secundaria
    def remover(self, chaveP, chaveS):
        pass 
    
    # Parametros:
    # - chave: valor valido de chave secundária
    def pesquisar(self, chave):
        pass
    
    def __lerRegistroPorRRN():
        pass
    
    def __buscaBinariaPrimaria():
        pass
   
    def __buscaBinariaSecundaria():
        pass
    
    def __ordenarTabelaPrimaria():
        pass 
    
    def __ordenarTabelaSecundaria():
        pass 
    
    def __storageCompaction():
        pass 
    
    def __lerCabecalho():
        pass
    
    def __escreverCabecalho():
        pass