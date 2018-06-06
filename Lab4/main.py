import pickle
from collections import Counter
import numpy as np
from bitarray import bitarray
import sys
sys.path.append('../BitHelper')
from encodedbitarchive import EncodedBitArchive #imported from BitHelper dir
from encoding_handler import * #imported from BitHelper dir

text = "ala ma kota a jan "

def load_text(filename):
    text = ''
    with open(filename, 'r') as file:
        text = text + file.readline()
    return text

def create_encoding(text, encoding_object):
    splitted = list(text)
    iter = 0
    characters = Counter(splitted)
    bin_length = int(np.ceil(np.log2(len(characters))))
    encoding_object.encoding_length = bin_length
    for k,i in characters.items():
        encoding_object.encoding_table[k] = bin(iter)[2:]
        #uzupelnienie 0 do poprawnej liczby znakow
        encoding_object.encoding_table[k] = '{}{}'.format('0'*(bin_length-len(encoding_object.encoding_table[k])) ,encoding_object.encoding_table[k])
        encoding_object.decoding_table[str(bitarray(encoding_object.encoding_table[k]))] = k

        iter += 1

def main():
    encoded_obj = EncodedBitArchive()
    decoded_obj = EncodedBitArchive()
    #text = load_text('../Data/short.txt')

    print('input len {}'.format(len(text)))

    create_encoding(text, encoded_obj)
    print('encoding', encoded_obj.encoding_table, 'unique characters', len(encoded_obj.encoding_table))
    output = encode(text, encoded_obj)
    print('encoding length {}'.format(encoded_obj.encoding_length))
    save('ala_ma_kota', encoded_obj)

    load('ala_ma_kota', decoded_obj)
    print('compressed len {}'.format(len(encoded_obj.data)))
    decoded_data = decode(decoded_obj)

    check_random_letters(text, decoded_data)

    if len(text) == len(decoded_data):
        print('OK')
    else:
        print(len(text), '<>', len(decoded_data))


if __name__=='__main__':
    main()
    #saving_tester()
