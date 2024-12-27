import numpy as np
import pandas as pd
from scipy.stats import norm
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import cloudscraper
from io import StringIO
import random
import math


def split_time_series(series, n):
    """
    Split a time series into n segments of equal size
    """
    split_series = [series[i:i+n] for i in range(0, len(series), n)]
    # if the last sequence is smaller than n, we discard it
    if len(split_series[-1]) < n:
        split_series = split_series[:-1]
    return np.array(split_series)

def split_sequence(sequence, k):
    """
    Split a sequence in two, where k is the size of the first sequence
    """
    return np.array(sequence[:int(len(sequence) * k)]), np.array(sequence[int(len(sequence) * k):])


def split_sequences(sequences, k=0.80):
    """
    Applies split_sequence on all elements of a list or array
    """
    return [split_sequence(sequence, k) for sequence in sequences]


# Parametri di ingresso
valInvest = 1121268
#valInvest = 1181507
symbol = ""
today = datetime.today()
some_months_ago = today - relativedelta(months=60)
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
Y = dati_chiusure_mese.values[::-1]  # Invertiamo i valori di Y per avere ordine cronologico crescente
#Y = (Y[1:] - Y[:-1]) / Y[:-1] * 100
Y = np.log(dati_chiusure_mese.values[::-1])
CHIUSURE=dati_chiusure_mese.values[::-1]
Y_min = np.min(Y)
Y_max = np.max(Y)

# Applicazione della normalizzazione Min-Max
Y = (Y - Y_min) / (Y_max - Y_min)


N = 10  # window size --> possiamo modificare questo parametro per sperimentare
K = 0.80 # split size --> 80% dei dati è in A, 20% in B

SEQS = split_time_series(Y, N) # crea sequenze di lunghezza N

SPLIT_SEQS = split_sequences(SEQS, K) # divide le sequenze in due

SEQS_CHIUSURE = split_time_series(CHIUSURE, N) 

SPLIT_SEQS_CHIUSURE = split_sequences(SEQS_CHIUSURE, K) 


A = [seq[0] for seq in SPLIT_SEQS]
B = [seq[1] for seq in SPLIT_SEQS]

A_CHIUSURE = [seq[0] for seq in SPLIT_SEQS_CHIUSURE]
B_CHIUSURE = [seq[1] for seq in SPLIT_SEQS_CHIUSURE]


def compute_dynamic_time_warping(a1, a2, chiusure_a1, chiusure_a2):
    """
    Compute the dynamic time warping between two sequences
    """
    
    DTW = {}

    for i in range(len(a1)):
        DTW[(i, -1)] = float('inf')
    for i in range(len(a2)):
        DTW[(-1, i)] = float('inf')
    DTW[(-1, -1)] = 0

    if chiusure_a1[-1]/chiusure_a1[0] >1.007 and chiusure_a2[-1]/chiusure_a2[0] <1:
        return 100
    if chiusure_a1[-1]/chiusure_a1[0] <0.993 and chiusure_a2[-1]/chiusure_a2[0] >1:
        return 100
    if chiusure_a2[-1]/chiusure_a2[0] >1.007 and chiusure_a1[-1]/chiusure_a1[0] <1:
        return 100
    if chiusure_a2[-1]/chiusure_a2[0] <0.993 and chiusure_a1[-1]/chiusure_a1[0] >1:
        return 100

    for i in range(len(a1)):
        for j in range(len(a2)):
            dist = (a1[i]-a2[j])**2
            DTW[(i, j)] = dist + min(DTW[(i-1, j)], DTW[(i, j-1)], DTW[(i-1, j-1)])

    return np.sqrt(DTW[len(a1)-1, len(a2)-1])


# create empty matrix
S = np.zeros((len(A), len(A)))

# populate S
for i in range(len(A)):
    for j in range(len(A)):
        # weigh the dynamic time warping with the correlation
        S[i, j] = compute_dynamic_time_warping(A[i], A[j],A_CHIUSURE[i], A_CHIUSURE[j])


# populate G
G = {}
#THRESHOLD =0.09*(N/10) # arbitrary value - tweak this to get different results
THRESHOLD =0.06*(N/10) # arbitrary value - tweak this to get different results
for i in range(len(S)):
    G[i] = []
    for j in range(len(S)):
        if S[i, j] < THRESHOLD and i != j and (i, j) not in G and (j, i) not in G and j not in G[i] and len(G[i])<5:
            already_added = False
            for key in G:
                if j in G[key]:
                    already_added = True
                    break
            # Aggiungi j solo se non è già stato aggiunto a nessun'altra chiave
            if not already_added:
                G[i].append(j)
            #G[i].append(j)


# remove any empty groups
G = {k: v for k, v in G.items() if len(v)>2}
print("Gruppi G")
print(G)


# Inizializzazione dei pesi e bias
def init_rnn_weights(DIM_INPUT, DIM_HIDDEN, DIM_OUTPUT):
    W_xh = [[random.gauss(0, 0.01) for _ in range(DIM_HIDDEN)] for _ in range(DIM_INPUT)]
    W_hh = [[random.gauss(0, 0.01) for _ in range(DIM_HIDDEN)] for _ in range(DIM_HIDDEN)]
    W_hy = [[random.gauss(0, 0.01) for _ in range(DIM_OUTPUT)] for _ in range(DIM_HIDDEN)]
    b_h = [0.0 for _ in range(DIM_HIDDEN)]
    b_y = [0.0 for _ in range(DIM_OUTPUT)]
    return W_xh, W_hh, W_hy, b_h, b_y

# Funzione di attivazione sigmoid
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

# Applica sigmoid elemento per elemento
def apply_sigmoid(vec):
    return [sigmoid(x) for x in vec]

# Forward pass della RNN
def rnn_forward(X, W_xh, W_hh, W_hy, b_h, b_y):
    N = len(X)
    DIM_INPUT = len(X[0])
    DIM_HIDDEN = len(W_xh[0])
    h = [[0.0 for _ in range(DIM_HIDDEN)] for _ in range(N)]
    for t in range(N):
        h_t = [0.0 for _ in range(DIM_HIDDEN)]
        for j in range(DIM_HIDDEN):
            sum_xh = sum(X[t][k] * W_xh[k][j] for k in range(DIM_INPUT))
            #sum_xh=0
            #for k in range(DIM_INPUT):
            #    sum_xh = sum_xh+(X[t][k] * W_xh[k][j])
            sum_hh = sum(h[t-1][l] * W_hh[l][j] for l in range(DIM_HIDDEN)) if t > 0 else 0
            h_t[j] = sigmoid(sum_xh + sum_hh + b_h[j])
        h[t] = h_t

    y = [[0.0 for _ in range(len(W_hy[0]))] for _ in range(N)]
    for i in range(N):
        for j in range(len(W_hy[0])):
            sum_hy = sum(h[i][k] * W_hy[k][j] for k in range(DIM_HIDDEN))
            y[i][j] = sigmoid(sum_hy + b_y[j])

    return y, h

# Funzione di loss: Mean Squared Error
def mean_squared_error(y_true, y_pred):
    N = len(y_true)
    error = 0.0
    for i in range(N):
        for j in range(len(y_true[i])):
            error += (y_true[i][j] - y_pred[i][j]) ** 2
        if y_true[i][-1]/y_true[i][0]>1 and y_pred[i][-1]/y_pred[i][0]<1:
                error +=0.1
        if y_true[i][-1]/y_true[i][0]<1 and y_pred[i][-1]/y_pred[i][0]>1:
                error +=0.1

    return error / N

# Derivata della funzione sigmoid
def sigmoid_derivative(x):
    return x * (1 - x)

# Applica la derivata della sigmoid elemento per elemento
def apply_sigmoid_derivative(vec):
    return [sigmoid_derivative(x) for x in vec]

# Backward pass della RNN e aggiornamento dei pesi
def rnn_backward(X, y_true, y_pred, h, W_xh, W_hh, W_hy, b_h, b_y, learning_rate):
    N = len(X)
    DIM_INPUT = len(X[0])
    DIM_HIDDEN = len(W_xh[0])
    DIM_OUTPUT = len(W_hy[0])

    # Gradienti per i pesi
    dW_xh = [[0.0 for _ in range(DIM_HIDDEN)] for _ in range(DIM_INPUT)]
    dW_hh = [[0.0 for _ in range(DIM_HIDDEN)] for _ in range(DIM_HIDDEN)]
    dW_hy = [[0.0 for _ in range(DIM_OUTPUT)] for _ in range(DIM_HIDDEN)]
    db_h = [0.0 for _ in range(DIM_HIDDEN)]
    db_y = [0.0 for _ in range(DIM_OUTPUT)]

    # Gradienti degli stati nascosti
    dh_next = [0.0 for _ in range(DIM_HIDDEN)]

    for t in reversed(range(N)):
        dy = [y_pred[t][j] - y_true[t][j] for j in range(DIM_OUTPUT)]
        dy = apply_sigmoid_derivative(dy)

        for j in range(DIM_OUTPUT):
            for k in range(DIM_HIDDEN):
                dW_hy[k][j] += dy[j] * h[t][k]
            db_y[j] += dy[j]

        dh = [0.0 for _ in range(DIM_HIDDEN)]
        for j in range(DIM_HIDDEN):
            dh[j] = sum(dy[k] * W_hy[j][k] for k in range(DIM_OUTPUT)) + dh_next[j]
            dh[j] *= sigmoid_derivative(h[t][j])

        for j in range(DIM_HIDDEN):
            for k in range(DIM_INPUT):
                dW_xh[k][j] += dh[j] * X[t][k]
            for k in range(DIM_HIDDEN):
                if t > 0:
                    dW_hh[k][j] += dh[j] * h[t-1][k]
            db_h[j] += dh[j]
            dh_next[j] = sum(dh[k] * W_hh[j][k] for k in range(DIM_HIDDEN))

    # Aggiornamento dei pesi
    for i in range(DIM_INPUT):
        for j in range(DIM_HIDDEN):
            W_xh[i][j] -= learning_rate * dW_xh[i][j]

    for i in range(DIM_HIDDEN):
        for j in range(DIM_HIDDEN):
            W_hh[i][j] -= learning_rate * dW_hh[i][j]

    for i in range(DIM_HIDDEN):
        for j in range(DIM_OUTPUT):
            W_hy[i][j] -= learning_rate * dW_hy[i][j]

    for j in range(DIM_HIDDEN):
        b_h[j] -= learning_rate * db_h[j]

    for j in range(DIM_OUTPUT):
        b_y[j] -= learning_rate * db_y[j]

# Addestramento della RNN
def train_rnn(X_train, y_train, DIM_INPUT, DIM_HIDDEN, DIM_OUTPUT, epochs=10, learning_rate=0.01):
    W_xh, W_hh, W_hy, b_h, b_y = init_rnn_weights(DIM_INPUT, DIM_HIDDEN, DIM_OUTPUT)
    loss=100
    epoch=0
    #for epoch in range(epochs):
    while loss>0.00001 and epoch<50000:
        y_pred, h = rnn_forward(X_train, W_xh, W_hh, W_hy, b_h, b_y)
        loss = mean_squared_error(y_train, y_pred)
        rnn_backward(X_train, y_train, y_pred, h, W_xh, W_hh, W_hy, b_h, b_y, learning_rate)
        epoch=epoch+1
        
    return W_xh, W_hh, W_hy, b_h, b_y

W_xh=[]
W_hh=[]
W_hy=[]
b_h=[]
b_y=[]

def flatten_list(nested_list):
    flattened_list = []
    for sublist in nested_list:
        for item in sublist:
            flattened_list.append(item)
    return flattened_list

RNNItems={}
for k, v in G.items():
    TargetA=[]
    TargetB=[]
    
    TargetA.append([list(A[seq]) for seq in v])
    TargetB.append([list(B[seq]) for seq in v])

    TargetA = flatten_list(TargetA)
    TargetB = flatten_list(TargetB)

    num_samples = len(TargetA)
    num_timesteps = len(TargetA[0])
    num_timestepsB = len(TargetB[0])
        
    # Parametri della RNN
    input_dim = num_timesteps
    hidden_units = int(num_timesteps/2)
    output_dim = num_timestepsB
    
    # Addestramento della RNN
    val_W_xh, val_W_hh, val_W_hy, val_b_h, val_b_y = train_rnn(TargetA, TargetB, input_dim, hidden_units, output_dim, epochs=200, learning_rate=0.1)
    W_xh.append(val_W_xh)
    W_hh.append(val_W_hh)
    W_hy.append(val_W_hy)
    b_h.append(val_b_h)
    trained_rnn_params=val_W_xh, val_W_hh, val_W_hy, val_b_h, val_b_y 
    RNNItems[k]=trained_rnn_params

def check_sequence_belongs_to_network(sequence, sequenceTest,chiusureA, chiusureB, trained_rnn_params):
    W_xh, W_hh, W_hy, b_h, b_y = trained_rnn_params
    output, _ = rnn_forward([sequence], W_xh, W_hh, W_hy, b_h, b_y)
    val=mean_squared_error(output,sequenceTest.reshape(1, -1))
    if chiusureB[-1]/chiusureA[-1]<1.0005 and chiusureB[-1]/chiusureA[-1]>0.9995:
        trend ="stabile"
    if chiusureB[-1]/chiusureA[-1]>1.0005:
        trend ="salita"
    if chiusureB[-1]/chiusureA[-1]<0.9995:
        trend ="discesa"

    return val,trend
    


import math

def plot_similar_sequences1(G):
    n_col = round(math.sqrt(len(G)))
    if (math.sqrt(len(G)) > int(math.sqrt(len(G)))):
         n_col = int(math.sqrt(len(G))) + 1
    fig, ax = plt.subplots(n_col, n_col, figsize=(n_col * 5, 5 * n_col))
    r = 0
    c = 0
    for key in G.keys():
        for j in G[key]:
            if (r >= n_col):
                print("Errore")
            if (c >= n_col):
                c = 0
                r = r + 1
            ax[r][c].set_title(f'Group {key}', fontdict={"fontsize": 10, "weight": 600})
            ax[r][c].plot(A[j], label=j, linewidth=3, alpha=0.50)
        ax[r][c].plot(A[key], label=f'target {j}', linewidth=5, color='black')
        #ax[r][c].annotate(f'{key}', xy=(len(A[key]) - 1, A[key][-1]), xytext=(len(A[key]) - 1, A[key][-1]))
        ax[r][c].plot(np.mean(A[key], axis=0), label='average', color='black', linestyle='--')
        c = c + 1
    #plt.tight_layout()
    plt.get_current_fig_manager().window.state('zoomed')
    plt.show()


def plot_similar_sequences(G):
    n_plots = len(G)
    n_col = round(math.sqrt(n_plots))
    n_row = n_col if n_col * n_col >= n_plots else n_col + 1
    
    fig, ax = plt.subplots(n_row, n_col, figsize=(n_col * 5, 5 * n_row))
    ax = ax.flatten()  # Rende l'array 2D degli assi un array 1D per una gestione più semplice

    r = 0
    c = 0
    for idx, key in enumerate(G.keys()):
        for j in G[key]:
            ax[idx].plot(A[j], label=j, linewidth=3, alpha=0.50)
        ax[idx].plot(A[key], linewidth=3, color='black')
        ax[idx].plot(np.mean([A[j] for j in G[key]], axis=0), label='average', color='black', linestyle='--')
        #ax[idx].set_title(f'Group {key}', fontdict={"fontsize": 10, "weight": 600})
    
    plt.tight_layout()
    plt.get_current_fig_manager().window.state('zoomed')
    plt.show()

plot_similar_sequences(G)

def classify_trend(a, b, threshold=0.05):
    """
    Classify the trend of a vector
    """
    # compute slope
    slope = np.mean((b[-1]-a[-1]) / (np.diff(np.arange(len(b)))+1))
    # if slope is positive, the trend is upward
    if slope + (slope * threshold) > 0:
        return 1
    # if slope is negative, the trend is downward
    elif slope - (slope * threshold) < 0:
        return -1
    # if slope is close to 0, the trend is flat
    else:
        return 0
        
# flatten list
flattened_G = [item for sublist in G.values() for item in sublist]
trends = [classify_trend(A[i],B[i]) for i in flattened_G]

# what is the probability of seeing a trend given the A sequence?
PROBABILITIES = {}
RNN={}

#for k, v in G.items():
#    total = len(v)
#    seq_trends = [classify_trend(A[seq],B[seq]) for seq in v]
#    prob_up = len([t for t in seq_trends if t == 1]) / total
#    prob_down = len([t for t in seq_trends if t == -1]) / total
#    prob_stable = len([t for t in seq_trends if t == 0]) / total
#    min_out=100
#    trendfix=""
#    item=-1
#    for seq in v:
#        for key, value in RNNItems.items():
#            out,trend=check_sequence_belongs_to_network(A[seq],B[seq], A_CHIUSURE[seq], B_CHIUSURE[seq],RNNItems[key])
#            if out<min_out:
#                min_out=out
#                item=key
#                trendfix=trend
#    PROBABILITIES[k] = {'up': prob_up, 'down': prob_down, 'stable': prob_stable, 'RNN': item, "Trend":trendfix}
                
       


for k, v in G.items():
    #for seq in v:
    total = len(v)
    seq_trends = [classify_trend(A[seq],B[seq]) for seq in v]
    prob_up = len([t for t in seq_trends if t == 1]) / total
    prob_down = len([t for t in seq_trends if t == -1]) / total
    prob_stable = len([t for t in seq_trends if t == 0]) / total
    min_out=100
    trendfix=""
    item=-1
    for key, value in RNNItems.items():
        sumout=0
        sumup=0
        sumdown=0
        sumst=0
        for seq in v:
            out,trend=check_sequence_belongs_to_network(A[seq],B[seq], A_CHIUSURE[seq], B_CHIUSURE[seq],RNNItems[key])
            sumout= sumout+out
            if trend=='salita':
                sumup=sumup+1
            if trend=='discesa':
                sumdown=sumdown+1
            if trend=='stabile':
                sumst=sumst+1
        if sumout<min_out:
            min_out=sumout
            item=key
        if sumup>sumdown:
            trendfix='salita'
        if sumdown>sumup:
            trendfix='discesa'
        if sumup==sumdown:
            trendfix='stabile'
    PROBABILITIES[k] = {'up': prob_up, 'down': prob_down, 'stable': prob_stable, 'RNN': k, "Trend":trendfix}


# Let's pack all in a Pandas DataFrame for an easier use
probs_df = pd.DataFrame(PROBABILITIES).T
# create a column that contains the number of elements in the group
probs_df['n_elements'] = probs_df.apply(lambda row: len(G[row.name]), axis=1)
probs_df.sort_values(by=["n_elements"], ascending=False, inplace=True)
print(probs_df)

#Calcolo ultima sequenza e cataloga in G
def split_time_series(series, n):
    split_series=[]
    for i in range(len(series)-n, len(series)):
        split_series.append(series[i])
    #split_series = [series[i:i+n] for i in range(len(series)-n, len(series), n)]
    return split_series

ULTIMASEQ = split_time_series(Y, int(N*K)) # crea ultima sequenze di lunghezza N
ULTIMASEQ_CHIUSURE = split_time_series(CHIUSURE, int(N*K))
print(ULTIMASEQ)
print(ULTIMASEQ_CHIUSURE)

dtw_results = {}

# Calcolare i risultati della funzione per ciascuna chiave in G.keys()
for k in G.keys():
    dtw_value = compute_dynamic_time_warping(ULTIMASEQ, A[k], ULTIMASEQ_CHIUSURE, A_CHIUSURE[k])
    dtw_results[k] = dtw_value
    out,trend=check_sequence_belongs_to_network(A[k],B[k], A_CHIUSURE[k], B_CHIUSURE[k],RNNItems[k])

# Ordinare il dizionario per valore (in ordine crescente)
sorted_dtw_results = dict(sorted(dtw_results.items(), key=lambda item: item[1]))

def check_sequence_RNN(sequence, trained_rnn_params):
    W_xh, W_hh, W_hy, b_h, b_y = trained_rnn_params
    output, _ = rnn_forward([sequence], W_xh, W_hh, W_hy, b_h, b_y)
    flat_list = sum(output, [])
    if flat_list[-1]/flat_list[0]<1.0005 and flat_list[-1]/flat_list[0]>0.9995:
        trend ="stabile"
    if flat_list[-1]/flat_list[0]>1.0005:
        trend ="salita"
    if flat_list[-1]/flat_list[0]<0.9995:
        trend ="discesa"

    return output,trend
    

# Stampa delle chiavi e dei valori ordinati
for k, v in sorted_dtw_results.items():
     print(f"{k} {v} {PROBABILITIES[k]} {ULTIMASEQ[-1]} {check_sequence_RNN(ULTIMASEQ,RNNItems[PROBABILITIES[k]['RNN']])}")   
     #print(f"{k} {v} {PROBABILITIES[k]} {ULTIMASEQ[-1]} {check_sequence_RNN(ULTIMASEQ,RNNItems[k])}")   