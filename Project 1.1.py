# IMPORTAR BIBLIOTECAS
import csv
import pandas as pd

# 1: Menu de escolha

def menu():
    print("+","-" *22,"+")
    print("| Gerenciamento de Epi's |")
    print("+","-" *22,"+ \n")


    print("1 -> Cadastrar Nova Epi     ")
    print("-" *26)
    print("2 -> Listar Epi's Cadastradas")
    print("-" *26)
    print("3 -> Remover Epi's por quantidade")
    print("-" *26)
    print("4 -> Remover Todas as Epi's ")
    print("-" *26)

# 2: Cadastramento de Epis
def cadastro():
    nome = input("Digite o Nome da Epi: ")
    idCodigo = int(input("Digite o Código da Epi (Apenas Números): "))
    qtd = int(input("Digite a quantidade (Apenas Números): "))

    lista_de_cadastro = {
        "Nome": nome,
        "Codigo": idCodigo,
        "Quantidade": qtd
    }

    arquivo_cadastro = "cadastro.csv"
    with open(arquivo_cadastro, mode="a", newline='') as arquivo_csv:
        columns_Name = ["Nome", "Codigo", "Quantidade"]
        writer = csv.DictWriter(arquivo_csv, fieldnames=columns_Name)

        if arquivo_csv.tell() == 0:
            writer.writeheader()
        writer.writerow(lista_de_cadastro)


# 3: Listagem de Apis cadastradas
def listagem():
    print("1 - Consultar Epi por código")
    print("2 - Consultar Todas as Epi's\n")

    escolha = int(input("Qual opção? "))

    if escolha == 1:
        id_codigo = int(input("Digite o código do produto: "))
        read = pd.read_csv('cadastro.csv', encoding='ISO-8859-1')
        epi = read[read['Codigo'] == id_codigo]
        if not epi.empty:
            print(epi)
        else:
            print("Nenhum Epi encontrado com o código informado!")
    elif escolha == 2:
        read = pd.read_csv('cadastro.csv', encoding='ISO-8859-1')
        print(read)


# 4: Remover Epis por quantidade
def remove_por_quantidade():
    id_codigo = int(input("Digite o código do Epi que deseja remover: "))
    quantidade = int(input("Digite a quantidade que deseja remover: "))

    arquivo_csv = "cadastro.csv"
    dados_atualizados = []

    with open(arquivo_csv, mode="r", newline='') as arquivo_leitura:
        reader = csv.DictReader(arquivo_leitura)

        for linha in reader:
            if int(linha["Codigo"]) == id_codigo:
                nova_quantidade = int(linha["Quantidade"]) - quantidade
                if nova_quantidade <= 0:
                    print("A quantidade a ser removida é maior do que a quantidade disponível.")
                    continue
                linha["Quantidade"] = nova_quantidade
            dados_atualizados.append(linha)

    with open(arquivo_csv, mode="w", newline='') as arquivo_escrita:
        columns_name = ["Nome", "Codigo", "Quantidade"]
        writer = csv.DictWriter(arquivo_escrita, fieldnames=columns_name)
        writer.writeheader()

        for dados in dados_atualizados:
            writer.writerow(dados)


# 5: Remover todas Epis
def remover_todas_epis():
    arquivo_csv = "cadastro.csv"
    open(arquivo_csv, 'w').close() # Isso sobrescreve o arquivo, removendo todos os dados

# Escopo principal
if not menu()  == None:
  print(menu())

escolha = int(input("Digite a opção correspondente com a numeração: "))

if escolha == 1:
   cadastro()

if escolha == 2:
   listagem()

if escolha == 3:
    remove_por_quantidade()

if escolha == 4:
    remover_todas_epis()
    print("Todos os Epis foram removidos com sucesso!")
