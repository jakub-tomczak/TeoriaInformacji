from collections import Counter
import numpy as np
from bitarray import bitarray
from encodedbitarchive import EncodedBitArchive
from random import randint
text = "ala ma kota a jan "

def load_text(filename):
    text = ''
    with open(filename, 'r') as file:
        text = text + file.readline()
    return text

def load(filename, encoding_object):
    encoding_object.fromFile(filename)

def save(filename, encoding_object):
    encoding_object.toFile(filename)

def encode(text, encoding_object):
    characters = list(text)
    encoded = [encoding_object.encoding_table[i] for i in characters]
    encoded = ''.join(encoded)
    encoding_object.data = bitarray(encoded, endian=EncodedBitArchive.endian)
    encoding_object.encoded_data_length = len(encoding_object.data)

def decode(encoding_object):
    return ''.join(encoding_object.decoding_table[str(encoding_object.data[i:i+encoding_object.encoding_length])] for i in range(0, encoding_object.encoded_data_length, encoding_object.encoding_length))
def decode_non_fixed_length_code(encoding_object):
    decoded = []
    i = 0
    offset = 1
    while i + offset <= encoding_object.encoded_data_length : #iterate over data
        code = str(bitarray( encoding_object.data[i : i + offset] ))
        if code in encoding_object.decoding_table:
            decoded.append(encoding_object.decoding_table[code]) #append next char to decoded array
            i += offset
            offset = 1
        else :
            offset += 1

    return ''.join(decoded)

def decode(encoding_object):
    return ''.join(encoding_object.decoding_table[str(encoding_object.data[i:i+encoding_object.encoding_length])] for i in range(0, encoding_object.encoded_data_length, encoding_object.encoding_length))

def check_random_letters(oryginal_text, decoded_text):
	result = []
	if len(oryginal_text) != len(decoded_text):
		print('Plik oryginalny ma inną długość niż zdekodowany! {}B <> {}B'.format(len(oryginal_text), len(decoded_text)))
		return False
	num = min(100, len(oryginal_text) // 4)
	print('comparing {} random characters'.format(num))
	for i in range(num):
		rand = randint(0, len(oryginal_text))
		print('`{}` ?==? `{}`'.format(oryginal_text[rand], decoded_text[rand]))
		result.append(oryginal_text[rand] == decoded_text[rand])
	return all(result)
	
def compression_summary(len_oryginal, len_encoded, len_decoded):
    print('Długość tekstu dekodowanego odpowiada długości zakodowanego ? {}\nrozmiar zakodowanego pliku ({}b) względem pierwotnego ({}b) {}%'.
          format( 'tak' if len_oryginal==len_decoded else 'nie ({}b <> {}b)'.format(len_oryginal, len_decoded), len_encoded, len_oryginal , len_encoded/len_oryginal ))
def decode_using_tree(encoding_object):
    pass