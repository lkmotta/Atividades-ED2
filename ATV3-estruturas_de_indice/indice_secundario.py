"""
Atividade 3 - Indexação Secundária - Estrutura de Dados 2

Acadêmicos:
    Gabriel Mancuso Bonfim  (2669498)
    Lucas Henrique Motta    (2669730)

Orientador:
    Prof. Dr. Rafael Gomes Mantovani
"""

import sys
import csv
import re


# -----------------------------------------------------------------------------
# CLASSES INDICES
# -----------------------------------------------------------------------------

class IndicePrimario:
    """
    mantem o indice primario
    mapeia: ID (string) -> byte offset (int)
    """
    def __init__(self):
        # lista de tuplas
        self.tabela = []

    def inserir(self, id_musica, pos_no_arquivo):
        self.tabela.append((id_musica, pos_no_arquivo))

    def ordenar(self):
        # ordena pelo id
        self.tabela.sort(key=lambda x: x[0])

    def buscar(self, id_busca):
        """
        faz a busca binaria no primeiro indice
        retorna:  byte_offset  ou None se não achar
        """
        inicio = 0
        fim = len(self.tabela) - 1

        while inicio <= fim:
            meio = (inicio + fim) // 2
            chave_atual = self.tabela[meio][0]

            if chave_atual == id_busca:
                return self.tabela[meio][1] # retorna o off set
            elif chave_atual < id_busca:
                inicio = meio + 1
            else:
                fim = meio - 1
        
        return None


class IndiceSecundario:
    """
    mantem um indice secundario (ex: artista ou Ano)
    mapeia: valor do campo (string) -> ID da musica (string)
    """
    def __init__(self, nome_campo):
        self.nome_campo = nome_campo
        # lista de tuplas
        self.tabela = []

    def inserir(self, valor_campo, id_primario):
        # armazena tudo como string minuscula mas mantem o id
        if valor_campo:
            # tira aspas e espacos
            val_limpo = valor_campo.strip().replace('"', '').replace("'", "")
            self.tabela.append((val_limpo.upper(), id_primario))

    def ordenar(self):
        """ordena a tabela pelo valor do campo (chave secundária)"""
        self.tabela.sort(key=lambda x: x[0])

    def buscar(self, chave_busca):
        """
        busca binaria
        encontrar registros que comecam com a chave
        """
        # normaliza a chave
        chave_busca = chave_busca.strip().replace('"', '').replace("'", "").upper()
        
        inicio = 0
        fim = len(self.tabela) - 1
        
        # 1. encontrar onde a chave pode estar
        while inicio <= fim:
            meio = (inicio + fim) // 2
            chave_atual = self.tabela[meio][0]
            
            if chave_atual < chave_busca:
                inicio = meio + 1
            else:
                fim = meio - 1
        
        # 'inicio' agora eh o indice do primeiro elemento
        match_index = inicio
        ids_encontrados = []
        
        # 2. vai para frente enquanto o prefixo estiver igual a chave
        # verifica se o indice eh valido e se a chave comeca com oq buscamos
        while match_index < len(self.tabela):
            chave_atual = self.tabela[match_index][0]
            
            # se a chave comeca com oq buscamos
            if chave_atual.startswith(chave_busca):
                ids_encontrados.append(self.tabela[match_index][1])
                match_index += 1
            else:
                # para a busca se achou diferente
                break
                
        return list(set(ids_encontrados))




# -----------------------------------------------------------------------------
# PROCESSADOR
# -----------------------------------------------------------------------------

class ProcessadorDeConsultas:
    def __init__(self, arquivo_dados):
        self.arquivo_dados = arquivo_dados
        self.idx_primario = IndicePrimario()
        self.idxs_secundarios = {}
        
        # mapeamento dos nomes das colunas para os indices do csv
        self.mapa_colunas = {
            "id": 0, "name": 1, "album": 2, "album_id": 3, 
            "artists": 4, "artist_ids": 5, "track_number": 6, 
            "disc_number": 7, "explicit": 8, "danceability": 9,
            "energy": 10, "key": 11, "loudness": 12, "mode": 13,
            "speechiness": 14, "acousticness": 15, "instrumentalness": 16,
            "liveness": 17, "valence": 18, "tempo": 19, "duration_ms": 20,
            "time_signature": 21, "year": 22, "release_date": 23
        }

    def criar_indices(self, campos_para_indexar):
        print(f"\033[96mCriando índices para: {campos_para_indexar}...\033[0m")
        
        for campo in campos_para_indexar:
            if campo not in self.idxs_secundarios:
                self.idxs_secundarios[campo] = IndiceSecundario(campo)

        try:
            with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                # pula header
                f.readline()
                
                while True:
                    offset_atual = f.tell()
                    linha = f.readline()
                    if not linha:
                        break
                    
                    # parse da linha CSV 
                    try:
                        dados = next(csv.reader([linha]))
                    except StopIteration:
                        continue
                    
                    # ignora se a linha estiver errada
                    if len(dados) < 24:
                        continue

                    id_track = dados[0]
                    
                    # 1. inserir no indice primario (ID -> Offset)
                    self.idx_primario.inserir(id_track, offset_atual)

                    # 2. inserir nos indices secundarios (Valor -> ID)
                    for campo in campos_para_indexar:
                        idx_col = self.mapa_colunas.get(campo)
                        if idx_col is not None:
                            valor = dados[idx_col]
                            
                            # tratamento para o campo artista 
                            if campo == 'artists':
                                # remove colchetes e aspas e quebra por virgula 
                                valor_limpo = valor.replace("[", "").replace("]", "").replace("'", "")
                                nomes = valor_limpo.split(",")
                                for nome in nomes:
                                    self.idxs_secundarios[campo].inserir(nome.strip(), id_track)
                            else:
                                self.idxs_secundarios[campo].inserir(valor, id_track)
        
            # ordenacao
            print("\033[96mOrdenando Índice Primário...\033[0m")
            self.idx_primario.ordenar()
            for campo, idx in self.idxs_secundarios.items():
                print(f"\033[96mOrdenando Índice Secundário ({campo})...\033[0m")
                idx.ordenar()
                
        except FileNotFoundError:
            print(f"\033[91mERRO: Arquivo {self.arquivo_dados} não encontrado.\033[0m")
            sys.exit(1)

    def recuperar_registro(self, byte_offset):
        with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
            f.seek(byte_offset)
            return f.readline().strip()

    # processa a query
    def executar(self, arq_query, arq_saida):
        # 1. ler Query
        print(f"\033[96mIniciando processamento da consulta...\033[0m")
        if not self._ler_query(arq_query, arq_saida): return

        linha_criterios = self.query_criterios
        linha_valores = self.query_valores

        # 2. separa os criterios com regex
        # separa critérios mantendo os operadores '||' e '&'
        # também encontra operadores ou blocos de texto que não contenham '&' ou '|' e
        # depois remove espaços em branco das partes
        partes = re.findall(r'\|\||&|[^&|]+', linha_criterios)
        criterios = [parte.strip() for parte in partes if parte.strip()]
        
        # separa os valores
        try:
            valores = next(csv.reader([linha_valores], skipinitialspace=True))
        except StopIteration:
            valores = []

        # pega somente os nomes 
        campos_para_indexar = [t for t in criterios if t != '&' and t != '||']
        
        # validacao
        if len(campos_para_indexar) != len(valores):
            print(f"\033[91mERRO: Número de critérios ({len(campos_para_indexar)}) diferente do número de valores ({len(valores)}).\033[0m")
            return

        # 3. criar os indices
        self.criar_indices(campos_para_indexar)

        # 4. execucao (esq para dir)
        # inicializa com o primeiro termo da busca
        campo_atual = criterios[0]
        valor_atual = valores[0]
        
        print(f"\033[96mExecutando busca inicial em '{campo_atual}' com valor '{valor_atual}'...\033[0m")
        # busca inicial
        ids_acumulados = set(self.idxs_secundarios[campo_atual].buscar(valor_atual))
        
        # ponteiro para percorrer o restande da query
        idx_valor = 1
        idx_criterios = 1
        
        while idx_criterios < len(criterios):
            operador = criterios[idx_criterios]             # ex: '||' ou '&'
            proximo_campo = criterios[idx_criterios+1]      # ex: 'year'
            proximo_valor = valores[idx_valor]              # ex: '1999'
            
            print(f"\033[96mAplicando operador '{operador}' com campo '{proximo_campo}' e valor '{proximo_valor}'...\033[0m")
            # busca o prox conj de ids
            ids_novos = set(self.idxs_secundarios[proximo_campo].buscar(proximo_valor))
            
            # aplica a operacao com o conj anterior
            if operador == '&':
                ids_acumulados = ids_acumulados.intersection(ids_novos)
            elif operador == '||':
                ids_acumulados = ids_acumulados.union(ids_novos)
            
            idx_criterios += 2 # pula o operador e o campo
            idx_valor += 1

        # 5. salva os dados na saida
        self._salvar_resultados(ids_acumulados, arq_saida)
        
        print(f"\033[92mConsulta finalizada. {len(ids_acumulados)} registros encontrados (salvos em {arq_saida}).\033[0m")


    def _ler_query(self, caminho, arq_saida):
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                
                linhas = f.read()
                linhas = linhas.strip()

                # arquivo vazio
                if not linhas:
                    print(f"\033[91mERRO: Arquivo de query está vazio.\033[0m")
                    with open(arq_saida, 'w', encoding='utf-8') as f_out:
                        f_out.write("Arquivo vazio !\n")
                    return False
                
                #volta o ponteiro
                f.seek(0)
                linhas = f.readlines()
                
                # arquivo invalido
                if len(linhas) < 2:
                    print(f"\033[91mERRO: Arquivo inválido (faltando linha de valores).\033[0m")
                    with open(arq_saida, 'w', encoding='utf-8') as f_out:
                        f_out.write("Arquivo inválido!\n")
                    return False
                self.query_criterios = linhas[0].strip()
                self.query_valores = linhas[1].strip()
                return True
        except FileNotFoundError:
            print(f"\033[91mERRO: Arquivo de query '{caminho}' não encontrado.\033[0m")
            return False

    def _salvar_resultados(self, ids_set, arq_saida):
        # 1. recupera (ID, Offset) para cada id
        # off set para ordenar e buscar no disco
        lista_com_offsets = []
        
        for id_track in ids_set:
            offset = self.idx_primario.buscar(id_track)
            if offset is not None:
                lista_com_offsets.append((id_track, offset))
        
        # 2. ordena pelo offset
        lista_com_offsets.sort(key=lambda x: x[1])

        # 3. busca no disco e salva
        with open(arq_saida, 'w', encoding='utf-8') as f_out:
            if not lista_com_offsets:
                f_out.write("Nenhum resultado foi encontrado!\n")
                print(f"\033[93mALERTA: Nenhum registro encontrado para a consulta.\033[0m")
            else:
                for id_track, offset in lista_com_offsets:
                    registro = self.recuperar_registro(offset)
                    f_out.write(registro + "\n")
        



# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("\033[93mUso Incorreto:\033[0m \033[93mpython programa.py <dados.csv> <query.txt> <saida.txt>\033[0m")
        sys.exit(1)

    arq_dados = sys.argv[1]
    arq_query = sys.argv[2]
    arq_saida = sys.argv[3]

    app = ProcessadorDeConsultas(arq_dados)
    app.executar(arq_query, arq_saida)