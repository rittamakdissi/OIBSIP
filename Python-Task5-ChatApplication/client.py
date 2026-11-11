
import socket
import threading

# Create a client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server address
HOST = "127.0.0.1"
PORT = 5000

# Connect to the server
client.connect((HOST, PORT))

username = input("Enter your username: ")

client.sendall(username.encode())


print("Connected to the chat server!")


# Function to send messages
def send_messages():
    while True:
        message = input("You: ")

        if message.lower() == "exit":
            client.sendall(message.encode())
            break

        try:
            client.sendall(message.encode())
        except OSError:
            break


# Function to receive messages
def receive_messages():
    while True:
        try:
            data = client.recv(1024)

            if not data:
                print("\nServer disconnected.")
                break

            message = data.decode()
            print(f"\n{message}")

        except OSError:
            break


# Create threads
send_thread = threading.Thread(target=send_messages)
receive_thread = threading.Thread(target=receive_messages)

# Start threads
send_thread.start()
receive_thread.start()

