from flask import Flask, request, jsonify

from huffman import HuffmanCodec
import crypto_utils


def decompress(compression_algorithm: str, data: str, **kwargs) -> str:
    match compression_algorithm:
        case 'huffman':
            if 'huffman_dict' not in kwargs:
                raise TypeError('Missing parameter: huffman_dict')

            return HuffmanCodec.decode(data, kwargs['huffman_dict'])
        
        case _:
            raise ValueError(f'Unsupported compression algorithm: {compression_algorithm}')


def decode(encoding: str, data: str, **kwargs) -> str:
    match encoding:
        case 'cyclic':
            return data
        
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
    decoded_message = decode(data['encoding'], decoded_message)

    # Decompress message with proper algorithm.
    decoded_message = decompress(
        data['compression_algorithm'], 
        decoded_message,
        huffman_dict = data['parameters'][0]
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
        'error_corrections': 0,
        'SHA256': decoded_sha256_hash,
        'SHA256_diff': sha256_diff,
        'entropy': decoded_entropy,
        'entropy_diff': entropy_diff
    }

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(port=5000)