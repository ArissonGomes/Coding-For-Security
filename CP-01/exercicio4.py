from funcoes import conectar_banco

usuarios = [("admin","admin@x.com"), ("ana","ana@x.com"), ("bruno","bruno@x.com")]
entrada = "' OR '1'='1"

# Saída esperada:
# [INSEGURO] entrada=' OR '1'='1  -> 3 usuários (VAZAMENTO)
# [SEGURO]   entrada=' OR '1'='1  -> 0 usuários (defesa OK)     

def consulta_insegura(busca):
    cursor.execute(f"SELECT * FROM usuarios_cp WHERE nome = '{busca}'")
    resultado = cursor.fetchall()
    return resultado

def consulta_segura(busca):
    cursor.execute("SELECT * FROM usuarios_cp WHERE nome = %s",(busca,))
    resultado = cursor.fetchall()
    return resultado

def verifica_quantidade(resultado):
    if len(resultado) > 1:
        print(f"[INSEGURO] Entrada: {entrada} -> {len(resultado)} usuários (VAZAMENTO)")
    else:
        print(f"[SEGURO] Entrada: {entrada} -> {len(resultado)} usuários (Defesa OK)")


conexao = conectar_banco()
cursor = conexao.cursor()

verifica_quantidade(consulta_insegura(entrada))
verifica_quantidade(consulta_segura(entrada))

# Executado uma vez para inserir os usuário no banco de dados
#for usuario in usuarios:
 #   cursor.execute(f"INSERT INTO usuarios_cp (nome,email) VALUES (%s,%s)",usuario)
  #  conexao.commit()
