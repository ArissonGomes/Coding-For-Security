from sklearn.ensemble import IsolationForest
import numpy as np

# [requisicoes_min, conexoes_simultaneas]
trafego = np.array([
    [100,5],[120,6],[110,5],[105,4],[50000,500],[109,5],[111,6],[45000,450],
])
# Dica: IsolationForest(contamination=0.25, random_state=42); -1 = anomalia

detector = IsolationForest(contamination=0.25,random_state=42)
resultados = detector.fit_predict(trafego)

for i, (amostra,r) in enumerate(zip(trafego,resultados)):
    if r == -1:
        print(f"Amostra {i+1}: {amostra} -> ANOMALIA")
print("Demais -> Normal")

# Saída esperada:
# Amostra 4: [50000, 500] -> ANOMALIA
# Amostra 7: [45000, 450] -> ANOMALIA
# Demais -> Normal