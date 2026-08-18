import socket
import os
from pathlib import Path
#function that revieves the exact amount of bytes as promiesed
def recv_exact(sock, num_bytes):
    buffer = b""
    while len(buffer)<num_bytes:
        chunk = sock.recv(num_bytes-len(buffer))
        if not chunk:
            #the connection stops
            raise ConnectionError("socket closed before expected data was received")
        buffer+=chunk
    return buffer




#function for recieving files
def recieving_file(sock, Ufolder):
    #recieving the file name length
    file_name_length = int.from_bytes(recv_exact(sock, 4), "big")
    if not file_name_length:
        return
    #recieving file name
    file_name = recv_exact(sock, file_name_length).decode('utf-8')
    #recieving full file size
    file_size = int.from_bytes(recv_exact(sock, 4), "big")
    if not file_size:
        return
    #recieving full file
    full_file = recv_exact(sock, file_size)
    full_path = os.path.join(Ufolder, file_name )
    #uploading file the the folder - upload_files_to_server
    with open(full_path, "wb") as file:
        file.write(full_file)
    print(f"file{file_name} recieved and stored in - {Ufolder}")


#function that checks if a folder has a file with a file name
def check_if_has_file(file_name, folder_path):
    folder = Path(folder_path)
    for item in folder.iterdir():
        if item.is_file():
            if item.name == file_name:
                return True
            
        elif item.is_dir():
            if check_if_has_file(file_name, item):
                return True

    return False



#function that returns a file path from a name and a foler, if after check already exists.
def return_file_path(name, folder_path):
    folder = Path(folder_path)
    for item in folder.iterdir():
        if item.is_file():
            if item.name == name:
                return Path(item)
        elif item.is_dir():
            if return_file_path(name, item):
                return Path(item)
        else:
            raise KeyError('file not found')


#function that sends a file for the user to download:
def send_file(sock, file_path):
    with open(file_path, "rb") as file:
        full_file = file.read()
        file_size_4_first_bytes = len(full_file).to_bytes(4, "big")
        sock.sendall(file_size_4_first_bytes)
        sock.sendall(full_file)


def run_server():
    HOST = "127.0.0.1"
    PORT = 12345
    #create a socket - server
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    UPLOAD_FOLDER = '/Users/omerbanvolgyi/Documents/programming_academy/UPLOAD_FILES_TO_SERVER'
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    socket_server.bind((HOST, PORT))
    print("waiting for connections...")
    socket_server.listen()
    print(f"server is listenning on {HOST}:{PORT}")
    
    while True:
        user_socket, user_address = socket_server.accept()
        print(f"connection made with {user_address}: {user_socket}")
        while True:
            flag_length = int.from_bytes(recv_exact(user_socket, 4), "big")
            flag = recv_exact(user_socket, flag_length).decode('utf-8')

            if flag == "upload request":
                recieving_file(user_socket, UPLOAD_FOLDER)
            elif flag == "download request":

                has_file_name_size = int.from_bytes(recv_exact(user_socket, 4), "big")
                has_file_name = recv_exact(user_socket, has_file_name).decode('utf-8')
                has_file = check_if_has_file(has_file_name, UPLOAD_FOLDER)
                if has_file:
                    string = "file found".encode('utf-8')
                    string_size_first_4_bytes = len(string).to_bytes(4, "big")
                    user_socket.sendall(string_size_first_4_bytes)
                    user_socket.sendall(string)
                    file_path = return_file_path(has_file_name, UPLOAD_FOLDER)
                    send_file(user_socket, file_path)



            

            #print(f"file recieved from {user_address}: '{file_name}'")
            #string = f"file: {file_name} recieved"
            #return_messege = string.encode('utf-8')
            #user_socket.send(return_messege)


run_server()