import socket
import ssl

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from argon2.profiles import RFC_9106_HIGH_MEMORY, RFC_9106_LOW_MEMORY

SECRET = 'my_secret_password'  # Both the client and server should have this

# hashes the password into argon2id with random salt
# Using the first recommendation per RFC 9106 with High memory.
HASHED_SECRET = '$argon2id$v=19$m=2097152,t=1,p=4$vT7UexZFsNYigbn2flmJRg$yIOPV3spwnNUIvfFb4B7EMSDh31E3u2C5DOc7Kplljs'


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
    if check_if_password_is_correct(data, HASHED_SECRET):
        conn.send("AUTH_SUCCESS".encode())
        # Now you can handle other requests
        data = conn.recv(1024).decode()
        if data == "GET_DATA":
            conn.sendall("Here's your data!".encode())
        conn.close()
    else:
        conn.sendall(b'Authentication failed')
        conn.close()

def check_if_password_is_correct(input_pass, hashed_pass) -> bool:
    ph = PasswordHasher().from_parameters(RFC_9106_HIGH_MEMORY)
    try:
        return ph.verify(hashed_pass, input_pass)
    except VerifyMismatchError:
        return False


if __name__ == "__main__":
    start_server()