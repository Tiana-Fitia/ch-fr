import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Modèle simple, rapide, local
model = RandomForestClassifier(n_estimators=20)

# Faux entraînement minimal (rapide)
X = [
    [0.2, 1, 0],  # bon flux
    [1.5, 4, 2],  # moyen
    [3.0, 6, 5],  # mauvais
]
y = [0, 1, 2]  # 0=OK, 1=RISQUE, 2=MAUVAIS

model.fit(X, y)

def predict(latency, start_time, errors):
    result = model.predict([[latency, start_time, errors]])
    return result[0]
