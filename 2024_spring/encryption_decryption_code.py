from cryptography.hazmat.primitives import hashes, hmac

MOD = 256

def plain2bitstring(plain: str):
    return "".join(format(ord(c), "0>8b") for c in plain)

def plain2bitarray(plain: str):
    bitstring = plain2bitstring(plain)
    encoded = bytearray([int(b) for b in bitstring])
    return encoded

def decimal2bytes(decimal_list):
    byte_string = bytes(decimal_list)
    return byte_string

def KSA(key):
    key_length = len(key)
    S = [n for n in range(MOD)]
    j = 0
    for i in range(0,MOD):
        j = (j + S[i] + key[i % key_length]) % MOD
        S[i], S[j] = S[j], S[i]

    return S


def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % MOD
        j = (j + S[i]) % MOD

        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % MOD]
        yield K

def get_keystream(key):
    S = KSA(key)
    return PRGA(S)

def encrypt(key, plaintext):
    # For plaintext key, use this
    if type(key) == type('abc'):
        key = [ord(c) for c in key]
    else:
        # If key is in hex:
        key = key.decode('hex')
        key = [ord(c) for c in key]

    # Get the keystream
    keystream = get_keystream(key)

    res = []
    for c in plaintext:
        if type(c) == type('s'):
            val = ("%02X" % (ord(c) ^ next(keystream)))  # XOR and taking hex
        elif type(c) == bytes:
            val = ("%02X" % (ord(c) ^ next(keystream)))
        else:
            val = ("%02X" % (c ^ next(keystream)))
        res.append(val)
    return res

def decrypt(key, ciphertext):
    if type(key) == type('c'):
        byte_array_key = bytearray(key, 'utf-8')
        hex_key = byte_array_key.hex()
    
    ciphertext = [bytes.fromhex(c) for c in ciphertext]

    #print('ciphertext to func:', ciphertext)
    res = encrypt(hex_key, ciphertext)
    return res

# Initial Data
data = [12,21,33,47]
key_origin = 'Friday'

# HMAC Algorithm using SHA-256
key = plain2bitarray(key_origin)
h = hmac.HMAC(key, hashes.SHA256())
mac_data = decimal2bytes(data)
h.update(mac_data)
signature = h.finalize()
print('Initial MAC: ',signature)

# Generate Send Message
signature = [byte for byte in signature]
send_data = signature[:4] + data
print('Send Data: ', send_data)

# Encryption using RC4
byte_array_key = bytearray(key_origin, 'utf-8')
hex_key = byte_array_key.hex()

ciphertext = encrypt(hex_key, send_data)
print('Cipher Data: ', ciphertext)

# Decryption using RC4
decrypted = decrypt(key_origin, ciphertext)
decrypted = [int(h,16) for h in decrypted]
print('Decryption Data: ', decrypted)