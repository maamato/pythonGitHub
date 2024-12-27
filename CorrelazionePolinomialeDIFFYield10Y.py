import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt


def leggiYield(anno):
    urlEuroBond="https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/irt_euryld_d?format=JSON&geo=EA&yld_curv=SPOT_RT&maturity=Y"+anno+"&bonds=CGB_EA&lang=en"
    #urlEuroBond="https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/irt_euryld_m?format=JSON&geo=EA&yld_curv=PAR&bonds=CGB_EA&maturity=Y"+anno+"&lang=en"

    response = requests.get(urlEuroBond)

    # Verifica se la richiesta è andata a buon fine (status code 200)
    if response.status_code == 200:
        # Carica i dati JSON dalla risposta
        data = response.json()

    else:
        print(f"Errore nella richiesta HTTP. Status code: {response.status_code}")

    #Leggi i valori del cambio
    value = data.get('value', {})
    #Leggi i valori del giorno
    label = data.get('dimension', {}).get('time', {}).get('category', {}).get('label', {})
    return value,label





data={}
valori, anni = leggiYield("10")
data['EA Yield10']=list(valori.values())

#data['Anno10']=[i for i in list(anni.values())]

dfYield10Y = pd.DataFrame(data)
print(dfYield10Y)


data={}
valori, anni = leggiYield("2")
data['EA Yield2']=list(valori.values())


dfYield2Y = pd.DataFrame(data)
print(dfYield2Y)




df_merged = dfYield2Y.join(dfYield10Y, how='inner')
df_merged.columns = ['EA Yield2', 'EA Yield10']




df_merged['DIFF_2Y10Y'] = df_merged['EA Yield10'] - df_merged['EA Yield2']


print(df_merged[['EA Yield10','EA Yield2', 'DIFF_2Y10Y']])

import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Grado del polinomio
degree = 2

# Anticipa DIFF_2Y10Y di 600 valori
#al = -1230
val = -3420
valabs=abs(val)
df_merged['DIFF_2Y10Y_shifted'] = df_merged['DIFF_2Y10Y'].shift(-val)

# Rimuovi le righe con valori NaN risultanti dallo shift
df_shifted = df_merged.dropna(subset=['DIFF_2Y10Y_shifted'])

# Estrai le colonne necessarie
x = df_shifted['EA Yield10'].values.reshape(-1, 1)
y = df_shifted['DIFF_2Y10Y_shifted'].values
plot=[]
elementi_view=100
plot = df_merged.loc[:len(df_merged['DIFF_2Y10Y'])+val+elementi_view, 'DIFF_2Y10Y']
# Crea plot con 100 elementi in più rispetto a df_shifted
#plot = df_merged.loc[:len(df_shifted) + 99, 'DIFF_2Y10Y'].values  # plot ha 100 elementi in più


print(df_shifted)
print('DIFF')
print(df_merged['DIFF_2Y10Y'])
print(plot)

# Crea un nuovo indice che copre i 100 punti extra
extended_index = np.arange(len(df_shifted))  # Indici originali di df_shifted
extended_index = np.append(valabs+extended_index, np.arange(len(df_shifted)+valabs, len(df_shifted)+valabs + elementi_view+1))  # Estendi l'indice

# Trasformazione dei dati per una regressione polinomiale
poly = PolynomialFeatures(degree)
x_poly = poly.fit_transform(x)

# Fit del modello polinomiale
model = LinearRegression()
model.fit(x_poly, y)

# Previsione dei valori di DIFF_2Y10Y_shifted
y_pred = model.predict(x_poly)

# Calcolo del coefficiente di correlazione
correlation = np.corrcoef(y, y_pred)[0, 1]

# Calcolo della retta di regressione polinomiale per il grafico
x_seq = np.linspace(x.min(), x.max(), 300).reshape(-1, 1)
y_seq_pred = model.predict(poly.fit_transform(x_seq))

# Creazione del grafico con due sottotrame
fig, ax = plt.subplots(2, 1, figsize=(10, 12))

# Prima sottotrama: Valori DIFF_2Y10Y_shifted e EA Yield10 nel tempo
ax[0].plot(df_shifted.index, df_shifted['DIFF_2Y10Y_shifted'], label=f'DIFF_2Y10Y anticipato di {val} valori', color='orange')
ax[0].plot(df_shifted.index, df_shifted['EA Yield10'], label='EA Yield10', color='blue')

# Plot con i 100 valori in più, estendendo l'asse temporale
ax[0].plot(extended_index, plot, label='DIFF_2Y10Y originale (plot) - 100 elementi in più', color='green')


ax[0].set_title('DIFF_2Y10Y anticipato e EA Yield10 nel tempo')
ax[0].set_xlabel('Tempo')
ax[0].set_ylabel('Valore')
ax[0].legend()
ax[0].grid(True)


# Seconda sottotrama: Correlazione polinomiale tra EA Yield10 e DIFF_2Y10Y anticipato
ax[1].scatter(x, y, color='blue', label='Dati')
ax[1].plot(x_seq, y_seq_pred, color='red', label=f'Polinomio di grado {degree}')
ax[1].set_title(f'Correlazione Polinomiale tra EA Yield10 e DIFF_2Y10Y anticipato di {val} valori\n'
                f'Coefficiente di correlazione: {correlation:.4f}')
ax[1].set_xlabel('EA Yield10')
ax[1].set_ylabel(f'DIFF_2Y10Y anticipato di {val} valori')
ax[1].legend()
ax[1].grid(True)

# Mostra il grafico
plt.tight_layout()
plt.show()



# Ottenere i coefficienti del modello
coefficients = model.coef_
intercept = model.intercept_

# Creare una stringa che rappresenti il polinomio
polynomial_str = " + ".join([f"{coefficients[i]:.4f}x^{i}" for i in range(len(coefficients))])
polynomial_str = f"{intercept:.4f} + " + polynomial_str
print(polynomial_str)

df_interpolazione=pd.DataFrame()
df_interpolazione['DIFF_2Y10Y']=plot
# Calcola i valori di Y in base al polinomio interpolante

from scipy.optimize import fsolve

# Funzione che rappresenta il polinomio interpolatore P(x)
def polinomio(x, coefficients, intercept):
    return sum(coefficients[i] * x**i for i in range(len(coefficients))) + intercept

# Funzione che risolve l'equazione P(x) = Y per un dato Y
def find_x_for_y(y, coefficients, intercept):
    # Funzione da annullare: P(x) - y = 0
    def equation(x):
        return polinomio(x, coefficients, intercept) - y
    
    # Trova la soluzione numerica usando fsolve con un valore iniziale (guess)
    x_initial_guess = 0  # Inizialmente supponiamo che x sia vicino a 0
    solution = fsolve(equation, x_initial_guess)
    return solution[0]  # Restituisce la soluzione trovata

# Applica la funzione per trovare X per ogni valore di DIFF_2Y10Y
df_interpolazione['X'] = df_interpolazione['DIFF_2Y10Y'].apply(lambda y: find_x_for_y(y, coefficients, intercept))
#df_shifted_extended = df_shifted.reindex(df_interpolazione.index)

df_interpolazione = df_interpolazione.reset_index(drop=True)
df_shifted = df_shifted.reset_index(drop=True)
df_interpolazione['REAL'] = df_shifted['EA Yield10']
#df_interpolazione['X'] = sum(coefficients[i] * df_interpolazione['DIFF_2Y10Y']**i for i in range(len(coefficients))) + intercept

print(df_interpolazione)

plt.figure(figsize=(10, 6))
plt.plot(df_interpolazione['DIFF_2Y10Y'], marker='')
plt.plot(df_interpolazione['X'], marker='')
plt.plot(df_interpolazione['REAL'],marker='')
# Aggiunta di etichette e titolo
plt.xlabel('Interpolazione X')
plt.ylabel('DIFF_2Y10Y')
plt.title('Correlazione')
plt.axhline(y=0, color='black', linestyle='-', linewidth=1)  # Linea di riferimento a 0
plt.grid(True)
plt.tight_layout()

# Mostra il grafico
plt.show()