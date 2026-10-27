from funcoes import conectar_mongodb
import hashlib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,classification_report
import numpy as np

# Cria um id único baseado na hash de toda a linha
# Formata os dados e cria uma lista de dicionários
def parser_logs(logs: str):
    lista_logs = []
    for log in logs:
        eventId = hashlib.sha256(log.encode("utf-8")).hexdigest()
        log = log.replace("="," ").split()
        doc = {
            "_id":eventId,
            "data":log[0],
            "hora":log[1],
            "status":log[2],
            "usuario":log[4],
            "ip":log[6]}
        lista_logs.append(doc)
    return lista_logs

# Cria o pipeline e retorna uma lista de dicionários que contém IP e total de falhas
def buscar_ips():
    qtd_fails = []
    pipeline = [{"$match": {"status":"FAIL"}},
    {"$group":{"_id":"$ip", "total": {"$sum":1}}},
    {"$sort": {"total":-1}}]

    for doc in logs_colecao.aggregate(pipeline):
        #print(f"{doc['_id']}: {doc['total']} falhas")
        qtd_fails.append({"ip":doc['_id'],"total_falhas":doc['total']})
    return qtd_fails 

# Para cada IP, se houver menos de 5 falhas adiciona 0 ao rótulo e 1 se houver 5 ou mais
def criar_rotulo(qtd_fails):
    rotulo  = []
    for ip in qtd_fails:
        if ip['total_falhas'] >= 5:
            rotulo.append(1)
        else:
            rotulo.append(0)
    return rotulo

# Cria uma lista que contém o total de falhas de cada IP
def criar_label(ips_falhas):
    label = []
    for ip in ips_falhas:
        label.append([ip['total_falhas']])
    return label

# Treina um modelo com dados recebidos
def treinar_modelo(X,y):
    X = np.array(X)
    y = np.array(y)
    
    X_train, X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=42)

    modelo = RandomForestClassifier(n_estimators=100,random_state=42)    
    modelo.fit(X_train,y_train)

    previsao = modelo.predict(X_test)
    acuracia = accuracy_score(y_test,previsao)
    return modelo,acuracia

# Recebe um número e transforma-o em uma array, retorna apenas 0 ou 1
def previsao_ip(modelo,ip_detectado):
    ip_detectado = np.array([[ip_detectado]])
    previsao = modelo.predict(ip_detectado)
    return previsao[0]



db = conectar_mongodb()
logs_colecao = db["logs"]
logs_colecao.create_index("ip")

novos_logs = 0
existentes = 0


try:
    with open("auth2.log","r") as logs:
        lista_logs = parser_logs(logs)

except FileNotFoundError:
    print("O arquivo de log não foi encontrado")     
    

for log_dict in lista_logs:
    resultados = logs_colecao.update_one({"_id":log_dict['_id']},{"$setOnInsert":log_dict},upsert=True)            
    if resultados.upserted_id:
        novos_logs += 1
    else:
        existentes += 1
print(f"Eventos inseridos no MongoDB: {novos_logs} - Eventos já existentes: {existentes}")



label = criar_label(buscar_ips())
rotulo = criar_rotulo(buscar_ips())

print(f"Dataset de treino {label} rótulos {rotulo}")
modelo,acuracia = treinar_modelo(label,rotulo)


novo_caso = 4

resultado = previsao_ip(modelo,novo_caso)


if resultado == 1:
    print(f"Previsão para IP com {novo_caso} falha(s) -> Malicioso ({resultado})")

else:
    print(f"Previsão para IP com {novo_caso} falha(s) -> Não malicioso {resultado}")

print(f"Acurácia do Modelo: {acuracia:.2f}")