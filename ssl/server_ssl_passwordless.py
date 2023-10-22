import os
import socket
import ssl

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def start_server():
    while True:
        """
            SSL source code <a href=https://docs.python.domainunion.de/3/library/ssl.html />
        """
        # Load the client's public key. In a real scenario, you'd securely manage and store these.
        with open("client_public_key.pem", "rb") as key_file:
            client_public_key = serialization.load_pem_public_key(key_file.read())
            HOST = 'localhost'
            PORT = 65434

            # Create a socket and bind it
            bind_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            """
                TCP has a TIME_WAIT sate by the os for a period of time. See <a href=https://en.wikipedia.org/wiki/Transmission_Control_Protocol#Protocol_operation />
                To over come this SO_REUSEADDR is used to bind immediately to the port again 
            """
            bind_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            bind_socket.bind((HOST, PORT))
            bind_socket.listen(5)
            print("Server listening...")

            # Loading certificate and running TLS server as a server
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile='server_cert.pem', keyfile='server_key.pem')

            conn, addr = context.wrap_socket(bind_socket, server_side=True).accept()
            print("Connected by", addr)

            """
                Send a unique challenge to the client. This uses a more secure random entropy sources to make the value more unpredictable
                Source <a href=https://docs.python.org/3/library/os.html#os.urandom
            """
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