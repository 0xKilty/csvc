import struct
import logging
from collections import deque

logger = logging.getLogger("csvc")

class BitStream:
    def __init__(self, bit_string=""):
        self.bit_string = bit_string
        self.length = len(bit_string)
        self.value = int(bit_string, 2) if bit_string else None

        num_bytes = (self.length + 7) // 8
        self.data = self.value.to_bytes(num_bytes, byteorder="big") if bit_string else None

    def __add__(self, other):
        if isinstance(other, BitStream):
            return BitStream(self.bit_string + other.bit_string)
        raise TypeError(f"Unsupported operand type(s) for +: 'BitStream' and '{type(other).__name__}'")
    
    def __str__(self):
        return self.data.hex()

class Header:
    def __init__(self, file_size, delimiter, headers, huffman_trees):
        self.file_size = file_size
        self.delimiter = delimiter
        self.headers = headers
        self.huffman_trees = huffman_trees
        
    def create_header(self):
        binary_string = ""

        logger.debug(f"Packing file size {self.file_size}")
        file_size_bytes = struct.pack(">I", self.file_size)
        binary_string += bytes_to_binary_string(file_size_bytes)
        logger.debug(f"Bytes: {bits_to_hex(binary_string)}")
        
        logger.debug(f"Packing delimiter {self.delimiter}")
        binary_string += pack_string(self.delimiter)
        logger.debug(f"Bytes: {bits_to_hex(binary_string)}")
        
        logger.debug(f"Packing headers {self.headers}")
        binary_string += pack_string_list(self.headers)
        logger.debug(f"Bytes: {bits_to_hex(binary_string)}")
        
        all_keys, huffman_binary_string = pack_huffman_trees(self.huffman_trees)
        key_strings = ["".join(keys) for keys in all_keys]
        
        logger.debug(f"Packing Huffman keys {self.headers}")
        binary_string += pack_string_list(key_strings)
        logger.debug(f"Bytes: {bits_to_hex(binary_string)}")
        
        logger.debug(f"Packing Huffman trees {self.headers}")
        binary_string += huffman_binary_string
        logger.debug(f"Bytes: {bits_to_hex(binary_string)}")
        
        return binary_string
    
    @staticmethod
    def read_header(fp):
        
        logger.debug("Unpacking file size")
        file_size_bytes = fp.read(4)
        file_size = struct.unpack(">I", file_size_bytes)[0]
        logger.debug(f"File size {file_size} ({hex(file_size)})")

        logger.debug("Unpacking delimiter")
        delimiter = unpack_string(fp)
        logger.debug(f"Delimiter {delimiter}")

        logger.debug("Unpacking headers")
        headers = unpack_string_list(fp)
        logger.debug(f"Headers {headers}")

        # Read Huffman keys
        key_strings = unpack_string_list(fp)
        all_keys = [list(s) for s in key_strings]
        print(all_keys)

        # Rebuild huffman_trees
        # huffman_trees = unpack_huffman_trees(fp, all_keys)
        return None
        # return Header(file_size, delimiter, headers, huffman_trees)

def bytes_to_binary_string(bytes):
    return "".join(format(byte, "08b") for byte in bytes)

def bits_to_hex(bin_str):
    value = int(bin_str, 2)
    num_bytes = (len(bin_str) + 7) // 8
    return value.to_bytes(num_bytes, "big").hex()

def pack_string(string):
    data = string.encode("utf-8") + b"\x00"
    return bytes_to_binary_string(data)

def unpack_string(fp):
    byte = fp.read(1)
    string = b""
    while byte != b"\x00":
        string += byte
        byte = fp.read(1)
    return string

def unpack_string_list(fp):
    string_list = []
    while True:
        string = unpack_string(fp)
        if string == b"":
            break
        string_list.append(string)
    return string_list

def pack_string_list(string_list):
    packed_string_list = ""
    for string in string_list:
        packed_string_list += pack_string(string)
    return packed_string_list + bytes_to_binary_string(b"\x00")


def pack_huffman_tree(root_node):
    if not root_node:
        return ""
    
    tree_binary_string = ""
    keys = []
    queue = deque([root_node])
    
    while queue:
        node = queue.popleft()
        if not node.left and not node.right:
            tree_binary_string += "1"
            keys.append(node.char)
        else:
            tree_binary_string += "0"

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return keys, tree_binary_string


def pack_huffman_trees(huffman_trees):
    huffman_binary_string = ""
    all_keys = []
    for _, tree in huffman_trees.items():
        keys, bit_string = pack_huffman_tree(tree) 
        huffman_binary_string += bit_string
        all_keys.append(keys)
    return all_keys, huffman_binary_string
        

def bytes_to_bits(bytes):
    return "".join(format(byte, "08b") for byte in bytes)
    
def read_header():
    pass
        