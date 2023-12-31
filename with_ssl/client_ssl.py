import os
import socket
import ssl

import psutil

"""
This is just for testing purposes, such passwords will be stored in a secure device such as a HSM
Source <a href=https://www.entrust.com/resources/hsm/faq/what-are-hardware-security-modules />
"""
SECRET = 'easypass'


def start_client():
    """
    SSL source code <a href=https://docs.python.domainunion.de/3/library/ssl.html />
    """
    HOST = 'localhost'
    PORT = 65433

    # Create a context for the secure connection
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(os.path.basename('/server_cert.pem'))  # Load the server's certificate to verify it

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
    process = psutil.Process(os.getpid())
    start_client()
    cpu_usage = process.cpu_percent(interval=0.001)
    memory_info = process.memory_info()
    print(f"CPU: {cpu_usage}%, Memory: {memory_info.rss / (1024 * 1024)} MB")