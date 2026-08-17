import socket

def run_server():
    HOST = "127.0.0.1"
    PORT = 12345
    #create a socket - server
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    socket_server.bind((HOST, PORT))
    print("waiting for connections...")
    socket_server.listen()
    print(f"server is listenning on {HOST}:{PORT}")
    
    while True:
        user_socket, user_address = socket_server.accept()
        print(f"connection made with {user_address}: {user_socket}")
        while True:
            data = user_socket.recv(1024)
            if not data:
                break

            messege = data.decode('utf-8')

            print(f"messege recieved from {user_address}: '{messege}'")
            string = "messege recieved"
            return_messege = string.encode('utf-8')
            user_socket.send(return_messege)


run_server()