import operator
from collections import Counter
from random import random


import sys
sys.path.append('../BitHelper')

from encodedbitarchive import EncodedBitArchive #imported from BitHelper dir
from encoding_handler import * #imported from BitHelper dir
from PriorityQueue import PriorityQueue

test_file = 'short.txt' #norm_wiki_sample

#sorts a dict from the lowest probabilities to the highest
def sort_dict(dictionary):
    return sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)

def calculate_data_probabilities(splitted_data):
    if splitted_data is None:
        raise Exception('splitted data is None')
    words_dict = Counter(splitted_data)
    xsum = sum( words_dict.values())
    words_dict_q = {k : v/xsum  for k,v in words_dict.items()} # char : float
    return words_dict_q

def create_encoding_table(root, code, mapping):
    if type(root[1]) is float and type(root[0]) is tuple:
        create_encoding_table(root[0], code, mapping)
    elif type(root[0]) is tuple and type(root[1]) is tuple:
        create_encoding_table(root[0], '{}0'.format(code), mapping) #dodaj '0' na końcu
        create_encoding_table(root[1], '{}1'.format(code), mapping) #dodaj '1' na końcu
    else:
        mapping[root[0]] = code

def generate_encoding(sorted_probabilities):
    compare_index = 1
    queue = PriorityQueue(compare_index)
    #sorted_probabilities = test_data()

    for i in sorted_probabilities:
        queue.put(i)

    while queue.size() > 1:
        newElement = (queue.get(), queue.get())
        e = (newElement, newElement[0][compare_index] + newElement[1][compare_index])
        queue.put(e)
    element = queue.get()   #get root
    mapping = dict()
    create_encoding_table(element, '', mapping)
    decoding_mapping = {str(bitarray(mapping)) : letter for letter, mapping in mapping.items()}
    return mapping, decoding_mapping

def test_data():
    sorted_probabilities = []
    sorted_probabilities.append((.5, 'a'))
    sorted_probabilities.append((.4, 'b'))
    sorted_probabilities.append((.3, 'c'))
    sorted_probabilities.append((.2, 'd'))
    sorted_probabilities.append((.099, 'e')) #.1
    return sorted_probabilities

def main():
    text = load_text(test_file)
    #text = 'asdsad dkjas naskjd qlwke asdlkma  fnkjsdnf askdn awkjdnaks'
    probabilities_dict = sort_dict(calculate_data_probabilities(text))
    encoding_map,decoding_map = generate_encoding(probabilities_dict)

    huffman = EncodedBitArchive()
    huffman.decoding_table = decoding_map
    huffman.encoding_table = encoding_map
    encode(text, huffman)
    huffman.toFile("data")

    huffman_read = EncodedBitArchive()
    huffman_read.fromFile("data")
    decoded_text = decode_non_fixed_length_code(huffman_read)

    len_oryginal = len(text)*8
    len_encoded = len(huffman.data)
    len_decoded = len(decoded_text)*8

    check_random_letters(text, decoded_text)


    compression_summary(len_oryginal, len_encoded, len_decoded)


if __name__ == '__main__':
    main()
