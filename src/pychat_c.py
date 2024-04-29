#!/bin/env python
import socket as socket
import sys
import threading
import pychat_config as pcf

# Client per la chatroom.
# Luca Casadei - Francesco Pazzaglia - Martin Tomassi
# Utilizzo di indirizzi IPV4 connection-oriented

# Lo script prende come argomenti l'indirizzo del server e il nome
# visualizzato sulla chat.
if len(sys.argv) != 3:
    print("Argomenti non corretti," +
          "per connettersi invocare il comando:" +
          "\npychat_c.py [ind_server] [nome_visualizzato]")
    sys.exit(0)

pychat_server_address = str(sys.argv[1])
name = str(sys.argv[2])

'''
Questa parte gestisce i metodi concorrenti di invio e ricezione dei messaggi,
avvengono sullo stesso terminale quindi l'esecuzione parallela è necessaria per
non bloccare la console sull'input.
'''

# Processo per l'invio dei messaggi.

def send_message(socket):
    while True:
        try:
            message = input()
            if message:
                socket.send(message.encode(pcf.encoding))
        except Exception:
            # Per qualsiasi eccezione termino questo thread.
            break


# Processo per la ricezione dei messaggi.

def receive_message(socket):
    while True:
        try:
            received_message = str(socket.recv(pcf.message_size), pcf.encoding)
            print(received_message)
        except Exception:
            # Per qualsiasi eccezione termino questo thread.
            break


'''
Qui viene tentata la connessione al server utilizzando i socket,
l'indirizzo IP del server viene preso come argomento, mentre la
porta è condivisa e viene specificata nel file di configurazione.
'''
try:
    pychat_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(
        "Tento la connessione al server " +
        pychat_server_address +
        ":" +
        str(pcf.port))
    pychat_client.connect((pychat_server_address, pcf.port))
except Exception as error_data:
    # Se mi capita un'eccezione durante la connessione, lo mostro e
    # l'applicazione termina.
    print("Connessione al server non riuscita, rieseguire lo script per ritentare la connessione.")
    print(Exception, ":", error_data)
    sys.exit(0)

print("Connessione al server riuscita, avvio i processi di ascolto e invio...")

# Invio il nome scelto al server.
pychat_client.send(name.encode(encoding=pcf.encoding))

t_send = threading.Thread(target=send_message, args=(pychat_client,))
t_read = threading.Thread(target=receive_message, args=(pychat_client,))

# Questo fa si che il main termini solo quando terminano i processi figli.
t_read.daemon = True
t_send.daemon = True

# Faccio partire i thread.
t_read.start()
t_send.start()

print("-- INFORMAZIONI: Digitare un messaggio e invio per scrivere in chat. --")

# Attendo i processi figli e la loro chiusura, senza che il thread main
# termini.
try:
    while True:
        pass
except KeyboardInterrupt:
    print("-- INFORMAZIONI: CTRL-C rilevato, chiudo i processi... --")

print("-- INFORMAZIONI: Processi terminati con successo, termino l'applicazione. --")

# Chiudo il socket del client.
pychat_client.close()

sys.exit(0)
