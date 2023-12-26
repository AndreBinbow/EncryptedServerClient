import socket
import threading
import sys
import base64



def string_to_binary(input_string):
    binary_representation = ''.join(format(ord(char), '08b') for char in input_string)
    return binary_representation

def xor(message, xor_key):
    xorbin = string_to_binary(xor_key)
    messagebin = string_to_binary(message)
   
    # Repeat the message or key to match the length of the longer one
    max_len = max(len(messagebin), len(xorbin))
    messagebin = (messagebin * ((max_len // len(messagebin)) + 1))[:max_len]
    xorbin = (xorbin * ((max_len // len(xorbin)) + 1))[:max_len]
   
    result = ''.join('1' if a != b else '0' for a, b in zip(messagebin, xorbin))
    return result

def binary_to_base64(binary_string):
    return base64.b64encode(int(binary_string, 2).to_bytes((len(binary_string) + 7) // 8, byteorder='big')).decode('utf-8')
def binary_to_string(binary_string):
    # Make sure the binary string is a multiple of 8
    binary_string = binary_string.zfill((len(binary_string) + 7) // 8 * 8)

    # Split the binary string into 8-bit chunks
    chunks = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]

    # Convert each 8-bit chunk to an integer and then to a character
    characters = [chr(int(chunk, 2)) for chunk in chunks]

    # Join the characters to form the resulting string
    resulting_string = ''.join(characters)

    return resulting_string

def base64_to_binary(base64_data):
    # Decode Base64 to bytes
    byte_data = base64.b64decode(base64_data)

    # Convert bytes to binary string
    binary_data = ''.join(format(byte, '08b') for byte in byte_data)

    return binary_data

def xor_decrypt(ciphertext, xor_key):
    xorbin = string_to_binary(xor_key)
    max_len = len(ciphertext)
    xorbin = (xorbin * ((max_len // len(xorbin)) + 1))[:max_len]

    result = ''.join('1' if a != b else '0' for a, b in zip(ciphertext, xorbin))
    return result

def receivemessages(socket):
    while True:
        data = socket.recv(1024).decode('utf-8')
        if not data:
            print("breaking")
            break
        parts = data.split(":")
        if len(parts) == 2:
            sender, encrypted_message = parts
            decrypted_binary = xor_decrypt(base64_to_binary(encrypted_message), password)
            decrypted_message = binary_to_string(decrypted_binary)
            #print("server message:", encrypted_message)
            #print("xordecrypt:", decrypted_binary)
            print("Decrypted message: ", decrypted_message)

def sendmessages(socket):
    while True:
        message = input("")
           
        if message == 'exit':
            socket.send(message.encode('utf-8'))
            socket.close()
            break  
        elif not message:
           continue
           
        else:
            try:
                encrypted_messagesend = xor(message, password).strip()
                base64message = binary_to_base64(encrypted_messagesend)
                strippedbase64 = base64message.strip()
                #print("base64send:",base64message)
                socket.send(base64message.encode('utf-8'))
                decrypted_binary = xor_decrypt(base64_to_binary(base64message), password)
                #print("xordecrypt: ", decrypted_binary)
                #print("localdecrypt:",binary_to_string(decrypted_binary))
                #print("mydecryption: "+binary_to_string(xor_decrypt(encrypted_messagesend, password)))
            except Exception as e:
                print(e)


   
           
           

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    address = input("Host ip/Port number/passkey (write as xx.xx.xx.xx, xxxx,xxxxxx): ").split(",")
    host = address[0]
    port = int(address[1])
    global password
    password = address[2]
    try:
        client.connect((host, port))
           
        receivethread = threading.Thread(target = receivemessages, args = (client,))
        sendthread = threading.Thread(target=sendmessages, args=(client,))

        receivethread.start()
        sendthread.start()
    except Exception as e:
        print(str(e))
        client.close()
            #sys.exit();
       
if __name__ == '__main__':
    main()
