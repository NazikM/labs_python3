import socket
import threading

HOST = 'localhost'
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

clients = {}


def broadcast(msg, user=None, for_all=False):
    for client_nickname, client_conn in clients.items():
        if not for_all and user == client_nickname:
            continue
        client_conn.send(msg.encode('utf-8'))


def client_handler(conn):
    nickname = ''
    try:
        nickname = conn.recv(1024).decode(encoding='utf-8')

        if not nickname:
            return conn.close()

        clients.update({
            nickname: conn
        })
        print(f"Client with nickname {nickname} joined!")
        broadcast(f"Server: {nickname} joined the chat.", for_all=True)
        while True:
            data = conn.recv(1024).decode(encoding='utf-8')
            if data:
                if data == "stop":
                    broadcast(f"Server: {nickname} left the chat.")
                    return conn.close()

                broadcast(f"{nickname}: {data}", user=nickname)
    except socket.error:
        clients.pop(nickname, None)
    finally:
        conn.close()


def server():
    print(f"Start listening on {HOST}:{PORT}")
    while True:
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        threading.Thread(target=client_handler, args=(conn,), daemon=True).start()


if __name__ == '__main__':
    server()
