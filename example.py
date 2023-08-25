import matplotlib.pyplot as plt
from datetime import datetime, timedelta

data1 = {
    '27/10/2021': -0.556, '05/11/2021': -0.567, '16/11/2021': -0.558, '25/11/2021': -0.575,
    '06/12/2021': -0.562, '15/12/2021': -0.602, '24/12/2021': -0.587, '04/01/2022': -0.565,
    '13/01/2022': -0.563, '24/01/2022': -0.543, '02/02/2022': -0.547, '11/02/2022': -0.523,
    '22/02/2022': -0.528, '03/03/2022': -0.526, '14/03/2022': -0.5, '23/03/2022': -0.493,
    '01/04/2022': -0.461, '12/04/2022': -0.433, '25/04/2022': -0.415, '04/05/2022': -0.427,
    '13/05/2022': -0.403, '24/05/2022': -0.356, '02/06/2022': -0.327, '13/06/2022': -0.281,
    '22/06/2022': -0.172, '01/07/2022': -0.176, '12/07/2022': -0.058, '21/07/2022': 0.145,
    '01/08/2022': 0.246, '10/08/2022': 0.325, '19/08/2022': 0.43, '30/08/2022': 0.62,
    '08/09/2022': 0.836, '19/09/2022': 1.066, '28/09/2022': 1.193, '07/10/2022': 1.288,
    '18/10/2022': 1.456, '27/10/2022': 1.605, '07/11/2022': 1.742, '16/11/2022': 1.803,
    '25/11/2022': 1.922, '06/12/2022': 1.993, '15/12/2022': 2.062, '27/12/2022': 2.128,
    '05/01/2023': 2.178, '16/01/2023': 2.334, '25/01/2023': 2.458, '03/02/2023': 2.545,
    '14/02/2023': 2.66, '23/02/2023': 2.693, '06/03/2023': 2.875, '15/03/2023': 2.815,
    '24/03/2023': 3.025, '04/04/2023': 3.052, '17/04/2023': 3.219, '26/04/2023': 3.242,
    '08/05/2023': 3.312, '17/05/2023': 3.388, '26/05/2023': 3.462, '06/06/2023': 3.476,
    '15/06/2023': 3.547, '26/06/2023': 3.577, '05/07/2023': 3.589, '14/07/2023': 3.66,
    '25/07/2023': 3.705, '03/08/2023': 3.722, '14/08/2023': 3.799, '23/08/2023': 3.826
}

data2 = {
    '04/09/2014': 0.05, '10/03/2016': 0.0, '21/07/2022': 0.5, '08/09/2022': 1.25,
    '27/10/2022': 2.0, '15/12/2022': 2.5, '02/02/2023': 3.0, '16/03/2023': 3.5,
    '04/05/2023': 3.75, '15/06/2023': 4.0, '27/07/2023': 4.25, '24/08/2023': 4.25
}

# Converte le stringhe delle date in oggetti datetime
dates1 = [datetime.strptime(date, '%d/%m/%Y') for date in data1.keys()]
values1 = list(data1.values())

dates2 = [datetime.strptime(date, '%d/%m/%Y') for date in data2.keys()]
values2 = list(data2.values())

# Trova le date di inizio e fine tra dates1 e dates2

start_date = min(min(dates1), min(dates2))
end_date = max(max(dates1), max(dates2))
#print(start_date)
#print(end_date)
# Crea una lista di date tra start_date e end_date
common_dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
print(common_dates)
# Crea una lista di valori scalati per data2
scaled_values2 = []
current_value = None

for date in common_dates:
    if date in dates2:
        current_value = data2[date]
    scaled_values2.append(current_value)

print(scaled_values2)
# Plot dei dati
plt.figure(figsize=(10, 6))

plt.plot(dates1, values1, marker='o', label='Data 1')
plt.step(common_dates, scaled_values2, where='post', color='orange', label='Data 2 Scaled')

plt.xlabel('Date')
plt.ylabel('Values')
plt.title('Graph of Values Over Dates')
plt.legend()
plt.tight_layout()

plt.xticks(rotation=45)
plt.show()

