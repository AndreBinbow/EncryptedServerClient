import socket
import signal
import sys
import threading



clientlist = []
iptonickname = {}
#clienttoid = {}
clientlist_lock = threading.Lock()

def sendmessages(client, clienttoid, clientlist_lock):
    exiting = False
    client_id = f"{client.getpeername()[0]}-{id(client)}"
    with clientlist_lock:
        clienttoid[client.getpeername()[0]] = client_id
    while not exiting:
        try:
            if not exiting:
                data = client.recv(1024).decode('utf-8')
            if not data:
                break

            sender_ip = client.getpeername()[0]
            username = sender_ip
           
            if data.strip().startswith("/nick"):
                iptonickname[sender_ip] = data.split(" ")[1]
                print(data.split(" ")[1])
           
           
            if sender_ip in iptonickname:
                username = iptonickname[sender_ip]
               
            ipmessage = f"{client_id}: {data}"
            print(f"dictionary: {clienttoid}")
            with clientlist_lock:
                clients_copy = list(clientlist)
                try:
                    print(ipmessage)
                    for c in clients_copy:
                        c.send(ipmessage.encode('utf-8'))
                        if data == 'exit':
                            print(f"Client {c.getpeername()[0]} disconnected gracefully.")
                            clientlist.remove(c)
                            c.close()
                            exiting = True
                except ConnectionAbortedError:
                    print(f"{c.getpeername()[0]} disconnected uncleanly")
                    clientlist.remove(c)
                    c.close()
                    exiting = True
                    break
                except ConnectionResetError:
                    print(f"Client {c.getpeername()[0]} forcibly closed the connection.")
                    clientlist.remove(c)
                    c.close()
                    exiting = True
                    break
                except OSError as e:
                    if "Transport endpoint is not connected" in str(e):
                        print(f"Client {sender_ip} is not connected. Closing the connection.")
                        clientlist.remove(c)
                        c.close()
                        break
                    else:
                        print(f"Error trying to send to {sender_ip}: {str(e)}")
        except ConnectionAbortedError:
            print(f"Client {client.getpeername()[0]} disconnected uncleanly")
            with clientlist_lock:
                clientlist.remove(client)
            client.close()
            exiting = True
        except ConnectionResetError:
            print(f"Client {client.getpeername()[0]} forcibly closed the connection.")
            with clientlist_lock:
                clientlist.remove(client)
            client.close()
            exiting = True
        except Exception as e:
            print(f"Error trying to send to {client} {str(e)}")
            with clientlist_lock:
                clientlist.remove(client)
            client.close()
            exiting = True


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    host = '0.0.0.0'
    port = 5557
    server.bind((host, port))
    server.listen(5)


    while True:
        try:
            client, addr = server.accept()
            print(f"{addr} connected")
            with clientlist_lock:
                clients_copy = list(clientlist)
            clienttoid = {}
            clientlist.append(client)
            client_handler = threading.Thread(target = sendmessages, args=(client, clienttoid, clientlist_lock))
            client_handler.start()
        except Exception as e:
            print(str(e))
            for client in clientlist:
                client.close()
                sys.exit()

if __name__ == '__main__':
    main()
