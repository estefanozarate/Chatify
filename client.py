#!/usr/bin/env python3
import socket
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText
#lambda arg : exp

#funcion solo de decoracion del texto
def decore_message(username, message) -> str:
    return f"{username}: {message} \n"

def list_all_active_users(client_socket):
    client_socket.sendall("get_all_the_users".encode())

def exit_function(client_socket, username, window):
    client_socket.sendall(f"[{username}] -> offline")
    client_socket.close()

    window.quit() #salir de manera ordenada y detener el root.mainloop(). No destruye la ventana ni los objetos widgets !!!
    window.destroy() #destruye la ventana principal y todos sus widgets, libera los recuesos asociados !!!

def send_message(event, client_socket, username, text_widget, entry_widget):
    message = entry_widget.get()
    client_socket.sendall(f"[{username}] {message}".encode())
    entry_widget.delete(0, END) #borrando el entry_widget
    text_widget.configure(state = "normal") #activando la modificacion del entry_widget
    text_widget.insert(END, decore_message(username, message))
    text_widget.configure(state = "disable")#impedir moficiaciones en el Entry()


def catch_message(client_socket, text_widget): 
    #ejecutarse en bucle infinito gracias al while True y al target de mi thread
    while True:
        try:
            message = (client_socket.recv(1024)).decode()
            if not message:
                break
            text_widget.configure(state = "normal")
            text_widget.insert(END, f"{message} \n")
            text_widget.configure(state = "disable")
        except:
            break

def client_program():
    host = "localhost"
    port = 54321

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    username = input("[+] username: ")
    client_socket.sendall(f"[{username}]".encode())

    window = Tk()
    window.title("chat")
    text_widget = ScrolledText(window, state = "disable")
    #state disable: no poder modificar el ScrolledText
    text_widget.pack(padx= 10, pady= 10)

    frame_widget = Frame(window)
    frame_widget.pack(padx = 5, pady = 5, fill= BOTH, expand = 1)

    entry_widget = Entry(frame_widget) #metiendo el entry_widget dentro del Frame
    entry_widget.bind("<Return>", lambda event: send_message(event, client_socket, 
                                            username, text_widget, entry_widget ))
        #lambda funciones para que no se llame automaticamente
    entry_widget.pack(side = LEFT, fill= X, expand = 1)
    
    #repasar funciones lambda...
    button_widget = Button(frame_widget, text = "Enviar", command = lambda: send_message(None, client_socket, username, text_widget, entry_widget))
    button_widget.pack(side = RIGHT, padx = 3)

    #boton listar todos los usuarios
    list_all_users_widget = Button(window, text = "Listar todos los usuarios", command = lambda: list_all_active_users(client_socket))
    list_all_users_widget.pack(padx = 5, pady =5)

    exit_widget = Button(window, text = "EXIT", command = lambda: exit_function(client_socket, username, window))
    exit_widget.pack(padx=5, pady =5)

    #lograr la continueamente corra la funcion catch_message() usando hilos
    thread = threading.Thread(target = catch_message, args = (client_socket, text_widget))
    thread.daemon = True #cuando finaliza el MAIN_THREAD todos los hilos muerne con el!
    thread.start() #running thr thread ->.<- 
    #closing (client_socket)
    window.mainloop()
    client_socket.close()



if __name__ == "__main__":
    client_program()