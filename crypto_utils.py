from collections import Counter
import numpy as np
import hashlib
import base64
import random


def add_noise(data: str, ratio: float) -> tuple[str, int]:
    assert 0 <= ratio <= 1
    
    data = list(data)
    errors = int((len(data)-1) * ratio)
    error_pos = random.sample(list(range(len(data))), errors)

    for i in error_pos:
        data[i] = str(1 - int(data[i]))
    
    return ''.join(data), errors


def entropy(data: str) -> float:
    freq_dict = Counter(data)
    total_count = sum(freq_dict.values())

    entropy = -sum((count / total_count) * np.log2(count / total_count) for count in freq_dict.values())

    return entropy


def sha256_hash(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def b64encode(data: str) -> str:
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')


def b64decode(data: str) -> str:
    return base64.b64decode(data).decode('utf-8')