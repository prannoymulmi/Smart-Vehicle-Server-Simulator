import socket
import ssl

password = "WORNG_PASS"


"""
Simple simulation of a possible credential stuffing attacks for regular passwords
Source <a href=https://owasp.org/www-community/attacks/Credential_stuffing />
"""
def wrong_password_test():
    print("Starting wrong password test")
    """
    SSL source code <a href=https://docs.python.domainunion.de/3/library/ssl.html />
    """
    HOST = 'localhost'
    PORT = 65433

    # Create a context for the secure connection
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations('../server_cert.pem')  # Load the server's certificate to verify it

    # Wrap the socket in the SSL context
    with socket.create_connection((HOST, PORT)) as client_socket:
        with context.wrap_socket(client_socket, server_hostname=HOST) as secure_socket:
            secure_socket.send(password.encode())

            # Receive auth response
            response = secure_socket.recv(1024).decode()
            if response == "AUTH_SUCCESS":
                print("Authentication Success")
                secure_socket.send("GET_DATA".encode())
                data = secure_socket.recv(1024).decode()
                print(f"Received data: {data}")
            else:
                print(f"Received data: {response}")
        secure_socket.close()
    client_socket.close()

if __name__ == "__main__":
    wrong_password_test()
