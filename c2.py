import socket          # modulo per la comunicazione di rete
import time            # modulo per gestire i ritardi (sleep)

# Indirizzo e porta del server
SERVER = ('127.0.0.1', 12345)

# Timeout di attesa per l'ACK in secondi
TIMEOUT = 2.5

# Attesa tra i tentativi di ritrasmissione
RETRY_INTERVAL = 2.5

# Numero totale di messaggi da inviare
NUM_MESSAGES = 10

# Creazione del socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Imposta il timeout: se non arriva risposta entro TIMEOUT, solleva eccezione
sock.settimeout(TIMEOUT)

# Variabile per contare gli ACK ricevuti
ack_received = 0

# Set per tenere traccia dei messaggi già inviati
sent_messages = set()

# Set per tenere traccia degli ACK ricevuti (evita doppi)
acked_messages = set()

# Ciclo per inviare i messaggi da 1 a NUM_MESSAGES
for i in range(1, NUM_MESSAGES + 1):
    message = f"Messaggio numero {i}"  # prepara il testo del messaggio
    attempts = 0                       # numero di tentativi per questo messaggio
    acked = False                      # diventa True quando si riceve l'ACK giusto

    # Continua a ritrasmettere finché non riceve un ACK valido
    while not acked:
        attempts += 1  # aumenta il numero di tentativi

        if message not in sent_messages:
            # Prima trasmissione
            print(f"Inviato: {message}")
            sent_messages.add(message)
        else:
            # Ritrasmissione
            print(f"Ritrasmissione tentativo {attempts} per: {message}")

        try:
            # Invia il messaggio al server
            sock.sendto(message.encode(), SERVER)

            # Attende la risposta (ACK)
            data, addr = sock.recvfrom(4096)  # blocca fino a ricezione o timeout
            ack = data.decode()               # decodifica la risposta

            if ack not in acked_messages:
                # Primo ACK per questo messaggio
                print(f"[CLIENT] Ricevuto ACK: {ack}")
                acked_messages.add(ack)
                ack_received += 1

            acked = True  # esce dal ciclo: ACK ricevuto

        except socket.timeout:
            # Se non arriva nulla entro il timeout, si riprova
            print(f"Timeout attesa ACK per messaggio {i} (tentativo {attempts}), ritrasmetto...")
            time.sleep(RETRY_INTERVAL)  # attende prima di ritrasmettere

# Al termine del ciclo, stampa quanti ACK sono stati ricevuti
print(f"\nTotale ACK ricevuti: {ack_received} su {NUM_MESSAGES}")

# Chiude il socket
sock.close()
