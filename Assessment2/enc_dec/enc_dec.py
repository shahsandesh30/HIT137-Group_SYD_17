import os

# Function to encrypt a given text based on provided values n and m
def encrypt_text(text, n, m):
    code = ""

    for t in text:
        # Encrypt lowercase letters
        if 'a' <= t <= 'z':
            ord_value = ord(t)

            if t <= 'm':
                # For 'a' to 'm': shift forward by n * m
                cipher_value = ord_value + n * m
            else:
                # For 'n' to 'z': shift backward by (n + m)
                cipher_value = ord_value - (n + m)

            # Wrap around if needed using modulo 26
            cipher_value = (cipher_value - ord('a')) % 26 + ord('a')
            code += chr(cipher_value)

        # Encrypt uppercase letters
        elif 'A' <= t <= 'Z':
            ord_value = ord(t)

            if t <= 'M':
                # For 'A' to 'M': shift backward by n
                cipher_value = ord_value - n
            else:
                # For 'N' to 'Z': shift forward by m * m
                cipher_value = ord_value + m * m

            # Wrap around if needed using modulo 26
            cipher_value = (cipher_value - ord('A')) % 26 + ord('A')
            code += chr(cipher_value)

        else:
            # Leave non-alphabetic characters unchanged
            code += t

    return code

# Function to decrypt text using original text as reference for logic direction
def decrypt_text(encrypted_text, n, m, original_text):
    decrypted = ""

    for i in range(len(encrypted_text)):
        e_char = encrypted_text[i]  # Current encrypted character
        o_char = original_text[i]   # Original character for reference

        # Decrypt lowercase letters
        if 'a' <= e_char <= 'z':
            base = ord('a')
            offset = ord(e_char) - base

            if o_char <= 'm':
                # If original char was from 'a' to 'm', reverse encryption by subtracting n * m
                new_offset = (offset - n * m) % 26
            else:
                # If original char was from 'n' to 'z', reverse by adding (n + m)
                new_offset = (offset + (n + m)) % 26

            decrypted += chr(base + new_offset)

        # Decrypt uppercase letters
        elif 'A' <= e_char <= 'Z':
            base = ord('A')
            offset = ord(e_char) - base

            if o_char <= 'M':
                # If original char was from 'A' to 'M', reverse by adding n
                new_offset = (offset + n) % 26
            else:
                # If original char was from 'N' to 'Z', reverse by subtracting m squared
                new_offset = (offset - m * m) % 26

            decrypted += chr(base + new_offset)

        # Leave non-alphabetic characters unchanged
        else:
            decrypted += e_char

    return decrypted

def check_correctness(original, decrypted):
    return original == decrypted


def main():
    # Input the values of n and m
    n = int(input("Enter value of n: "))
    m = int(input("Enter value of m: "))

    current_dir = os.path.dirname(__file__) # current directory path
    parent_dir = os.path.dirname(current_dir)
    
    raw_datafile_dir = os.path.join(parent_dir, "data_files","raw_text.txt") # data_files directory path
    
    # Read the raw text from the file
    with open(raw_datafile_dir, "r") as file:
        raw_text = file.read()


    # Encrypt the raw text
    encrypted_text = encrypt_text(raw_text, n, m)

    enc_datafile_dir = os.path.join(current_dir, "result_files","encrypted_text.txt") 
    # Write the encrypted text to a new  txt file
    with open(enc_datafile_dir, "w") as file:
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
