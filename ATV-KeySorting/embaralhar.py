# arquivo usado para gerar um arquivo de entrada de teste para o keysorting
import random
import csv

def embaralha_chaves(input_csv, output_txt):
    sort = ['Q', 'M', 'H', 'I']
    order = ['C', 'D']

    # escolhe aleatoriamente
    random_sort = random.choice(sort)
    random_order = random.choice(order)

    # cria o header
    header = f"SORT={random_sort}|ORDER={random_order}"

    with open(input_csv, 'r', newline='', encoding='utf-8') as arq:
        reader = csv.reader(arq)
        header_row = next(reader)  # Skipa o header original
        linhas = list(reader)
        registros = len(linhas)

    with open(output_txt, 'w', newline='', encoding='utf-8') as txt_saida:
        txt_saida.write(header + '\n')  # novo header

        # escrevendo registros
        for pos, linha in enumerate(linhas):
            key = random.randint(0, registros -1)
            # juntando os campos e delimitando com |
            nova_linha = f"{key}|{'|'.join(linha)}\n"
            txt_saida.write(nova_linha)

input_csv = input("Digite o caminho do arquivo CSV: ").strip()
output_txt = 'input1.txt'

embaralha_chaves(input_csv, output_txt)

print(f"Arquivo '{output_txt}' gerado com sucesso.")
    
        