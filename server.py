import socket
import random
import time

HOST = "127.0.0.1"
PORT = 5005

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"Server UDP con perdita e ritardo ACK in ascolto su {HOST}:{PORT}...")

while True:
    data, addr = server_socket.recvfrom(1024)
    messaggio = data.decode()

    # Simulazione perdita pacchetto (30%)
    if random.random() < 0.3:
        print(f"[SCARTATO] {messaggio} da {addr}")
        continue

    print(f"[RICEVUTO] {messaggio} da {addr}")

    # Ritardo casuale prima di inviare l'ACK
    delay = random.uniform(0, 5)
    print(f"⏳ Ritardo ACK: {delay:.2f}s")
    time.sleep(delay)

    ack = f"ACK:{messaggio}"
    server_socket.sendto(ack.encode(), addr)
    print(f"[INVIATO] {ack} a {addr}")
