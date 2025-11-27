# Exemplo de import usando classes e herança

from IndicePrimario import *
class IndiceSecundario(IndicePrimario):

    #atributos
    __tabelaIndiceSecundario = []
    __arquivoIndiceSecundario = None 
        
    # Parametros:
    #  - campo: nome do campo que será definido o indice secundário
    def __init__(self, campo):
        #super()
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
    
    def __buscaBinariaSecundaria():
        pass
    
    def __ordenarTabelaSecundaria():
        pass 