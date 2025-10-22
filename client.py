import socket
import time

# Configurazione del client
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5005

# Creazione del socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(2.5)  # timeout di 2.5 secondi

ack_atteso = 1  # iniziamo da Messaggio 1

while ack_atteso <= 10:
    messaggio = f"Messaggio {ack_atteso}"
    inviato = False

    while not inviato:
        print(f"\n➡️ Invio: {messaggio}")
        client_socket.sendto(messaggio.encode(), (SERVER_HOST, SERVER_PORT))

        try:
            data, _ = client_socket.recvfrom(1024)
            ack = data.decode()

            if ack == f"ACK:Messaggio {ack_atteso}":
                print(f"✅ Ricevuto {ack}")
                inviato = True
                ack_atteso += 1  # passa al prossimo messaggio
            else:
                print(f"ℹ️ ACK irrilevante ricevuto (atteso: Messaggio {ack_atteso}): {ack}")
                # NON considerare questo un errore: è solo un ACK vecchio, lo scartiamo silenziosamente

        except socket.timeout:
            print("⏱ Timeout: nessuna risposta, ritento...")

        time.sleep(0.5)

print("\nClient terminato.")
client_socket.close()
