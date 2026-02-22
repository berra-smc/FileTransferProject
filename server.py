import socket
from datetime import datetime

HOST = "127.0.0.1"
PORT= 45982

#Create a TCP/IP socket for the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    try:
        #Bind the socket to the address and port
        s.bind((HOST, PORT))

        #Listen for incoming connections
        s.listen(10) # adjusted client queue size
    except Exception as e:
        print(f"Error occurred while setting up the server: {e}")

    
    #inform the user that the server is running
    print(f"Server listening on port {PORT}...\n")

    #Accept and handle incoming connections with a loop
    while True:
        
        try:
            conn,addr = s.accept()
        except Exception as e:
            print(f"Error occurred while accepting a connection: {e}")


        with conn:
            #inform the user that a connection has been established
            print(f"Connection from {addr} \n")

            try:
                #Recieve data packets with a loop
                received_data = ""
                while True:
                    data= conn.recv(1024).decode('utf-8')
                    received_data += data
                    if not data: break
            except Exception as e:
                print(f"Error occurred while receiving data: {e}")        

            print("Received Message:\n")

            line_counter = 0
            for line in received_data.split('\n'):
                print(line) # Print each line
                line_counter += 1 #count lines printed
                
                #if printed lines reach 40, wait for user input to continue
                if line_counter == 40:
                    while True:
                        user_input = input("\n Press SPACE and ENTER to continue: ")
                        
                        if user_input == " ": 
                            line_counter = 0  
                            break
                        else:
                            print("\n Press SPACE and ENTER to continue:")

            #Generate a unique file name based on client IP and current date/time
            now = datetime.now()
            creation_date = now.strftime("_%Y-%m-%d_%H-%M-%S.txt")
            client_ıp = addr[0].replace(".", "_")
            file_name = client_ıp + creation_date 

            #Send the file name back to the client
            conn.sendall(file_name.encode())

            try:
                #Save the received data to a file
                with open(file_name, 'w') as f:
                    f.write(received_data) 
            except Exception as e:
                print(f"Error occurred while saving data to file: {e}")

            #Inform the user about the saved file
            print(f"\n Saved as {file_name} \n")

            try:
                #Create log data and append it to the server log file
                log_data= f"{file_name} {len(received_data)}"
                with open("22303056-serverLOG.txt", 'a') as log_file:
                    log_file.write( log_data + "\n")
            except Exception as e:
                print(f"Error occurred while logging data: {e}")
            

            #Inform the user that logging was successful
            print("Logged successfully. \n")
                


            


