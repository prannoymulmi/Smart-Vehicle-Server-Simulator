# Smart-Vehicle-Server-Simulator

Python applications which simulates the communication between a smart car and a cloud server the data-flow-diagram show
the system which this project is trying to simulate.

![alt text](docs/DFD.png)

## Hypothesis

This project delves into the hypothesis
**Is it more secure to use encrypted passwords inside the smart vehicle or use passwordless authentication while
communicating with the server**
and implements it into two applications server and smart-vehicle.

# Mitigations applied

* Use of secure encrypted protocols like SSL to transmit the data between client and the server.
  ### Test for Man-in-the-middle
    * Two test scenarios were applied where the client-server connection was in plain text and the other encrypted with
      its corresponding certificates.
      Wireshark as a tool was used to intercept the data packets during communications.
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
