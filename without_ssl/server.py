import socket
"""
Unsecured version of client and server communication done in plain text.
"""
SECRET = 'my_secret_password'  # Both the client and server should have this


def start_server():
    HOST = '127.0.0.1'
    PORT = 65431

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server listening...")

        conn, addr = s.accept()
        """
            TCP has a TIME_WAIT sate by the os for a period of time. See <a href=https://en.wikipedia.org/wiki/Transmission_Control_Protocol#Protocol_operation />
            To over come this SO_REUSEADDR is used to bind immediately to the port again 
        """
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        with conn:
            print("Connected by", addr)

            # Authentication
            data = conn.recv(1024).decode()
            if data == SECRET:
                print(data)
                conn.sendall(b'Authentication successful')
                conn.close()
                # Handle authenticated client
            else:
                conn.sendall(b'Authentication failed')
                conn.close()

if __name__ == "__main__":
    start_server()
