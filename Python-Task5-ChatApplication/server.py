
import socket
import threading
from datetime import datetime
# Create server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "127.0.0.1"
PORT = 5000

server.bind((HOST, PORT))
server.listen()

print(f"Server is listening on {HOST}:{PORT}")

# Store connected clients
clients = {}

# Lock to protect shared clients dictionary
clients_lock = threading.Lock()


# Function to send messages to all clients except the sender
def broadcast(message, sender=None):
    with clients_lock:
        connected_clients = list(clients.keys())

    for client in connected_clients:
        if client != sender:
            try:
                client.sendall(message.encode())
            except OSError:
                pass


# Function to handle each client
def handle_client(conn, addr):
    try:
        # Receive username
        username = conn.recv(1024).decode().strip()

        if not username:
            return

        with clients_lock:
            clients[conn] = username

        print(f"{username} connected from {addr}")

      
        # Receive messages continuously
        while True:
            data = conn.recv(1024)

            if not data:
                break

            message = data.decode().strip()

            if message.lower() == "exit":
                break

            timestamp = datetime.now().strftime("%H:%M")

            formatted_message = f"[{timestamp}] {username}: {message}"

            print(formatted_message)

            broadcast(formatted_message, sender=conn)
    except OSError:
        pass

    finally:
        with clients_lock:
            username = clients.pop(conn, None)

        conn.close()

        if username:
            print(f"{username} disconnected.")
            broadcast(f"{username} disconnected.")


# Accept multiple clients
while True:
    conn, addr = server.accept()

    print(f"New connection from {addr}")

    client_thread = threading.Thread(
        target=handle_client,
        args=(conn, addr)
    )

    client_thread.start()
