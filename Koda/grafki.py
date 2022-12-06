import pandas as pd
from matplotlib import pyplot as plt

def time_to_seconds(cas):
    if len(cas) == 7:
        return 0
    else:
        return int(cas[5:7]) + int(cas[-6:])/1000000
    
    

# %%

imena_datotek = ["poskus_n_10_p_3.csv", "poskus_n_10_p_4.csv", "poskus_n_10_p_5.csv", "poskus_n_10_p_6.csv", "poskus_n_10_p_7.csv"]

rezultat_p = []
rezultat_b = []
rezultat_n = []

times_p = []
times_b = []


for ime in imena_datotek:
    csv = pd.read_csv(ime, sep = ';')
    
    cas_p = list(csv["casIzvajanja_P"])
    cas_b = list(csv["casIzvajanja_B"])
    
    T_p = [time_to_seconds(time) for time in cas_p]
    T_b = [time_to_seconds(time) for time in cas_b]
    
    times_p.append(sum(T_p)/100)
    times_b.append(sum(T_b)/100)
    
  
    csv = csv[csv["najmanjsaRazdalja_B"] != "None"]
    n_none = 100 - len(csv)
    csv["najmanjsaRazdalja_B"] = csv["najmanjsaRazdalja_B"].astype(float)
    csv = csv[csv["najmanjsaRazdalja_B"] > csv["najmanjsaRazdalja_P"]]
    n_bisekcija = len(csv)
    n_pozresna = 100 - n_none - n_bisekcija
    rezultat_p.append(n_pozresna)
    rezultat_b.append(n_bisekcija)
    rezultat_n.append(n_none)
    
x = [3, 4, 5, 6, 7]
    
plt.plot(x, rezultat_p, label = "Pozresna metoda")
plt.plot(x, rezultat_b, label = "Bisekcija")
plt.plot(x, rezultat_n, label = "Bisekcija ne vrne rezultata")
plt.legend(loc="upper right")
plt.xticks(x)
plt.xlabel('p')
plt.ylabel('Število bolje rešenih primerov')

plt.clf()

plt.plot(x, times_p, label = 'Požrešna metoda')
plt.plot(x, times_b, label = 'Bisekcija')
plt.xticks(x)
plt.legend(loc="upper right")
plt.xlabel('p')
plt.ylabel('Povprečni čas izvajanja v sekundah')

# %%

imena_datotek = ["poskus_n_20_p_5.csv", "poskus_n_20_p_8.csv","poskus_n_20_p_10.csv","poskus_n_20_p_12.csv", "poskus_n_20_p_15.csv"]

rezultat_p = []
rezultat_b = []
rezultat_n = []

times_p = []
times_b = []


for ime in imena_datotek:
    csv = pd.read_csv(ime, sep = ';')
    
    cas_p = list(csv["casIzvajanja_P"])
    cas_b = list(csv["casIzvajanja_B"])
    
    T_p = [time_to_seconds(time) for time in cas_p]
    T_b = [time_to_seconds(time) for time in cas_b]
    
    times_p.append(sum(T_p)/100)
    times_b.append(sum(T_b)/100)
    
  
    csv = csv[csv["najmanjsaRazdalja_B"] != "None"]
    n_none = 100 - len(csv)
    csv["najmanjsaRazdalja_B"] = csv["najmanjsaRazdalja_B"].astype(float)
    csv = csv[csv["najmanjsaRazdalja_B"] > csv["najmanjsaRazdalja_P"]]
    n_bisekcija = len(csv)
    n_pozresna = 100 - n_none - n_bisekcija
    rezultat_p.append(n_pozresna)
    rezultat_b.append(n_bisekcija)
    rezultat_n.append(n_none)
    
x = [5, 8, 10, 12, 15]
    
plt.plot(x, rezultat_p, label = "Pozresna metoda")
plt.plot(x, rezultat_b, label = "Bisekcija")
plt.plot(x, rezultat_n, label = "Bisekcija ne vrne rezultata")
plt.legend(loc="upper right")
plt.xticks(x)
plt.xlabel('p')
plt.ylabel('Število bolje rešenih primerov')

plt.clf()

plt.plot(x, times_p, label = 'Požrešna metoda')
plt.plot(x, times_b, label = 'Bisekcija')
plt.xticks(x)
plt.legend(loc="upper right")
plt.xlabel('p')
plt.ylabel('Povprečni čas izvajanja v sekundah')

# %%

imena_datotek = ["poskus_n_50_p_10.csv", "poskus_n_50_p_20.csv", "poskus_n_50_p_25.csv","poskus_n_50_p_30.csv", "poskus_n_50_p_40.csv"]

rezultat_p = []
rezultat_b = []
rezultat_n = []

times_p = []
times_b = []


for ime in imena_datotek:
    csv = pd.read_csv(ime, sep = ';')
    
    cas_p = list(csv["casIzvajanja_P"])
    cas_b = list(csv["casIzvajanja_B"])
    
    T_p = [time_to_seconds(time) for time in cas_p]
    T_b = [time_to_seconds(time) for time in cas_b]
    
    times_p.append(sum(T_p)/100)
    times_b.append(sum(T_b)/100)
    
  
    csv = csv[csv["najmanjsaRazdalja_B"] != "None"]
    n_none = 100 - len(csv)
    csv["najmanjsaRazdalja_B"] = csv["najmanjsaRazdalja_B"].astype(float)
    csv = csv[csv["najmanjsaRazdalja_B"] > csv["najmanjsaRazdalja_P"]]
    n_bisekcija = len(csv)
    n_pozresna = 100 - n_none - n_bisekcija
    rezultat_p.append(n_pozresna)
    rezultat_b.append(n_bisekcija)
    rezultat_n.append(n_none)
    
x = [10, 20, 25, 30, 40]
    
plt.plot(x, rezultat_p, label = "Pozresna metoda")
plt.plot(x, rezultat_b, label = "Bisekcija")
plt.plot(x, rezultat_n, label = "Bisekcija ne vrne rezultata")
plt.legend(loc="upper right")
plt.xticks(x)
plt.xlabel('p')
plt.ylabel('Število bolje rešenih primerov')

plt.clf()

plt.plot(x, times_p, label = 'Požrešna metoda')
plt.plot(x, times_b, label = 'Bisekcija')
plt.xticks(x)
plt.legend(loc="upper right")
plt.xlabel('p')
plt.ylabel('Povprečni čas izvajanja v sekundah')
