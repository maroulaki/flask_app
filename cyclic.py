from sage.all import *
from sage.coding.cyclic_code import CyclicCode
from sympy.ntheory import isprime
import random


class CyclicCodec():
    __RING = PolynomialRing(GF(2), 'x')
    __PRIMES = [i for i in range(5, 100) if isprime(i)]


    @staticmethod
    def encode(data: str) -> tuple[str, dict]:
        data = list(map(int, data)) 

        gen_poly, n = CyclicCodec.__generate_cyclic_code_pair()

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
    def __generate_cyclic_code_pair() -> tuple[Polynomial, int]:
        while True:
            n = random.choice(CyclicCodec.__PRIMES)
            
            x = CyclicCodec.__RING.gen()
            p = x**n - 1
            
            divisors = [CyclicCodec.__RING(d[0]) for d in p.factor()]
            filtered = [d for d in divisors if 1 < d.degree() < 10]

            if not filtered:
                continue

            gen_poly = random.choice(filtered)
            break

        return gen_poly, n
    

    @staticmethod
    def __count_error_fixes(init: vector, corrected: vector):
        return sum(1 for i, j in zip(init, corrected) if i != j)