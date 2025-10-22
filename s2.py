import socket           # modulo per la comunicazione via rete (sockets)
import random           # per simulare la perdita casuale dei pacchetti
import time             # per simulare ritardi

# Impostazioni del server
HOST = '127.0.0.1'      # indirizzo localhost (solo connessioni locali)
PORT = 12345            # porta su cui il server ascolta
DROP_PROB = 0.3         # probabilità di perdere (ignorare) un messaggio
BUFFER = 4096           # dimensione massima del messaggio ricevuto (in byte)

# Creazione del socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))  # il server si mette in ascolto su HOST e PORT

print(f"[SERVER] in ascolto su {HOST}:{PORT} (drop prob {DROP_PROB*100:.0f}%)")

# Set per salvare i messaggi già ricevuti (serve per riconoscere i duplicati)
received_messages = set()

try:
    while True:
        # Riceve un messaggio UDP (bloccante finché non arriva qualcosa)
        data, addr = sock.recvfrom(BUFFER)
        text = data.decode(errors='ignore')  # decodifica il messaggio ricevuto

        # Controllo se il messaggio è già stato ricevuto in precedenza
        if text in received_messages:
            print(f"[DUPLICATO] Messaggio già ricevuto: {text!r} da {addr}")
            continue  # non invia ACK di nuovo

        # Genera un numero casuale per decidere se droppare il messaggio
        r = random.random()
        print(f"[DEBUG] random={r:.3f}")

        # Se il numero è minore della DROP_PROB, il messaggio viene ignorato
        if r < DROP_PROB:
            print(f"[DROPPED] da {addr} messaggio: {text!r} (r={r:.3f})")
            continue  # non invia ACK

        # Introduce un ritardo casuale prima di rispondere (0-5 secondi)
        delay = random.uniform(0, 5)
        print(f"[DELAY] ritardo ACK {delay:.2f}s per messaggio {text!r}")
        time.sleep(delay)  # simula la latenza di rete

        # Il messaggio è valido e non è duplicato: lo elabora
        print(f"[RECEIVED] da {addr} messaggio: {text!r} (r={r:.3f})")
        reply = f"ACK: {text}"              # crea la risposta (ACK)
        sock.sendto(reply.encode(), addr)   # invia l'ACK al mittente

        received_messages.add(text)         # salva il messaggio come "già ricevuto"

except KeyboardInterrupt:
    # Permette di interrompere il server con CTRL+C
    print("\n[SERVER] terminato dall'utente")

finally:
    # Chiude il socket alla fine (libera la porta)
    sock.close()
