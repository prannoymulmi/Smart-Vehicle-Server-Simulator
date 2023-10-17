import socket

SECRET = 'my_secret_password'


def start_client():
    HOST = '127.0.0.1'
    PORT = 65431

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Send the secret for authentication
        s.sendall(SECRET.encode())

        response = s.recv(1024).decode()
        print(response)


if __name__ == "__main__":
    start_client()
