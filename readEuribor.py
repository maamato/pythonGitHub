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


def plot_data(formatted_data1, formatted_data2, formatted_data3, formatted_data4):
    plt.figure(figsize=(10, 6))

    #Considero tutte le date dei due set di valori e le ordino
    all_dates = set(formatted_data1.keys()).union((formatted_data2.keys()),(formatted_data3.keys()), formatted_data4.keys())
    all_dates = sorted(all_dates)
     
    values3 = [formatted_data3.get(date, None) for date in all_dates]
    #values1 = [formatted_data1.get(date, None) for date in all_dates]
    values1=preparazione_scalette(formatted_data1,all_dates)
    #Creao un grafico a scaletta i valori precedenti a x valgono x-1 anche per
    #i giorni in cun non è definito alcun valore
    scaled_values2=preparazione_scalette(formatted_data2,all_dates)

    scaled_values4=preparazione_scalette(formatted_data4,all_dates)
    
    # Traccia il grafico per il secondo dizionario
    plt.step(all_dates, scaled_values2, where='post', color='orange', label='Tassi ECB')
    plt.step(all_dates, values3, where='post', color='green', label='Euro Bond 10Y')
    plt.step(all_dates, values1, where='post', color='blue',label='Euribor 3mesi')
    plt.step(all_dates, scaled_values4, where='post', color='red', label='HICP')
    
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

formatted_data1=readFromUrl(urlEuribor6m)
formatted_data2=readFromUrl(urlEcbRates)
formatted_data3=readFromEurostatUrl(urlEuroBond, 0)
formatted_data4=readFromEurostatUrl(urlEuroHicp, 1)
plot_data(formatted_data1, formatted_data2, formatted_data3, formatted_data4)
