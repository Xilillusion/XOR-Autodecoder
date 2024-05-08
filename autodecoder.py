# Support both Hex and ASCII
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


class Ciphers:
    def __init__(self, ciphers):
        self.ciphers = ciphers
        self.num = len(ciphers)
        self.len = max([len(c) for c in ciphers])

    def is_valid(self):
        # Check if there are more than 2 ciphertexts
        assert self.num > 1, "Error: Not enough ciphertexts"
        
        # Check if the ciphertexts have an even length
        assert self.len % 2 == 0, "Error: Odd ciphertext length"

        for i in range(self.num):
            # Check if the ciphertexts have the same length
            if len(self.ciphers[i]) != self.len:
                assert len(self.ciphers[i]) * 2 == self.len, "Error: Ciphertext length not match"
                self.ciphers[i] = self.ciphers[i].encode().hex()

            else:
                # Convert ASCII ciphers to hex
                try:
                    int(self.ciphers[i], 16)
                except ValueError:
                    self.ciphers[i] = self.ciphers[i].encode().hex()
                    self.len *= 2


def is_ascii(char):
    # Check if the characters are in the ASCII range
    for c in char:
        if c not in ASCII_RANGE:
            return False
    return True


def display_results(ciphers, key):
    # Display the possible messages
    for cipher in ciphers:
        print(f"Message: {cipher}")
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
    C = Ciphers(CIPHERS)
    try:
        C.is_valid()
    except AssertionError as e:
        print(e)
    
    key = []
    
    for i in range(C.len // 2):    # every 2 hex represent an ASCII
        # Convert the paired hex into dec
        char = [int(c[2*i:2*i+2], 16) for c in C.ciphers]

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
    
    display_results(C.ciphers, key)


if __name__ == "__main__":
    main()
