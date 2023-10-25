import socket
import ssl

SECRET = 'my_secret_password'

"""
This test is an experiment with a hypothetical scenario that the Smartcar Client is comprised with  
"""
def connect_without_certificate():
    try:
        """
        SSL source code <a href=https://docs.python.domainunion.de/3/library/ssl.html />
        """
        HOST = 'localhost'
        PORT = 65433

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.send("password".encode())
            # Receive auth response
            response = s.recv(1024).decode()
            if response == "AUTH_SUCCESS":
                s.send("GET_DATA".encode())
                data = s.recv(1024).decode()
                print(f"Received data: {data}")
            else:
                print(f"Received data: {response}")
            s.close()
    except ConnectionResetError:
        print("Connection Not successful")

if __name__ == "__main__":
    connect_without_certificate()
