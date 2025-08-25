import csv
import logging

logger = logging.getLogger("csvc")


class SVFileCompressor:
    def __init__(self, filename, delimiter):
        self.filename = filename
        self.delimiter = delimiter
        self.data = self.read_sv_file()
        
    def read_sv_file(self):
        logger.info(f"Reading file '{self.filename}'")
        with open(self.filename) as fp:
            data_list = list(csv.reader(fp, delimiter=self.delimiter))
        headers = data_list[0]
        
        data = {header: [] for header in headers}
        
        logger.info(f"Creating Dictionary from SV file")
        for line in data_list[1:]:
            for header_index, header in enumerate(headers):
                data[header].append(line[header_index])
                
        return data
    
    def get_column_frequencies(self):
        freq_table = {header: {} for header in self.get_headers()}
        
        for header, column in self.data.items():
            for row in column:
                for char in row:
                    if char in freq_table[header]:
                        freq_table[header][char] += 1
                    else:
                        freq_table[header][char] = 1
        return freq_table       
        
    def get_headers(self):
        return self.data.keys()
        
    def compress(self):
        logger.info(f"Starting compression for '{self.filename}'")

        headers = self.get_headers()
        logger.debug(f"Headers: {headers}")
        
        logger.info(f"Calculating column frequencies")
        freq_table = self.get_column_frequencies()
        
        
        
        
        
        