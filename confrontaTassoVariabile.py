import requests
import json
import matplotlib.pyplot as plt
import datetime
from datetime import datetime
import re
import streamlit as st
import pandas as pd



# extract_number utilizza una espressione regolare per cercare
# una sequenza di numeri all'interno della stringa. 
# Se trova una corrispondenza, restituisce il numero come intero
def extract_number(text):
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    return None

titoli_tassoVariabile={"IT0005312142":"Nov23", "IT0005399230":"Cct23", "IT0005174906":"Apr24","IT0005252520":"Cct24", "IT0005217770":"Ott24", "IT0005311508":"Cct25","IT0005410912":"Mag25","IT0005428617":"Cct26", "IT0005332835":"Mag26", "IT0005374043":"Cdp26","IT0005388175":"Ott27","IT0005532723":"Mar28","IT0005534984":"Cct28","IT0005517195":"Nov28","IT0005497000":"Giu30", "IT0005491250":"Cct30"}
titoli_Cct = {k: v for k, v in titoli_tassoVariabile.items() if v.startswith("Cct")}
print(titoli_Cct)

titoli_Btp_Ita = {k: v for k, v in titoli_tassoVariabile.items() if not(v.startswith("Cct") or v.startswith("Cdp"))}
print(titoli_Btp_Ita)

titoli_fino24 = {k: v for k, v in titoli_tassoVariabile.items() if extract_number(v) is not None and 23 <= extract_number(v) <= 24}
print(titoli_fino24)

titoli_25_26 = {k: v for k, v in titoli_tassoVariabile.items() if extract_number(v) is not None and 25 <= extract_number(v) <= 26}
print(titoli_25_26)

titoli_oltre27 = {k: v for k, v in titoli_tassoVariabile.items() if extract_number(v) >= 27}
print(titoli_oltre27)

data_inserita=datetime(2023, 6, 1)


st.sidebar.header('Titoli tasso variabile')

def get_input():
    selezione = st.sidebar.selectbox('Titoli', ('Tutti', 'CCT', 'Btp Ita', 'Fino 2024', 'Da 2025 a 2026', "Oltre 2027"))
    return selezione

def get_data():
    d = st.sidebar.date_input("Data iniziale", datetime(2023, 8, 1))
    return d

scelta_titoli = get_input()
data_scelta = get_data()

st.header(f"""
    Titoli: {scelta_titoli} dal {data_scelta}
    """)

# URL del servizio
url = "https://charts.borsaitaliana.it/charts/services/ChartWService.asmx/GetPrices"

# Dati da inviare nella richiesta

def calcola_variazione_percentuale(lista):
    variazioni_percentuali = []
    
    for i in range(1, len(lista)):
        variazione = ((lista[i] - lista[i - 1]) / lista[i - 1]) * 100
        variazioni_percentuali.append(variazione)
    
    return variazioni_percentuali


def calcola_variazione_percentuale_primo(lista):
    variazioni_percentuali = []
    
    for i in range(1, len(lista)):
        variazione = ((lista[i] - lista[0]) / lista[0]) * 100
        variazioni_percentuali.append(variazione)
    
    return variazioni_percentuali

def build_data_post_request(sampletime,timeframe,key):
    data = {
        "request": {
            "SampleTime": sampletime,
            "TimeFrame": timeframe,
            "RequestedDataSetType": "ohlc",
            "ChartPriceType": "price",
            "Key": key+".MOT",
            "OffSet": 0,
            "FromDate": None,
            "ToDate": None,
            "UseDelay": False,
            "KeyType": "Topic",
            "KeyType2": "Topic",
            "Language": "it-IT"
        }
    }
    return data

dictionary_variazioni={}
dictionary_variazioni_primo={}
for key,val in titoli_tassoVariabile.items():
    timeframe="10y"
    sampletime="1d"
    data=build_data_post_request(sampletime,timeframe,key)
    response = requests.post(url, json=data)
    parsed_data = json.loads(response.text)

    data_list = parsed_data['d']

    
    lista_variazioni=[]
    for riga in data_list:
        timestamp_seconds = riga[0] / 1000  # Convert to seconds
        date_time = datetime.fromtimestamp(timestamp_seconds)
        if date_time > data_inserita:
            lista_variazioni.append(riga[-1])

    dictionary_variazioni[val] =calcola_variazione_percentuale(lista_variazioni)
    dictionary_variazioni_primo[val] =calcola_variazione_percentuale_primo(lista_variazioni)





# Estrai i nomi e i valori dal dizionario
nomi = list(dictionary_variazioni.keys())
valori = list(dictionary_variazioni.values())

st.title("Grafico a Dispersione dei Valori")
st.subheader("Data: " + str(data_inserita.date()))

plt.figure(figsize=(15, 8))
for nome, valore in zip(nomi, valori):
    plt.scatter([nome] * len(valore), valore, label=nome)

# Aggiungi etichette agli assi
plt.xlabel("Nomi")
plt.ylabel("Valori")

# Aggiungi una legenda
#plt.legend()

# Aggiungi un titolo al grafico
plt.title("Grafico a Dispersione dei Valori")

# Mostra il grafico utilizzando Streamlit
st.pyplot(plt)

# Visualizza la tabella dei valori
#st.subheader("Tabella dei Valori")
#df = pd.DataFrame(dictionary_variazioni)
#st.dataframe(df)

def equalize_lists(dictionary):
    # Trova la lunghezza massima delle liste nel dizionario
    max_length = max(len(lst) for lst in dictionary.values())
    
    # Aggiungi zeri alle liste all'inizio finchè è raggiunta la lunghezza max
    for key in dictionary:
        while len(dictionary[key]) < max_length:
            dictionary[key].insert(0, 0)

for nome, valori in dictionary_variazioni_primo.items():
    valori.insert(0, 0)

nomi = list(dictionary_variazioni_primo.keys())
valori = list(dictionary_variazioni_primo.values())

equalize_lists(dictionary_variazioni_primo)
# Genera un range di valori per l'asse x (0, 1, 2, ...)
x = range(len(valori[0]))  # Assumendo che tutte le liste abbiano la stessa lunghezza
plt.figure(figsize=(15, 8))
for i in range(len(nomi)):
    plt.plot(x, valori[i], label=nomi[i])  # Creazione del grafico lineare con marcatori circolari

plt.xlabel('Valori')
plt.ylabel('Variazioni')
plt.title('Variazioni da '+str(data_inserita.date()))
plt.legend()  # Aggiungi legenda
plt.grid(True)  # Aggiungi griglia

# Mostra il grafico utilizzando Streamlit
st.pyplot(plt)



