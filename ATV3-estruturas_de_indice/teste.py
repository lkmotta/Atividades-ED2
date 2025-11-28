"""
Atividade 3/4 - Indexação Secundária - Estrutura de Dados 2
Descrição: Programa para indexação e busca em base de dados do Spotify.
Arquitetura: Índice Secundário -> Chave Primária (ID) -> Índice Primário -> RRN
"""

from sys import argv
import os
import csv
import re 

# --- Classe Musica ---
class Musica:
    def __init__(
            self, RRN, id, name, album, album_id, artists, artist_ids,
            track_number, disc_number, explicit, danceability, energy,
            key, loudness, mode, speechiness, acousticness,
            instrumentalness, liveness, valence, tempo, duration_ms,
            time_signature, year, release_date
        ):
        self.RRN = RRN 
        self.id = id
        self.name = name
        self.album = album
        self.album_id = album_id
        self.artists = artists
        self.artist_ids = artist_ids
        self.track_number = track_number
        self.disc_number = disc_number
        self.explicit = explicit
        self.danceability = danceability
        self.energy = energy
        self.key = key
        self.loudness = loudness
        self.mode = mode
        self.speechiness = speechiness
        self.acousticness = acousticness
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.valence = valence
        self.tempo = tempo
        self.duration_ms = duration_ms
        self.time_signature = time_signature
        self.year = year
        self.release_date = release_date

    def __str__(self):
        return (f"{self.id},{self.name},{self.album},{self.album_id},{self.artists},"
                f"{self.artist_ids},{self.track_number},{self.disc_number},{self.explicit},"
                f"{self.danceability},{self.energy},{self.key},{self.loudness},"
                f"{self.mode},{self.speechiness},{self.acousticness},{self.instrumentalness},"
                f"{self.liveness},{self.valence},{self.tempo},{self.duration_ms},"
                f"{self.time_signature},{self.year},{self.release_date}")

# --- Classe IndicePrimario  ---
class IndicePrimario:
    def __init__(self):
        # Mapeia: ID (String) -> RRN 
        self.indices = {}

    def adicionar_musica(self, id_musica, rrn):
        self.indices[id_musica] = rrn

    def buscar_rrn(self, id_musica):
        return self.indices.get(id_musica, None)

# --- Classe IndiceSecundario  ---
class IndiceSecundario:
    def __init__(self):
        self.indices = {} 
    
    def cria_indice(self, campo, lista_musicas) -> dict:
        """
        Cria um índice secundário que mapeia Valor -> Lista de IDs (Chaves Primárias)
        """
        if campo in self.indices:
            return self.indices[campo]

        indice = {}
        
        for musica in lista_musicas:
            try:
                valor_campo = getattr(musica, campo)
            except AttributeError:
                print(f"Erro: Atributo '{campo}' não existe na classe Musica.")
                return {}

            valor_campo = str(valor_campo).strip()
            # Limpeza de caracteres de lista
            valor_campo = valor_campo.strip("[]'")

            if valor_campo not in indice:
                indice[valor_campo] = []
            
            # guardamos o ID da música, não o RRN direto
            indice[valor_campo].append(musica.id)
        
        self.indices[campo] = indice
        return indice
    
    def buscar_ids(self, campo, valor) -> list:
        """Retorna lista de IDs para um valor"""
        if campo not in self.indices:
            return []
        
        valor_str = str(valor).strip()
        if valor_str in self.indices[campo]:
            return self.indices[campo][valor_str]
        return []


# --- Função Principal ---
def main():
    if len(argv) != 4:
        print("\033[1;91mERRO\033[1;30m\nUso: python main.py <arq_dados> <arq_consulta> <arq_saida>")
        return

    arq_dados = argv[1]
    arq_consulta = argv[2]
    arq_saida = argv[3]

    if not os.path.isfile(arq_dados):
        print(f"O arquivo de dados '{arq_dados}' não foi encontrado.")
        return

    # Inicializa Índice Primário
    indice_primario = IndicePrimario()
    lista_musicas = []

    # Leitura do CSV
    try:
        print("Carregando arquivo de dados e criando Índice Primário...")
        arquivo_csv = open(arq_dados, encoding="utf-8", newline='')
        data = csv.reader(arquivo_csv, delimiter=",")
        
        header = next(data, None) 
        
        for pos, linha in enumerate(data):
            if not linha: continue 

            musica = Musica(
                RRN=pos, # Endereço Físico/Lógico
                id=linha[0], # Chave Primária
                name=linha[1], album=linha[2], album_id=linha[3],
                artists=linha[4], artist_ids=linha[5], 
                track_number=linha[6], disc_number=linha[7],
                explicit=linha[8], danceability=linha[9],
                energy=linha[10], key=linha[11],
                loudness=linha[12], mode=linha[13],
                speechiness=linha[14], acousticness=linha[15],
                instrumentalness=linha[16], liveness=linha[17],
                valence=linha[18], tempo=linha[19], duration_ms=linha[20],
                time_signature=linha[21], year=linha[22], release_date=linha[23]
            )
            lista_musicas.append(musica)
            
            # Adiciona ao Índice Primário (ID -> RRN)
            indice_primario.adicionar_musica(musica.id, musica.RRN)
        
        arquivo_csv.close()
        print(f"Total de músicas carregadas: {len(lista_musicas)}")

    except Exception as erro:
        print(f"ERRO na leitura dos dados: {erro}")
        return

    # Processamento da Consulta
    try:
        if not os.path.isfile(arq_consulta):
            print(f"Arquivo de consulta '{arq_consulta}' não encontrado.")
            return

        with open(arq_consulta, 'r', encoding='utf-8') as f:
            linhas_query = f.readlines()
        
        if len(linhas_query) < 2:
            print("Arquivo de consulta inválido.")
            return

        linha_campos = linhas_query[0].strip()
        linha_valores = linhas_query[1].strip()

        campos = re.split(r' \|\| | & ', linha_campos)
        operadores = re.findall(r' \|\| | & ', linha_campos)
        operadores = [op.strip() for op in operadores]
        valores = [v.strip() for v in linha_valores.split(',')]

        if len(campos) != len(valores):
            print(f"ERRO: A query possui {len(campos)} campos mas {len(valores)} valores.")
            with open(arq_saida, 'w', encoding='utf-8') as f_out:
                f_out.write("ERRO: Inconsistencia entre campos e valores.")
            return

    except Exception as e:
        print(f"Erro ao processar query: {e}")
        return

    # Busca Secundária (Retorna IDs)
    gerenciador_secundario = IndiceSecundario()
    
    campo_inicial = campos[0]
    valor_inicial = valores[0]
    
    gerenciador_secundario.cria_indice(campo_inicial, lista_musicas)
    
    # OBS: Agora trabalhamos com Sets de IDs, não de RRNs
    ids_acumulados = set(gerenciador_secundario.buscar_ids(campo_inicial, valor_inicial))

    for i in range(len(operadores)):
        op_atual = operadores[i]
        proximo_campo = campos[i+1]
        proximo_valor = valores[i+1]
        
        gerenciador_secundario.cria_indice(proximo_campo, lista_musicas)
        ids_novos = set(gerenciador_secundario.buscar_ids(proximo_campo, proximo_valor))

        if op_atual == '&':
            ids_acumulados = ids_acumulados.intersection(ids_novos)
        elif op_atual == '||':
            ids_acumulados = ids_acumulados.union(ids_novos)

    # Resolução Final: IDs -> RRNs -> Objetos Musica
    # Aqui usamos o Índice Primário para localizar os registros
    lista_musicas_final = []
    
    for id_musica in ids_acumulados:
        rrn = indice_primario.buscar_rrn(id_musica)
        if rrn is not None:
            lista_musicas_final.append(lista_musicas[rrn])

    # Escrita
    try:
        with open(arq_saida, 'w', encoding='utf-8') as f_out:
            if not lista_musicas_final:
                f_out.write("Nenhum resultado foi encontrado!") 
            else:
                # Ordenar por RRN (opcional, para consistência visual)
                lista_musicas_final.sort(key=lambda x: x.RRN)
                
                for musica in lista_musicas_final:
                    f_out.write(str(musica) + "\n")
        
        print(f"Busca concluída. Resultados salvos em '{arq_saida}'.")

    except Exception as erro:
        print(f"Erro ao escrever arquivo de saída: {erro}")

if __name__ == "__main__":
    main()