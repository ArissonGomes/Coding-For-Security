import mysql.connector
from funcoes import conectar_banco
# Schema esperado:
# ativos(id PK AUTO_INCREMENT, nome, ip UNIQUE, tipo, criticidade ENUM('baixa','media','alta'), status)

# Dados iniciais:
ativos = [
    ("SRV-WEB01", "192.168.1.10", "servidor", "alta",  "ativo"),
    ("PC-RH03",   "192.168.1.45", "estacao",  "baixa", "ativo"),
    ("SW-CORE01", "192.168.1.1",  "switch",   "media", "inativo"),
]
        

# Função que pega as informações do novo ativo, confirma se estão corretas e retorna no formato list
def novo_ativo():
    ativo = []
    criticidade = ['baixa','media','alta']
    ativo.append(input("Digite o nome do ativo: ").strip())
    ativo.append(input("Insira o IP do ativo: ").strip())
    ativo.append(input("Digite o tipo de ativo (Ex: servidor, switch): ").strip())
    
    criticidade_enviada = input("Digite a criticidade do ativo (baixa, media ou alta): ".strip())
    if criticidade_enviada not in criticidade: 
        raise ValueError("Erro! O nível de criticidade deve ser baixa, media ou alta!")
    
    ativo.append(criticidade_enviada)
    ativo.append(input("Digite o status do ativo (Ex: ativo, inativo): ").strip())
    for i in ativo:
        if not i:
            raise ValueError("Erro! Nenhum campo pode ficar vazio")
    confirmacao = input(f"Os dados abaixo estão corretos?\nNome: {ativo[0]}\nIP: {ativo[1]}\nTipo: {ativo[2]}\nCriticidade: {ativo[3]}\nStatus: {ativo[4]}\n[S] Sim [N] Não\nOpção escolhida:")
    if confirmacao.lower() == "s":
        return ativo
    else:
        return 1 

# Função que recebe um dicionário e insere no banco de dados
def inserir_ativo(ativo):
    sql_insercao = """
    INSERT INTO ativos (nome,ip,tipo,criticidade,status) VALUES (%s,%s,%s,%s,%s)
    """
    # Verifica se é uma lista composta
    if isinstance(ativo[0],list):
        cursor.executemany(sql_insercao,ativo)
    else:
        cursor.execute(sql_insercao,ativo)

def buscar_ativo(coluna,conteudo_buscado=None):
    if coluna == "todos":
        cursor.execute(f"SELECT * FROM ativos;")
    else:
        cursor.execute(f"SELECT * FROM ativos WHERE {coluna} = %s",(conteudo_buscado,))
        
    resultado_busca = cursor.fetchall()
    return resultado_busca

def altera_status(ativo,novo_status):
    valida_ativo = buscar_ativo("nome",ativo)
    if valida_ativo:
        cursor.execute("UPDATE ativos SET status = %s WHERE nome = %s",(novo_status,ativo,))
        conexao.commit()
        return 0
    else:
        return 1

def deleta_ativo(ativo):
    valida_ativo = buscar_ativo("nome",ativo)
    if valida_ativo:
        cursor.execute("DELETE FROM ativos WHERE nome = %s",(ativo,))
        return 0
    else:
        return 1
    
# Chama a função de conectar-se ao banco e cria o cursor

conexao = conectar_banco()  
cursor = conexao.cursor(dictionary=True)
    
    
# Executado uma vez para inserir os ativos iniciais na base de dados
#inserir_ativo(ativos)

#Cria tabela ativos se não existir
cursor.execute("""CREATE TABLE IF NOT EXISTS ativos(
id INT PRIMARY KEY AUTO_INCREMENT, 
nome VARCHAR(100) NOT NULL,
ip VARCHAR(50) UNIQUE,
tipo VARCHAR(100) NOT NULL,
criticidade ENUM('baixa','media','alta'),
status VARCHAR(50) NOT NULL)
""")

# Menu principal do programa
while True:
    print("-------------------------------------------------------")
    print("Menu de Gerenciamento de Ativos")
    print("[1] Cadastrar novo ativo")
    print("[2] Listar ativos por tipo") 
    print("[3] Atualizar status do ativo")
    print("[4] Remover ativo")
    print("[5] Sair")
    print("-------------------------------------------------------")   

    opcao_escolhida = input("Opção escolhida: ")

    match opcao_escolhida:
        case "1":
            try:
                ativo = novo_ativo()
                if ativo != 1:
                    inserir_ativo(ativo)
                    conexao.commit()
                    print("Ativo cadastrado com sucesso")
                else:
                    print("Operação mal sucedida")
            except mysql.connector.errors.IntegrityError:
                print("Erro! O IP informado já está cadastrado!")
                conexao.rollback()
            except ValueError as e:
                print(e)
        case "2":
            # Lista contendo as opções disponíveis
            atributos_disponiveis = ['id','nome','ip','tipo','criticidade','status','todos']
            
            print("Deseja buscar ativos por qual atributo?")
            print("Atributos disponíveis: ID | Nome | IP | Tipo | Criticidade | Status | Todos")
            atributo_escolhido = input("Opção escolhida: ").lower()

            # Válida se a opção escolhida é válida
            if atributo_escolhido in atributos_disponiveis:
                # Atributo válido que não seja todos (A query para todos é diferente)
                if atributo_escolhido != "todos":
                    valor_escolhido = input(f"Digite o valor de {atributo_escolhido} que será buscado: ")
                    resultados = buscar_ativo(atributo_escolhido,valor_escolhido)
                else:
                    resultados = buscar_ativo("todos")    

                if resultados:
                        # Alinha os atributos com os valores
                        print(f"{'ID':<5} {'Nome':<15} {'IP':<16} {'Tipo':<12} {'Criticidade':<14} {'Status':<12}")
                        for i in resultados:
                            print(f"{i['id']:<5} {i['nome']:<15} {i['ip']:<16} {i['tipo']:<12} {i['criticidade']:<14} {i['status']:<12}")
                else:
                        print("A busca realizada não encontrou resultados!")
                 

            else:
                print("Opção inválida! Por favor, escolha um atributo válido!")            

        case "3":
            ativo = input("Digite o ativo que será alterado: ")
            novo_status = input(f"Digite o novo status de {ativo}: ")
            retorno = altera_status(ativo,novo_status)
            if retorno == 0:
                print("1 registro atualizado")
            elif retorno == 1:
                print("O ativo não foi encontrado na base de dados!")

        case "4":
            ativo_deletado = input("Digite o nome do ativo que será deletado: ")
            confirmar_remocao = input(f"Deseja realmente deletar {ativo_deletado} das bases de dados?\n[S] Sim - [N]").lower()
            if confirmar_remocao == "s":
                retorno = deleta_ativo(ativo_deletado)
                if retorno == 0:
                    print(f"Ativo {ativo_deletado} removido com sucesso!")
                else:
                    print(f"O ativo não existe ou já foi deletado anteriormente!")
            else:
                print("Operação cancelada!")
        case "5":
            print("Saindo do programa!")
            conexao.close()
            break

# Saída esperada:
# Listar tipo='servidor' -> SRV-WEB01 | 192.168.1.10 | alta | ativo
# Após UPDATE status de SW-CORE01 para 'ativo' -> "1 registro atualizado"
# Inserir IP duplicado (192.168.1.10) -> erro de UNIQUE tratado