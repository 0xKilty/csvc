import csv
import logging
import os

from huffman import build_huffman_tree, generate_huffman_codes
from header import create_header

logger = logging.getLogger("csvc")


class SVFileCompressor:
    def __init__(self, filename, delimiter, output_file):
        self.filename = filename
        self.delimiter = delimiter
        self.output_file = output_file
        self.file_size = os.path.getsize(self.filename)
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
        freq_table = {header: {} for header in self.get_sv_headers()}
        
        for header, column in self.data.items():
            for row in column:
                for char in row:
                    if char in freq_table[header]:
                        freq_table[header][char] += 1
                    else:
                        freq_table[header][char] = 1
        return freq_table       
        
    def get_sv_headers(self):
        return list(self.data.keys())
        
    def compress(self):
        logger.info(f"Starting compression for '{self.filename}'")
        
        logger.info(f"Getting SV file headers")
        headers = self.get_sv_headers()
        
        logger.info(f"Calculating column frequencies")
        freq_table = self.get_column_frequencies()
        
        logger.info(f"Creating Huffman Trees and Codes")
        huffman_trees = {header: {} for header in headers}
        code_tables = {header: {} for header in headers}
        
        for header in freq_table.keys():
            huffman_trees[header] = build_huffman_tree(freq_table[header])
            code_tables[header] = generate_huffman_codes(huffman_trees[header])
                
        logger.info("Generating svc header")
        header = create_header(self.file_size, self.delimiter, headers, huffman_trees)
        
        logger.info("Getting binary sequence")
        binary = ""
        with open(self.filename, "r", encoding="utf-8") as fp:
            next(fp) # skip headers
            for line in fp:
                columns = line.strip().split(self.delimiter)
                for column_index, column in enumerate(columns):
                    current_column = headers[column_index]
                    for char in column:
                        binary_string = code_tables[current_column][char]
                        binary += binary_string

        logger.info(f"Writing out to {self.output_file}")
        
     