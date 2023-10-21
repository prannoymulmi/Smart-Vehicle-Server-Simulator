import socket
import ssl

SECRET = 'my_secret_password'


def start_client():
    HOST = 'localhost'
    PORT = 65433

    # Create a context for the secure connection
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations('server_cert.pem')  # Load the server's certificate to verify it

    # Wrap the socket in the SSL context
    with socket.create_connection((HOST, PORT)) as client_socket:
        with context.wrap_socket(client_socket, server_hostname=HOST) as secure_socket:
            secure_socket.send(SECRET.encode())
            # Receive auth response
            response = secure_socket.recv(1024).decode()
            if response == "AUTH_SUCCESS":
                secure_socket.send("GET_DATA".encode())
                data = secure_socket.recv(1024).decode()
                print(f"Received data: {data}")
            else:
                print(f"Received data: {response}")
        secure_socket.close()
    client_socket.close()

if __name__ == "__main__":
    start_client()