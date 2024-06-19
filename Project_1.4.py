import pandas as pd
import time
import os
import sys
from openpyxl import load_workbook


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
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="")
        sys.stdout.flush()
    sys.exit()


# Menu de escolha
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
            atencao = input("Remover todas as Epis cadastradas? (sim ou não) ").strip().lower()
            if atencao == "sim":
                remover_todas_epis()
                print("Todos os Epis foram removidos com sucesso!")
                time.sleep(1.5)
            else:
                print("Voltando para o Menu", end="")
                for _ in range(3):
                    time.sleep(0.5)
                    print(".", end="")
                    sys.stdout.flush()
                print("")
        elif escolha == 5:
            encerrarPrograma()
        else:
            print("Opção não identificada")
            continue


# Função para ler dados do arquivo Excel
def ler_dados_excel():
    try:
        return pd.read_excel('cadastro.xlsx')
    except FileNotFoundError:
        return pd.DataFrame(columns=["Nome", "Codigo", "Quantidade"])


# Função para salvar dados no arquivo Excel e ajustar a largura das colunas
def salvar_dados_excel(df):
    with pd.ExcelWriter('cadastro.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    ajustar_largura_colunas('cadastro.xlsx')


# Função para ajustar a largura das colunas
def ajustar_largura_colunas(file_path):
    wb = load_workbook(file_path)
    ws = wb.active

    for column in ws.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column[0].column_letter].width = adjusted_width

    wb.save(file_path)


# Cadastramento de Epis
def cadastro():
    nome = input("Digite o Nome da Epi: ")
    nEpi = " ".join(word.capitalize() for word in nome.split())

    while len(nEpi) <= 1:
        print("Epi Inválida!")
        nome = input("Digite o Nome da Epi: ")
        nEpi = " ".join(word.capitalize() for word in nome.split())

    while True:
        try:
            idCodigo = int(input("Digite o Código da Epi (Apenas Números): "))
            break
        except ValueError:
            print("Entrada inválida. Por favor, digite números.")

    df = ler_dados_excel()
    if not df[df['Codigo'] == idCodigo].empty:
        print("Atenção!! Esse código já está atribuído a uma Epi.")
        return

    while True:
        try:
            qtd = int(input("Digite a quantidade (Apenas Números): "))
            break
        except ValueError:
            print("Quantidade inválida! Por favor indique uma quantidade.")

    novo_cadastro = pd.DataFrame([{
        "Nome": nEpi,
        "Codigo": idCodigo,
        "Quantidade": qtd
    }])

    df = pd.concat([df, novo_cadastro], ignore_index=True)
    salvar_dados_excel(df)

    print("Registrando Epi", end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="")
        sys.stdout.flush()
    time.sleep(0.7)
    print("\nEpi registrada com sucesso!")
    time.sleep(1.5)


# Listagem de Epis cadastradas
def listagem():
    print("1 - Consultar Epi por código")
    print("2 - Consultar Todas as Epi")

    try:
        escolha = int(input("Qual opção? "))
        df = ler_dados_excel()

        if escolha == 1:
            id_codigo = int(input("Digite o código do produto: "))
            epi = df[df['Codigo'] == id_codigo]
            if not epi.empty:
                print(epi)
            else:
                print("Nenhum Epi encontrado com o código informado!")
        elif escolha == 2:
            print(df)
        else:
            print("Opção inválida. Escolha 1 ou 2.")
            return

        continuar = input("\nTecle ENTER para voltar para o Menu Inicial. ")
        if continuar == "":
            print("Voltando para tela inicial..")
            time.sleep(1.2)
        else:
            print("Voltando para tela inicial..")
            time.sleep(1.2)

    except pd.errors.EmptyDataError:
        print("\nArquivo de cadastro vazio ou não contém dados válidos.")
        time.sleep(1.5)
    except FileNotFoundError:
        print("\nArquivo de cadastro não encontrado.")
        time.sleep(1.5)
    except Exception as e:
        print(f"\nOcorreu um erro ao ler o arquivo: {e}")
        time.sleep(1.5)


# Remover Epis por quantidade
def remove_por_quantidade():
    try:
        print("Se certifique das informações antes de remover as Epis")
        time.sleep(3.5)
        id_codigo = int(input("Digite o código da Epi que deseja remover: "))
        nome = input("Digite o nome da Epi: ")
        nEpi = " ".join(word.capitalize() for word in nome.split())
        quantidade = int(input("Digite a quantidade que deseja remover: "))

        df = ler_dados_excel()
        epi = df[(df['Codigo'] == id_codigo) & (df['Nome'] == nEpi)]

        if not epi.empty:
            nova_quantidade = epi['Quantidade'].values[0] - quantidade
            if nova_quantidade < 0:
                print(f"A quantidade a ser removida é maior do que a quantidade disponível.")
            elif nova_quantidade == 0:
                df = df[~((df['Codigo'] == id_codigo) & (df['Nome'] == nEpi))]
                print(f"A quantidade da EPI {nEpi} chegou a zero e foi removida do cadastro.")
            else:
                df.loc[(df['Codigo'] == id_codigo) & (df['Nome'] == nEpi), 'Quantidade'] = nova_quantidade
                print("\nEpi removida com sucesso!")
            salvar_dados_excel(df)
            time.sleep(1.5)
        else:
            print("Epi não identificada")
            time.sleep(3)
    except ValueError:
        print("Ação Inválida")


# Remover todas Epis
def remover_todas_epis():
    df = pd.DataFrame(columns=["Nome", "Codigo", "Quantidade"])
    salvar_dados_excel(df)


# Escopo principal
menu()
