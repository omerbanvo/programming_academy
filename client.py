import socket
import os
def recv_exact(sock, recv_size):
    buffer = b""
    while len(buffer) < recv_size:
        chunk = sock.recv(recv_size - len(buffer))
        if not chunk:
            raise ConnectionError("connection faild\nconnection stopped unexpectedly before recieveing expected data ")
        buffer += chunk
    return buffer

def upload_file(sock):
    string = "upload request"
    string = string.encode('utf-8')
    stringL = len(string).to_bytes(4, "big")
    sock.sendall(stringL)
    sock.sendall(string)
    file_path = str(input("write the file path you want to upload\n"))
    if not os.path.exists(file_path):
        print("file doesnt exist, please check again")
        return
    with open(file_path, "rb") as file:
        full_file = file.read()
        file_size = len(full_file)
        first_4_bytes_file = file_size.to_bytes(4, "big")
        file_name = os.path.basename(file_path)
        
        
        
    file_name = file_name.encode()
    file_name_size = len(file_name)
    first_4_bytes_filename = file_name_size.to_bytes(4)
    #send first 4 bytes for the file name
    sock.sendall(first_4_bytes_filename)
    #send the file name
    sock.sendall(file_name)
    #send first 4 bytees of the file size 
    sock.sendall(first_4_bytes_file)
    #send the entire file 
    sock.sendall(full_file)


#function for downloading a file
def recieving_file(sock, folder, name):
    file_name = name
    file_size_4_first_bytes = int.from_bytes(recv_exact(sock, 4), "big")
    full_file = recv_exact(sock, file_size_4_first_bytes)
    file_path = os.path.join(folder, name)
    with open(file_path, 'wb') as file:
        file.write(full_file)
    print(f"file{file_name} recieved and stored in - {folder}")






def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_HOST = "127.0.0.1"
    s_PORT = 12345

    client_socket.connect((s_HOST, s_PORT))
    print(f"connected to a server - {s_HOST}: {s_PORT}")
    while True:
        messege = str(input("would you like to upload a file or download one? (type - 'exit' if you want to exit) \n"))
        if (messege.lower().strip() == "exit"):
            break
        elif (messege.lower().strip() == "upload"):
            upload_file(client_socket)
        elif messege.lower().strip() == "download":
            string = "download request"
            string = string.encode('utf-8')
            stringL = len(string).to_bytes(4, "big")

            client_socket.sendall(stringL)
            client_socket.sendall(string)

            file_name = str(input("whats the name of the file you want to download?\n"))
            file_name = file_name.encode('utf-8')
            file_name_size_first_4_bytes = len(file_name).to_bytes(4, "big")

            client_socket.sendall(file_name_size_first_4_bytes)
            client_socket.sendall(file_name)

            has_file_size = int.from_bytes(recv_exact(client_socket, 4), "big")
            has_file = recv_exact(client_socket, has_file_size).decode('utf')
            if has_file.lower().strip() == "file not found":
                print("file was not found in the server's storage, please try another name")
                continue
            else:
                where_to_save = str(input("where do you want to save the file?\nwrite the path..."))
                while not os.path.exists(where_to_save):
                    print("not found, check again")
                recive_file_for_download(client_socket, where_to_save, file_name)

        
        data = client_socket.recv(1024)

        returned_messege = data.decode('utf-8')
        print(f"server's response: {returned_messege}")

    print("closing connection.")
    client_socket.close()

start_client()