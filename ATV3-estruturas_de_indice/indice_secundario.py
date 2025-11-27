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


def main():
    if len(argv) != 4:
        print("\033[1;91mERRO\033[1;30m\nO comando de execução deve ser\033[m: python indice_secundario.py <arq_dados> <arq_consulta> <arq_saida>")
        return

    arq_dados = argv[1]
    arq_consulta = argv[2]
    arq_saida = argv[3]

    data = csv.reader(open(arq_dados, encoding = "utf-8"), delimiter = ",")
    lista_dados = list(data)

    for linha in lista_dados:
        if(len(linha)) != 24:
            print(linha)


if __name__ == "__main__":
    main()