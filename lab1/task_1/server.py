import socket
import datetime
from time import sleep
import threading


HOST = 'localhost'
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(10)


def client_handler(conn):
    while True:
        data = conn.recv(1024).decode(encoding='utf-8')
        if data == "stop":
            return conn.close()
        print(data, datetime.datetime.now().strftime("%H:%M:%S"))
        sleep(5)
        data_sent = conn.send(data.encode(encoding='utf-8'))
        if data_sent == len(data):
            print("Successfully sent")
        else:
            print("Not all data was sent")


def server():
    print(f"Start listening on {HOST}:{PORT}")
    while True:
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        threading.Thread(target=client_handler, args=(conn,), daemon=True).start()


if __name__ == '__main__':
    server()
