import socket as socket
import sys

# Utilizzo di indirizzi IPV4 connection-oriented
pychat_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 3:
    print("Argomenti non corretti," +
          "per connettersi invocare il comando:" +
          "\npychat_c.py [ind_server] [nome_visualizzato]")
    sys.exit(0)

pychat_server_address = str(sys.argv[1])
name = str(sys.argv[2])
pychat_server_port = 3500

try:
    print(
        "Tento la connessione al server " +
        pychat_server_address +
        ":" +
        str(pychat_server_port))
    pychat_client.connect((pychat_server_address, pychat_server_port))
except Exception as error_data:
    print(Exception, ":", error_data)
    sys.exit(0)

'''
Arrivati in questo punto la connessione è stata stabilita, posso eseguire
il loop di invio e ricezione dei messaggi.

'''

try:
    while True:
        message = input()
        complete_message = name + ": " + message
        if message:
            pychat_client.send(complete_message.encode())
except KeyboardInterrupt:
    pass

pychat_client.close()
