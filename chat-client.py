import socket
import threading
from zeroconf import Zeroconf, ServiceBrowser
import logging
import time
import select

logging.basicConfig(level=logging.DEBUG)


class ChatClient:
    def __init__(self):
        self.zeroconf = Zeroconf()
        self.services = {}
        self.selected_service = None
        self.client_socket = None
        self.running = True

    def discover_services(self):
        class MyListener:
            def __init__(self, client):
                self.client = client

            def remove_service(self, zeroconf, type, name):
                print(f"Service {name} removed")
                if name in self.client.services:
                    del self.client.services[name]

            def add_service(self, zeroconf, type, name):
                info = zeroconf.get_service_info(type, name)
                if info:
                    self.client.services[name] = info
                    print(f"Service {name} added, service info: {info}")

        listener = MyListener(self)
        ServiceBrowser(self.zeroconf, "_chat._tcp.local.", listener)
        print("Browsing for chat services...")
        time.sleep(2)  # Give some time to discover services

    def display_services(self):
        if not self.services:
            print("No chat services found.")
            return False

        print("Available chat services:")
        for i, (name, info) in enumerate(self.services.items()):
            print(f"{i + 1}. {name}")
            if info.properties:
                for key, value in info.properties.items():
                    print(f"   {key} : {value.decode('utf-8')}")

        return True


    def select_service(self):
        while True:
            try:
                choice = input("Select a service number to connect to: ")
                choice = int(choice) - 1
                if 0 <= choice < len(self.services):
                    self.selected_service = list(self.services.keys())[choice]
                    return True
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def connect_to_service(self):
        if not self.selected_service:
            print("No service selected.")
            return False

        service_info = self.services[self.selected_service]
        if service_info:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                address = socket.inet_ntoa(service_info.addresses[0])
                self.client_socket.connect((address, service_info.port))
                print(f"Connected to {self.selected_service} at {address}:{service_info.port}")
                return True
            except Exception as e:
                print(f"Error connecting to service: {e}")
                return False

    def receive_messages(self):
      while self.running:
        if self.client_socket:
            ready = select.select([self.client_socket], [], [], 0.1)[0]
            if ready:
                try:
                    message = self.client_socket.recv(1024).decode('utf-8')
                    if not message:
                        print("Server disconnected.")
                        self.running = False
                        break
                    print(f"Server: {message}")
                except Exception as e:
                    print(f"Error receiving message: {e}")
                    self.running = False
                    break
        else:
            time.sleep(0.1)

    def send_message(self, message):
        if self.client_socket:
          try:
            self.client_socket.send(message.encode('utf-8'))
          except Exception as e:
            print(f"Error sending message: {e}")
            self.running = False

    def chat(self):
        if not self.client_socket:
            print("Not connected to any service.")
            return
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        while self.running:
            message = input("You: ")
            if message.lower() == "exit":
                self.running = False
                break
            self.send_message(message)

        if self.client_socket:
          self.client_socket.close()
        self.zeroconf.close()
        print("Chat ended")


    def run(self):
        self.discover_services()
        if self.display_services():
            if self.select_service():
                if self.connect_to_service():
                   self.chat()

if __name__ == "__main__":
    client = ChatClient()
    client.run()

