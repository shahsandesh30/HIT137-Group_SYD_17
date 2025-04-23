# Encryption
text = input("Enter text to encrypt: ")
n = int(input("Enter value for n: "))
m = int(input("Enter value for m: "))
code = ""

for ch in text:
    if 'a' <= ch <= 'z':
        ordvalue = ord(ch)
        if ch <= 'm':
            ciphervalue = ordvalue + n * m
            if ciphervalue > ord('z'):
                x = ciphervalue - ord('z')
                ciphervalue = ord('a') + x - 1
        else:
            ciphervalue = ordvalue - (n + m)
            if ciphervalue < ord('a'):
                x = ord('a') - ciphervalue
                ciphervalue = ord('z') - x + 1
        code = code + chr(ciphervalue)

    elif 'A' <= ch <= 'Z':
        ordvalue = ord(ch)
        if ch <= 'M':
            ciphervalue = ordvalue - n
            if ciphervalue < ord('A'):
                x = ord('A') - ciphervalue
                ciphervalue = ord('Z') - x + 1
        else:
            ciphervalue = ordvalue + m * m
            if ciphervalue > ord('Z'):
                x = ciphervalue - ord('Z')
                ciphervalue = ord('A') + (x - 1) % 26
        code = code + chr(ciphervalue)

    else:
        code = code + ch  # Leave special characters unchanged

print("Encrypted text is:", code)



# Decryption

