import socket
import ssl

SECRET = 'my_secret_password'


def start_client():
    HOST = 'localhost'
    PORT = 65432

    # Create a context for the secure connection
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations('server_cert.pem')  # Load the server's certificate to verify it

    # Wrap the socket in the SSL context
    with socket.create_connection((HOST, PORT)) as client_socket:
        with context.wrap_socket(client_socket, server_hostname=HOST) as secure_socket:
            secure_socket.sendall(SECRET.encode())
            print(secure_socket.recv(1024).decode())


if __name__ == "__main__":
    start_client()