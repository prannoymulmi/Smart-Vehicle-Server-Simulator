# Smart-Vehicle-Server-Simulator

Python applications which simulates the communication between a smart car and a cloud server the data-flow-diagram show
the system which this project is trying to simulate.

![alt text](docs/DFD.png)

## Hypothesis

This project delves into the hypothesis
**Is it more secure to use encrypted passwords inside the smart vehicle or use passwordless authentication while
communicating with the server**
and implements it into two applications server and smart-vehicle.

### Passwordless Authentication Analysis

### Generated private and public keys for passwordless authentication
In order to carry out passwordless authentication a symmetric key-based protocol (public and private key) for a
passwordless authentication. This method of symmetric authentication (passwordless) is straightforward and is resilient to many
known attacks like Man-in-the-Middle, and brute-force attacks (Bruce, N. and Lee, H.J., 2014). 

````bash
## How to generate keys for passwordless authentication Source (OpenSSL Project, 2021)
openssl genpkey -algorithm RSA -out client_private_key.pem
openssl pkey -in client_private_key.pem -pubout -out client_public_key.pem
````

#### Issue for passwordless
However, one of the main challenges for this
type of authentication is the size of the certificates/keys which have a rather complex structure and is resource intensive, which would create
difficulties in processing and verifying them as the IoT devices have very limited resources (Schukat, M. and Cortijo, P., 2015).


# Additional Mitigations applied

* Use of secure encrypted protocols like SSL to transmit the data between client and the server. This is achieved by using the TLS/SSL
wrapper provided by python which uses the TLSv1.3 with OpenSSL v1.1.1 (Python Software Foundation, 2023).
  ### Test for Man-in-the-middle
    * Two test scenarios were applied where the client-server connection was in plain text and the other encrypted with
      its corresponding certificates.
      Wireshark as a tool was used to intercept the data packets during communications and packets were inspected using TCP Stream function (Wireshark (n.d.)).
      Legend :

    * | Host | Port | Description | Protocol | Figure |
      |-----------------------|-------|-------------|----------|--------|
      | localhost (127.0.0.1) | 65431 | Uencrpyted  | TCP | 1 |
      | localhost (127.0.0.1) | 65433 | Encrypted   | TCP | 2 |

     ![alt text](docs/unecrypted_wireshark.png)
      Figure X shows that the TCP stream between the client and server is in clear text and MITM attacks can be easily
      carried out.
  
* 
     ![alt text](docs/encrypted_wireshark.png)
      Figure X shows that the TCP stream between the client and server is in encrypted form and the connection is not in
      clear text strengthening our
      communication against MITM attacks.
* **Note: The certificates generated here are just for testing purposes and are self-signed which can be compromised and should not 
be used to secure devices instead use a validated certificate from a trusted source.**


# Reference
* Bruce, N. and Lee, H.J., 2014, February. Cryptographic computation of private shared key based mutual authentication protocol: Simulation and modeling over wireless networks. In The International Conference on Information Networking 2014 (ICOIN2014) (pp. 578-582). IEEE.
* OpenSSL Project, 2021. OpenSSL Man Pages: Version 3.1. OpenSSL Software Foundation. Available from: https://www.openssl.org/docs/man3.1/man1/ [Accessed 19 October 2023].
* Python Software Foundation, 2023. ssl — TLS/SSL wrapper for socket objects. Available at: https://docs.python.domainunion.de/3/library/ssl.html [Accessed 22 October 2023].
* Schukat, M. and Cortijo, P., 2015, June. Public key infrastructures and digital certificates for the Internet of things. In 2015 26th Irish signals and systems conference (ISSC) (pp. 1-5). IEEE.
* Wireshark (n.d.) 6.5.2. The “Follow TCP Stream” dialog box. Available from: https://www.wireshark.org/docs/wsug_html_chunked/ChAdvFollowStreamSection.html (Accessed: [21 Oct 2023])