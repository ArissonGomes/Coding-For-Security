from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score
y_true = [0,0,0,0,0,0,0,0,1,1]   # 8 normais, 2 ataques
y_pred = [0,0,0,0,0,0,0,0,0,1]   # perdeu 1 ataque

a,b = confusion_matrix(y_true,y_pred)
precisao = precision_score(y_true,y_pred)
recall = recall_score(y_true,y_pred)
f1 = f1_score(y_true,y_pred)
acuracia = accuracy_score(y_true,y_pred)

print(f"Matriz: {a},{b}")
print(f"Acurácia: {acuracia:.2f} | Precisão: {precisao:.2f} | Recall: {recall:.2f} | F1: {f1:.2f}")
print("Comentário: acurácia 0.90 mascara que METADE dos ataques passou (recall 0.50).")

# Saída esperada:
# Matriz: [[8,0],[1,1]]
# Acurácia: 0.90 | Precisão: 1.00 | Recall: 0.50 | F1: 0.67
# Comentário: acurácia 0.90 mascara que METADE dos ataques passou (recall 0.50).