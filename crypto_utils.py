from collections import Counter
import numpy as np
import hashlib
import base64


def add_error(data: str, error_pos: float) -> str:
    error_i = int((len(data)-1) * error_pos)
    
    return data[:error_i] + str(1 - int(data[error_i])) + data[error_i + 1:] 


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