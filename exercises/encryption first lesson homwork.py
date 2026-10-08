def encrypt_plain_text(text: str, key: str) -> str:
    s= ""
    key_length = len(str(key))
    i = 0
    while i < len(text):
        ascii_value = ord(text[i]) 
        key_value = ord(str(key)[i % key_length])
        numeric_value = ascii_value + key_value
        print(numeric_value)
        char = chr(numeric_value)
        s += char
        i+=1
    return s

text = input("enter a text to encrypt\n")
key = input("enter encryption key\n")
encrypted_text = encrypt_plain_text(text, key)
print(repr(encrypt_plain_text(text, key)))


def decrypt_text(encrypted_text: str, key: str) ->str:
    text = ""
    key_length = len(str(key))
    i = 0
    while i < len(encrypted_text):
        ascii_value = ord(encrypted_text[i]) 
        key_value = ord(str(key)[i % key_length])
        char = chr(ascii_value - key_value)
        text+=char
        i+=1
    return text

print(decrypt_text(encrypted_text,key ))