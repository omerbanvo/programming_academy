import socket 
from pathlib import Path
import os
#function for recieving a file
def recieve_file(sock, path):
    file_name = sock.recv(1024).decode('utf-8')
    full_path = os.path.join(path, file_name)
    with open(full_path, "wb") as f:
        chunk = sock.recv(1024)
        while chunk:
            print("recieving....")
            f.write(chunk)
            chunk = sock.recv(1024)
        print(f"{file_name} was revieved succesfully")

#function for sending file to client
def send_file(sock, folderpath, name):
    full_path = os.path.join(folderpath, name)
    with open(full_path, "rb") as f:
        chunk = f.read(1024)
        while chunk:
            print("sending...")
            sock.send(chunk)
            chunk = f.read(1024)
        print(f"{name} was sent succesfully")


#function thats creating a list of all the files that are in the server
def all_file_names(folder):
    lst = []
    for file in os.listdir(folder):
        full_path = os.path.join(folder, file)
        if os.path.isdir(full_path):
            lst.extend(all_file_names(full_path))   # recurse into subfolder, keep results
        else:
            if not file[0]=='.':
                lst.append(file)                        # it's a file, add its name
    return lst




#server socket
def start_server():
    HOST = "127.0.0.1"
    PORT = 2345
    folder = '/Users/omerbanvolgyi/Documents/programming_academy/UPLOAD_FILES_TO_SERVER'
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    print("waiting for connections...\n")
    server_socket.listen(5)
    print(f"listening for connections on {HOST}:{PORT}\n")
    
    client_socket, client_adress = server_socket.accept()
    print(f"connection made with {client_adress}")

    
        
    flag = client_socket.recv(1024)
    client_flag = flag.decode("utf-8")
    if(client_flag == 'upload'):
        recieve_file(client_socket, folder)
    elif client_flag == 'download':
        all_files = all_file_names(folder)
        allfiles = ",".join(all_files).encode('utf-8')
        client_socket.sendall(allfiles)
        selected_file = client_socket.recv(1024).decode('utf-8')
        send_file(client_socket, folder, selected_file)
    
#start the server
start_server() 