from funcoes import conectar_banco

def transferencia_saldo(usuario1,usuario2,valor_transferencia):
    saldo_atual1 = buscar_saldo(usuario1)
    novo_saldo1 = saldo_atual1 - valor_transferencia
    cursor.execute("UPDATE contas_financeiras SET saldo = %s WHERE titular = %s",(novo_saldo1,usuario1))
    
    saldo_atual2 = buscar_saldo(usuario2)
    if saldo_atual2:   
        novo_saldo2 = saldo_atual2 + valor_transferencia
        cursor.execute("UPDATE contas_financeiras SET saldo = %s WHERE titular = %s",(novo_saldo2,usuario2))
        conexao.commit()
        return buscar_saldo(usuario1), buscar_saldo(usuario2),0
    else:
        conexao.rollback()
        return buscar_saldo(usuario1), buscar_saldo(usuario2),1 


def buscar_saldo(usuario):
    cursor.execute("SELECT titular,saldo FROM contas_financeiras WHERE titular = %s",(usuario,))
    saldo_atual = cursor.fetchone()
    #print(saldo_atual)
    if saldo_atual:
        return saldo_atual[1]
    else:
        return False

conexao = conectar_banco()
cursor = conexao.cursor()

# Tabela: contas(id, titular, saldo)
contas = [(1, "Alice", 1000), (2, "Bob", 500)]

print("-" * 100)
print("Serviço de transferência de valores")
print("-" * 100)

usuario1 = input("Digite o nome de usuário da conta debitada: ")

saldo_atual = buscar_saldo(usuario1)
if saldo_atual:
    print(f"Saldo atual do usuário {usuario1}: R${saldo_atual}")
else:
    print(f"O usuário {usuario1} não foi encontrado na base de dados")
    exit()

valor_transferencia = int(input("Digite o valor que será debitado: "))
usuario2 = input("Digite o nome do usuário que receberá o valor: ")

valores_atualizados = transferencia_saldo(usuario1,usuario2,valor_transferencia)
#print(valores_atualizados)
if valores_atualizados[2] == 0:
    print(f"Transferência bem sucedida! Valores atuais: {usuario1} = R${valores_atualizados[0]} | {usuario2} = R${valores_atualizados[1]}")
else:
    print(f"Operação Mal sucedida! Saldo de {usuario1} inalterado\nValor disponível = R${valores_atualizados[0]}")
#Executado uma vez para inserir dados
#cursor.executemany("INSERT INTO contas_financeiras (id,titular,saldo) VALUES (%s,%s,%s)",contas)
#conexao.commit()
#print("Transação bem sucedida")


# Cenário de teste:
# Transferir 200 de Alice para Bob      -> commit, saldos: Alice=800, Bob=700
# Transferir 100 de Alice para conta 99 -> rollback, saldos INALTERADOS: Alice=800

# Saída esperada:
# Transferência 1 OK. Alice=800, Bob=700
# Transferência 2 FALHOU (conta destino inexistente). Rollback. Alice=800