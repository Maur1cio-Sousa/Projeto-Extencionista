# IMPORTAR BIBLIOTECAS
import csv
import pandas as pd
import time
import os, sys, keyboard


# Função apagar tela
def apagarTela():
    sistemaOperacional = os.name
    if sistemaOperacional == "nt" or sistemaOperacional == "windows":
        os.system("cls")
    else:
        os.system("clear")


# Função Encerrar Programa
def encerrarPrograma():
    print("Encerrando Programa", end="")
    for i in range(3):
        time.sleep(0.5)
        print(".", end="")
        sys.stdout.flush()

# 1: Menu de escolha
def menu():
    while True:
        apagarTela()
        print("+", "-" * 22, "+")
        print("| Gerenciamento de Epi's |")
        print("+", "-" * 22, "+ \n")

        print("1 -> Cadastrar Nova Epi     ")
        print("-" * 26)
        print("2 -> Listar Epi's Cadastradas")
        print("-" * 26)
        print("3 -> Remover Epi's por quantidade")
        print("-" * 26)
        print("4 -> Remover Todas as Epi's")
        print("-" * 26)
        print("5 -> Encerrar Programa")
        print("-" * 26)
        try:
            escolha = int(input("Digite a opção correspondente com a numeração: "))
            print(" ")
        except ValueError:
            print("\nOpção Inválida! Digite uma opção de 1 a 5")
            time.sleep(1.5)
            continue
        if escolha == 1:
            cadastro()

        elif escolha == 2:
            listagem()

        elif escolha == 3:
            remove_por_quantidade()

        elif escolha == 4:
            atencao = input("Remover todas as Epis cadastradas ? (sim ou não) ").strip().lower()
            if atencao == "sim":
                remover_todas_epis()
                print("Todos os Epis foram removidos com sucesso!")
                time.sleep(1.5)
            else:
                print("Voltando para o Menu", end="")
                for i in range(3):
                    time.sleep(0.5)
                    print(".", end="")
                    sys.stdout.flush()
                print("")

        elif escolha == 5:
            encerrarPrograma()
            break
        else:
            print("Opção não identificada")
            continue

# 2: Cadastramento de Epis
def cadastro():
    # Nome Epi
    nome = input("Digite o Nome da Epi: ").capitalize()
    while len(nome) <= 1:
        print("Epi Inválida!")
        nome = input("Digite o Nome da Epi: ").capitalize()

    # Codigo Epi
    while True:
        try:
            idCodigo = int(input("Digite o Código da Epi (Apenas Números): "))
            break  # Sai do loop se a entrada for um número válido
        except ValueError:
            print("Entrada inválida. Por favor, digite números.")

    arquivo_cadastro = "cadastro.csv"
    if os.path.exists(arquivo_cadastro):
        with open(arquivo_cadastro, mode="r", newline='') as arquivo_csv:
            reader = csv.DictReader(arquivo_csv)
            for linha in reader:
                if int(linha["Codigo"]) == idCodigo:
                    print("Atenção!! Esse código já está atribuído a uma Epi.")
                    return  # Retorna para interromper o cadastro caso o código já esteja em uso
    # Quantidade
    while True:
        try:
            qtd = int(input("Digite a quantidade (Apenas Números): "))
            break
        except ValueError:
            print("Quantidade inválida! Por favor indique uma quantidade.")

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

    print("Registrando Epi", end="")
    for i in range(3):
        time.sleep(0.5)
        print(".", end="")
        sys.stdout.flush()
    time.sleep(0.7)
# 3: Listagem de Apis cadastradas
def listagem():
    print("1 - Consultar Epi por código")
    print("2 - Consultar Todas as Epi")

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

    continuar = input("\nTecle ENTER para voltar para o Menu Inicial. ")
    if continuar == "":
        print("Voltando para tela inicial..")
        time.sleep(1.3)

    else:
        print("Voltando para tela inicial..")
        time.sleep(1.3)


# 4: Remover Epis por quantidade
def remove_por_quantidade():
    print("Se certifique das informações antes de remover as Epis")
    time.sleep(4.5)
    id_codigo = int(input("Digite o código do Epi que deseja remover: "))
    quantidade = int(input("Digite a quantidade que deseja remover: "))
    nome = input("Digite o nome da Epi: ")

    arquivo_csv = "cadastro.csv"
    dados_atualizados = []

    with open(arquivo_csv, mode="r", newline='') as arquivo_leitura:
        reader = csv.DictReader(arquivo_leitura)

        for linha in reader:
            if int(linha["Codigo"]) == id_codigo:
                if str(linha["Nome"]) == nome:
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
    open(arquivo_csv, 'w').close()  # Isso sobrescreve o arquivo, removendo todos os dados


# Escopo principal

menu()
