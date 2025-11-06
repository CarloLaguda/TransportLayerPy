import socket     # Importa il modulo socket per la comunicazione di rete
import random     # Importa il modulo random per simulare perdite e ritardi casuali
import time       # Importa il modulo time per gestire i ritardi

# Configurazione del server
HOST = "127.0.0.1"   # Indirizzo IP locale (localhost)
PORT = 5005          # Porta su cui il server ascolta i messaggi UDP

# Creazione del socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Crea un socket UDP
server_socket.bind((HOST, PORT))  # Associa il socket all’indirizzo e alla porta specificati

print(f"Server UDP (perdita 30% + ritardo 0-5s) in ascolto su {HOST}:{PORT}...")

# Ciclo principale del server: riceve e gestisce messaggi continuamente
while True:
    data, addr = server_socket.recvfrom(1024)  # Riceve un messaggio (fino a 1024 byte) e l’indirizzo del mittente
    messaggio = data.decode()                  # Decodifica i byte ricevuti in stringa leggibile

    # Simulazione di perdita pacchetto con probabilità del 30%
    if random.random() < 0.3:
        print(f"[SCARTATO] Messaggio da {addr}: {messaggio}")  # Simula perdita → non invia ACK
        continue  # Passa al prossimo ciclo, ignorando questo messaggio

    # Se il messaggio non è stato scartato, viene elaborato normalmente
    print(f"[RICEVUTO] Messaggio da {addr}: {messaggio}")

    # Simulazione di ritardo casuale tra 0 e 5 secondi
    delay = random.uniform(0, 5)  # Genera un numero casuale tra 0 e 5
    print(f"⏳ Attendo {delay:.2f} secondi prima di inviare ACK...")
    time.sleep(delay)  # Attende il tempo generato per simulare ritardo di rete

    # Creazione e invio dell'ACK al client
    ack = f"ACK:{messaggio}"                  # Costruisce la risposta ACK con il messaggio ricevuto
    server_socket.sendto(ack.encode(), addr)  # Invia l’ACK al client
    print(f"[INVIATO] {ack} a {addr}")        # Conferma a console l’invio dell’ACK
