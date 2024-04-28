#!/bin/env python
import socketserver as srv
import pychat_config as pcf

'''
Programmazione di Reti
Server della chatroom, realizzata da
Luca Casadei - Martin Tomassi - Francesco Pazzaglia
'''

# Conservo qui i client che si sono connessi al server.
clients = []

# Invio a tutti i client connessi un messaggio.


def do_broadcast(message):
    for conn in clients:
        conn.send(message.encode(pcf.encoding))


'''
Classe che gestisce le richieste di invio di un messaggio, handler passato
come parametro al metodo ThreadingTCPServer di socketserver.
'''


class ChatReqHandler(srv.BaseRequestHandler):
    def handle(self):
        # Client connesso, lo aggiungo alla lista
        clients.append(self.request)
        name = str(self.request.recv(pcf.message_size), pcf.encoding)
        do_broadcast(name + " si è unito alla chat.")
        while True:
            try:
                # Il messaggio contiene [Nome]: Testo
                message = str(
                    self.request.recv(
                        pcf.message_size),
                    pcf.encoding)
                if message:
                    do_broadcast(name + ": " + message)
                else:
                    # Se il messaggio è vuoto ho un errore o il client non è
                    # più raggiungibile.
                    break
            except ConnectionResetError:
                # Gestisco la disconnessione forzata dell'host remoto.
                break
        # Quando si verifica un errore di disconnessione forzata, elimino il
        # client dalla lista.
        clients.remove(self.request)
        do_broadcast(name + " si è disconnesso dalla chat.")


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
