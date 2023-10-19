import socket
import ssl

SECRET = 'my_secret_password'  # Both the client and server should have this


def start_server():
    HOST = 'localhost'
    PORT = 65433

    # Create a socket and bind it
    bind_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bind_socket.bind((HOST, PORT))
    bind_socket.listen(5)
    print("Server listening...")

    # Wrap the socket using SSL
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='server_cert.pem', keyfile='server_key.pem')

    conn, addr = context.wrap_socket(bind_socket, server_side=True).accept()
    print("Connected by", addr)

    data = conn.recv(1024).decode()
    if data == SECRET:
        conn.send("AUTH_SUCCESS".encode())
        # Now you can handle other requests
        data = conn.recv(1024).decode()
        if data == "GET_DATA":
            conn.send("Here's your data!".encode())
        conn.close()
    else:
        conn.sendall(b'Authentication failed')
        conn.close()

    conn.close()


if __name__ == "__main__":
    start_server()