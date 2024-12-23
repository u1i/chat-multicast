import socket
import threading
from zeroconf import Zeroconf, ServiceInfo
import logging

logging.basicConfig(level=logging.DEBUG)

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received: {message}")
            client_socket.send("Message received".encode('utf-8'))
        except:
            break

    client_socket.close()

def start_server(port, service_name, device_name, version):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}")

    zeroconf = Zeroconf()
    service_type = "_chat._tcp.local."
    properties = {
        'device_name': device_name,
        'version': version,
        'fn': device_name,  # Friendly name
        'st': '1',       # Status
        'bs': '1',       # Boolean status
        'id': 'unique_id', # some unique id
        'rm': 'optional_info' # some optional info
    }
    info = ServiceInfo(
        service_type,
        f"{service_name}-{device_name}.{service_type}",
        addresses=[socket.inet_aton(socket.gethostbyname(socket.gethostname()))],
        port=port,
        properties=properties
    )
    zeroconf.register_service(info)
    print(f"Service '{service_name}' registered on mDNS with device name '{device_name}' and version '{version}'")


    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        zeroconf.unregister_service(info)
        zeroconf.close()
        server_socket.close()
        print("Server stopped.")

if __name__ == "__main__":
    PORT = 5050
    SERVICE_NAME = "MyChat"
    DEVICE_NAME = "titan"
    VERSION = "0.1" # You can change this
    start_server(PORT, SERVICE_NAME, DEVICE_NAME, VERSION)

