import itertools
import numpy as np
import cvxpy as cp
from scipy.spatial import distance_matrix
from math import floor
import datetime
np.random.seed(2022)


def GeneratorProblema(n, p):
    # Generiramo problem velikosti n
    # z najkljucno izbranim p med 3 in n,
    # saj so primeri, ko izberemo le en
    # par tock trivialni.
    if p < 2 or p > n:
        print('Neveljaven p')
    tocke = np.random.rand(n, 2)
    D = distance_matrix(tocke, tocke)
    return (D, p)


def GeneratorMatrike(n):
    # Generirajmo simetricno matriko z
    # niclami na diagonali.
    D = np.random.rand(n, n)
    D = (D + D.T) / 2
    np.fill_diagonal(D, 0)
    return D


def MinRazdalja(D, P):
    # Elemetnt matrike D[i,j] je razdalja
    # od i-te do j-te tocke. Predpostavljamo,
    # da je matrika D simetricna. P je mnozica
    # izbranih tock.
    # Funkcija vrne minimalno razdlajo
    # med izbranimi tockami in tocki,
    # kjer je dosezena.
    par = set
    min_razdalja = np.max(D)
    for i in P:
        for j in P:
            if i == j:
                continue
            else:
                if D[i, j] <= min_razdalja:
                    min_razdalja = D[i, j]
                    par = {i, j}
    return (min_razdalja, par)


def BruteForceMetoda(D, p):
    # Generiramo seznam vsej moznih naborov
    # p tock izmed n in poiscemo optimalnega.
    # Funkcija vrne minimalno razdaljo in
    # nabor tock P, kjer je dosezena.
    n = len(D)
    P = set()
    optimalna_razdalja = 0
    tocke = list(range(0, n))
    vsi_izbori_p_tock = itertools.combinations(tocke, p)
    for izbor in vsi_izbori_p_tock:
        min_razdalja = MinRazdalja(D, izbor)[0]
        if min_razdalja > optimalna_razdalja:
            optimalna_razdalja = min_razdalja
            P = set(izbor)
    return (MinRazdalja(D, P), P)


def PozresnaMetoda(D, p):
    # Zacnemo z parom tock, ki sta med
    # seboj najbolj oddaljena. Nato na
    # vsakem koraku dodamo optimalno tocko
    # glede na prejsni nabor tock. Ponavljamo
    # dokler ne izberemo p tock.
    # Z n oznacimo dimenzijo kvadratne matrike.
    # S P oznacimo mnozico izbranih tock.
    n = len(D)
    P = set()
    # V prvem koraku poiscemo najbolj oddaljen par
    # in ga dodamo v mnozico P.
    # Ker je matrika po predpostavki simetricna
    # pogledamo le zgorjno diagonalo.
    max_razdalja = 0
    max_par = ()
    for i in range(0, n):
        for j in range(i+1, n):
            if D[i, j] > max_razdalja:
                max_razdalja = D[i, j]
                max_par = (i, j)
    P.update([max_par[0], max_par[1]])
    # Na vsakem koraku glede na prejsni nabor tock
    # izberemo optimalno tocko. Ponavljamo dokler
    # ne izberemo p tock.
    while len(P) < p:
        razdalja = 0
        optimalna_tocka = None
        for t in range(0, n):
            # Ce je tocka t ze vsebovana v p, jo
            # preskocimo.
            if t in P:
                continue
            # Ce ne pogledamo razdalje do ze
            # izbranih tock. Razdaljo posodobimo
            # ce najdemo daljso, posodobimo
            # razdaljo in optimalno tocko.
            else:
                for q in P:
                    if D[t, q] > razdalja:
                        razdalja = D[t, q]
                        optimalna_tocka = t
            # Nasli smo optimalno tocko t glede
            # na ze izbrane tocke iz mnozice P.
            # Tocko t dodamo v mnozico P.
        P.add(optimalna_tocka)
    return (MinRazdalja(D, P), P)


# Pomozna funckija za BisekcijskaMetoda
def RSeperationLin(D, r):
    # Ustvarimo matriko enacb E
    n = len(D)
    A = D.copy()
    A[A < r] = 1
    np.fill_diagonal(A, 0)
    stevilo_enic = np.count_nonzero(A == 1)
    E = [[0 for x in range(n)] for y in range(stevilo_enic)]
    stevilo_enacb = 0
    while stevilo_enacb < stevilo_enic:
        for i in range(0, n):
            for j in range(i+1, n):
                if A[i][j] == 1:
                    E[stevilo_enacb][i] = 1
                    E[stevilo_enacb][j] = 1
                    stevilo_enacb += 1
    # Resimo (0-1) linearni program
    E = np.array(E)
    x = cp.Variable(n, boolean=True)
    c = [1] * n
    b = [1] * stevilo_enacb
    program = cp.Problem(cp.Minimize(c @ x), [E @ x >= b])
    # Preberemo koliko tock izmed n smo izbrali
    p = program.solve(solver=cp.GLPK_MI)
    # Preberemo katere tocke smo vzeli
    P = set()
    for i in range(0, n):
        if x.value[i] == 1:
            P.add(i)
    return (p, P)


def BisekcijskaMetoda(D, p):
    n = len(D)
    # Uredimo razdalje iz matrike D po velikosti
    # z upostevanjem veckratnosti
    R = list()
    for i in range(0, n):
        for j in range(i+1, n):
            R.append(D[i][j])
    R.sort()
    # Upostevamo hevristiko
    # Zgornja meja u
    u = int(n * (n - 1) / 2 - p * (p - 1) / 2 - 1)
    # Spodna meja
    l = n - p - 1
    # Funckija RSeperationLin je narascajoca funkcija
    # v argumentu r.
    # Zacnimo z bisekcijo, najprej pogledamo spodnjo
    # mejo. Nato se premikamo s polovicnimi koraki.
    # Ko naletimi resitev, ki izvere p tock se ustavimo.
    # To ni optimalna resitev, le dopustna.
    RestiveLin = RSeperationLin(D, R[l])
    stevec = 0
    while RestiveLin[0] != p:
        stevec += 1
        c = floor((l + u) / 2)
        RestiveLin = RSeperationLin(D, R[c])
        if RestiveLin[0] < p:
            l = c
        elif RestiveLin[0] > p:
            u = c
        if stevec == 200:
            return((None, None), None)
    return (MinRazdalja(D, RestiveLin[1]), RestiveLin[1])

        
def izvedi_funkcijo(N, P, stevilo_ponovitev):
    # Poskusi je kolikokrat ponovimo funkcijo
    for n in N:
        for p in P:
            print(n, p)
            ime_datoteke = "poskus_n_" + str(n) + "_p_" + str(p) + ".csv"
            f = open(ime_datoteke, "w") # w --> Za na novo write, "a" --> za append
            f.write('ponovitev;najmanjsaRazdalja_B;najblizjiPar_B;tocke_B;casIzvajanja_B;najmanjsaRazdalja_P;najblizjiPar_P;tocke_;casIzvajanja_P\n')
            for i in range(stevilo_ponovitev):
                D, p = GeneratorProblema(n, p)
                   
                zacetek1 = datetime.datetime.now()
                r1, tocke1 = BisekcijskaMetoda(D, p)
                rez1, mini1 = r1
                konec1 = datetime.datetime.now()-zacetek1
                    
                zacetek2 = datetime.datetime.now()
                r2, tocke2 = PozresnaMetoda(D, p)
                rez2, mini2 = r2
                konec2 = datetime.datetime.now()-zacetek2
                
                f.write(str(i+1) + ';' + str(rez1) + ';' + str(mini1) + ';' + str(tocke1) + ';' + str(konec1) + ';' + str(rez2) + ';' + str(mini2) + ';' + str(tocke2) + ';' + str(konec2) + '\n')
            f.close()
    
izvedi_funkcijo([10], [3, 4, 5, 6, 7], 100)
izvedi_funkcijo([20], [5, 8, 10, 12, 15], 100)
izvedi_funkcijo([50], [10, 20, 25, 30, 40], 100)