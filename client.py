import socket
import threading
import tkinter as tk


class ClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")
        self.root.configure(bg="black")

        self.message_listbox = tk.Listbox(root, width=60, height=20, font=("Arial", 12), bg="black", fg="white",
                                          borderwidth=0, highlightthickness=0)
        self.message_listbox.pack(pady=10, padx=10, expand=True, fill="both")

        self.entry = tk.Entry(root, width=60, font=("Arial", 12), bg="black", fg="white", insertbackground="white",
                              borderwidth=0)
        self.entry.pack(pady=10, padx=10)

        self.send_button = tk.Button(root, text="Send", command=self.send_message, font=("Arial", 12), bg="white",
                                     fg="black", bd=0)
        self.send_button.pack(pady=5)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def send_message(self):
        message = self.entry.get()
        if message:
            self.client_socket.send(message.encode("utf-8"))
            self.entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode("utf-8")
                if not message:
                    break

                self.message_listbox.insert(tk.END, message)
                self.message_listbox.see(tk.END)  # Scroll to the latest message

            except Exception as e:
                print(f"Error receiving message: {e}")
                break


HOST = socket.gethostbyname(socket.gethostname())
PORT = 12345

root = tk.Tk()
app = ClientGUI(root)
root.mainloop()
