import base64
from pathlib import Path

KEY = Path(__file__).with_name("key").read_bytes().strip()
PLAINTEXT = b'id,US name,JP name,US description,JP description,CN name,CN description'


def xor_bytes(data, key=KEY):
    return bytes(byte ^ key[i % len(key)] for i, byte in enumerate(data))

def find_key(encrypted, plaintext=PLAINTEXT):
    candidate_key = bytes(byte ^ encrypted[i] for i, byte in enumerate(plaintext))
    print(f'Header XOR yields {candidate_key}')

def decode_translation(text):
    encrypted = base64.b64decode(text)
    find_key(encrypted)
    decrypted = xor_bytes(encrypted)
    return decrypted.decode('utf-8')

def encode_translation(text):
    raw = text.encode('utf-8')
    encrypted = xor_bytes(raw)
    return base64.b64encode(encrypted).decode('ascii')
