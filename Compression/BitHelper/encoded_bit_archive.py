from bitarray import bitarray
import pickle
import sys

from BitHelper import Tree


class EncodedBitArchive:
    endian = 'big'
    info_filename_suffix = '_compressed'
    def __init__(self):
        self.encoding_length = 0
        self.encoded_data_length = 0
        self.encoding_table = dict()
        self.decoding_table = dict()
        self.deciding_tree = Tree.node()
        self.data = bitarray()
        self.entropy = 0.0

    def fromFile(self, filename):
        with open('{}{}'.format(filename, EncodedBitArchive.info_filename_suffix), 'rb') as file:
            encoding_data = pickle.load(file)
        self.encoding_table = encoding_data.encoding_table
        self.decoding_table = encoding_data.decoding_table
        self.encoded_data_length = encoding_data.encoded_data_length
        self.encoding_length = encoding_data.encoding_length
        self.data = encoding_data.data

    def toFile(self, filename):
        info_sum = sys.getsizeof(self.encoding_table) + sys.getsizeof(self.decoding_table)
        print('Zapisywanie zakodowanego tekstu oraz informacji dot kodowania do pliku {}\n\trozmiar zakodowanego tekstu {}b, {}KB\n\trozmiar tablicy kodowania {}B\n\trozmiar tablicy dekodowania {}B\n\tRozmiar danych o kodowaniu {}B'.
              format(filename, len(self.data), int(len(self.data)/1024/8), sys.getsizeof(self.encoding_table) , sys.getsizeof(self.decoding_table) , info_sum))
        print('Informacje o kodowaniu zajmują {} % zakodowanych danych'.format(info_sum/len(self.data)))
        with open('{}{}'.format(filename, EncodedBitArchive.info_filename_suffix), 'wb') as file:
            pickle.dump(self, file)