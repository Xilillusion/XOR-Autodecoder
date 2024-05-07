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
    #ord('\\'),
    #ord('-'),
    #ord('.'),
]


def is_valid_len(num, length):
    # Check if there are more than 2 ciphertexts
    if num < 2:
        raise Exception("Error: Not enough ciphertexts")
    # Check if the ciphertexts have an even length
    elif length % 2 != 0:
        raise Exception("Error: Odd ciphertext length") 

    # Check if the ciphertexts have the same length
    for c in range(num - 1):
        if len(CIPHERS[c]) != len(CIPHERS[c+1]):
            raise Exception("Error: Ciphertext length not match")


def is_ascii(char):
    # Check if the characters are in the ASCII range
    for c in char:
        if c not in ASCII_RANGE:
            return False
    return True


def display_results(key):
    # Display the possible messages
    for cipher in CIPHERS:
        print("Message: {cipher}")
        for i in range(len(key)):
            print("\t", end='')
            
            char = int(cipher[2*i:2*i+2], 16)
            for k in key[i]:
                print("%-2s" % chr(char ^ k), end=' ')
            print()
        print()

    # Display the possible key
    print("\nKey:")
    for k in key:
        print("\t", end='')
        for i in k:
            value = hex(i)[2:]
            if len(value) == 1:
                value = '0' + value
            
            print(f"{value}", end=' ')
        print()


def main():
    is_valid_len(len(CIPHERS), len(CIPHERS[0]))
    
    key = []
    
    for i in range(len(CIPHERS[0]) // 2):    # every 2 hex represent an ASCII
        # Convert the paired hex into dec
        char = []
        for cipher in CIPHERS:
            char.append(int(cipher[2*i:2*i+2], 16))

        # Try all keys
        key.append([])
        for k in range(0xFF):
            msg = []
            for c in char:
                msg.append(c ^ k)    # message = ciphertext xor key

            if is_ascii(msg):
                key[i].append(k)

        if not key[i]:
            print(f"Warning: Search range too small. Empty result at position {i}")
    
    display_results(key)


if __name__ == "__main__":
    main()
