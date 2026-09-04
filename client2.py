import socket
import pathlib
import os

#function for uploading a file
def upload_file(sock, path):
    file = pathlib.Path(path)

    #sending file name for the server to save 
    file_name = file.name.encode('utf-8')
    sock.sendall(file_name)
    #opening file
    with open(file, "rb") as f:
        #deviding file to chunks and sending chunk by chunk
        chunk = f.read(1024)
        while chunk:
            print("sending...")
            sock.send(chunk)
            chunk = f.read(1024)
    print(f"file {file_name} uploaded succesfully")
#function to recieve file
def download_file(sock, folderpath, name):
    #creating a new path for the file
    name = name.decode('utf-8')
    new_path = os.path.join(folderpath, name)
    with open(new_path, "wb") as f:
        #recieving chunks of the file from server
        chunk = sock.recv(1024)
        while chunk:
            print("recieving...")
            #writing the chunks in the new path
            f.write(chunk)
            chunk = sock.recv(1024)
    print(f"file {name} download completed succesfully")
    


def start_client():
    tempfolder = '/Users/omerbanvolgyi/Documents/Temp'
    adress = ("127.0.0.1", 2345)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(adress)
    messege = str(input("type 'upload' for uploading a file\ntype 'download' for downloading a file:"))
    if 'upload' in messege.lower():
        #sending upload request to the server
        flag = "upload".encode('utf-8')
        client_socket.sendall(flag)
        filepath = input("enter file path:")
        upload_file(client_socket, filepath)

    elif 'download' in messege.lower():
        #sending a download request to the server
        flag = "download".encode('utf-8')
        client_socket.sendall(flag)
        all_files = client_socket.recv(1024).decode('utf-8')
        q = str(input(f"whats the name of the file you want to download:\nfiles in server: {all_files}\n"))
        file_name = q.encode('utf-8')
        client_socket.sendall(file_name)

        download_file(client_socket, tempfolder, file_name)

#i use the upload and the download functions in the gui file... so i only want them to run threre
if __name__ == "__main__":   
    start_client()











    