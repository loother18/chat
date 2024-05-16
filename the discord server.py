import socket
import threading
import tkinter as tk


class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Server")
        self.root.configure(bg="black")

        self.message_listbox = tk.Listbox(root, width=60, height=20, font=("Arial", 12), bg="black", fg="white",
                                          borderwidth=0, highlightthickness=0)
        self.message_listbox.pack(pady=10, padx=10, expand=True, fill="both")

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(5)

        self.clients = []

        self.accept_thread = threading.Thread(target=self.accept_connections)
        self.accept_thread.start()

    def accept_connections(self):
        while True:
            client_socket, address = self.server_socket.accept()
            self.clients.append((client_socket, address))
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_thread.start()

    def handle_client(self, client_socket, address):
        print(f"Accepted connection from {address}")

        while True:
            try:
                message = client_socket.recv(1024).decode("utf-8")
                if not message:
                    break

                print(f"Received message from {address}: {message}")

                # Display message on GUI
                self.message_listbox.insert(tk.END, f"{address[0]}: {message}")

                # Broadcast message to all clients
                self.broadcast(message)

            except Exception as e:
                print(f"Error handling client {address}: {e}")
                break

        self.clients.remove((client_socket, address))
        client_socket.close()
        print(f"Connection from {address} closed.")

    def broadcast(self, message):
        for client, _ in self.clients:
            try:
                client.send(message.encode("utf-8"))
            except Exception as e:
                print(f"Error broadcasting message: {e}")
                client.close()
                self.clients.remove((client, _))


HOST = socket.gethostbyname(socket.gethostname())
PORT = 12345

root = tk.Tk()
app = ServerGUI(root)
root.mainloop()
