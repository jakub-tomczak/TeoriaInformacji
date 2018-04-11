import operator
from random import random

alfabet = 'abcdefghijklmnopqrstuvwxyz '


# alfabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '

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
    return [{'{znak}{sufiks}'.format(znak=klucz, sufiks=val): slownik[val] / suma * 100} for val in slownik]


def dopasuj_regex(wyrazenie, text):
    import re
    return len(re.findall(wyrazenie, text))


def generuj_regex(znak, sufiks):
    return r'[{lower}{upper}]{suffix}'.format(lower=znak.lower(), upper=znak.upper(), suffix=sufiks)


def generuj_rownomiernie():
    return alfabet[(int)(random() * len(alfabet))]


def sortuj_slownik(slownik):
    return sorted(slownik.items(), key=operator.itemgetter(1))


def generuj_z_prawd_lista(lista_rozklad):
    liczba = random() * lista_rozklad[-1][1]
    dolna_granica = 0
    for znak, granica in lista_rozklad:
        if liczba > dolna_granica and liczba < granica:
            return znak
        dolna_granica = granica


def generuj_z_prawdopodobienstwem(rozklad):
    liczba = random()
    dolna_granica = 0
    for znak in rozklad.keys():
        granica = rozklad[znak] / 100.0
        if liczba > dolna_granica and liczba < granica:
            return znak
        dolna_granica = granica


def zad1():
    print("Zadanie 1")
    # zadanie 1
    generated = ''
    for i in range(1000000):
        generated += alfabet[(int)(random() * len(alfabet))]

    print("śr. {sr}".format(sr=srednia_liczba_liter(generated)))


def zad2():
    print("\nZadanie 2")
    # zadanie 2
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
    liczba_znakow_w_tekscie = sum

    sorted_x = sorted(count.items(), key=operator.itemgetter(1))
    print("Dwa najczęstsze znaki {last2}".format(last2=sorted_x[-3:-1]))
    return (sorted_x, liczba_znakow_w_tekscie)  # zwroc korpus


def zad3(korpus):
    print("\nZadanie 3")
    # przygotowanie struktury dla generatora z prawdopodobienstwem
    # sumuj kolejne
    values = []
    sum = 0
    for (x, y) in korpus:
        values.append((x, y + sum))
        sum += y

    # generator z prawdopodobienstwem
    generated = ''
    for i in range(1000000):
        generated += (generuj_z_prawd_lista(values))
    sr = srednia_liczba_liter(generated)
    print("Srednia liczba liter {sr}".format(sr=sr))
    return sr


def zad4(znak, liczba_znakow, text):
    liczba_znakow = (int)(liczba_znakow/2)
    return [ ("{a}{b}".format(a = znak, b = i),dopasuj_regex(generuj_regex(znak, i),text) /liczba_znakow) for i in alfabet]

def znajdz_pozycje(wyrazenie, text):
    return text.find(wyrazenie)

if __name__ == '__main__':
    text = ''
    with open('norm_wiki_sample.txt') as f:
        for line in f:
            text += line

    #zad1()
    korpus, liczba_znakow = zad2()
    #zad3(korpus)
    znaki = korpus[-3:-1]
    prawdopodobienstwa = [zad4(znak, liczba_znakow, text) for znak,y in znaki]  # korpus[-3:-1] -> dwa najczesciej wystepujace (pomijamy spacje)

    #text = "asldasldasilityjasdhjas"

    print("\nZadanie 5")
    wygenerowany = 'probability'
    rzad = 3
    dlugosc = len(text) -1
    ostatnie = wygenerowany[-rzad:]
    for i in range(5000):

        for j in range(10):
            poz = (int)(random() * dlugosc)
            znaleziono = znajdz_pozycje(ostatnie, text[poz:])
            if(znaleziono > -1):
                if(poz + znaleziono + rzad >= len(text)):
                    break;
                wygenerowany = wygenerowany + text[poz + znaleziono+rzad]
                break;

        ostatnie = wygenerowany[-rzad:]
        if len(wygenerowany) > 700:
            break;
    sr_dl = srednia_liczba_liter(wygenerowany)
    print("wygenerowany tekst dla rzedu ({rz}):\n{tekst}\nSrednia dl:{sr}".format(rz =  rzad, tekst = wygenerowany, sr = sr_dl))



    exit()
