# IMPORTAR BIBLIOTECAS
import csv
import pandas as pd
import shutil
# 1: Menu de escolha

def menu():
    print("+","-" *22,"+")
    print("| Gerenciamento de Epi's |")
    print("+","-" *22,"+ \n")


    print("1 -> Cadastrar Nova Epi     ")
    print("-" *26)
    print("2 -> Listar Epi's Cadastradas")
    print("-" *26)
    print("3 -> Remover Epi's          ")
    print("-" *26)

# 2: Cadastramento de Epis
def cadastro():
    nome = input("Digite o Nome da Epi: ")
    idCodigo = int(input("Digite o Código da Epi (Apenas Números): "))
    qtd = int(input("Digite a quantidade (Apenas Números): "))

    lista_de_cadastro = {
        "Nome": nome,
        "Codigo": idCodigo,
        "Quantidade": qtd}

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
        epi = read[read['Codigo'] == id_codigo] #chamo o arquivo e indico a coluna para comparação com
        # o código que será inserido pelo user para a listagem da epi
        if not epi.empty: #verifica se o campo do código existe / se está vazio
            print(epi)
        else:
            print("Nenhum Epi encontrado com o código informado!") #se estiver vazio, essa mensagem
            2# será exibida
    elif escolha == 2:
        read = pd.read_csv('cadastro.csv', encoding='ISO-8859-1')
        print(read)


# 4: Remover Epis
def remove(criterio):
      arquivo_csv = "cadastro.csv"
      dados_mantidos = []

      with open(arquivo_csv, mode="r", newline='') as arquivo_leitura:
          reader = csv.DictReader(arquivo_leitura)

          for linha in reader:
              if linha["Nome"] != criterio:
                  dados_mantidos.append(linha)

      with open(arquivo_csv, mode="w", newline='') as arquivo_escrita:
          columns_name = ["Nome", "Codigo", "Quantidade"]
          writer = csv.DictWriter(arquivo_escrita, fieldnames=columns_name)
          writer.writeheader() #é usado para escrever a linha de cabeçalho no arquivo CSV.

          for dados in dados_mantidos:
              writer.writerow(dados) #é usado para escrever uma única linha de dados em um arquivo CSV.



#Escopo principal
if not menu()  == None:
  print(menu())

escolha = int(input("Digite a opção correspodente com a numeração: "))

if escolha == 1:
   cadastro()

if escolha == 2:
   listagem()

if escolha == 3:
    remover_dado = input("Digite o Nome da Epi que deseja remover: ")
    remove(remover_dado)







