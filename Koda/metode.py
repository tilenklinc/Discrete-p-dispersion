import itertools
import numpy as np

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
    return (optimalna_razdalja, P)


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
                for p in P:
                    if D[t, p] > razdalja:
                        razdalja = D[t, p]
                        optimalna_tocka = t
            # Nasli smo optimalno tocko t glede
            # na ze izbrane tocke iz mnozice P.
            # Tocko t dodamo v mnozico P.
            P.add(t)
    return P