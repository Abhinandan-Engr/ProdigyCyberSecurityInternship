def caesar_cipher(text, shift, mode):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            if mode == "encrypt":
                result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            elif mode == "decrypt":
                result += chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
        else:
            result += char
    return result

message = input("Enter your message: ")
shift = int(input("Enter shift value: "))

encrypted = caesar_cipher(message, shift, "encrypt")
print("Encrypted text:", encrypted)

decrypted = caesar_cipher(encrypted, shift, "decrypt")
print("Decrypted text:", decrypted)
