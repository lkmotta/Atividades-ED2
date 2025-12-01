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
import io

# =============================================================================
# CLASSES DE ESTRUTURA DE DADOS (ÍNDICES)
# =============================================================================

class IndicePrimario:
    """
    Mantém o índice primário em Memória RAM.
    Mapeia: ID (string) -> Byte Offset (int)
    """
    def __init__(self):
        # Lista de tuplas: [(id_track, offset), ...]
        self.tabela = []

    def inserir(self, id_musica, pos_no_arquivo):
        self.tabela.append((id_musica, pos_no_arquivo))

    def ordenar(self):
        """Ordena a tabela pelo ID para permitir busca binária."""
        # Ordena pela chave (posição 0 da tupla)
        self.tabela.sort(key=lambda x: x[0])

    def buscar(self, id_busca):
        """
        Realiza Busca Binária no índice primário.
        Retorno: O byte_offset (int) ou None se não achar.
        """
        inicio = 0
        fim = len(self.tabela) - 1

        while inicio <= fim:
            meio = (inicio + fim) // 2
            chave_atual = self.tabela[meio][0]

            if chave_atual == id_busca:
                return self.tabela[meio][1] # Retorna o Offset
            elif chave_atual < id_busca:
                inicio = meio + 1
            else:
                fim = meio - 1
        
        return None


class IndiceSecundario:
    """
    Mantém um índice secundário (ex: Artista ou Ano).
    Mapeia: Valor do Campo (string) -> ID da Faixa (string)
    """
    def __init__(self, nome_campo):
        self.nome_campo = nome_campo
        # Lista de tuplas: [(valor_campo, id_primario), ...]
        self.tabela = []

    def inserir(self, valor_campo, id_primario):
        # Armazena tudo como string minúscula para facilitar busca case-insensitive
        # Mas mantém o ID original
        if valor_campo:
            # Remove aspas extras que o CSV pode ter deixado e espaços
            val_limpo = valor_campo.strip().replace('"', '').replace("'", "")
            self.tabela.append((val_limpo.upper(), id_primario))

    def ordenar(self):
        """Ordena a tabela pelo valor do campo (chave secundária)."""
        self.tabela.sort(key=lambda x: x[0])

    def buscar(self, chave_busca):
        """
        Realiza Busca Binária para encontrar TODOS os IDs associados à chave.
        Retorno: Uma lista de IDs [id1, id2, ...]
        """
        chave_busca = chave_busca.strip().replace('"', '').replace("'", "").upper()
        
        inicio = 0
        fim = len(self.tabela) - 1
        encontrou_indice = -1

        # 1. Busca binária para achar UMA ocorrência
        while inicio <= fim:
            meio = (inicio + fim) // 2
            chave_atual = self.tabela[meio][0]

            if chave_atual == chave_busca:
                encontrou_indice = meio
                break # Achamos um, paramos o loop principal
            elif chave_atual < chave_busca:
                inicio = meio + 1
            else:
                fim = meio - 1

        if encontrou_indice == -1:
            return []

        # 2. Expansão para encontrar duplicatas (já que artistas têm várias músicas)
        ids_encontrados = []
        
        # Expande para a esquerda
        i = encontrou_indice
        while i >= 0 and self.tabela[i][0] == chave_busca:
            ids_encontrados.append(self.tabela[i][1])
            i -= 1
        
        # Expande para a direita
        i = encontrou_indice + 1
        while i < len(self.tabela) and self.tabela[i][0] == chave_busca:
            ids_encontrados.append(self.tabela[i][1])
            i += 1

        return list(set(ids_encontrados)) # Remove duplicatas exatas se houver


# =============================================================================
# PROCESSADOR (LÓGICA PRINCIPAL)
# =============================================================================

class ProcessadorDeConsultas:
    def __init__(self, arquivo_dados):
        self.arquivo_dados = arquivo_dados
        self.idx_primario = IndicePrimario()
        self.idxs_secundarios = {}
        
        # Mapeamento de nomes de colunas para índices do CSV (Baseado no código do seu colega e PDF)
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
        print(f"Criando índices para: {campos_para_indexar}...")
        
        for campo in campos_para_indexar:
            if campo not in self.idxs_secundarios:
                self.idxs_secundarios[campo] = IndiceSecundario(campo)

        try:
            with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                # Pula cabeçalho
                f.readline()
                
                while True:
                    offset_atual = f.tell()
                    linha = f.readline()
                    if not linha:
                        break
                    
                    # Parse da linha CSV respeitando aspas (ex: "Music, The")
                    # Usamos o módulo csv para parsear apenas esta linha string
                    try:
                        dados = next(csv.reader([linha]))
                    except StopIteration:
                        continue
                    
                    # Se a linha estiver quebrada/incompleta, ignora
                    if len(dados) < 24:
                        continue

                    id_track = dados[0]
                    
                    # 1. Inserir no Índice Primário (ID -> Offset)
                    self.idx_primario.inserir(id_track, offset_atual)

                    # 2. Inserir nos Índices Secundários (Valor -> ID)
                    for campo in campos_para_indexar:
                        idx_col = self.mapa_colunas.get(campo)
                        if idx_col is not None:
                            valor = dados[idx_col]
                            
                            # Tratamento especial para o campo 'artists' que vem como list string "['Queen']"
                            if campo == 'artists':
                                # Remove colchetes e aspas e quebra por vírgula se tiver múltiplos
                                valor_limpo = valor.replace("[", "").replace("]", "").replace("'", "")
                                nomes = valor_limpo.split(",")
                                for nome in nomes:
                                    self.idxs_secundarios[campo].inserir(nome.strip(), id_track)
                            else:
                                self.idxs_secundarios[campo].inserir(valor, id_track)
        
            # ORDENAÇÃO (CRUCIAL)
            print("Ordenando Índice Primário...")
            self.idx_primario.ordenar()
            for campo, idx in self.idxs_secundarios.items():
                print(f"Ordenando Índice Secundário ({campo})...")
                idx.ordenar()
                
        except FileNotFoundError:
            print(f"ERRO: Arquivo {self.arquivo_dados} não encontrado.")
            sys.exit(1)

    def recuperar_registro(self, byte_offset):
        with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
            f.seek(byte_offset)
            return f.readline().strip()

    # processa a query
    def executar(self, arq_query, arq_saida):
        # 1. Ler a Query
        if not self._ler_query(arq_query):
            return

        # 2. Identificar operador e campos
        linha_criterios = self.query_criterios
        linha_valores = self.query_valores
        
        operador = None
        if '&' in linha_criterios:
            operador = '&'
            campos = [c.strip() for c in linha_criterios.split('&')]
            valores = [v.strip() for v in linha_valores.split(',')]
        elif '||' in linha_criterios:
            operador = '||'
            campos = [c.strip() for c in linha_criterios.split('||')]
            # Assumindo que no OR os valores também são separados por vírgula na mesma ordem
            # Se for "artist || year", valores deve ser "Queen, 2020"
            # O split da string de valores deve considerar vírgulas dentro de aspas? 
            # Simplificação: split por vírgula.
            valores = [v.strip() for v in linha_valores.split(',')]
        else:
            # Consulta Simples
            campos = [linha_criterios.strip()]
            valores = [linha_valores.strip()]

        # 3. Criar os índices necessários
        # Verifica se campos existem no mapa
        for c in campos:
            if c not in self.mapa_colunas:
                print(f"ERRO: Campo '{c}' inválido ou não suportado.")
                return
        
        self.criar_indices(campos)

        # 4. Realizar buscas
        sets_de_ids = []
        
        for i, campo in enumerate(campos):
            valor_buscado = valores[i]
            # Busca no índice secundário -> retorna lista de IDs
            ids = self.idxs_secundarios[campo].buscar(valor_buscado)
            sets_de_ids.append(set(ids))

        # 5. Aplicar Lógica Booleana
        resultado_ids = set()
        if not sets_de_ids:
            resultado_ids = set()
        elif operador == '&':
            # Interseção: começa com o primeiro set e faz intersection com os demais
            resultado_ids = sets_de_ids[0]
            for s in sets_de_ids[1:]:
                resultado_ids = resultado_ids.intersection(s)
        elif operador == '||':
            # União
            for s in sets_de_ids:
                resultado_ids = resultado_ids.union(s)
        else:
            # Simples
            resultado_ids = sets_de_ids[0]

        # 6. Recuperar dados finais e Salvar
        with open(arq_saida, 'w', encoding='utf-8') as f_out:
            lista_ids = list(resultado_ids)
            if not lista_ids:
                f_out.write("Nenhum resultado foi encontrado!\n")
            else:
                # Opcional: ordenar a saída para ficar bonito
                lista_ids.sort()
                
                for id_track in lista_ids:
                    # Busca offset no primário
                    offset = self.idx_primario.buscar(id_track)
                    if offset is not None:
                        registro = self.recuperar_registro(offset)
                        f_out.write(registro + "\n")
        
        print(f"Consulta finalizada. {len(lista_ids)} registros encontrados.")


    def _ler_query(self, caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
                if len(linhas) < 2:
                    print("ERRO: Arquivo de query inválido (linhas insuficientes).")
                    return False
                self.query_criterios = linhas[0].strip()
                self.query_valores = linhas[1].strip()
                return True
        except FileNotFoundError:
            print(f"ERRO: Arquivo {caminho} não encontrado.")
            return False

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python programa.py <dados.csv> <query.txt> <saida.txt>")
        sys.exit(1)

    arq_dados = sys.argv[1]
    arq_query = sys.argv[2]
    arq_saida = sys.argv[3]

    app = ProcessadorDeConsultas(arq_dados)
    app.executar(arq_query, arq_saida)