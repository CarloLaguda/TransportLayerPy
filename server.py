import socket
import random
import time

# Configurazione del server
HOST = "127.0.0.1"
PORT = 5005

# Creazione del socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

# Insieme per tracciare i messaggi già ricevuti
messaggi_ricevuti = set()

print(f"Server UDP in ascolto su {HOST}:{PORT}...")

while True:
    data, addr = server_socket.recvfrom(1024)
    messaggio = data.decode()

    # Simulazione perdita pacchetto (30%)
    if random.random() < 0.3:
        print(f"[SCARTATO] Messaggio da {addr}: {messaggio}")
        continue

    # Stampa solo se è la prima volta che riceviamo quel messaggio
    if messaggio not in messaggi_ricevuti:
        print(f"[RICEVUTO] Messaggio da {addr}: {messaggio}")
        messaggi_ricevuti.add(messaggio)
    else:
        print(f"[DUPLICATO] {messaggio} da {addr} (ACK comunque inviato)")

    # Ritardo casuale tra 0 e 5 secondi
    delay = random.uniform(0, 5)
    print(f"⏳ Attendo {delay:.2f} secondi prima di inviare ACK...")
    time.sleep(delay)

    # Invio ACK
    ack = f"ACK:{messaggio}"
    server_socket.sendto(ack.encode(), addr)
    print(f"[INVIATO] {ack} a {addr}")