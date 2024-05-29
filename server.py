import threading
import socket
from datetime import datetime


def get_time() -> str:
    ahora = datetime.now()
    formato = "%Y-%m-%d %H:%M:%S"
    fecha_hora_actual = ahora.strftime(formato)

    return fecha_hora_actual

def print_all(usernames):
    print(f"USERNAMES_DICT: {usernames}")

def client_thread(client_socket, clients, usernames):
    username = (client_socket.recv(1024)).decode()
    usernames[client_socket] = username
    print(f"username: {username} <online>") #just visible at the terminal
    sock_time_on = get_time()
    for client in clients:
                client.sendall(f"{username} (ONLINE) {sock_time_on}".encode())#notificacion de online 
    while True:
         try:
              message = client_socket.recv(1024).decode()
              if not message:
                   break
              if message == "get_all_the_users":
                   client_socket.sendall(f"[+] Usuarios Activos [{sock_time_on}]: {', '.join(usernames.values())}: \n".encode())
                   continue #saltandonse a la siguient eteracion omitiendo en for client in clients:
              for client in clients:
                   if client is not client_socket: #para no recibir mi mismo mensaje
                        client.sendall(message.encode())
         except:
              break
    client_socket.close()
    clients.remove(client_socket)
    del usernames[client_socket]

def server_program():
    host = "localhost"
    port = 54321
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #poder reutilizar puertos
    server_socket.bind((host, port))
    server_socket.listen()

    print("[+] El servidor esta a la escucha de conexiones entrantes...")
    clients = []
    usernames = {}


    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        print(f"[+] Se ha conectado un nuevo cliente: {addr}")
        #creando un thread para manejar las conexiones de los clientes por separadp
        thread = threading.Thread(target= client_thread, args = (client_socket, clients, usernames), 
                                  daemon=True, name = "my_client_thread_is_running") #¢reando un hilo demomio
        thread.start() #running the thread...

    server_socket.close() #closing the server_socket
if __name__ == "__main__":
    server_program() #here the program starts ...







