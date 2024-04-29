#!/bin/env python
import socketserver as srv
import pychat_config as pcf

'''
Programmazione di Reti
Server della chatroom, realizzata da
Luca Casadei - Martin Tomassi - Francesco Pazzaglia
'''

# Conservo qui i client che si sono connessi al server.
clients = {}

# Invio a tutti i client connessi un messaggio di informazione.
def do_info_broadcast(message):
    for conn in clients.values():
        conn.send(message.encode(pcf.encoding))

# Invio a tutti i client connessi un messaggio da parte di un utente.
def do_message_broadcast(name, message):
    for client_name, conn in clients.items():
        if name != client_name:
            conn.send((name + ": " + message).encode(pcf.encoding))
        
# Invio la lista dei client connessi solo al client che lo ha eseguito.
def get_user_list():
    user_count = len(clients)
    prefix = f"Utenti online ({user_count}):\n"
    user_list = "\n".join(clients.keys())
    return prefix + user_list

'''
Classe che gestisce le richieste di invio di un messaggio, handler passato
come parametro al metodo ThreadingTCPServer di socketserver.
'''


class ChatReqHandler(srv.BaseRequestHandler):
    def handle(self):
        # Client connesso, lo aggiungo alla lista
        while True:
            name = str(self.request.recv(pcf.message_size), pcf.encoding)
            if name in clients:
                self.request.send("Il nome utente è già in uso. Riprova con un altro nome:".encode(pcf.encoding))
            else:
                clients[name] = self.request
                break

        do_info_broadcast(name + " si è unito alla chat.")

        while True:
            try:
                message = str(
                    self.request.recv(
                        pcf.message_size),
                    pcf.encoding)
                if message: 
                    if message.lower() == "/list":
                        self.request.send(get_user_list().encode(pcf.encoding))
                    else:
                        self.request.send(("Tu: " + message).encode(pcf.encoding))
                        do_message_broadcast(name, message)
                else:
                    # Se il messaggio è vuoto ho un errore o il client non è
                    # più raggiungibile.
                    break
            except ConnectionResetError:
                # Gestisco la disconnessione forzata dell'host remoto.
                break

        # Quando si verifica un errore di disconnessione forzata, elimino il
        # client dalla lista.
        del clients[name]
        do_info_broadcast(name + " si è disconnesso dalla chat.")



server = srv.ThreadingTCPServer(('', pcf.port), ChatReqHandler)
server.daemon_threads = True
# Permette di utilizzare più volte la stessa porta se una connessione che
# la usava non esiste più.
server.allow_reuse_address = True

try:
    print("Inizio l'ascolto su:", pcf.port)
    while True:
        # Il server si mette in ascolto per l'invio dei messaggi.
        server.serve_forever()
except KeyboardInterrupt:
    # Se interrompo l'esecuzione con CTRL-C, termino il processo e chiudo
    # l'applicazione.
    print("CTRL-C Rilevato, termino il processo server.")
    pass
finally:
    server.server_close()
