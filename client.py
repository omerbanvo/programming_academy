import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_HOST = "127.0.0.1"
    s_PORT = 12345

    client_socket.connect((s_HOST, s_PORT))
    print(f"connected to a server - {s_HOST}:{s_PORT}")
    while True:
        messege = str(input("what do you want to send ? (type - 'exit' if you want to exit) \n"))
        if (messege.lower().strip() == "exit"):
            break
        final_messege = messege.encode('utf-8')
        client_socket.sendall(final_messege)

        data = client_socket.recv(1024)

        returned_messege = data.decode('utf-8')
        print(f"server's response: {returned_messege}")

    print("closing connection.")
    client_socket.close()

start_client()