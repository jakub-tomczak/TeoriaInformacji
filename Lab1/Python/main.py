import operator
from random import random
alfabet = 'abcdefghijklmnopqrstuvwxyz '
#alfabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '

def srednia_liczba_liter(text):
    splitted = text.split(' ')
    import re
    REGEX = r'\w+'
    sum = 0
    words = 0
    for i in splitted:
        if re.search(REGEX, i):
                sum += len(i)
                words += 1
    return sum / words

def oblicz_prawdopodobienstwa(klucz, slownik):
    suma = sum(slownik.values())
    return [{'{znak}{sufiks}'.format(znak = klucz, sufiks = val) : slownik[val]/ suma * 100} for val in slownik]

def dopasuj_regex(wyrazenie, text):
    import re
    return len(re.findall(wyrazenie, text))

def generuj_regex(znak, sufiks):
    return r'[{lower}{upper}]{suffix}'.format(lower = znak.lower(), upper = znak.upper(), suffix = sufiks)

def generuj_rownomiernie():
    return alfabet[(int)(random() * len(alfabet))]

def sortuj_slownik(slownik):
    return sorted(slownik.items(), key=operator.itemgetter(1))

def generuj_z_prawdopodobienstwem(rozklad):
    liczba = random()
    dolna_granica = 0
    for znak in rozklad.keys():
        granica = rozklad[znak] / 100.0
        if liczba > dolna_granica and liczba < granica:
            return znak
        dolna_granica = granica

def zad1():
    # zadanie 1
    generated = ''
    for i in range(1000000):
        generated += alfabet[(int)(random() * len(alfabet))]
    # print(generated)

    print("śr. {sr}".format(sr=srednia_liczba_liter(generated)))

def zad2():
    #zadanie 2
    import operator
    word = ""
    sum = 0
    words = 0
    count = {}

    with open('norm_romeo_and_juliet.txt') as f:
        for line in f:
            sum += len(line)
            words += 1
            for s in line:
              if s in count:
                count[s] += 1
              else:
                count[s] = 1


    sorted_x = sorted(count.items(), key=operator.itemgetter(1))

    #przygotowanie struktury dla generatora z prawdopodobienstwem
    values = [(sorted_x[i][0], sorted_x[i][1] + (sorted_x[i-1][1] if i > 0 else 0) ) for i in range(0, len(sorted_x))]
    print(values)
    values_max = 0
    for i in values:
        if i[1] > values_max:
            values_max = i[1]

    # generator z prawdopodobienstwem
    generated = ''
    for i in range(1000000):
        generated += (pobierz_losowa_litere_prawdo())
    #print(generated)
    print(srednia_liczba_liter(generated))

def zad3():
    wystapienia = dict()
    for znak in alfabet:
        if znak not in wystapienia:
            wystapienia[znak] = dict()
        for p in alfabet:
            if p not in wystapienia[znak]:
                wystapienia[znak][p] = dict()
            wystapienia[znak][p] = dopasuj_regex(generuj_regex(znak, p), text)
        wystapienia[znak] = oblicz_prawdopodobienstwa(znak, wystapienia[znak])
    posortowany = sortuj_slownik(wystapienia['a'])
    print('a')
'''
rozklad = dict()
rozklad['a'] = 10
rozklad['b'] = 23
rozklad['c'] = 100
sorted(rozklad.items(), key=lambda x: x[1])  # sortuj po wartościach
'''
def hashed(text):
    import hashlib
    return hashlib.sha256(znak.encode('UTF-8')).hexdigest()

if __name__=='__main__':
    text = ''
    with open('norm_romeo_and_juliet.txt') as f:
        for line in f:
            text += line



    '''
    text = "Alexander Fleming discovered panicillin in 1928. " \
           "He had no sonner noticed an interesting mould growth " \
           "in one of his glass dishes than he knew that it was " \
           "something important. He only later realised what a " \
           "diffrence it would make to our lives. There had never " \
           "been a drug like this before. Patients with infections " \
           "could only be successfully cured by taking penicillin. " \
           "Penicillin not only advanced medical technology, " \
           "but also saved thousands of lives. " \
           "People rarely die from infections these days."
    '''
    newText = "probalbility"

    for i in range(1, 1000):
       newText +=
