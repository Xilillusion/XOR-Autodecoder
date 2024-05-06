CIPHERS = [
    "2c1549100043130b1000290a1b",
    "3f16421617175203114c020b1c",
]

# Decimal range in ASCII
ASCII_RANGE = [
    *range(65, 91),    # Upper alphabets
    *range(97, 123),   # Lower alphabets
    #*range(48, 58),    # Numbers
    ord(' '),
    #ord('I'),
    #ord('\\'),
    #ord('-'),
    #ord('.'),
]


def is_valid_len(num, len):
    # Ensure the ciphertexts have an even length
    if len % 2 != 0:
        raise Exception("Error: Odd ciphertext length") 

    # Ensure the ciphertexts have the same length
    for c in range(num - 1):
        if len(CIPHERS[c]) != len(CIPHERS[c+1]):
            raise Exception("Error: Ciphertext length not match")


def is_ascii(chars):
    # Check if the characters are in the ASCII range
    for char in chars:
        if char not in ASCII_RANGE:
            return False
    return True


def main():
    cipher_num = len(CIPHERS)
    cipher_len = len(CIPHERS[0]) // 2
    is_valid_len(cipher_num, len(CIPHERS[0]))
    
    # Initialize the deciphered messages and their possible keys
    messages = []
    keys = []
    for i in range(cipher_num):
        messages.append([])
        keys.append([])
        for j in range(cipher_len):
            messages[i].append([])
            keys[i].append([])

    for i in range(cipher_len):    # every 2 hex represent an ASCII char
        # Convert the paired hex into dec
        ints = []
        for c in CIPHERS:
            ints.append(int(c[2*i:2*i+2], 16))

        # Try keys
        for k in range(0xFF):
            chars = []
            for int in ints:
                chars.append(int ^ k)    # message = ciphertext xor key

            if is_ascii(chars):
                for n in cipher_num:
                    messages[n][i].append(chr(chars[n]))
                    keys[n][i].append(hex(k))
            
        for j in range(cipher_len):
            if messages[0][j] == []:
                print(f"Warning: Search range too small. Empty result at position {i}")

