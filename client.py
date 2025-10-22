import socket
import time

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5005

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(2.5)  # timeout di 2.5 secondi

NUM_MSG = 10

for i in range(1, NUM_MSG + 1):
    messaggio = f"Messaggio {i}"
    print(f"\n➡️ Invio: {messaggio}")
    client_socket.sendto(messaggio.encode(), (SERVER_HOST, SERVER_PORT))

    try:
        data, _ = client_socket.recvfrom(1024)
        ack = data.decode()
        print(f"📩 Ricevuto {ack}")  # stampa sempre l'ACK ricevuto

        if ack == f"ACK:{messaggio}":
            print(f"✅ Conferma valida per {messaggio}")
        else:
            print(f"⚠️ ACK non corrispondente al messaggio corrente")
    except socket.timeout:
        print("⏱ Timeout: nessuna risposta dal server")

    time.sleep(0.5)

print("\nClient terminato.")
client_socket.close()