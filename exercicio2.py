from funcoes import conectar_mongodb
from pymongo.errors import DuplicateKeyError

db = conectar_mongodb()
vulnerabilidades = db["vulnerabilidades"]
vulnerabilidades.create_index("cve_id",unique=True)

def inserir_banco(vuln):
    if isinstance(vuln,dict):
        vulnerabilidades.insert_one(vuln)

    else:
        vulnerabilidades.insert_many(vuln)


vulns = [
    {"cve_id": "CVE-2024-001", "tipo": "SQL Injection", "severidade": "Alta",  "corrigida": False},
    {"cve_id": "CVE-2024-002", "tipo": "XSS",           "severidade": "Media", "corrigida": True},
    {"cve_id": "CVE-2024-003", "tipo": "Path Traversal","severidade": "Critica","corrigida": False},
]

while True:
    print("-" * 100)
    print("Menu de Gerenciamento de Vulnerabilidades")
    print("-" * 100)
    print("Opções disponíveis:")
    print("[1] Inserir nova vulnerabilidade")
    print("[2] Buscar por severidade")
    print("[3] Atualizar status de uma vulnerabilidade")
    print("[4] Deletar vulnerabilidade")
    print("[5] Sair")
    opcao_escolhida = input("Opção escolhida: ")

    match opcao_escolhida:
        case "1":
            nova_vuln = {}
            nova_vuln["cve_id"] = input("Insira o ID da CVE: ")
            nova_vuln["tipo"] = input("Insira o tipo de vulnerabilidade: ")
            nova_vuln["severidade"] = input("Insira a severidade da vulnerabilidade: ")
            corrigida = input("A vulnerabilidade já foi corrigida?\n[S] Sim [N] Não")
            while corrigida.lower() != "s" and corrigida.lower() != "n":
                if corrigida.lower() == "s":
                    nova_vuln["corrigida"] = True
                elif corrigida.lower() == "n":
                    nova_vuln["corrigida"] = False
                else:
                    corrigida = input("Opção inválida. A vulnerabilidade foi corrigida? [S] Sim [N] Não\nOpção escolhida: ")
            try:
                inserir_banco(nova_vuln)
                print("Inserção bem sucedida!")
            except DuplicateKeyError:
                print("Erro! A CVE já foi cadastrada na base de dados")

        case "2":
            niveis = {"c":"Critica","a":"Alta","m":"Media","b":"Baixa"}
            nivel_severidade = input("Deseja buscar por qual nível de severidade?\n[C] Crítica [A] Alta [M] Média [B] Baixa")
            if nivel_severidade in niveis:
                nivel_severidade = niveis[nivel_severidade.lower()]
                print(f"Buscando todas as vulnerabilidades com a severidade {nivel_severidade}")
                for doc in vulnerabilidades.find({'severidade':nivel_severidade}):
                    print(f"{doc['cve_id']}: {doc['tipo']}")

            else:
                print("Por favor, escolha um nível de criticidade válido")

        case "3":
            vulnerabilidade_alterada = input("Digite o CVE ID da vulnerabilidade que será alterado: ")
            status_atual = vulnerabilidades.find_one({'cve_id':vulnerabilidade_alterada})
            if status_atual:
                if status_atual['corrigida'] == True:
                    vuln_corrigida = input(f"A vulnerabilidade com o ID {vulnerabilidade_alterada} já está corrigida. Deseja alterar? [S] Sim [N] Não")
                    if vuln_corrigida.lower() == "s":
                        vulnerabilidades.update_one({'cve_id':vulnerabilidade_alterada},{"$set":{'corrigida':False}})
                        print(f"OK Novo status da vulnerabilidade: Não Corrigida")
                    else:
                        print("Vulnerabilidade não alterada")
                    
                elif status_atual['corrigida'] == False:
                    vulnerabilidades.update_one({'cve_id':vulnerabilidade_alterada},{'$set':{'corrigida':True}})
                    print("OK Novo status da vulnerabilidade: Corrigida")
                
                resultado = vulnerabilidades.find({'corrigida':False})
                print(f"Número de vulnerabilidades não corrigidas: {len(resultado)}")

                for doc in resultado:
                    print(f"{doc['cve_id']} {doc['tipo']} {doc['severidade']}")

            else:
                print("A CVE não foi encontrada na base de dados")

        case "4":
            vulnerabilidade_deletada = input("Digite o CVE-ID que será deletado: ")
            resultado = vulnerabilidades.find_one_and_delete({'cve_id':vulnerabilidade_deletada})
            if resultado:
                print("CVE deletada com sucesso!")

            else:
                print("A CVE não foi encontrada na base de dados!")

        case "5":
            print("Saindo do programa")
            exit()
# Saída esperada:
# Buscar severidade='Alta'      -> CVE-2024-001: SQL Injection
# update corrigida=True em 001  -> "1 documento modificado"
# count corrigida=False         -> 1 (só a CVE-2024-003 restou aberta)