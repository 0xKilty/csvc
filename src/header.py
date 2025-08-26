import struct

def pack_string(string):
    return string.encode("utf-8") + b"\x00"

def pack_string_list(string_list):
    packed_string_list = b""
    for string in string_list:
        packed_string_list += pack_string(string)
    return packed_string_list + b"\x00"

def pack_huffman_tree(node, prefix=""):
    

def create_header(file_size, delimiter, headers, huffman_trees):
    header = b""
    header += struct.pack("<I", file_size)
    header += pack_string(delimiter)
    header += pack_string_list(headers)
    
    pack_huffman_tree(huffman_trees[0])
    
    return header
    
def read_header():
    pass
        