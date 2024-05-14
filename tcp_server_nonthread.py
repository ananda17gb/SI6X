from socket import *

def contentType(file) :
  type = file.split('.')[-1]
  print(type)
  if type=="html":
      return "text/html"
  elif type=="jpg":
      return "image/jpeg"
  elif type=="gif":
      return "image/gif"
  elif type=="png":
      return "image/png"
  elif type=="ico":
      return "image/x-icon"
  elif type =="css":
      return "text/css"
  elif type == "svg":
      return "image/svg+xml"

server_address = gethostbyname(gethostname())
server_port = 1988 
server = (server_address,server_port)

server_socket = socket(AF_INET, SOCK_STREAM)

server_socket.bind(server)
server_socket.listen(5)

print(f"Watch and listen on addres {server_address} with port {server_port}  ")

while True:
  client_socket, client_address = server_socket.accept()
  print(f"Connected Bang sama {client_address}")

  request = client_socket.recv(1024).decode()
  headers = request.split('\n')
  filename = headers[0].split()[1]

  if filename == "/":
    filename = '/index.html'
  
  try:
    with open(filename[1:], 'rb') as fin:
      content = fin.read()
      content_type = contentType(filename)
      response = f'HTTP/1.0 200 OK\nContent-Type: {content_type}\n\n'.encode() + content
  except FileNotFoundError:
    with open('404.html', 'rb') as fin:
      content = fin.read()
      content_type = 'text/html'
      response = f'HTTP/1.0 404 NOT FOUND\nContent-Type: {content_type}\n\n'.encode() + content
      
  client_socket.sendall(response)
  client_socket.close()
