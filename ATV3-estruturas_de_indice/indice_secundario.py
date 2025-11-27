"""
Atividade 3 - Indexação Secundária - Estrutura de Dados 2

Acadêmicos:
    Gabriel Mancuso Bonfim  (2669498)
    Lucas Henrique Motta    (2669730)

Orientador:
    Prof. Dr. Rafael Gomes Mantovani
"""

from sys import argv
import os
import csv

class Musica:
    def __init__(
            self, RRN, id, nome, album, album_id, artistas, artistas_ids,
            num_trilha, num_disco, explicito, dancabilidade, energia,
            chave, intensidade, modo, fonetica, acustica,
            instrumentalidade, vivacidade, valencia, tempo, duracao_ms,
            compasso, ano, data_lancamento
        ):
        self.RRN = RRN
        self.id = id
        self.nome = nome
        self.album = album
        self.album_id = album_id
        self.artistas = artistas
        self.artistas_ids = artistas_ids
        self.num_trilha = num_trilha
        self.num_disco = num_disco
        self.explicito = explicito
        self.dancabilidade = dancabilidade
        self.energia = energia
        self.chave = chave
        self.intensidade = intensidade
        self.modo = modo
        self.fonetica = fonetica
        self.acustica = acustica
        self.instrumentalidade = instrumentalidade
        self.vivacidade = vivacidade
        self.valencia = valencia
        self.tempo = tempo
        self.duracao_ms = duracao_ms
        self.compasso = compasso
        self.ano = ano
        self.data_lancamento = data_lancamento

    def __del__(self):
        pass


class IndiceSecundario:
    def __init__(self):
        self.indices = {}
    
    def cria_indice(self, campo, lista_musicas) -> dict:
        """
        Cria um índice secundário para um campo específico
        Args:
            campo (str): O nome do campo para o qual o índice será criado
            lista_musicas (list): Lista de objetos Musica
        Returns:
            dict: dicionário do índice secundário
        """
        indice = {}
        for musica in lista_musicas:
            # pega o valor do campo
            valor_campo = getattr(musica, campo)
            
            # campo vazio
            if not valor_campo:
                valor_campo = "-"
            
            if valor_campo not in indice:
                indice[valor_campo] = []
            indice[valor_campo].append(musica.RRN)
        
        self.indices[campo] = indice
        return indice
    
    def buscar(self, campo, valor) -> list:
        """
        Busca por um valor específico em um campo indexado
        Args:
            campo (str): O nome do campo a ser buscado
            valor: O valor a ser buscado no campo
        Returns:
            list: Lista de RRNs correspondentes ao valor buscado
        """
        if campo not in self.indices:
            return []
        
        valor_str = str(valor)
        if valor_str in self.indices[campo]:
            return self.indices[campo][valor_str]
        return []
    

def main():
    if len(argv) != 4:
        print("\033[1;91mERRO\033[1;30m\nO comando de execução deve ser\033[m: python indice_secundario.py <arq_dados> <arq_consulta> <arq_saida>")
        return

    arq_dados = argv[1]
    arq_consulta = argv[2]
    arq_saida = argv[3]

    if not os.path.isfile(arq_dados):
        print(f"\033[1;91mERRO\033[1;30m\nO arquivo de dados '{arq_dados}' não encontrado.\033[m")
        return

    try:
        data = csv.reader(open(arq_dados, encoding = "utf-8"), delimiter = ",")
        lista_dados = list(data)

        lista_musicas = []
        for pos, linha in enumerate(lista_dados):
            musica = Musica(
                RRN = pos, id = linha[0], nome = linha[1],
                album = linha[2], album_id = linha[3],
                artistas = linha[4], artistas_ids = linha[5],
                num_trilha = linha[6], num_disco = linha[7],
                explicito = linha[8],
                dancabilidade = linha[9],
                energia = linha[10],
                chave = linha[11],
                intensidade = linha[12],
                modo = linha[13],
                fonetica = linha[14],
                acustica = linha[15],
                instrumentalidade = linha[16],
                vivacidade = linha[17],
                valencia = linha[18],
                tempo = linha[19], duracao_ms = linha[20],
                compasso = linha[21],
                ano = linha[22], data_lancamento = linha[23]
            )
            lista_musicas.append(musica)

    except Exception as erro:
        print(f"\033[1;91mERRO: \033[1;30m{erro}\033[m")
        return

if __name__ == "__main__":
    main()