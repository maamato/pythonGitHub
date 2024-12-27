import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import cloudscraper
from io import StringIO


def find_local_maxima(correlations, threshold):
    local_maxima = []
    for i in range(1, len(correlations) - 1):
        # Controlla se il valore corrente è un massimo relativo
        if correlations[i] > correlations[i - 1] and correlations[i] > correlations[i + 1] and correlations[i] > correlations[i - 2] and correlations[i] > correlations[i +2] and correlations[i] > correlations[i - 3] and correlations[i] > correlations[i +3]:
            # Controlla se il massimo relativo supera la soglia di 0.8
            if correlations[i] > threshold:
                local_maxima.append((i, correlations[i]))
    return local_maxima

def find_local_minimi(correlations, threshold):
    minimi_locali = []
    for i in range(1, len(correlations) - 1):
        # Controlla se il valore corrente è un massimo relativo
        if correlations[i] < correlations[i - 1] and correlations[i] < correlations[i + 1] and correlations[i] < correlations[i - 2] and correlations[i] < correlations[i +2] and correlations[i] < correlations[i - 3] and correlations[i] < correlations[i +3]:
            # Controlla se il massimo relativo supera la soglia di 0.8
            if correlations[i] < threshold:
                minimi_locali.append((i, correlations[i]))
    return minimi_locali


# Parametri di ingresso
valInvest = 1121268
valInvest=1080335
#valInvest = 1181507
symbol = ""
today = datetime.today()
some_months_ago = today - relativedelta(months=200)
period1 = some_months_ago.strftime("%m/%d/%Y")
period2 = today.strftime("%m/%d/%Y")

headers={
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
		"Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection":"keep-alive",
        "Cookie":"adBlockerNewUserDomains=1625321155; udid=8eb245098823de8e790347210ea247b0; OptanonConsent=isIABGlobal=false&datestamp=Thu+Feb+23+2023+14%3A38%3A23+GMT%2B0100+(Ora+standard+dell%E2%80%99Europa+centrale)&version=202209.2.0&hosts=&consentId=ddc2d70c-836c-42ca-800a-698c44dcb229&interactionCount=4&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CSTACK42%3A1&geolocation=IT%3B62&AwaitingReconsent=false&isGpcEnabled=0; _ga=GA1.2.1031880264.1625321158; _fbp=fb.1.1625321158434.1010563068; eupubconsent-v2=CPlHDFgPlHDFgAcABBENC4CsAP_AAH_AAChQJMtf_X__b2_r-_5_f_t0eY1P9_7__-0zjhfdl-8N3f_X_L8X52M7vF36tq4KuR4ku3LBIUdlHOHcTUmw6okVryPsbk2cr7NKJ7PEmnMbOydYGH9_n1_z-ZKY7___f_7z_v-v________7-3f3__5___-__e_V__9zfn9_____9vP___9v-_9__________3_7997_H4JMgEmGrcQBdmWODNtGEUCIEYVhIVQKACigGFogMIHVwU7K4CfWECABAKAJwIgQ4AowYBAAAJAEhEQEgR4IBAARAIAAQAKhEIAGNgEFgBYGAQACgGhYoxQBCBIQZEBEUpgQFSJBQT2VCCUH-hphCHWWAFBo_4qEBGsgYrAiEhYOQ4IkBLxZIHmKN8gBGAFAKJUK1FJ6YAA.f_gAD_gAAAAA; _ga_H1WYEJQ780=GS1.1.1654768225.11.1.1654768285.60; _cc_id=d977806b5e970aaa80b2cf2c12dcb71f; _hjSessionUser_174945=eyJpZCI6IjEyMGE2NDY0LWFiMDgtNTU3ZC04NDgyLTdiZWQ4MTczNTJmMCIsImNyZWF0ZWQiOjE2NTI5NzAyNjA4MTcsImV4aXN0aW5nIjp0cnVlfQ==; ses_id=NXthIGNsMTk%2BemFnYzJjYWU2Yzg%2BPzExNzNhajYxMCZkcGJsYTY1czU6PnBlZmN%2FMWA%2BP2M1YjdiY2RhMGFhNTVhYWdjMjE5Pj1hZGNlYzNlZmM7PmgxYDc1YTM2MzBrZGFiN2FjNTg1Nj5nZTljPzEjPiJjJ2JzYjBkNDBxYSY1OmEgYzMxbj4%2BYTxjNWNmZTVjPz4%2BMTA3Z2FqNjYwKGQv; __gads=ID=34b5321ff1088be1-22d3311733ce00fa:T=1662369116:S=ALNI_MZpn0nno_eNBfbBlrEhtkQPX0-5-w; __gpi=UID=00000b23850c29f8:T=1662369649:RT=1677350676:S=ALNI_MZTxEIHZs-uQ8oNVfOj6Gq6HMp9Bw; user-browser-sessions=101; _ga_C4NDLGKVMK=GS1.1.1677350679.229.1.1677350758.60.0.0; OptanonAlertBoxClosed=2023-01-05T09:55:10.406Z; OTAdditionalConsentString=1~39.43.46.55.61.70.83.89.93.108.117.122.124.135.136.143.144.147.149.159.162.167.171.192.196.202.211.218.228.230.239.241.259.266.286.291.311.317.322.323.326.327.338.367.371.385.389.394.397.407.413.415.424.430.436.445.449.453.482.486.491.494.495.501.503.505.522.523.540.550.559.560.568.574.576.584.587.591.737.745.787.802.803.817.820.821.839.864.867.874.899.904.922.931.938.979.981.985.1003.1024.1027.1031.1033.1040.1046.1051.1053.1067.1085.1092.1095.1097.1099.1107.1127.1135.1143.1149.1152.1162.1166.1186.1188.1201.1205.1211.1215.1226.1227.1230.1252.1268.1270.1276.1284.1286.1290.1301.1307.1312.1345.1356.1364.1365.1375.1403.1415.1416.1419.1440.1442.1449.1455.1456.1465.1495.1512.1516.1525.1540.1548.1555.1558.1564.1570.1577.1579.1583.1584.1591.1603.1616.1638.1651.1653.1665.1667.1677.1678.1682.1697.1699.1703.1712.1716.1721.1725.1732.1745.1750.1765.1769.1782.1786.1800.1810.1825.1827.1832.1838.1840.1842.1843.1845.1859.1866.1870.1878.1880.1889.1899.1917.1929.1942.1944.1962.1963.1964.1967.1968.1969.1978.2003.2007.2008.2027.2035.2039.2044.2047.2052.2056.2064.2068.2070.2072.2074.2088.2090.2103.2107.2109.2115.2124.2130.2133.2137.2140.2145.2147.2150.2156.2166.2177.2183.2186.2202.2205.2216.2219.2220.2222.2225.2234.2253.2264.2279.2282.2292.2299.2305.2309.2312.2316.2322.2325.2328.2331.2334.2335.2336.2337.2343.2354.2357.2358.2359.2370.2376.2377.2387.2392.2394.2400.2403.2405.2407.2411.2414.2416.2418.2425.2440.2447.2461.2462.2465.2468.2472.2477.2481.2484.2486.2488.2493.2497.2498.2499.2501.2510.2511.2517.2526.2527.2532.2534.2535.2542.2552.2563.2564.2567.2568.2569.2571.2572.2575.2577.2583.2584.2596.2601.2604.2605.2608.2609.2610.2612.2614.2621.2628.2629.2633.2634.2636.2642.2643.2645.2646.2647.2650.2651.2652.2656.2657.2658.2660.2661.2669.2670.2677.2681.2684.2686.2687.2690.2695.2698.2707.2713.2714.2729.2739.2767.2768.2770.2772.2784.2787.2791.2792.2798.2801.2805.2812.2813.2816.2817.2818.2821.2822.2827.2830.2831.2834.2838.2839.2840.2844.2846.2847.2849.2850.2852.2854.2856.2860.2862.2863.2865.2867.2869.2873.2874.2875.2876.2878.2880.2881.2882.2883.2884.2886.2887.2888.2889.2891.2893.2894.2895.2897.2898.2900.2901.2908.2909.2911.2912.2913.2914.2916.2917.2918.2919.2920.2922.2923.2924.2927.2929.2930.2931.2939.2940.2941.2947.2949.2950.2956.2958.2961.2962.2963.2964.2965.2966.2968.2970.2973.2974.2975.2979.2980.2981.2983.2985.2986.2987.2991.2994.2995.2997.2999.3000.3002.3003.3005.3008.3009.3010.3012.3016.3017.3018.3019.3024.3025.3028.3034.3037.3038.3043.3045.3048.3052.3053.3055.3058.3059.3063.3065.3066.3068.3070.3072.3073.3074.3075.3076.3077.3078.3089.3090.3093.3094.3095.3097.3099.3104.3106.3109.3112.3117.3118.3119.3120.3124.3126.3127.3128.3130.3135.3136.3145.3149.3150.3151.3154.3155.3162.3163.3167.3172.3173.3180.3182.3183.3184.3185.3187.3188.3189.3190.3194.3196.3197.3209.3210.3211.3214.3215.3217.3219.3222.3223.3225.3226.3227.3228.3230.3231.3232.3234.3235.3236.3237.3238.3240.3244.3245.3250.3251.3253.3257.3260.3268.3270.3272.3281.3288.3290.3292.3293.3295.3296.3300.3306.3307.3308.3314.3315.3316.3318.3324.3327.3328.3330.3531.3831.3931; pm_score=clear; ab_test_header_bidding=headerBidding_enabled; r_p_s_n=1; G_ENABLED_IDPS=google; kppid_managed=kppidff_PMDlA05M; _pbjs_userid_consent_data=6317595435334274; invpc=1; _gid=GA1.2.174362482.1677350680; panoramaId_expiry=1677437081717; __cf_bm=idUc1aYBfv1ZL75aurAGRx9ePiAWPoBrhEjJ6mjd_LY-1677354520-0-Act6FP1rVbVyO1MTApWT+3Bfn0pP1M8gsfz4SpvLX3MjbdJ4unmKfBdb8HZD/MTCfcj5lVg3DM+t24A+LzSCiAs=",
        "Host":"www.investing.com",
        "Sec-Fetch-Dest":"document",
        "Sec-Fetch-Mode":"navigate",
        "Sec-Fetch-Site":"none",
        "Sec-Fetch-User":"?1",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"
}
# URL per lo scraping
u2 = f'https://www.investing.com/instruments/DownloadHistoricalData?curr_id={valInvest}&smlID=106682&header={symbol}+Historical+Data&st_date={period1}&end_date={period2}&interval_sec=Daily&sort_col=date&sort_ord=DESC'

# Creazione scraper
scraper = cloudscraper.create_scraper(delay=10, browser="chrome")
content = scraper.get(u2, headers=headers).text

# Lettura dei dati
data_io = StringIO(content)
data_lettura = pd.read_csv(data_io, header=0, sep=",")
data_lettura = data_lettura.dropna()

# Trasformazione dei dati numerici
dati_chiusure_mese = data_lettura['Price'].str.replace(',', '').astype(float)
# Convertiamo e invertiamo le date
data_lettura['Date'] = pd.to_datetime(data_lettura['Date'])
data_lettura = data_lettura.iloc[::-1].reset_index(drop=True)

# Creazione della variabile temporale
X = (data_lettura['Date'] - data_lettura['Date'].min()).dt.days.values.reshape(-1, 1)

#Normalizzazione logaritmica
#Y = dati_chiusure_mese.values[::-1]  # Invertiamo i valori di Y per avere ordine cronologico crescente
#Y = np.log(dati_chiusure_mese.values[::-1])
#Y_min = np.min(Y)
#Y_max = np.max(Y)
# Applicazione della normalizzazione Min-Max
#Y = (Y - Y_min) / (Y_max - Y_min)
#data_lettura['Y']=Y


#Normalizzazione Max Min
#Y = dati_chiusure_mese.values[::-1]  # Invertiamo i valori di Y per avere ordine cronologico crescente
#Y_min = np.min(Y)
#Y_max = np.max(Y)
# Normalizzazione tra -1 e 1
#Y = 2 * (Y - Y_min) / (Y_max - Y_min) - 1
#data_lettura['Y'] = Y


#Standardizzazione z-score
Y = np.log(dati_chiusure_mese.values[::-1])
Y_mean = np.mean(Y)
Y_std = np.std(Y)
# Applicazione della standardizzazione Z-score
Y = (Y - Y_mean) / Y_std
data_lettura['Y'] = Y


# Definisci l'intervallo di lag (es. da -12 a +12 mesi)
max_lag = 1400
lags = range(-max_lag, 1)

import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
delta =40
print(Y)
print("Ultimi Valori")
last_values = Y[-delta:]
print(last_values)
data_lettura_ultimi=pd.DataFrame()
data_lettura_ultimi['LAST_VALUES']=last_values
print(data_lettura_ultimi)
# Lista per memorizzare le correlazioni
correlations = []
liste=[]
liste_forward=[]


high_corr_sequences = []
high_corr_reverse_sequences = []
# Numero di valori aggiuntivi da plottare
extra_values = 10


for lag in lags:
    # Shift della serie Tasso_10Y per il lag corrente
    shifted_series = data_lettura['Y'].shift(-lag)
    forward_series = data_lettura['Y'].shift(-lag-extra_values)
    non_nan_values = shifted_series.dropna()
    non_nan_values_forward = forward_series.dropna()
    data_lettura_ultimi_shifted=pd.DataFrame()
    data_lettura_ultimi_forward=pd.DataFrame()
    data_lettura_ultimi_shifted['SHIFTED']=non_nan_values[-delta:]
    data_lettura_ultimi_forward['NEXT']=non_nan_values_forward[-extra_values:]
    data_lettura_ultimi_shifted['index'] = range(len(data_lettura_ultimi_shifted))
    data_lettura_ultimi_forward['index'] = range(delta,delta+len(data_lettura_ultimi_forward))
    data_lettura_ultimi_forward.set_index('index', inplace=True)

    data_lettura_ultimi['index'] = range(len(data_lettura_ultimi))
    verso = 1 if data_lettura_ultimi['index'].iloc[-1] > data_lettura_ultimi['index'].iloc[0] else 0

    combined = pd.merge(data_lettura_ultimi_shifted, data_lettura_ultimi, on='index').dropna()
    combined=combined.drop(['index'], axis = 1) 
    
    #combined = pd.concat([data_lettura_ultimi_shifted, data_lettura_ultimi], axis=1).reset_index().dropna()
    print(combined)
    print(data_lettura_ultimi_forward)

    if not combined.empty:
        
        X = combined.iloc[:, 0].astype(float).values.reshape(-1, 1)  
        #print(X)
        y = combined.iloc[:, 1].astype(float).values  
        #print(y)
        X_FORWARD = data_lettura_ultimi_forward.iloc[:, 0].astype(float).values.reshape(-1, 1)

        ULTIMI_VAL =data_lettura_ultimi.iloc[:, 0].astype(float).values.reshape(-1, 1)
        
        #Correlazione Polinomiale errore quadratico [0..1]
        #n = 1  
        #poly = PolynomialFeatures(degree=n)
        #X_poly = poly.fit_transform(X)
        #model = LinearRegression().fit(X_poly, y)
        #y_pred = model.predict(X_poly)
        #correlation = np.corrcoef(y, y_pred)[0, 1]


        #Correlazione lineare [-1,1]
        X_flat = X.flatten()
        correlation_matrix = np.corrcoef(X_flat, y)
        correlation = correlation_matrix[0, 1]
        print(f"Correlazione calcolata: {correlation}")
    else:
        # Se non ci sono dati dopo lo shift, la correlazione è impostata a NaN
        correlation = np.nan
    
    # Aggiunta della correlazione alla lista
    correlations.append(correlation)
    liste.append(X)
    liste_forward.append(X_FORWARD)


    # Controlliamo se la correlazione supera 0.90
    #if correlation > 0.9:
    #    high_corr_sequences.append(X)  # Aggiungiamo la sequenza estesa


massimi_relativi = find_local_maxima(correlations, threshold=0.7)   
for i,val in massimi_relativi:
    #if verso==1 and liste[i][-1]> liste[i][0]: 
    #    conc= np.concatenate((liste[i], liste_forward[i]), axis=0)
    #    print(i)
    #    high_corr_sequences.append(conc)
    #if verso==0 and liste[i][-1]<= liste[i][0]: 
    #    conc= np.concatenate((liste[i], liste_forward[i]), axis=0)
    #    print(i)
    #    high_corr_sequences.append(conc)
    conc= np.concatenate((liste[i], liste_forward[i]), axis=0)
    print(i)
    high_corr_sequences.append(conc)
 
    
minimi_relativi = find_local_minimi(correlations, threshold=-0.7)   
for i,val in minimi_relativi:
    #if verso==1 and liste[i][-1]< liste[i][0]: 
    #    conc= np.concatenate((liste[i], liste_forward[i]), axis=0)
    #    print(i)
    #    high_corr_reverse_sequences.append(conc)
    #if verso==0 and liste[i][-1]>= liste[i][0]: 
    #    conc= np.concatenate((liste[i], liste_forward[i]), axis=0)
    #    print(i)
    #    high_corr_reverse_sequences.append(conc)
    conc= np.concatenate((liste[i], liste_forward[i]), axis=0)
    print(i)
    high_corr_reverse_sequences.append(conc)

    

# Plot delle sequenze con correlazione > 0.90 in un unico grafico

plt.figure(figsize=(12, 8))
for i, seq in enumerate(high_corr_sequences):
    color = np.random.rand(3,)
    plt.plot(range(delta),seq[:delta] -seq[0], linestyle='-', color=color)
    # Disegna la linea spezzata
    plt.plot(range(delta,delta+extra_values), seq[delta:]-seq[0], linestyle='--', color=color)
plt.plot(range(delta),ULTIMI_VAL[:delta]-ULTIMI_VAL[0], linestyle='-', linewidth=4,color='BLACK')
    
times=0;    
for i, seq in enumerate(high_corr_sequences):
    perc=((seq[-1]-seq[delta-1])/abs(seq[delta-1]))*100
    if perc>=0:
        times+=1
    print("Sequenze "+ str(i) + " Andamento "+str(perc))
print("Percentuale "+ str(100*times/(i+1)))


# Impostazioni del grafico
plt.title('Sequenze Originali con Correlazione > 0.90 (Estese di 5 Valori)')
plt.xlabel('Index')
plt.ylabel('Valori')
plt.legend()
plt.show()


plt.figure(figsize=(12, 8))
for i, seq in enumerate(high_corr_reverse_sequences):
    color = np.random.rand(3,)
    plt.plot(range(delta),seq[:delta] -seq[0], linestyle='-', color=color)
    # Disegna la linea spezzata
    plt.plot(range(delta,delta+extra_values), seq[delta:]-seq[0], linestyle='--', color=color)
plt.plot(range(delta),ULTIMI_VAL[:delta]-ULTIMI_VAL[0], linestyle='-', linewidth=4,color='BLACK')

times=0;    
for i, seq in enumerate(high_corr_reverse_sequences):
    perc=((seq[-1]-seq[delta-1])/abs(seq[delta-1]))*100
    if perc>=0:
        times+=1
    print("Sequenze "+ str(i) + " Andamento "+str(perc))
print("Percentuale "+ str(100*times/(i+1)))


# Impostazioni del grafico
plt.title('Sequenze Originali con Correlazione > 0.90 (Estese di 5 Valori)')
plt.xlabel('Index')
plt.ylabel('Valori')
plt.legend()
plt.show()

# Creazione del grafico delle correlazioni shiftate
plt.figure(figsize=(10, 6))
plt.plot(lags, correlations, marker='o')

# Aggiunta di etichette e titolo
plt.xlabel('Lag (mesi)')
plt.ylabel('Coefficiente di correlazione')
plt.title('Correlazione shiftata')
plt.axhline(y=0, color='black', linestyle='-', linewidth=1)  # Linea di riferimento a 0
plt.grid(True)
plt.tight_layout()

# Mostra il grafico
plt.show()