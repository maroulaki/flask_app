from dataclasses import dataclass, field
from collections import Counter
import heapq
from typing import Optional


class HuffmanCodec():
    @staticmethod
    def encode(data: str) -> tuple[str, dict[str, str]]:
        huffman_dict = _HuffmanTree(data).generate_huffman_dict()
        encoded = ''.join(huffman_dict[ch] for ch in data)

        return encoded, huffman_dict


    @staticmethod
    def decode(data: str, huffman_dict: dict[str, str]) -> str:
        reversed_dict = {v: k for k, v in huffman_dict.items()}

        decoded = ''
        code = ''

        for bit in data:
            code += bit

            if code in reversed_dict:
                decoded += reversed_dict[code]
                code = ''

        return decoded
    

@dataclass(order=True)
class _Node:
    freq: int = field(compare=True, default=0)
    item: Optional[str] = field(compare=False, default=None)
    left: Optional['_Node'] = field(compare=False, default=None)
    right: Optional['_Node'] = field(compare=False, default=None)


class _HuffmanTree():
    def __init__(self, data: str) -> None:
        freq_dict = Counter(data)

        min_heap = [_Node(freq, item) for item, freq in freq_dict.items()]
        heapq.heapify(min_heap)

        while len(min_heap) > 1:
            node_1: _Node = heapq.heappop(min_heap)
            node_2: _Node = heapq.heappop(min_heap)

            freq_sum = node_1.freq + node_2.freq
            parent_node = _Node(freq=freq_sum, left=node_1, right=node_2)

            heapq.heappush(min_heap, parent_node)

        self._root: _Node = min_heap[0]


    def generate_huffman_dict(self) -> dict[str, str]:
        huffman_dict = {}
        frontier = [(self._root, [])]

        while frontier:
            node, code = frontier.pop()

            if node.item:
                huffman_dict[node.item] = ''.join(code)
                continue

            frontier.append((node.left, code + ['0']))
            frontier.append((node.right, code + ['1']))

        return huffman_dict