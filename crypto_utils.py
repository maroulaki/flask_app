from collections import Counter
import numpy as np
import hashlib


def entropy(data: str) -> float:
    freq_dict = Counter(data)
    total_count = sum(freq_dict.values())

    entropy = -sum((count / total_count) * np.log2(count / total_count) for count in freq_dict.values())

    return entropy


def sha256_hash(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()