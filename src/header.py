import struct
from collections import deque

def pack_string(string):
    return string.encode("utf-8") + b"\x00"

def pack_string_list(string_list):
    packed_string_list = b""
    for string in string_list:
        packed_string_list += pack_string(string)
    return packed_string_list + b"\x00"

def pack_huffman_tree(root_node):
    if not root_node:
        return ""
    
    tree_binary = ""
    queue = deque([root_node])
    
    while queue:
        node = queue.popleft()
        if not node.left and not node.right:
            tree_binary += "1"
        else:
            tree_binary += "0"

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return tree_binary


def pack_huffman_trees(huffman_trees):
    huffman_binary = ""
    for header, tree in huffman_trees.items():
        huffman_binary += pack_huffman_tree(tree)
    return huffman_binary


def create_header(file_size, delimiter, headers, huffman_trees):
    header = b""
    header += struct.pack("<I", file_size)
    header += pack_string(delimiter)
    header += pack_string_list(headers)
    huffman_binary = pack_huffman_trees(huffman_trees)
    
    print(huffman_binary)
    print(len(huffman_binary) // 8)
    
    return header
    
def read_header():
    pass
        