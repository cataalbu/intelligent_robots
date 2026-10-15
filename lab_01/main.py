import socket
import readchar
from readchar import key as keys


ESC = "\x1b"
CTRL_C = "\x03"
ADDRESS = ("localhost", 8089)
ARROW_KEYS = {keys.UP: "UP", keys.DOWN: "DOWN", keys.LEFT: "LEFT", keys.RIGHT: "RIGHT"}


def send(sock, message):
    # each message ends with "\n" so the receiver knows where it stops
    sock.sendall((message + "\n").encode())


def main():
    print(f"Connecting to {ADDRESS[0]}:{ADDRESS[1]} ...")
    sock = socket.create_connection(ADDRESS)
    sock.settimeout(None)
    print("Connected. Press keys to send (ESC twice or Ctrl+C to quit).")
    while True:
        try:
            # readkey waits for a second byte after ESC (it could be an arrow key),
            # so a lone ESC never returns; ESC ESC comes back as "\x1b\x1b"
            key = readchar.readkey()
        except KeyboardInterrupt:
            # readkey raises on Ctrl+C instead of returning "\x03"
            key = CTRL_C
        if key in (ESC + ESC, CTRL_C):
            send(sock, "QUIT")
            print("Quit requested, closing connection.")
            break
        message = ARROW_KEYS.get(key, key)
        send(sock, message)
        print(f"Sent: {message}")
    sock.close()


if __name__ == "__main__":
    main()
