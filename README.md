# Simple mDNS Chat Server and Client

This project provides a simple chat server and client that use mDNS (Multicast DNS) for service discovery on a local network. The server advertises its presence using mDNS, and the client discovers and connects to the server, allowing you to send and receive chat messages.

## Overview

The project consists of two main components:

1.  **Chat Server (`chat_server_with_full_info.py`)**:
    *   A Python server that listens for incoming connections on a specified port (default is 5050).
    *   Advertises its presence on the local network using mDNS, making it discoverable by clients.
    *   Includes detailed information in the mDNS advertisement, such as device name, version, and other properties.
2.  **Chat Client (`chat_client.py`)**:
    *   A Python client that discovers chat servers on the local network using mDNS.
    *   Presents a list of available servers with details.
    *   Allows users to select a server and connect to it.
    *   Enables users to send and receive chat messages.

## How It Works

### Chat Server

1.  **Initialization**: The server creates a socket, binds it to port 5050 (default), and starts listening for incoming connections.
2.  **mDNS Advertisement**: The server uses the `zeroconf` library to register a service on the local network using mDNS.
    *   The service type is `_chat._tcp.local.`.
    *   The service instance name is constructed as `MyChat-titan._chat._tcp.local.` (where `titan` is the default device name).
    *   The mDNS advertisement includes the following TXT record properties:
        *   `device_name`: The device name (default is `titan`).
        *   `version`: The version of the service (default is `0.1`).
        *   `fn`: A friendly name (same as device name).
        *   `st`: Status (set to `1`).
        *   `bs`: Boolean status (set to `1`).
        *  `id`: A unique identifier.
        *  `rm`: Some optional info.
3.  **Connection Handling**: When a client connects, the server creates a new thread to handle the client connection.
4.  **Message Handling**: The server receives messages from the client, prints them to the console, and sends a simple "Message received" response.

### Chat Client

1.  **Service Discovery**: The client uses the `zeroconf` library to browse for `_chat._tcp.local.` services on the network.
2.  **Service Listing**: The client displays a numbered list of discovered services, including details from their mDNS advertisements.
3.  **Service Selection**: The user is prompted to select a service to connect to.
4.  **Connection Establishment**: The client creates a socket and connects to the selected server using its IP and port.
5.  **Chat Interaction**:
    *   The client starts a new thread to receive messages from the server.
    *   The user is prompted to enter messages to send to the server.
    *   The client sends messages to the server and prints the server's responses.
    *   The chat session ends when the user types `exit`.

## How to Run

### Prerequisites

*   Python 3.6 or higher
*   `zeroconf` library (`pip install zeroconf`)

### Steps

1.  **Save the files**: Save the server code as `chat_server_with_full_info.py` and the client code as `chat_client.py`.
2.  **Run the server**:
    ```
    python chat_server_with_full_info.py
    ```
    The server will start and advertise its presence on the local network. The default port is 5050.
3.  **Run the client**:
    ```
    python chat_client.py
    ```
    The client will discover available chat services, list them, and prompt you to select one.
4.  **Select a server**: Enter the number corresponding to the server you want to connect to.
5.  **Chat**: Once connected, you can type messages, and they will be sent to the server. The server's responses will be displayed in the console.
6.  **Exit**: Type `exit` to end the chat and close the connection.

## Configuration

*   **Server Port**: The server uses port 5050 by default. You can change this in the `chat_server_with_full_info.py` file by modifying the `PORT` variable in the `if __name__ == "__main__":` block.
*   **Service Name**: The service name is `MyChat` by default. You can change this in the `chat_server_with_full_info.py` file by modifying the `SERVICE_NAME` variable.
*   **Device Name**: The device name is `titan` by default. You can change this in the `chat_server_with_full_info.py` file by modifying the `DEVICE_NAME` variable.
*   **Version**: The version is `0.1` by default. You can change this in the `chat_server_with_full_info.py` file by modifying the `VERSION` variable.

## Example

**Server Output:**

```
Server listening on port 5050
Service 'MyChat' registered on mDNS with device name 'titan' and version '0.1'
```

**Client Output:**

```
Browsing for chat services...
Available chat services:
1. MyChat-titan
   device_name : titan
   version : 0.1
   fn : titan
   st : 1
   bs : 1
   id : unique_id
   rm : optional_info
Select a service number to connect to: 1
Connected to MyChat-titan at 192.168.1.100:5050
You: Hello
Server: Message received
You: How are you
Server: Message received
You: exit
Chat ended
```

## Notes

*   Both the server and client need to be on the same local network.
*   The server needs to be running before the client can discover it.
*   This is a basic example and does not include features such as encryption or user authentication.
*   The server IP address shown in the client output will be your local IP address.

This README provides all the necessary information to understand, run, and use the chat server and client.

