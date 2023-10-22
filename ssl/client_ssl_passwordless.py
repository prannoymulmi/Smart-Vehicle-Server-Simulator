import socket
import ssl

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def start_client():
    """
    SSL source code <a href=https://docs.python.domainunion.de/3/library/ssl.html />
    """
    HOST = 'localhost'
    PORT = 65434

    # Create a context for the secure connection
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations('server_cert.pem')  # Load the server's certificate to verify it

    # Load the client's private key. Keep this secure!
    with open("client_private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)


        # Wrap the socket in the SSL context
        with socket.create_connection((HOST, PORT)) as client_socket:
            with context.wrap_socket(client_socket, server_hostname=HOST) as secure_socket:
                # Receive the challenge from the server
                challenge = secure_socket.recv(1024)

                # Sign the challenge
                signature = private_key.sign(
                    challenge,
                    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                    hashes.SHA256()
                )

                # Send the signature back to the server
                secure_socket.send(signature)

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