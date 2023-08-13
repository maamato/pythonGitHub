from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from dateutil import parser
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from dateutil import parser
import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.sidebar.header('Inflazione')

def get_input():
    selezione = st.sidebar.selectbox('Inflazione tasso', ('2.0', '2.5', '3.0', '4.0'))
    return selezione

infl = float(get_input())
st.header(f"""
    Grafico TIR inflazione {infl}
    """)


def request(val):
    req = Request(
        url='https://it.investing.com/rates-bonds/'+val+'-historical-data', 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req).read()
    soup=BeautifulSoup(webpage,'html.parser')

    price = soup.find('span', {'class': 'text-2xl', 'data-test': 'instrument-price-last'})
    #element = soup.find('input', attrs={'class': "newInput inputTextBox alertValue"})
    #print(element)
    valore=price.text
    #print(element.get('value'))
    return valore

dizionarioPrezzi={}
dizionario = {'Nov23':'btp-italia-nv23-eur','Apr24':'btp-italia-ap24-eur','Oct24':'btp-italia-ot24-eur','Mag25':'it0005410912','Mag26':'btp-italia-mg26-eur','Oct27':'itgovt-.65-28-oct-2027','Mar28':'it0005532723','Nov28':'it0005517195', 'Giu30':'it0005497000' }
for key, value in dizionario.items():
    prezzo=request(value)
    valore = prezzo.replace(",",".")
    #prezzo=0
    dizionarioPrezzi[key]=float(valore)


#print(dizionarioPrezzi)

#def requestFOI():
#    read_foi=pd.read_html('http://dati.istat.it/Index.aspx?DataSetCode=DCSP_FOI1B2015')
#    print(f'Tabelle totali = {len(read_foi)}')

    #Converte in dataframe la tabella 0
#    df=read_foi[0]

    #Visualizza informazioni sui campi della tabella
#    print(df.info())
#    print(df)
 
#requestFOI()

def listaDiffDate(dateCedole):
    diffDateCashFlow =[]
    diffDateCashFlow = [(parser.parse(dateCedole[i + 1]) - parser.parse(dateCedole[i])).days for i in range(len(dateCedole)-1)]
    listaDiffDate=[]
    tot=1
    for i in diffDateCashFlow:
        listaDiffDate.append(i+tot)
        tot =i+tot
    return listaDiffDate


def listaDateCedole(dataScadenza):
    listDate =[]
    six_months_before = dataScadenza - relativedelta(months=+6)
    listDate.append(dataScadenza.strftime('%Y-%m-%d'))
    while date.today()<six_months_before:
        listDate.append(six_months_before.strftime('%Y-%m-%d'))
        six_months_before = six_months_before - relativedelta(months=+6)
    listDate.append(date.today().strftime('%Y-%m-%d'))
    
    return listDate


dizionarioScadenze= {'Nov23':'2023-11-20','Apr24':'2024-04-11','Oct24':'2024-10-24','Mag25':'2025-05-26','Mag26':'2026-05-21','Oct27':'2027-10-28','Mar28':'2028-03-14','Nov28':'2028-11-22', 'Giu30':'2030-06-28' }
dizionarioCedole= {'Nov23':'0.25','Apr24':'0.40','Oct24':'0.35','Mag25':'1.40','Mag26':'0.55','Oct27':'0.65','Mar28':'2.00','Nov28':'1.60', 'Giu30':'1.60' }

dizionarioCadenzaCedole={}
for key, value in dizionarioScadenze.items():
    val=datetime.datetime.strptime(value, "%Y-%m-%d").date()
    #print(val)
    listaCedoleDate=listaDateCedole(val)
    listaCedoleDate.reverse()
    #print(listaCedoleDate)
    listaDifferenzaDate=listaDiffDate(listaCedoleDate)
    dizionarioCadenzaCedole[key]=listaDifferenzaDate

print(dizionarioCadenzaCedole)

def nome_mese_italiano(numero_mese):
    mesi_italiani = {
        1: "gennaio",
        2: "febbraio",
        3: "marzo",
        4: "aprile",
        5: "maggio",
        6: "giugno",
        7: "luglio",
        8: "agosto",
        9: "settembre",
        10: "ottobre",
        11: "novembre",
        12: "dicembre"
    }

    if numero_mese in mesi_italiani:
        return mesi_italiani[numero_mese]
    else:
        return "Numero mese non valido"

#mese='luglio-2023'
datedataOggi = date.today()+timedelta(days=0)
todayYear= datedataOggi.year
todayMonth=datedataOggi.month
meseItaliano=nome_mese_italiano(todayMonth)
mese=meseItaliano+'-'+str(todayYear)
dizionarioFileCI= {'Nov23':'https://www.dt.mef.gov.it/modules/documenti_it/debito_pubblico/coefficienti_indicizzazione/btp_italia_20231120/Coefficienti-di-indicizzazione-BTP-Italia-'+mese+'-20.11.2023.csv','Apr24':'https://www.dt.mef.gov.it/modules/documenti_it/debito_pubblico/coefficienti_indicizzazione/btp_italia_20240411/Coefficienti-di-indicizzazione-BTP-Italia-'+mese+'-11.04.2024.csv','Oct24':'https://www.dt.mef.gov.it/modules/documenti_it/debito_pubblico/coefficienti_indicizzazione/btp_italia_20241024/Coefficienti-di-indicizzazione-BTP-Italia-'+mese+'-24.10.2024.csv','Mag25':'https://www.dt.mef.gov.it/modules/documenti_it/debito_pubblico/coefficienti_indicizzazione/btp_italia_20250526/Coefficienti-di-indicizzazione-BTP-Italia-'+mese+'-26.05.2025.csv','Mag26':'https://www.dt.mef.gov.it/modules/documenti_it/debito_pubblico/coefficienti_indicizzazione/btp_italia_20260521/Coefficienti-di-indicizzazione-BTP-Italia-'+mese+'-21.05.2026.csv','Oct27':'https://www.dt.mef.gov.it/modules/documenti_it/debito_pubblico/coefficienti_indicizzazione/btp_italia_20271028/Coefficienti-di-indicizzazione-BTP-Italia-'+mese+'-28.10.2027.csv','Mar28':'https://www.dt.mef.gov.it/modules/documenti_it/debito_pubblico/coefficienti_indicizzazione/btp_italia_20280314/Coefficienti-di-indicizzazione-BTP-Italia-'+mese+'-14.03.2028.csv','Nov28':'https://www.dt.mef.gov.it/modules/documenti_it/debito_pubblico/coefficienti_indicizzazione/btp_italia_20281122/Coefficienti-di-indicizzazione-BTP-Italia-'+mese+'-22.11.2028.csv', 'Giu30':'https://www.dt.mef.gov.it/modules/documenti_it/debito_pubblico/coefficienti_indicizzazione/btp_italia_20300628/Coefficienti-di-indicizzazione-BTP-Italia-'+mese+'-28.06.2030.csv' }



import pandas as pd

def leggiCI(val):
    #print(val)
    table_read =pd.read_csv(val, sep=';')
    table_read1 = table_read.iloc[:,1:3]
    table_read1=table_read1.dropna()
    dateContenuta = date.today()+timedelta(days=0)
    riga=table_read1[table_read1['Unnamed: 1'].str.contains(dateContenuta.strftime('%d/%m/%Y'))]
    try:
        valore = riga.iloc[0,1]
    except:
        table_read2 = table_read.iloc[:,[1,3]]
        table_read2=table_read2.dropna()
        riga2=table_read2[table_read2['Unnamed: 1'].str.contains(dateContenuta.strftime('%d/%m/%Y'))]
        valore = riga2.iloc[0,1]
        
 
    valore = valore.replace(",",".")
    return float(valore)

dizionarioCI={}
for key, value in dizionarioFileCI.items():
    coeffCI=leggiCI(value)
    dizionarioCI[key]=coeffCI

#print(dizionarioCI)
import math
def tir_calcolo1(cashFlows, listaDiffDate):
    copialistDiffDate = listaDiffDate.copy()
    copiaCashFlow=cashFlows.copy()
    faceValue=10000
    flussoDiCassa=[]
    price=0
    r1=-1.0
    r2=1.0
    for i in range(len(copiaCashFlow)):
        if i==0:
            price=abs(copiaCashFlow[0])
        else:
            flussoDiCassa.append(copiaCashFlow[i])
    flussoDiCassa[-1]=abs(faceValue-flussoDiCassa[-1])
    rate = (r1 + r2)/2
    estimatedPrice=0
    for i in range(len(flussoDiCassa)-1):
        estimatedPrice = estimatedPrice + (flussoDiCassa[i]/pow(math.e, rate*copialistDiffDate[i]/356.0))
    estimatedPrice = estimatedPrice + ((flussoDiCassa[-1]+faceValue)/pow(math.e, rate*copialistDiffDate[-1]/356.0))
    while abs(estimatedPrice-price)>0.01:
        if estimatedPrice-price>0:
            r1=rate
            rate=(r1 + r2)/2 
        else:
            r2 = rate
            rate = (r1 + r2)/2
        estimatedPrice=0
        for i in range(len(flussoDiCassa)-1):
            estimatedPrice = estimatedPrice + (flussoDiCassa[i]/pow(math.e, rate*copialistDiffDate[i]/356.0))
        estimatedPrice = estimatedPrice + ((flussoDiCassa[-1]+faceValue)/pow(math.e, rate*copialistDiffDate[-1]/356.0))
    return rate*100


def tir_calcolo(cashFlows, listaDiffDate):
    copialistDiffDate = listaDiffDate.copy()
    copialistDiffDate.insert(0,1)
    copiaCashFlow=cashFlows.copy()
    
    print(copiaCashFlow)
    print(copialistDiffDate)
    for volte in range(-1000,1000):
        guess=float(volte/10000)
        sum=0
        for i in range(len(copiaCashFlow)):
            sum += float(copiaCashFlow[i])/pow((1+guess),(copialistDiffDate[i])/365)
        if sum<0.00001:
            break
    if guess==0.0999:
        for volte in range(-1000,1000):
            guess=float(volte/10000)
            sum=0
            for i in range(len(copiaCashFlow)):
                sum += float(copiaCashFlow[i])/pow((1+guess),(copialistDiffDate[i])/365)
            if (sum<100):
                break

    return guess*100



def generateCashFlow(dizionarioCadenzaCedole, dizionarioCedole, val):
    diz={}
    for key, value in dizionarioCedole.items():
        cedoleLista=[]
        for i in range(len(dizionarioCadenzaCedole[key])+1):
            if val=='Defl':
                if i==0:
                    valoreIniziale =((-1)*float(dizionarioPrezzi[key])*(float(dizionarioCI[key]))*100-0.875*float(dizionarioCI[key])*(float(value)*100/2-float(value)*100*float(dizionarioCadenzaCedole[key][i])/365))
                    cedoleLista.append(valoreIniziale)
                else:
                    if i==1:
                        cedoleLista.append(0.875*float(value)*100/2)
                    else:
                        cedoleLista.append(0.875*float(value)*100/2)
            if val=='CI':
                if i==0:
                    #print(dizionarioCadenzaCedole[key][0])
                    valoreIniziale =((-1)*float(dizionarioPrezzi[key]*((float(dizionarioCI[key]))))*100-0.875*float(dizionarioCI[key])*(float(value)*100/2-float(value)*100*float(dizionarioCadenzaCedole[key][i])/365))
                    cedoleLista.append(valoreIniziale)
                else:
                    if i==1:
                        cedoleLista.append(((float(dizionarioCI[key])-1)*10000*0.875+0.875*float(value)*float(dizionarioCI[key])*100/2))
                    else:
                        cedoleLista.append(0.875*float(value)*100/2)
            if val=='Infl':
                if i==0:
                    valoreIniziale =((-1)*float(dizionarioPrezzi[key]*((float(dizionarioCI[key]))))*100-0.875*float(dizionarioCI[key])*(float(value)*100/2-float(value)*100*float(dizionarioCadenzaCedole[key][i])/365))
                    cedoleLista.append(valoreIniziale)
                else:
                    if i==1:
                        cedoleLista.append(max(100*0.875*infl/2+0.875*float(value)*100/2,((float(dizionarioCI[key])-1)*10000*0.875+0.875*float(value)*float(dizionarioCI[key])*100/2)))
                    else:
                        cedoleLista.append(100*0.875*infl/2+0.875*float(value)*100/2)
          
        cedoleLista[-1]=float(cedoleLista[-1])+10000
        diz[key]=cedoleLista
    return diz



print("DIZIONARIO DEFLAZIONE")
dizionarioCedoleDeflLista={}
dizionarioCedoleDeflLista=generateCashFlow(dizionarioCadenzaCedole, dizionarioCedole, 'Defl')
print(dizionarioCedoleDeflLista)

print("DIZIONARIO CI")
dizionarioCedoleCILista={}
dizionarioCedoleCILista=generateCashFlow(dizionarioCadenzaCedole, dizionarioCedole,'CI')
print(dizionarioCedoleCILista)

print("DIZIONARIO CI poi inflazione")
dizionarioCedoleInflLista={}
dizionarioCedoleInflLista=generateCashFlow(dizionarioCadenzaCedole, dizionarioCedole, 'Infl')
print(dizionarioCedoleInflLista)


print("TIR con DEFLAZIONE")

dizionarioTIRDEFL={}
for key, value in dizionarioCedoleDeflLista.items():
    dizionarioTIRDEFL[key]=tir_calcolo1(dizionarioCedoleDeflLista[key],dizionarioCadenzaCedole[key])

print(dizionarioTIRDEFL)

print("TIR CON CI e senza inflazione")
dizionarioTIR={}
for key, value in dizionarioCedoleCILista.items():
    dizionarioTIR[key]=tir_calcolo1(dizionarioCedoleCILista[key],dizionarioCadenzaCedole[key])

print(dizionarioTIR)

print("TIR con Inflazione")
dizionarioTIRINFL={}
for key, value in dizionarioCedoleInflLista.items():
    dizionarioTIRINFL[key]=tir_calcolo1(dizionarioCedoleInflLista[key],dizionarioCadenzaCedole[key])

print(dizionarioTIRINFL)


print("TIR SuperReale Infl")
dizionarioSuperR={}
for key, value in dizionarioTIRINFL.items():
    dizionarioSuperR[key]=((1+dizionarioTIRINFL[key]/100)/(1+infl/100)-1)*100

print(dizionarioSuperR)

diffDateCashFlowString=list(dizionarioScadenze.values())
tir=list(dizionarioTIR.values())
tirDefl=list(dizionarioTIRDEFL.values())
tirInfl=list(dizionarioTIRINFL.values())
tirSR=list(dizionarioSuperR.values())
#print("REGRESSIONE")
diffDateCashFlow = [[((parser.parse(diffDateCashFlowString[i]) - parser.parse(date.today().strftime('%Y-%m-%d'))).days)/365] for i in range(len(diffDateCashFlowString))]
diffDateCashFlowx = [((parser.parse(diffDateCashFlowString[i]) - parser.parse(date.today().strftime('%Y-%m-%d'))).days)/365 for i in range(len(diffDateCashFlowString))]
#print(diffDateCashFlow)
tiry = [[tir[i]] for i in range(len(tir))]
tiryDefl = [[tirDefl[i]] for i in range(len(tirDefl))]
tiryInfl = [[tirInfl[i]] for i in range(len(tirInfl))]
tirySR = [[tirSR[i]] for i in range(len(tirSR))]
#tiry = np.array(tir).reshape(1,-1)
#print(tiry)

def getRegression(x_diffDateCashFlow, y_tir):
    linear_reg = LinearRegression()
    linear_reg.fit(x_diffDateCashFlow, y_tir)
    polynomial_reg = PolynomialFeatures(degree=3)
    X_poly = polynomial_reg.fit_transform(x_diffDateCashFlow)
    polynom_reg = LinearRegression()
    polynom_reg.fit(X_poly, y_tir)
    return linear_reg, polynom_reg, polynomial_reg


lin_reg, pol_reg, poly_reg=getRegression(diffDateCashFlow, tiry)
X=diffDateCashFlow
y=tiry

lin_regDefl, pol_regDefl, poly_regDefl=getRegression(diffDateCashFlow,tiryDefl)
XDefl=diffDateCashFlow
yDefl=tiryDefl

lin_regInfl, pol_regInfl, poly_regInfl=getRegression(diffDateCashFlow,tiryInfl)
XInfl=diffDateCashFlow
yInfl=tiryInfl

lin_regSR, pol_regSR, poly_regSR=getRegression(diffDateCashFlow,tirySR)
XSR=diffDateCashFlow
ySR=tirySR

fig = go.Figure()


fig.add_trace(go.Scatter(
    x=diffDateCashFlowx,
    y=tir,
    mode='markers',
    name="tir"       
))

Y=(lin_reg.predict(X).flatten())
fig.add_trace(go.Scatter(
    x=diffDateCashFlowx,
    y=Y,
    mode='lines',
    name="Lineare"       
))

Y=(pol_reg.predict(poly_reg.fit_transform(X)).flatten())
fig.add_trace(go.Scatter(
    x=diffDateCashFlowx,
    y=Y,
    mode='lines',
    name="Polinomiale"       
))


fig.update_layout(
    title="Regressione TIR CI",
    xaxis_title="Anni",
    yaxis_title="Tir%",
    legend_title="Correlazioni",
    font=dict(
        family="Courier New, monospace",
        size=12,
        color="RebeccaPurple"
    )
)

figSR = go.Figure()


figSR.add_trace(go.Scatter(
    x=diffDateCashFlowx,
    y=tirSR,
    mode='markers',
    name="tir"       
))

YSR=(lin_regSR.predict(X).flatten())
figSR.add_trace(go.Scatter(
    x=diffDateCashFlowx,
    y=YSR,
    mode='lines',
    name="Lineare"       
))

YSR=(pol_regSR.predict(poly_regSR.fit_transform(XSR)).flatten())
figSR.add_trace(go.Scatter(
    x=diffDateCashFlowx,
    y=YSR,
    mode='lines',
    name="Polinomiale"       
))


figSR.update_layout(
    title="Super Reale",
    xaxis_title="Anni",
    yaxis_title="Tir%",
    legend_title="Correlazioni",
    font=dict(
        family="Courier New, monospace",
        size=12,
        color="RebeccaPurple"
    )
)


figDefl = go.Figure()


figDefl.add_trace(go.Scatter(
    x=diffDateCashFlowx,
    y=tirDefl,
    mode='markers',
    name="tir"       
))

YDefl=(lin_regDefl.predict(X).flatten())
figDefl.add_trace(go.Scatter(
    x=diffDateCashFlowx,
    y=YDefl,
    mode='lines',
    name="Lineare"       
))

YDefl=(pol_regDefl.predict(poly_regDefl.fit_transform(XDefl)).flatten())
figDefl.add_trace(go.Scatter(
    x=diffDateCashFlowx,
    y=YDefl,
    mode='lines',
    name="Polinomiale"       
))


figDefl.update_layout(
    title="Regressione TIR Deflazione",
    xaxis_title="Anni",
    yaxis_title="Tir%",
    legend_title="Correlazioni",
    font=dict(
        family="Courier New, monospace",
        size=12,
        color="RebeccaPurple"
    )
)

figInfl = go.Figure()


figInfl.add_trace(go.Scatter(
    x=diffDateCashFlowx,
    y=tirInfl,
    mode='markers',
    name="tir"       
))

YInfl=(lin_regInfl.predict(X).flatten())
figInfl.add_trace(go.Scatter(
    x=diffDateCashFlowx,
    y=YInfl,
    mode='lines',
    name="Lineare"       
))

YInfl=(pol_regInfl.predict(poly_regInfl.fit_transform(XInfl)).flatten())
figInfl.add_trace(go.Scatter(
    x=diffDateCashFlowx,
    y=YInfl,
    mode='lines',
    name="Polinomiale"       
))


figInfl.update_layout(
    title="Regressione TIR Inflazione",
    xaxis_title="Anni",
    yaxis_title="Tir%",
    legend_title="Correlazioni",
    font=dict(
        family="Courier New, monospace",
        size=12,
        color="RebeccaPurple"
    )
)


tableDataframe=[]
listaPrezzi=[]
listaTitoli=[]
listaCI=[]
listaSR=[]
listaTIR=[]
listaTIRDefl=[]
listaTIRInfl=[]
for key, value in dizionarioPrezzi.items():
    listaTitoli.append(key)
    listaPrezzi.append(value)

for key, value in dizionarioCI.items():
    listaCI.append(value)


for key, value in dizionarioTIR.items():
    listaTIR.append(value)

for key, value in dizionarioSuperR.items():
    listaSR.append(value)
    
for key, value in dizionarioTIRDEFL.items():
    listaTIRDefl.append(value)

for key, value in dizionarioTIRINFL.items():
    listaTIRInfl.append(value)


for i in range(len(listaTIR)):
    tableDataframe.append((listaTitoli[i],listaPrezzi[i],listaCI[i],listaTIR[i], listaSR[i], listaTIRDefl[i],listaTIRInfl[i]))

pdFinale= pd.DataFrame(tableDataframe, columns=('Titolo', 'Prezzo', 'CI', 'TirCI%', 'TirSR%', 'TirDefl%', 'TirInfl%'))


left, middle, right = st.columns((1, 6, 1))
with middle:
    st.write(pdFinale.astype(object))


#st.dataframe(pdFinale)

st.plotly_chart(fig, use_container_width=True)
st.plotly_chart(figSR, use_container_width=True)
st.plotly_chart(figDefl, use_container_width=True)
st.plotly_chart(figInfl, use_container_width=True)