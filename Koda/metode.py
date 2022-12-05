import itertools
import numpy as np
import cvxpy as cp
from scipy.spatial import distance_matrix
np.random.seed(2022)

def GeneratorProblema(n):
    # Generiramo problem velikosti n
    # z najkljucno izbranim p med 3 in n,
    # saj so primeri, ko izberemo le en 
    # par tock trivialni.
    tocke = np.random.rand(n,2)
    D = distance_matrix(tocke,tocke)
    p = np.random.randint(1,n)
    return (D,p)

def GeneratorMatrike(n):
    # Generirajmo simetricno matriko z
    # niclami na diagonali.
    D = np.random.rand(n,n)
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
    min_razdalja = 1
    for i in P:
        for j in P:
            if i == j:
                continue
            else:
                if D[i, j] < min_razdalja:
                    min_razdalja = D[i, j]
                    par = {i, j}
    return (min_razdalja, par)


def BruteForceMetoda(D, p):
    # Generiramo seznam vsej moznih naborov
    # p tock izmed n in poiscemo optimalnega.
    # Funkcija vrne minimalno razdaljo in
    # nabor tock P, kjer je dosezena.
    n = len(D)
    P = set
    optimalna_razdalja = 0
    tocke = list(range(0, n))
    vsi_izbori_p_tock = itertools.combinations(tocke, p)
    for izbor in vsi_izbori_p_tock:
        min_razdalja = MinRazdalja(D, izbor)[0]
        if min_razdalja > optimalna_razdalja:
            optimalna_razdalja = min_razdalja
            P = set(izbor)
    return (MinRazdalja(D,P), P)


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
    return (MinRazdalja(D,P), P)
 
# Pomozna funckija 
def RSeperationLin(D,r):
    # Ustvarimo matriko enacb E
    n = len(D)
    A = D.copy
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
                    stevilo_enacb +=1
    # Resimo (0-1) linearni program
    x = cp.Variable(n, boole = True)
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
    return (p,P)