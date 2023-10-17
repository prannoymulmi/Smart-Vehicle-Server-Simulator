import socket


def capture_biometric_data():
    # Simulate capturing biometric data
    print("Please place your finger on the scanner...")
    return "fingerprint_signature_123"  # In reality, this would be some unique data from the user


def start_client():
    HOST = '127.0.0.1'
    PORT = 65432

    biometric_signature = capture_biometric_data()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(biometric_signature.encode())

        response = s.recv(1024).decode()
        print(response)


if __name__ == "__main__":
    start_client()
