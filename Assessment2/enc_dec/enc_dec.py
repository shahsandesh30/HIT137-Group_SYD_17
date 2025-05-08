import os

# Function to encrypt text based on input values
def encrypt_text(text, n, m):
    code = ""

    for t in text:
        # for lower case
        if 'a' <= t <= 'z':
            ord_value = ord(t)

            if t <= 'm':
                # For a to m shift forward by n * m
                cipher_value = ord_value + n * m
            else:
                # For n to z shift backward by n + m
                cipher_value = ord_value - (n + m)

            # Wrap if needed to use modulo 6
            cipher_value = (cipher_value - ord('a')) % 26 + ord('a')
            code += chr(cipher_value)

        # for upper case letters
        elif 'A' <= t <= 'Z':
            ord_value = ord(t)

            if t <= 'M':
                # For A to M  shift backward by n
                cipher_value = ord_value - n
            else:
                # For N to Z shift forward by m * m
                cipher_value = ord_value + m * m

            cipher_value = (cipher_value - ord('A')) % 26 + ord('A')
            code += chr(cipher_value)

        else:
            # leave non alphabet unchanged
            code += t

    return code

# decrypt using original text
def decrypt_text(encrypted_text, n, m, original_text):
    decrypted = ""

    for i in range(len(encrypted_text)):
        e_char = encrypted_text[i]  # Current encrypted character
        o_char = original_text[i]   # Original character 

        # Decrypt lowercase letters
        if 'a' <= e_char <= 'z':
            base = ord('a')
            offset = ord(e_char) - base

            if o_char <= 'm':
                # for  a to m, decrypt by subtracting n * m
                new_offset = (offset - n * m) % 26
            else:
                # for n to z, decrypt by adding n + m
                new_offset = (offset + (n + m)) % 26

            decrypted += chr(base + new_offset)

        # Decrypt uppercase letters
        elif 'A' <= e_char <= 'Z':
            base = ord('A')
            offset = ord(e_char) - base

            if o_char <= 'M':
                # for a to m, reverse by adding n
                new_offset = (offset + n) % 26
            else:
                # for n to z , reverse by subtracting m squared
                new_offset = (offset - m * m) % 26

            decrypted += chr(base + new_offset)

        else:
            decrypted += e_char

    return decrypted

def check_correctness(original, decrypted):
    return original == decrypted


def main():
    # inputs
    n = int(input("Enter value of n: "))
    m = int(input("Enter value of m: "))

    current_dir = os.path.dirname(__file__) # current directory path
    parent_dir = os.path.dirname(current_dir)
    
    raw_datafile_dir = os.path.join(parent_dir, "data_files","raw_text.txt") # data_files directory path
    
    # read raw text from data file
    with open(raw_datafile_dir, "r") as file:
        raw_text = file.read()


    # encrypt 
    encrypted_text = encrypt_text(raw_text, n, m)

    enc_datafile_dir = os.path.join(current_dir, "result_files","encrypted_text.txt") 
    
    # Write the encrypted text to a new  txt file
    with open(enc_datafile_dir, "w") as file:
        file.write(encrypted_text)

    print(f"Encrypted text is : {encrypted_text}")

    # Decrypt the text to check correctness
    decrypted_text = decrypt_text(encrypted_text, n, m, raw_text)

    print(f"Decrypted text is : {decrypted_text}")

    # Check decrypted text matches the original
    if check_correctness(raw_text, decrypted_text):
        print("The original text and decrypted text match.")
    else:
        print("The original text and decrypted text donot match.")


if __name__ == "__main__":
    main()
