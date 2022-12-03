import numpy as np

def PozresnaMetoda(M,p):
    # Zacnemo z parom tock, ki sta med 
    # seboj najbolj oddaljena. Nato na 
    # vsakem koraku dodamo optimalno tocko
    # glede na prejsni nabor tock. Ponavljamo
    # dokler ne izberemo p tock.

    # Z n oznacimo dimenzijo kvadratne matrike.
    # S P oznacimo mnozico izbranih tock.

    n = len(M)
    P = set() 

    # V prvem koraku poiscemo najbolj oddaljen par
    # in ga dodamo v mnozico P.
    # Ker je matrika po predpostavki simetricna
    # pogledamo le zgorjno diagonalo.

    max_razdalja = 0
    max_par = ()
    for i in range(0, n):
        for j in range(i+1, n):
            if M[i,j] > max_razdalja:
                max_razdalja = M[i,j]
                max_par = (i,j)
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
                    if M[t,p] > razdalja:
                        razdalja = M[t,p]
                        optimalna_tocka = t
            # Nasli smo optimalno tocko t glede
            # na ze izbrane tocke iz mnozice P.
            # Tocko t dodamo v mnozico P.
            P.add(t)
