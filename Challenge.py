import oracledb
import pwinput
import requests


def menu():
    opcao = int(input("Digite: \n(1) Para fazer o cadastro \n(2) Para realizar o seguro da bike" +
        "\n(3) Para sair do atendimento \nOpção: "))
    return opcao

def cadastro():
    try:
        print("Você selecionou a opção 1 - fazer o cadastro \nA seguir temos um formulário para realizar o cadastro:")
        nome = input("\nDigite seu nome completo: ")
        idade = int(input("Digite sua idade: "))
        if idade >= 18:
            cpf = input("Digite seu CPF: ")
            telefone = input("Digite seu telefone: ")
            email = input("Digite seu email: ")
            cep = input("Digite seu cep: ")
            url = f'https://viacep.com.br/ws/{cep}/json/'

            resposta = requests.get(url)        # realiza a requisição

            if resposta.status_code == 200:     # código 200 - Sucesso 
                dados = resposta.json()         # converte o texto de resposta para um dicionario

                if 'erro' in dados: 
                    print('O CEP informado não foi encontrado')
                else:
                    # acessa dados do dicionário
                    endereco = f'Bairro: {dados["bairro"]}'

                    print("\nNome: " + nome  + "\nIdade: " + str(idade) + "\nCPF: " + cpf
                        + "\nTelefone: " + telefone + "\nEmail: " +  email + "\nEndereco: " + endereco) 

                    cadastro = f"""INSERT INTO CLIENTE (cpf_clien, tel_clien, nm_clien , idade_clien, endereco_clien, email_clien) 
                    VALUES ('{cpf}', '{telefone}', '{nome}', {idade}, '{endereco}', '{email}')"""

                    # Executa e grava o registro na Tabela
                    cursor.execute(cadastro)
                    conn.commit()
                    print("\nParabéns, cadastro concluído!!")
                    return True


            elif resposta.status_code == 400:   # código 400 - Erro
                # código 400 - ERRO
                print('O cep não possui 8 caracteres')
            else:
                print(resposta.status_code)

        else:
             print("\nApenas maior de idade")

    except ValueError:
        print("\nDigite um número inteiro para a idade!")
    except:
        print("\nErro na transação do BD")

def seguro ():
        try:
            print("\nVocê selecionou a opção 2 - realizar o seguro da bike")
            print("\nOlá estamos felizes com seu interesse pelo seguro de bikes. A seguir temos umas perguntas para serem feitas:  ")

            marca = input("\nQual a marca da sua bike: ")
            tipo = input("Qual o tipo do sua bike: ")
            material = input("Qual o material da sua bike: ")
            peso = input("Qual o peso da sua bike: ")
            valor_bike = float(input("Qual o valor da sua bike: "))

            # Monta a instrução SQL de cadastro em uma string
            cadastro2 = f"""INSERT INTO BICICLETA (peso, preco, marca, tipo, material) 
            VALUES ({peso}, {valor_bike}, '{marca}', '{tipo}', '{material}')"""

            # Executa e grava o registro na Tabela
            cursor.execute(cadastro2)
            conn.commit()

            print("\nSeguro realizado com sucesso")

            return seguro

        except Exception as erro:
            print(erro)
def sair ():
    print("\nVocê selecionou a opção 5 - sair do atendimento")
    print("Espero ter ajudado. Até mais!")
    return sair
# Tentativa de Conexão com o Banco de Dados
conexao = False

while not conexao:
    try:
        # Credenciais de Acesso (usuário e senha)
        usuario = input('\nInforme de Usuário: ')
        senha = pwinput.pwinput('Informe a senha: ')

        # Conexão com o banco de dados
        conn = oracledb.connect(user=usuario, 
                                password=senha, 
                                host="oracle.fiap.com.br", 
                                port=1521, 
                                service_name="ORCL")
        # Cria o cursor para realizar as operações no banco de dados
        cursor = conn.cursor()

    
    except Exception as erro:
        print(f"Erro: {erro}")      # Informa o erro
        print("\nCredenciais incorretas. Tente novamente.")
        conexao = False             # Flag para não executar a Aplicação
    else:
        conexao = True              # Flag para executar a Aplicação

while conexao:
    try:
        #Apresentação
        print("\nOlá, seja bem-vindo(a) ao sistema de seguro de bicicleta da Porto Seguro!")

        #Chamada do menu
        resposta = menu()

        if resposta == 1:
            #Cadastro
            cad = cadastro()
            
        elif resposta == 2:
            # Seguro da bike
            try:
                if cad:
                    seguro()
                else:
                    print("\nFaça o cadastro primeiro")

            except ValueError:
                print("\nFormato invalido (somente numeros)")
            except NameError:
                print("\nFaça o cadastro primeiro")

        elif resposta == 3:
            # Sair do atendimento
            sair()
            break
        else:
            # Mensagem de erro para opções inválidas
            print("\nOpção inválida. Por favor, selecione uma opção válida do menu.")
    except ValueError:
        print("\nOpção inválida. Por favor, selecione uma opção válida do menu.")

