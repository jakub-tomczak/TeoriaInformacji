import operator
import re
from collections import Counter
import random
import itertools

def load_text():
    text = ''
    with open('norm_wiki_sample.txt') as f:
        for line in f:
            text += line
    return text

def sortuj_slownik(slownik):
    return sorted(slownik.items(), key=operator.itemgetter(1), reverse=True)

def dopasuj_regex(wyrazenie, text):
    return len(re.findall(wyrazenie, text))

def wez_n_gramy(data, n_gram_len):
    return [[data[j+i] for j in range(n_gram_len)] for i in range(len(data)-(n_gram_len-1))]

def generate_ngram_markov(splitted_data,n_gram_len):
    markov_dict = dict()
    n_grams = wez_n_gramy(splitted_data, n_gram_len)
    for n_gram in n_grams:
        context = " ".join(n_gram[:-1])
        last_word = str(n_gram[-1])

        if context not in markov_dict.keys():
            markov_dict[context] = list()
        markov_dict[context].append(last_word)

    for context in markov_dict.keys():
        markov_dict[context] = Counter(markov_dict[context])  # stwórz histogram słów

    return markov_dict

def zad1(text):
    splitted = text.split(' ')
    words_dict = Counter(splitted)

    words_dict_sorted = sortuj_slownik(words_dict)
    all_words_sum = sum([x[1] for x in words_dict_sorted])
    first30_sum = sum([x[1] for x in words_dict_sorted[:30000]])
    first6_sum = sum([x[1] for x in words_dict_sorted[:6000]])
    #ok20,8% slow posiada 92% udzialu
    print("Pierwsze 30tys. wyrazów stanowi {f}%, pierwsze 6tys. stanowi {s}%.".
          format(f = round(first30_sum/all_words_sum * 100, 2), s = round(first6_sum/all_words_sum * 100, 2)))
    return splitted, words_dict, words_dict_sorted

def get_random_word_from_text(words_dict):
    probability_list = [[words_dict[0][1], words_dict[0][0]]]
    for i in range(1, len(words_dict)):
        probability_list.append([words_dict[i][1] + probability_list[i-1][0], words_dict[i][0]])
    num = random.randrange(probability_list[-1][0])
    for i in range(len(probability_list)):
        if probability_list[i][0] > num:
            if i-1 >= 0:
                return probability_list[i-1][1]
    return ''
def first_rank(splitted_text, words_dict, length, words_dict_sorted, start = ''):
    leng = len(splitted_text)
    border = leng if leng % 2 == 0 else leng-1
    rank = dict()
    for word in words_dict:
        rank[word] = []
    for index in range(0, border, 2):
        rank[splitted_text[index]].append(splitted_text[index + 1])

    if start == '':
        sentence = get_random_word_from_text(words_dict_sorted)
    else:
        sentence = start

    last_word = sentence.split(' ')[-1]
    limit = 0
    for i in range(length):
        if len(rank[last_word]) == 0:
            limit += 1
            #remove last element to try again
            curr_sentence = sentence.split(' ')
            sentence = ' '.join(curr_sentence[:-1])
            last_word = curr_sentence[-1]
            continue
        else:
            limit = 0
        if limit > 19:
            break
        num = random.randrange(len(rank[last_word]))
        last_word = rank[last_word][num]
        sentence += ' {}'.format(last_word)
    return len(sentence.split(' ')), sentence

def markov_generator(splitted_text, n_gram_len, sentence_length, words_dict, words_dict_sorted, markov_dict, start=''):
    arr = start.split(' ')
    if start == 0:
        length, sentence = first_rank(splitted_text, words_dict, 2, words_dict_sorted)
    else:
        length, sentence = first_rank(splitted_text, words_dict, 1, words_dict_sorted, arr[-1])
    if length < 2:
        return 0,''

    for i in range(sentence_length-n_gram_len):
        text_spl = sentence.split(" ")
        context = " ".join(text_spl[-n_gram_len + 1:])  # pobieramy ostatnie ostatnie n_gram_len - 1 słów
        idx = random.randrange(sum(markov_dict[context].values()))
        new_word = next(itertools.islice(markov_dict[context].elements(), idx, None))
        sentence = "{} {}".format(sentence, new_word)
    return len(sentence.split(' ')),sentence


if __name__ == '__main__':
    text = load_text()
    splitted, words_dict, words_dict_sorted = zad1(text)

    n_gram_len = 2
    markov_dict = generate_ngram_markov(splitted, n_gram_len)
    length, sentence = markov_generator(splitted, n_gram_len, 200, words_dict,words_dict_sorted, markov_dict)
    print("1.{}gram. Generated sentence is {} words long.\n{}".format(n_gram_len, length, sentence))

    n_gram_len = 3
    markov_dict = generate_ngram_markov(splitted, n_gram_len)
    length, sentence = markov_generator(splitted, n_gram_len, 200, words_dict,words_dict_sorted, markov_dict)
    print("2.{}gram. Generated sentence is {} words long.\n{}".format(n_gram_len, length, sentence))

    start = 'probability'
    length, sentence = markov_generator(splitted, n_gram_len, 200, words_dict, words_dict_sorted, markov_dict, start)
    print("3.{}gram. Generated sentence is {} words long.\n{}".format(n_gram_len, length, sentence))
