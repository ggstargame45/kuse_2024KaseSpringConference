import os
import can
from cryptography.hazmat.primitives import hashes, hmac

bus = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
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

while 1:
    # Receive Can Message
    message = bus.recv(10.0)
    receive_data = message.data
    
    receive_data = [hex(n) for n in receive_data]
    receive_data = [t[2:] for t in receive_data]    # delete '0x'

    # Decryption using RC4
    key_origin = 'Friday'
    decrypted = decrypt(key_origin, receive_data)
    decrypted = [int(h,16) for h in decrypted]
    print('Decryption Data: ', decrypted)

    # HMAC Algorithm using SHA-256
    mac_data = decrypted[4:]    
    key = plain2bitarray(key_origin)
    h = hmac.HMAC(key, hashes.SHA256())
    mac_data = decimal2bytes(mac_data)
    h.update(mac_data)
    signature = h.finalize()
    print('Calculate MAC: ',signature)

    # Check Authorization
    signature = [byte for byte in signature]

    if signature[:4] == decrypted[:4]:
        print("This Message is correct")
    else:
        print("Deny the Message")
