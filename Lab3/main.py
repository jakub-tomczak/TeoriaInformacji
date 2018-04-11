from collections import Counter

import numpy as np
def load_text(file):
    data = ''
    with open(file, 'r') as f:
        data = f.read()
    return data

def generate_n_grams(data, n_gram_len):
    return [[data[j+i] for j in range(n_gram_len)] for i in range(len(data)-(n_gram_len-1))]

def generate_ngram_dictionary(data, ngram_len, characters_mode = False):
    markov_dict = dict()
    ngrams = generate_n_grams(data, ngram_len)
    for ngram in ngrams:
        #przerzuca elementy tablicy do stringa rozdzielajac je spacja
        context = "".join(ngram[:-1]) if characters_mode else " ".join(ngram[:-1])

        last_word = ngram[-1]
        if context not in markov_dict:
            markov_dict[context] = []
        markov_dict[context].append(last_word)
    #oblicz licznosci elementow
    markov_dict = {k: Counter(v) for k,v in markov_dict.items()}
    return markov_dict

#https://en.wikipedia.org/wiki/Entropy_(information_theory)#Definition
def entropy(p_value, divider):
    return -p_value*np.log2(p_value/divider)

def calculate_sum_entropy(ngrams, words_in_text):
    entropy_sum = 0
    for ngram, values in ngrams.items():
        count_values = sum(values.values())
        entropy_sum += sum([entropy(v/words_in_text, count_values/words_in_text) for k,v in values.items()])

    return entropy_sum

#for 0-ngrams
def count_data_probabilities(splitted_data = None, splited_data_counter = None):
    if splitted_data is not None:
        words_dict = Counter(splitted_data)
    else:
        words_dict = splited_data_counter
    xsum = sum(words_dict.values())
    words_dict = {k: v/xsum for k,v in words_dict.items()}
    return words_dict

def calculate_entropy(data_dict):
    return -np.sum([v*np.log2(v) for v in data_dict.values()])



def calculate_entropy(text):
    # short_text = 'ala ma kota ala nie umie jesc ala ma balon'
    # a = generate_ngram_dictionary(short_text, 1, characters_mode=True)
    # splitted_short_text = short_text.split()
    # a = generate_ngram_dictionary(splitted_short_text, 3)
    # c = calculate_sum_entropy(a, len(splitted_short_text))
    w_results = []
    ch_results = []
    splitted_text = text.split()
    splitted_characters = list(text)
    #characters_in_text = count_data_probabilities(splitted_characters)
    #characters_entropy = calculate_entropy(characters_in_text)
    #ch_results.append([0, characters_entropy])

    #words_in_text = count_data_probabilities(splitted_text)
    #words_entropy = calculate_entropy(words_in_text)
    #w_results.append([0, words_entropy])

    #print("word {} and characters {} entropies.".format(words_entropy, characters_entropy))
    for level in range(1, 5):
        print("level is {}".format(level))
        words_ngrams = generate_ngram_dictionary(splitted_text, level + 1)
        words_entropy = calculate_sum_entropy(words_ngrams, len(splitted_text))
        w_results.append([level, words_entropy])
        character_ngrams = generate_ngram_dictionary(text, level + 1)
        characters_entropy = calculate_sum_entropy(character_ngrams, len(text))
        ch_results.append([level, characters_entropy])
    return (ch_results, w_results)
import os
if __name__=='__main__':
    data_directory = "{}{}".format(os.getcwd(), "/data/")
    files = os.listdir(data_directory)
    results_file = open('results.txt', 'w')

    for file in files:
        print("Parsing file: {}\n" .format(file))
        results_file.write("{}\n".format(file))
        text = load_text("{}{}".format(data_directory, file))
        result = calculate_entropy(text)
        #write words
        results_file.write("\n".join(["wyraz, rząd: {}, entropia {}".format(val[0], val[1]) for val in result[0]]))
        results_file.write("\n")
        #write characters
        results_file.write("\n".join(["znaki, rząd: {}, entropia {}".format(val[0], val[1]) for val in result[1]]))
        results_file.write("\n")
    results_file.close()
