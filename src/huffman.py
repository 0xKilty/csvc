import heapq

class HuffmanNode:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(freq_dict):
    heap = [HuffmanNode(char, freq) for char, freq in freq_dict.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0] if heap else None


def generate_huffman_codes(node, prefix="", code_table=None):
    if code_table is None:
        code_table = {}

    if node is None:
        return code_table

    if node.char is not None:
        code_table[node.char] = prefix
    else:
        generate_huffman_codes(node.left, prefix + "0", code_table)
        generate_huffman_codes(node.right, prefix + "1", code_table)

    return code_table
