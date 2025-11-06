import socket      # Importa il modulo socket per usare la comunicazione di rete
import time        # Importa il modulo time per gestire ritardi e pause

# Configurazione del client
SERVER_HOST = "127.0.0.1"   # Indirizzo IP del server (localhost)
SERVER_PORT = 5005          # Porta su cui il server è in ascolto

# Creazione del socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Crea un socket UDP (senza connessione)
client_socket.settimeout(2.5)  # Imposta un timeout di 2.5 secondi per la ricezione

# Ciclo principale per inviare 10 messaggi
for i in range(1, 11):
    messaggio = f"Messaggio {i}"   # Crea il messaggio con numero progressivo
    inviato = False                # Flag che diventa True quando si riceve l’ACK corretto

    while not inviato:             # Continua a tentare finché non arriva l’ACK corretto
        print(f"\n➡️ Invio: {messaggio}")  # Mostra quale messaggio sta per essere inviato
        client_socket.sendto(messaggio.encode(), (SERVER_HOST, SERVER_PORT))  # Invia il messaggio codificato al server

        try:
            data, _ = client_socket.recvfrom(1024)  # Attende una risposta (ACK) dal server, massimo 1024 byte
            ack = data.decode()                     # Decodifica i byte ricevuti in stringa leggibile

            if ack == f"ACK:{messaggio}":           # Controlla se l’ACK ricevuto corrisponde al messaggio inviato
                print(f"✅ Ricevuto {ack}")         # ACK corretto → messaggio confermato
                inviato = True                      # Esce dal ciclo interno e passa al messaggio successivo
            else:
                print(f"⚠️ ACK non valido: {ack}")  # ACK non corrisponde → probabilmente un ACK ritardato o errato

        except socket.timeout:
            print("⏱ Timeout: nessuna risposta, ritento...")  # Nessun ACK ricevuto entro il timeout, ritenta l’invio

        time.sleep(0.5)  # Attende mezzo secondo per evitare di saturare la rete o il server

print("\nClient terminato.")  # Tutti i messaggi inviati correttamente
client_socket.close()         # Chiude il socket UDP
