import argparse
import requests
import json
import base64
from colorama import Style, Fore

from huffman import HuffmanCodec
import crypto_utils


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required='true', help='Path to message file.')

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

    pretty_print_json('Sending payload', payload)

    return requests.post(url, data=json.dumps(payload), headers=HEADERS).json()


def main() -> None:
    # Parse file path argument.
    args = parse_args()

    # Read message file
    message = read_message(args.file)
    
    if len(message) == 0:
        raise ValueError('Invalid message. Message should not be empty.')

    # Calculate message hash.
    sha256_hash = crypto_utils.sha256_hash(message)

    # Calculate message entropy.
    entropy = crypto_utils.entropy(message)

    # Compress message.
    encoded_message, huffman_dict = HuffmanCodec.encode(message)

    # Base64 encode.
    encoded_message = crypto_utils.b64encode(encoded_message)

    # Send payload
    payload = {
        'encoded_message': encoded_message,
        'compression_algorithm':'huffman',
        'encoding': 'cyclic',
        'parameters': [huffman_dict],
        'errors': 0,
        'SHA256': sha256_hash,
        'entropy': entropy
    }

    response = send_payload(payload)

    # Output server response.
    pretty_print_json('Response from server', response)


if __name__ == '__main__':
    main()