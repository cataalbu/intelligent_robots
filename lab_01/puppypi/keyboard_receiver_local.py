#!/usr/bin/env python3
import socket

PORT = 8089


def handle_input(key):
    print(f"Received key: '{key}'")


def handle_client(conn, addr):
    print(f"Client connected from {addr[0]}:{addr[1]}")
    buffer = ""
    while True:
        data = conn.recv(1024)
        if not data:
            break
        buffer += data.decode(errors="replace")
        while "\n" in buffer:
            message, buffer = buffer.split("\n", 1)
            if message == "QUIT":
                print("Client requested quit")
                return
            handle_input(message)
    print(f"Client {addr[0]}:{addr[1]} disconnected")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", PORT))
    server.listen(1)
    server.settimeout(1.0)  # so Ctrl+C is noticed promptly
    print(f"Keyboard receiver listening on port {PORT}")

    try:
        while True:
            try:
                conn, addr = server.accept()
            except socket.timeout:
                continue
            with conn:
                conn.settimeout(None)
                handle_client(conn, addr)
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        print("Keyboard receiver stopped")


if __name__ == "__main__":
    main()
