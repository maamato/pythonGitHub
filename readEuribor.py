import json
import requests
from datetime import datetime
import matplotlib.pyplot as plt

urlEuribor6m="https://www.euribor-rates.eu/umbraco/api/euriborpageapi/highchartsdata?series[0]=2"
urlEcbRates="https://www.euribor-rates.eu/umbraco/api/ecbpageapi/highchartsData?series[0]=1"
urlEuroBond="https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/irt_euryld_d?format=JSON&sinceTimePeriod=2004-09-06&geo=EA&maturity=Y10&yld_curv=SPOT_RT&bonds=CGB_EA&lang=en"

def readFromUrl(url):

    response = requests.get(url)
    parsed_data = json.loads(response.text)

    for data_dict in parsed_data:
        date_values = data_dict['Data']
        dizionario = {entry[0]: entry[1] for entry in date_values}
        print(dizionario)
        return dizionario
        
def readFromEurostatUrl(url):

    response = requests.get(url)
    parsed_data = json.loads(response.text)

    valori=[]
    for i in range(len(parsed_data['value'])):
        valori.append(parsed_data['value'][str(i)])

    date_datetime_list=[]
    date_format = "%Y-%m-%d"

    for key, values in (parsed_data['dimension']['time']['category']['label'].items()):
        date_datetime = datetime.strptime(str(key), date_format)
        date_datetime_without_seconds = date_datetime.replace(second=0) 
        date_datetime_list.append(date_datetime_without_seconds)
 
    result_dict = dict(zip(date_datetime_list,valori))
    return result_dict
    

def plot_data(formatted_data1, formatted_data2):
    plt.figure(figsize=(10, 6))

    #Considero tutte le date dei due set di valori e le ordino
    all_dates = set(formatted_data1.keys()).union(set(formatted_data2.keys()))
    all_dates = sorted(all_dates)

    values1 = [formatted_data1.get(date, None) for date in all_dates]
    
    #Creao un grafico a scaletta i valori precedenti a x valgono x-1 anche per
    #i giorni in cun non è definito alcun valore
    scaled_values2 = []
    current_value = None

    for date in all_dates:
        if date in formatted_data2:
            current_value = formatted_data2[date]
        scaled_values2.append(current_value)


    # Traccia il grafico per il primo dizionario
    plt.plot(all_dates, values1, label='Euribor 3mesi')

    # Traccia il grafico per il secondo dizionario
    plt.step(all_dates, scaled_values2, where='post', color='orange', label='Tassi ECB')
    # Configurazione delle etichette dell'asse delle x
    plt.xticks(rotation=45)
    
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.title('Graph of Values Over Dates')
    plt.legend()
    plt.tight_layout()

    plt.show()

formatted_data1=readFromUrl(urlEuribor6m)
formatted_data2=readFromUrl(urlEcbRates)

plot_data(formatted_data1, formatted_data2)

formatted_data3=readFromEurostatUrl(urlEuroBond)
print(formatted_data3)
#Aggiungere Tasso di inflazione