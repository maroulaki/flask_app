import argparse
import requests
import json
from colorama import Style, Fore

from huffman import HuffmanCodec
from cyclic import CyclicCodec
import crypto_utils


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required='true', help='Path to message file.')
    parser.add_argument('-x', '--noise', type=float, required='true', help='Errors count / message length ratio.')

    return parser.parse_args()


def read_message(file_path: str) -> str:
    with open(file_path, 'r') as file:
        content = ''.join(line.strip() for line in file.readlines())

    return content


def pretty_print_json(message: str, data: dict) -> None:
    print(f'{Fore.GREEN}{message}:{Style.RESET_ALL}')
    print(Fore.CYAN)
    print(json.dumps(data, indent=4), end='\n\n')
    print(Style.RESET_ALL)


def send_payload(payload: dict, url: str='http://127.0.0.1:5000/') -> dict:
    HEADERS = {'Content-Type': 'application/json'}

    return requests.post(url, data=json.dumps(payload), headers=HEADERS).json()


def main() -> None:
    args = parse_args()

    message = read_message(args.file)
    
    if len(message) == 0:
        raise ValueError('Invalid message. Message should not be empty.')
    
    noise_ratio = args.noise

    if noise_ratio < 0 or noise_ratio > 1:
        raise ValueError(f'Invalid noise ratio value: {noise_ratio}. Values must be between 0 and 1.')

    # Calculate message hash.
    sha256_hash = crypto_utils.sha256_hash(message)

    # Calculate message entropy.
    entropy = crypto_utils.entropy(message)

    # Compress message.
    encoded_message, huffman_dict = HuffmanCodec.encode(message)

    # Encode message.
    encoded_message, cyclic_dict = CyclicCodec.encode(encoded_message)

    # Add noise at X% of message.
    encoded_message, errors = crypto_utils.add_noise(encoded_message, noise_ratio)

    # Base64 encode.
    encoded_message = crypto_utils.b64encode(encoded_message)

    # Send payload.
    payload = {
        'encoded_message': encoded_message,
        'compression_algorithm':'huffman',
        'encoding': 'cyclic',
        'parameters': {
            'huffman_dict': huffman_dict,
            'cyclic_dict': cyclic_dict
        },
        'errors': errors,
        'SHA256': sha256_hash,
        'entropy': entropy
    }
    pretty_print_json('Sending payload', payload)

    response = send_payload(payload)

    # Output server response.
    pretty_print_json('Response from server', response)


if __name__ == '__main__':
    main()