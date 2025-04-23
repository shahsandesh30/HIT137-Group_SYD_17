def encrypt_text(text, n, m):
    code = ""
    for t in text:
        if 'a' <= t <= 'z':
            ord_value = ord(t)
            if t <= 'm':
                cipher_value = ord_value + n * m  # encrypting formula for a to m
                cipher_value = (cipher_value - ord('a')) % 26 + ord('a') # Apply modulo if ASCII value exceeds 'z'
            else:
                cipher_value = ord_value - (n + m) # encrypting formula for n to z
                cipher_value = (cipher_value - ord('a')) % 26 + ord('a') # Apply modulo if ASCII value exceeds 'z'
            code += chr(cipher_value)

        elif 'A' <= t <= 'Z':
            ord_value = ord(t)
            if t <= 'M':
                cipher_value = ord_value - n # encrypting formula for A to M
                cipher_value = (cipher_value - ord('A')) % 26 + ord('A') # Apply modulo if ASCII value exceeds 'Z'
            else:
                cipher_value = ord_value + m * m    # encrypting formula for N to Z
                cipher_value = (cipher_value - ord('A')) % 26 + ord('A') # Apply modulo if ASCII value exceeds 'Z'
            code += chr(cipher_value)

        else:
            code += t # characters remain same

    return code


def decrypt_text(encrypted_text, n, m, original_text):
    code2 = ""
    for i in range(len(encrypted_text)):
        d = encrypted_text[i]
        t = original_text[i]  

        if 'a' <= d <= 'z':
            ord_value = ord(d)
            if t <= 'm':
                cipher_value = ord_value - n * m # decrypting formula for a to m
                cipher_value = (cipher_value - ord('a')) % 26 + ord('a') # Apply modulo if ASCII value exceeds 'z'
            else:
                cipher_value = ord_value + (n + m) # decrypting formula for n to z
                cipher_value = (cipher_value - ord('a')) % 26 + ord('a') # Apply modulo if ASCII value exceeds 'z'
            code2 += chr(cipher_value)

        elif 'A' <= d <= 'Z':
            ord_value = ord(d)
            if t <= 'M':
                cipher_value = ord_value + n # decrypting formula for A to M
                cipher_value = (cipher_value - ord('A')) % 26 + ord('A') # Apply modulo if ASCII value exceeds 'Z'
            else:
                cipher_value = ord_value - m * m   # decrypting formula for N to Z
                cipher_value = (cipher_value - ord('A')) % 26 + ord('A') # Apply modulo if ASCII value exceeds 'Z'
            code2 += chr(cipher_value)

        else:
            code2 += d # characters remain same

    return code2


def check_correctness(original, decrypted):
    return original == decrypted


def main():
    # Input the values of n and m
    n = int(input("Enter value of n: "))
    m = int(input("Enter value of m: "))

    # Read the raw text from the file
    with open("raw_text.txt", "r") as file:
        raw_text = file.read()

    # Encrypt the raw text
    encrypted_text = encrypt_text(raw_text, n, m)

    # Write the encrypted text to a new  txt file
    with open("encrypted_text.txt", "w") as file:
        file.write(encrypted_text)

    print(f"Encrypted text: {encrypted_text}")

    # Decrypt the text to check correctness
    decrypted_text = decrypt_text(encrypted_text, n, m, raw_text)

    # Print the decrypted text
    print(f"Decrypted text: {decrypted_text}")

    # Check if the decrypted text matches the original
    if check_correctness(raw_text, decrypted_text):
        print("The original text and decrypted text match.")
    else:
        print("The original text and decrypted text don't match.")


if __name__ == "__main__":
    main()
