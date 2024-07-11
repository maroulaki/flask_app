from sage.all import *
from sage.coding.cyclic_code import CyclicCode


class CyclicCodec():
    __RING = PolynomialRing(GF(2), 'x')


    @staticmethod
    def encode(data: str) -> tuple[str, dict]:
        data = list(map(int, data)) 

        n = 7
        x = CyclicCodec.__RING.gen()
        gen_poly = x**3 + x + 1

        k = n - gen_poly.degree()
        cyclic_code = CyclicCode(gen_poly, n)

        padding = k - (len(data) % k)

        data += [0] * padding 

        encoded_data = []

        for i in range(0, len(data), k):
            chunk = vector(GF(2), data[i:i + k])
            encoded_chunk = cyclic_code.encode(chunk)
            encoded_data += map(str, encoded_chunk)

        cyclic_dict = {
            'n': int(n),
            'gen_poly': str(gen_poly),
            'padding': int(padding)
        }
        
        return ''.join(encoded_data), cyclic_dict
        

    @staticmethod
    def decode(data: str, cyclic_dict: dict) -> tuple[str, int]:
        n = cyclic_dict['n']
        gen_poly = CyclicCodec.__RING(cyclic_dict['gen_poly'])
        padding = cyclic_dict['padding']

        cyclic_code = CyclicCode(gen_poly, n)

        decoded_data = []
        fixed_errors = 0

        for i in range(0, len(data), n):
            chunk = vector(GF(2), data[i:i + n])
            corrected_chunk = cyclic_code.decode_to_code(chunk)

            fixed_errors += CyclicCodec.__count_error_fixes(chunk, corrected_chunk)

            decoded_chunk = cyclic_code.unencode(corrected_chunk)
            decoded_data += map(str, decoded_chunk)

        return ''.join(decoded_data)[:-padding], fixed_errors
    

    @staticmethod
    def __count_error_fixes(init: vector, corrected: vector):
        return sum(1 for i, j in zip(init, corrected) if i != j)