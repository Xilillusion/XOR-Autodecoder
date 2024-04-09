cipher1 = "2c1549100043130b1000290a1b"
cipher2 = "3f16421617175203114c020b1c"

if len(cipher1) != len(cipher2):
    raise Exception("Error: Ciphertexts length not match")

# Decimal range in ASCII
ascii_range = [
    *range(48, 58),    # Numbers
    *range(65, 91),    # Upper alphabets
    *range(97, 123),   # Lower alphabets
    ord('\\'),
    #ord('-'),
    #ord('.'),
    #ord('I'),
]


message1 = []
message2 = []

for i in range(len(cipher1) // 2):  # every 2 hex represent an ASCII char
    char1 = []
    char2 = []
    
    int1 = int(cipher1[2*i:2*i+2], 16)
    int2 = int(cipher2[2*i:2*i+2], 16)
    
    for key in range(256):
        result1 = int1 ^ key    # message = ciphertext xor key
        result2 = int2 ^ key
        
        # Check whether the decipherted messages are characters
        if result1 in ascii_range and result2 in ascii_range:
            char1.append(chr(result1))
            char2.append(chr(result2))
    
    if char1 == [] or char2 == []:
        print(f"Error: Search range too small. Empty result at {i}: {cipher1[i:i+2]} {cipher2[i:i+2]}")
    
    message1.append(char1)
    message2.append(char2)


print("\nLength:", len(message1))
print("Message 1:", message1)
print("Message 2:", message2)
