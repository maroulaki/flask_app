from flask import Flask, request, jsonify

from huffman import HuffmanCodec
from cyclic import CyclicCodec
import crypto_utils


def decompress(compression_algorithm: str, data: str, params: dict) -> str:
    match compression_algorithm:
        case 'huffman':
            if 'huffman_dict' not in params:
                raise TypeError('Missing parameter: huffman_dict.')

            return HuffmanCodec.decode(data, params['huffman_dict'])
        
        case _:
            raise ValueError(f'Unsupported compression algorithm: {compression_algorithm}')


def decode(encoding: str, data: str, params: dict) -> tuple[str, int]:
    match encoding:
        case 'cyclic':
            if 'cyclic_dict' not in params:
                raise TypeError('Missing parameter: cyclic_dict.')

            return CyclicCodec.decode(data, params['cyclic_dict'])
        
        case _:
            raise ValueError(f'Unsupported encoding: {encoding}')


app = Flask(__name__)


@app.route('/', methods=['POST'])
def receive_json():
    # Retrieve data.
    data = request.get_json()

    # Base64 decode.
    decoded_message = crypto_utils.b64decode(data['encoded_message'])

    # Decode message with proper algorithm.
    decoded_message, fixed_errors = decode(
        data['encoding'], 
        decoded_message, 
        data['parameters']
    )

    errors_dif = data['errors'] - fixed_errors

    # Decompress message with proper algorithm.
    decoded_message = decompress(
        data['compression_algorithm'], 
        decoded_message,
        data['parameters']
    )

    # Calculate new hash and compare with original.
    decoded_sha256_hash = crypto_utils.sha256_hash(decoded_message)
    sha256_diff = data['SHA256'] != decoded_sha256_hash

    # Calculate new entropy and compare with original.
    decoded_entropy = crypto_utils.entropy(decoded_message)
    entropy_diff = data['entropy'] - decoded_entropy

    # Send response
    response = {
        'decoded_message': decoded_message,
        'fixed_errors': fixed_errors,
        'errors_dif': errors_dif,
        'SHA256': decoded_sha256_hash,
        'SHA256_diff': sha256_diff,
        'entropy': decoded_entropy,
        'entropy_diff': entropy_diff
    }

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(port=5000)