import socket
import threading


HOST = 'localhost'
PORT = 5000

s = socket.socket()

s.connect((HOST, PORT))


def listener():
    while True:
        print(s.recv(1024).decode())


def client():
    while not (nickname := input("Enter nickname for server: ")):
        print("Not correct nickname. Try one more time!")

    s.send(nickname.encode(encoding='utf-8'))

    threading.Thread(target=listener, daemon=True).start()
    while True:
        msg_to_send = input()
        s.send(msg_to_send.encode(encoding='utf-8'))

        if msg_to_send == "stop":
            break
    s.close()


if __name__ == '__main__':
    try:
        client()
    except socket.error:
        print("Client unexpectedly closed connection. Try again later!")
    finally:
        s.close()
