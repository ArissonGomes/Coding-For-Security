from funcoes import conectar_mongodb

db = conectar_mongodb()
eventos_colection = db["eventos"]

eventos = [
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
#Garante que o número de dados irá manter-se o mesmo em cada execução (60 eventos), utilizarei a mesma coleção em outros exercícios 
eventos_colection.delete_many({})
eventos_colection.insert_many(eventos)

#Criação do pipeline
pipeline = [{"$match": {"tipo":"FAIL"}},
            {"$group": {"_id":"$ip", "total_eventos": {"$sum":1}}},
            {"$sort": {"total_eventos": -1}},
            {"$limit": 3}
            ]

for doc in eventos_colection.aggregate(pipeline):
    print(f"{doc['_id']} -> {doc['total_eventos']}")

# Saída esperada:
# 185.220.101.1 -> 4
# 91.240.118.172 -> 2
# 45.33.32.156  -> 1

