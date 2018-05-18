from bitarray import bitarray
import pickle

class Encoding:
    endian = 'big'
    info_filename_suffix = '_info.data'
    def __init__(self):
        self.encoding_length = 0
        self.encoded_data_length = 0
        self.encoding_table = dict()
        self.decoding_table = dict()
        self.data = bitarray()

    def fromFile(self, filename):
        temp_array = bitarray(endian=Encoding.endian)
        with open(filename, 'rb') as file:
            temp_array.fromfile(file)
            self.data = temp_array
        with open('{}{}'.format(filename, Encoding.info_filename_suffix), 'rb') as file:
            encoding_data = pickle.load(file)
        self.encoding_table = encoding_data.encoding_table
        self.decoding_table = encoding_data.decoding_table
        self.encoded_data_length = encoding_data.encoded_data_length
        self.encoding_length = encoding_data.encoding_length

    def toFile(self, filename):
        info_sum = len(self.encoding_table) + len(self.decoding_table) + 4 + 4
        print('Saving data and info to a file {}\n\tdata size {}\n\tencoding table size {}\n\tdecoding table size {}\n\tencoded data length {}\n\tencoding length {}\n\tsize of info file {}'.
              format(filename, len(self.data), len(self.encoding_table), len(self.decoding_table), 4, 4, info_sum))
        with open('{}{}'.format(filename, Encoding.info_filename_suffix), 'wb') as file:
            pickle.dump(self, file)