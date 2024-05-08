class Ciphers:
    def __init__(self, ciphers):
        self.ciphers = ciphers
        self.num = len(ciphers)
        self.len = max([len(c) for c in ciphers])
        
        self.init_ciphers()

    def init_ciphers(self):
        # Check if there are more than 2 ciphertexts
        assert self.num > 1, "Not enough ciphertexts"
        
        # Check if the ciphertexts have an even length
        assert self.len % 2 == 0, "Odd ciphertext length"

        for i in range(self.num):
            # Check if the ciphertexts have the same length
            if len(self.ciphers[i]) != self.len:
                assert len(self.ciphers[i]) * 2 == self.len, "Ciphertext length not match"
                self.ciphers[i] = self.ciphers[i].encode().hex()

            else:
                # Convert ASCII ciphers to hex
                try:
                    int(self.ciphers[i], 16)
                except ValueError:
                    self.ciphers[i] = self.ciphers[i].encode().hex()
                    self.len *= 2


def read_config():
    """Read and intitialize the config file"""
    import json
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # Initialize the search_range
    search_range = []
    for i in config["SearchRange"]:
        if i.lower() in ["lower", "loweralphabets"]:
            search_range += range(97, 123)
        elif i.upper() in ["UPPER", "UPPERALPHABETS"]:
            search_range += range(65, 91)
        elif i.lower() in ["num", "numbers"]:
            search_range += range(48, 58)
        else:
            try:
                search_range.append(ord(i))
            except TypeError as e:
                print(f'Warning: Invalid search range "{i}"')
    
    return config["Ciphertexts"], search_range


def is_range(char, search_range):
    """Return True if all the characters are in ASCII range"""
    for c in char:
        if c not in search_range:
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
    ciphers, search_range = read_config()
    
    C = Ciphers(ciphers)
    
    key = []
    
    for i in range(C.len // 2):    # every 2 hex represent an ASCII
        # Convert the paired hex into dec
        char = []
        for cipher in C.ciphers:
            char.append(int(cipher[2*i:2*i+2], 16))

        # Try all keys
        key.append([])
        for k in range(0xFF):
            msg = []
            for c in char:
                msg.append(c ^ k)    # message = ciphertext xor key

            if is_range(msg, search_range):
                key[i].append(k)

        if not key[i]:
            print(f"Warning: Search range too small. Empty result at position {i}")
    
    display_results(C.ciphers, key)


if __name__ == "__main__":
    main()
