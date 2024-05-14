from socket import *
import sys
import threading

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen(5)

while True:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(1024).decode()
    print(message)
    
    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = False
    filetouse = "/" + filename
    print(filetouse)
    
    try:
        # Check whether the file exists in the cache
        with open(filetouse[1:], "r") as f:
            outputdata = f.readlines()
            fileExist = True
            # ProxyServer finds a cache hit and generates a response message
            tcpCliSock.send(b"HTTP/1.0 200 OK\r\n")
            tcpCliSock.send(b"Content-Type:text/html\r\n\r\n")
            # Send the content of the requested file to the client
            for line in outputdata:
                tcpCliSock.send(line.encode())
            print('Read from cache')
    except IOError:
        if not fileExist:
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace("www.", "", 1)
            print(hostn)
            try:
                # Connect to the socket to port 80
                c.connect((hostn, 80))
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile('r', 0)
                fileobj.write(f"GET http://{filename} HTTP/1.0\n\n".encode())
                # Read the response into buffer
                buff = fileobj.readlines()
                # Create a new file in the cache for the requested file.
                with open("./" + filename, "wb") as tmpFile:
                    # Also send the response in the buffer to client socket and the corresponding file in the cache
                    for line in buff:
                        tmpFile.write(line.encode())
                        tcpCliSock.send(line.encode())
            except Exception as e:
                print("Exception: ", e)
                print("Illegal request")
                # HTTP response message for file not found
                tcpCliSock.send(b"HTTP/1.0 404 Not Found\r\n")
                tcpCliSock.send(b"Content-Type:text/html\r\n\r\n")
            finally:
                c.close()
    # Close the client socket
    tcpCliSock.close()

# Close the server socket
tcpSerSock.close()