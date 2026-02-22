import socket
import sys

HOST = '127.0.0.1'
PORT= 45982

#Create a TCP/IP socket for the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:

    try:
        #Connect to the server
        c.connect((HOST, PORT))
    except Exception as e:
        print(f"Error occurred while connecting to the server: {e}")

    #inform the user that the client is connected
    print(f"Connected to server on port {PORT}... \n")

    try:
        #Get the file name from command line arguments
        fileName = sys.argv[1]
    except IndexError:
        print("Please provide the file name as a command line argument.")

    #Read the file and send its contents to the server
    with open(fileName, 'r') as f:
        data = f.read()
        
    try:    
        c.sendall(data.encode()) 
        c.shutdown(socket.SHUT_WR)  # Indicate we're done sending
    except Exception as e:
        print(f"Error occurred while sending data: {e}")

    # Receive the generated file name from the server
    saved_file_name = c.recv(1024).decode('utf-8')   

    # Inform the user about the saved file name
    print(f"Server stored file as {saved_file_name} \n")    
       

    
