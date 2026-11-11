# Real-Time Chat Application

A simple real-time chat application built with Python using socket programming and multithreading. The application allows multiple clients to connect to a central server and exchange messages simultaneously.

## Features

- **TCP Socket Communication:** Establishes communication between the server and multiple clients.
- **Multiple Client Support:** Allows multiple users to connect to the same server.
- **Real-Time Messaging:** Users can send and receive messages simultaneously.
- **Message Broadcasting:** Messages are delivered to all connected clients except the sender.
- **Timestamps:** Each message includes the time it was sent.
- **Graceful Disconnection:** Detects when a user exits and notifies the remaining clients.
- **Username Identification:** Each client joins the chat using a username.

## Technologies Used

- Python
- Socket Programming
- TCP Protocol
- Threading
- DateTime Module

## Project Structure

```text
ChatApplication/
│
├── server.py
├── client.py
└── README.md
```

## How to Run

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
```

### 2. Navigate to the Project Folder

```bash
cd ChatApplication
```

### 3. Start the Server

Open a terminal and run:

```bash
python server.py
```

The server will start listening for incoming connections on:

```text
127.0.0.1:5000
```

### 4. Start the Clients

Open separate terminal windows for each client and run:

```bash
python client.py
```

Enter a username when prompted.

Multiple clients can connect to the same server and start chatting.

### 5. Send Messages

Type your message and press Enter to send it.

To leave the chat, type:

```text
exit
```

The server will detect the disconnection and notify the remaining clients.

## Example

```text
[15:30] momo: Hello everyone!
[15:31] popo: Hi momo!
[15:32] gggg: Nice to meet you!
```

## Learning Outcomes

Through this project, I practiced:

- Understanding client-server architecture.
- Working with TCP sockets.
- Handling multiple client connections.
- Using Python threads for concurrent communication.
- Broadcasting messages between connected clients.
- Managing client connections and disconnections.

## Project Scope

This project implements the **Beginner Tier** of a real-time chat application, focusing on fundamental networking concepts and client-server communication.

