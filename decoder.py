from autodecoder import Ciphers

def main():
    # Read ciphertexts from config file
    import json
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    C = Ciphers(config["Ciphertexts"])
    
    while True:
        #key = input("Enter the key: ")
        key = "my secret key"
        if len(key) != C.len:
            if len(key) * 2 != C.len:
                print("Invalid key length. Please try again\n")
            else:
                # Convert ASCII key to hex
                key = key.encode().hex()
                break
        else:
            break
    
    # Display the deciphered message
    print(f"Key:\n\t {key}")
    for cipher in C.ciphers:
        print(f"\nMessage: {cipher}\n\t ", end='')
        for i in range(len(key) // 2):
            char = int(cipher[2*i:2*i+2], 16) ^ int(key[2*i:2*i+2], 16)
            print(chr(char), end='')


if __name__ == "__main__":
    main()