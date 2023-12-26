# Python Server + Client scripts for hosting a TCP chat room using flimsy "encryption"

#### Server:
The machine hosting the server (running the Server.py file) requires an open port, which can be specified in the code
TCP packets are receieved and sent by the server using utf-8 encoding.
The server requires python 3+ to run 
The server is able to send anything that can be encoded in utf-8

#### Client:
To connect to a server, running the python script will ask for an input for the host (IP address trying to connect to), port (port of machine you are trying to connect to), and a secret (the secret key used to obfuscate messages)

The obfuscation is done using an XOR function, which takes the secret string provided, and turns that and your message into a binary string. They are both brought to the same length by repeated material to make up the difference, so sending short messages may cause slightly incorrect decoding based on the length of the secret chosen. This XOR'd binary is converted to base 64 for less characters to transmit, then is turned into utf-8 and sent to the server. 

When a client receieves a message from the server, if the same secret key is used when connecting, the message will undergo the same XOR function, and will turn out the same message again as XORing an XOR will give you the original result. 