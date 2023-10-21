import os
import socket
import ssl

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding



def start_server():
    # Load the client's public key. In a real scenario, you'd securely manage and store these.
    with open("client_public_key.pem", "rb") as key_file:
        client_public_key = serialization.load_pem_public_key(key_file.read())
        HOST = 'localhost'
        PORT = 65434

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

        # Send a unique challenge to the client.
        challenge = os.urandom(32)
        conn.send(challenge)

        # Get the signature from the client
        signature = conn.recv(1024)

        # Verify the signature
        try:
            client_public_key.verify(
                signature,
                challenge,
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256()
            )
            print("Client authentication succeeded!")
            conn.send(b"AUTH_SUCCESS")
            data = conn.recv(1024).decode()
            if data == "GET_DATA":
                conn.sendall("Here's your data!".encode())
            conn.close()
        except:
            print("Client authentication failed!")
            conn.send(b"AUTH_FAILED")


if __name__ == "__main__":
    start_server()