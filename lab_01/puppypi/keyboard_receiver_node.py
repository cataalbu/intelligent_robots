#!/usr/bin/env python3
import socket
import rospy
from std_msgs.msg import String


def handle_input(key, pub):
    rospy.loginfo("Received key: '%s'", key)
    pub.publish(String(data=key))


def handle_client(conn, addr, pub):
    rospy.loginfo("Client connected from %s:%d", *addr)
    conn.settimeout(1.0)
    buffer = ""
    while not rospy.is_shutdown():
        try:
            data = conn.recv(1024)
        except socket.timeout:
            continue
        if not data:
            break
        buffer += data.decode(errors="replace")
        while "\n" in buffer:
            message, buffer = buffer.split("\n", 1)
            if message == "QUIT":
                rospy.loginfo("Client requested quit")
                return
            handle_input(message, pub)
    conn.close()
    rospy.loginfo("Client %s:%d disconnected", *addr)


def main():
    rospy.init_node("keyboard_receiver")
    port = rospy.get_param("~port", 8089)
    pub = rospy.Publisher("keyboard_input", String, queue_size=10)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", port))
    server.listen(1)
    server.settimeout(1.0)  # so Ctrl+C / rospy shutdown is noticed
    rospy.loginfo("Keyboard receiver listening on port %d", port)

    while not rospy.is_shutdown():
        try:
            conn, addr = server.accept()
        except socket.timeout:
            continue
        with conn:
            handle_client(conn, addr, pub)

    server.close()
    rospy.loginfo("Keyboard receiver stopped")


if __name__ == "__main__":
    main()
