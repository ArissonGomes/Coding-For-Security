from funcoes import conectar_mongodb
from copy import deepcopy

db = conectar_mongodb()
colecao_eventos = db['eventos']


eventos = [ #60 eventos
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "OK",   "ip": "192.168.1.10"},
    {"tipo": "FAIL", "ip": "91.240.118.172"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "FAIL", "ip": "91.240.118.172"},
    {"tipo": "FAIL", "ip": "45.33.32.156"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "OK",   "ip": "192.168.1.15"},
    {"tipo": "FAIL", "ip": "103.21.244.0"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "FAIL", "ip": "45.33.32.156"},
    {"tipo": "OK",   "ip": "192.168.1.20"},
    {"tipo": "FAIL", "ip": "91.240.118.172"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "FAIL", "ip": "103.21.244.0"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "OK",   "ip": "192.168.1.10"},
    {"tipo": "FAIL", "ip": "45.33.32.156"},
    {"tipo": "FAIL", "ip": "91.240.118.172"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "OK",   "ip": "192.168.1.25"},
    {"tipo": "FAIL", "ip": "103.21.244.0"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "FAIL", "ip": "91.240.118.172"},
    {"tipo": "FAIL", "ip": "45.33.32.156"},
    {"tipo": "OK",   "ip": "192.168.1.15"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "FAIL", "ip": "103.21.244.0"},
    {"tipo": "FAIL", "ip": "91.240.118.172"},
    {"tipo": "OK",   "ip": "192.168.1.30"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "FAIL", "ip": "45.33.32.156"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "OK",   "ip": "192.168.1.20"},
    {"tipo": "FAIL", "ip": "91.240.118.172"},
    {"tipo": "FAIL", "ip": "103.21.244.0"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "FAIL", "ip": "45.33.32.156"},
    {"tipo": "OK",   "ip": "192.168.1.10"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "FAIL", "ip": "91.240.118.172"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "OK",   "ip": "192.168.1.35"},
    {"tipo": "FAIL", "ip": "103.21.244.0"},
    {"tipo": "FAIL", "ip": "45.33.32.156"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "OK",   "ip": "192.168.1.25"},
    {"tipo": "FAIL", "ip": "91.240.118.172"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "FAIL", "ip": "103.21.244.0"},
    {"tipo": "OK",   "ip": "192.168.1.15"},
    {"tipo": "FAIL", "ip": "45.33.32.156"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "FAIL", "ip": "91.240.118.172"},
    {"tipo": "OK",   "ip": "192.168.1.40"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "FAIL", "ip": "103.21.244.0"},
    {"tipo": "FAIL", "ip": "45.33.32.156"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "OK",   "ip": "192.168.1.30"},
]

colecao_eventos.delete_many({})
for i in range(17): #Irá inserir os 60 eventos 17 vezes, totalizando 1020 eventos
    colecao_eventos.insert_many(deepcopy(eventos)) #Faz o mongodb criar um _id único para cada evento

#colecao_eventos.create_index({"ip",1}) # Cria o Index com o campo ip


ip_procurado = input("Digite o IP procurado: ")
numero_eventos =  colecao_eventos.count_documents({"ip":ip_procurado})
print(f"Eventos do IP {ip_procurado}: {numero_eventos} eventos")

# Sem índice, o MongoDB iria procurar pelo IP em cada documento. 1000 documentos = Até 1000 buscas. O(n)
# Com índice, os dados podem ser ordenados de uma forma que reduza a quantidade de buscas. Por exemplo, 1000 documentos podem ser buscados em até 10 consultas. O(log n)