import json
import requests
from datetime import datetime
import matplotlib.pyplot as plt

urlEuribor6m="https://www.euribor-rates.eu/umbraco/api/euriborpageapi/highchartsdata?series[0]=2"
urlEcbRates="https://www.euribor-rates.eu/umbraco/api/ecbpageapi/highchartsData?series[0]=1"
urlEuroBond="https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/irt_euryld_d?format=JSON&geo=EA&maturity=Y10&yld_curv=SPOT_RT&bonds=CGB_EA&lang=en"
urlEuroHicp="https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_manr?format=JSON&sinceTimePeriod=1999-01&geo=EA&coicop=CP00&lang=en"
def readFromUrl(url):

    response = requests.get(url)
    parsed_data = json.loads(response.text)

    for data_dict in parsed_data:
        date_values = data_dict['Data']
        dizionario = {entry[0]: entry[1] for entry in date_values}
        return dizionario
        
def readFromEurostatUrl(url, hicp):

    response = requests.get(url)
    parsed_data = json.loads(response.text)

    valori=[]
    for i in range(len(parsed_data['value'])):
        valori.append(parsed_data['value'][str(i)])

    date_datetime_list=[]
    date_format = "%Y-%m-%d"
    if hicp==1:
        #Formato mese-anno per dati inflazione
        date_format = "%Y-%m"
    

    for key, values in (parsed_data['dimension']['time']['category']['label'].items()):
        date_datetime = datetime.strptime(str(key), date_format)
        date_datetime_without_seconds = date_datetime.replace(second=0) 
        date_datetime_list.append(int(date_datetime_without_seconds.timestamp()*1000))
 
    result_dict = dict(zip(date_datetime_list,valori))
    return result_dict
    
def preparazione_scalette(formatted_data, all_dates):
    scaled_values = []
    current_value = None

    for date in all_dates:
        if date in formatted_data:
            current_value = formatted_data[date]
        scaled_values.append(current_value)
    return scaled_values


def calcola_reale(tassi, inflazione):
    lunghezza_minima = min(len(tassi), len(inflazione))
    risultato = []

    for i in range(lunghezza_minima):
        valore1 = tassi[i]
        valore2 = inflazione[i]

        if valore1 is not None:
            differenza = valore1 - valore2
            risultato.append(differenza)
        else:
            risultato.append(None)
    return risultato
 
def plot_data(formatted_euribor, formatted_ecbrates, formatted_yield, formatted_inflazione):
    plt.figure(figsize=(10, 6))

    #Considero tutte le date dei due set di valori e le ordino
    all_dates = set(formatted_euribor.keys()).union((formatted_ecbrates.keys()),(formatted_yield.keys()), formatted_inflazione.keys())
    all_dates = sorted(all_dates)
     
    euribor=preparazione_scalette(formatted_euribor,all_dates)
    ecbrates=preparazione_scalette(formatted_ecbrates,all_dates)
    yield10y=preparazione_scalette(formatted_yield,all_dates)
    inflazione=preparazione_scalette(formatted_inflazione,all_dates)
    
    values_reale=calcola_reale(yield10y, inflazione)
    # Traccia il grafico per il secondo dizionario
    plt.step(all_dates, ecbrates, where='post', color='orange', label='Tassi ECB')
    plt.step(all_dates, yield10y, where='post', color='green', label='Euro Bond 10Y')
    plt.step(all_dates, euribor, where='post', color='blue',label='Euribor 3mesi')
    plt.step(all_dates, inflazione, where='post', color='red', label='HICP')
    plt.step(all_dates, values_reale, where='post', color='black', label='Tasso Reale')
    # Trucco per vedere le date sull'asse delle X suggerito da ChatGBT
    # Configurazione delle etichette dell'asse delle x
    current_labels = plt.xticks()[0]
    # Specificare il valore minimo e massimo
    min_value = current_labels[1] 
    max_value = current_labels[-2]

    # Clip per mantenere le etichette all'interno del range minimo e massimo
    clipped_labels = [max(min_value, min(max_value, label)) for label in current_labels]

    # Converti le etichette da millisecondi a oggetti datetime
    date_labels = [datetime.fromtimestamp(int(label) // 1000) for label in clipped_labels]

    # Converti gli oggetti datetime in stringhe "YYYY-MM-DD"
    formatted_date_labels = [dt.strftime('%Y-%m') for dt in date_labels]

    # Imposta le nuove etichette sull'asse x
    plt.xticks(clipped_labels, formatted_date_labels)

    plt.xticks(rotation=45)
    plt.xlabel('Data')
    plt.ylabel('Valori')
    plt.title('Inflazione e Tassi')
    plt.legend()
    plt.tight_layout()

    plt.show()

formatted_euribor=readFromUrl(urlEuribor6m)
formatted_ecbrates=readFromUrl(urlEcbRates)
formatted_yield=readFromEurostatUrl(urlEuroBond, 0)
formatted_inflazione=readFromEurostatUrl(urlEuroHicp, 1)
plot_data(formatted_euribor, formatted_ecbrates, formatted_yield, formatted_inflazione)
