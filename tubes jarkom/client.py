from socket import *
import sys

if len(sys.argv) != 4:
    print("Usage: python client.py <server_address> <server_port> <filename>")
    sys.exit(1)

server_address = sys.argv[1]
server_port = int(sys.argv[2])
wanted_filename = sys.argv[3]

server = (server_address,server_port)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(server)


request = f"GET /{wanted_filename} HTTP/1.1\r\nHost: {server_address}\r\n\r\n"

client_socket.send(request.encode())

server_response = ""

while True:
    filename_data = client_socket.recv(1024).decode()
    if not filename_data:
        break
    server_response = server_response + filename_data

print(server_response)

client_socket.close()