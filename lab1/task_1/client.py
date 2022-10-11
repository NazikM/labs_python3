import socket
import datetime


HOST = 'localhost'
PORT = 5000


def client():
    s = socket.socket()

    s.connect((HOST, PORT))

    while True:
        msg_to_send = input(":: ")
        print(f"Current time: {datetime.datetime.now().strftime('%H:%M:%S')}")
        s.send(msg_to_send.encode(encoding='utf-8'))
        print(s.recv(1024).decode())
        print(f"After msg time: {datetime.datetime.now().strftime('%H:%M:%S')}")

        if msg_to_send == "stop":
            break
    s.close()


if __name__ == '__main__':
    client()
