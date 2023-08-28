import json
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

urlEuribor6m="https://www.euribor-rates.eu/umbraco/api/euriborpageapi/highchartsdata?series[0]=2"
urlEcbRates="https://www.euribor-rates.eu/umbraco/api/ecbpageapi/highchartsData?series[0]=1"
urlEuroBond="https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/irt_euryld_d?format=JSON&sinceTimePeriod=2004-09-06&geo=EA&maturity=Y10&yld_curv=SPOT_RT&bonds=CGB_EA&lang=en"
urlEuroHicp="https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_manr?format=JSON&sinceTimePeriod=2001-01&geo=EA&coicop=CP00&lang=en"
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
    

def plot_data(formatted_data1, formatted_data2, formatted_data3, formatted_data4):
    plt.figure(figsize=(10, 6))

    #Considero tutte le date dei due set di valori e le ordino
    all_dates = set(formatted_data1.keys()).union((formatted_data2.keys()),(formatted_data3.keys()), formatted_data4.keys())
    all_dates = sorted(all_dates)
   
    values3 = [formatted_data3.get(date, None) for date in all_dates]
    values1 = [formatted_data1.get(date, None) for date in all_dates]

    #Creao un grafico a scaletta i valori precedenti a x valgono x-1 anche per
    #i giorni in cun non è definito alcun valore
    scaled_values2 = []
    current_value = None

    for date in all_dates:
        if date in formatted_data2:
            current_value = formatted_data2[date]
        scaled_values2.append(current_value)

    scaled_values4 = []
    current_value = None

    for date in all_dates:
        if date in formatted_data4:
            current_value = formatted_data4[date]
        scaled_values4.append(current_value)
    
    # Traccia il grafico per il secondo dizionario
    plt.step(all_dates, scaled_values2, where='post', color='orange', label='Tassi ECB')
    plt.step(all_dates, values3, where='post', color='grey', label='Euro Bond 10Y')
    plt.step(all_dates, values1, where='post', color='blue',label='Euribor 3mesi')
    plt.step(all_dates, scaled_values4, where='post', color='red', label='HICP')
    #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
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
formatted_data3=readFromEurostatUrl(urlEuroBond, 0)
formatted_data4=readFromEurostatUrl(urlEuroHicp, 1)
plot_data(formatted_data1, formatted_data2, formatted_data3, formatted_data4)
