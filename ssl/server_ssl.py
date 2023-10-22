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
    """
        SSL source code <a href=https://docs.python.domainunion.de/3/library/ssl.html />
    """
    HOST = 'localhost'
    PORT = 65433

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
    context.load_cert_chain(certfile='ssl/server_cert.pem', keyfile='ssl/server_key.pem')

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