import requests
import subprocess
import socket
import psutil
import time
import os

# Customisation: Tor Data Folder
tor_data_folder = "tor_data"


def check_tor_state():
	for process in psutil.process_iter(["name"]):
		if process.info["name"] == "tor":
			return True
	return False

def start_tor():
	if not os.path.exists(f"{tor_data_folder}"):
		os.makedirs(f"{tor_data_folder}")

	running = check_tor_state()

	if running is True:
		print("Tor is already running, skipping...")
	else:		
		tor = subprocess.Popen([
			"tor",
			"-f", "torrc",
			"--ControlPort", "9051",
			"--SocksPort", "9050",
			"--DataDirectory", f"{tor_data_folder}",
			"--CookieAuthentication", "1",
			"--Log", "notice stdout",
		])

		return tor # returning tor so it can be killed later

def connect_control():
	return socket.create_connection(("127.0.0.1", 9051))

def auth(csocket, cookie_path=f"{tor_data_folder}/control_auth_cookie"):
	with open (cookie_path, "rb") as file:
		cookie = file.read()
	command = b"AUTHENTICATE " + cookie.hex().encode() + b"\r\n"
	csocket.sendall(command)
	response = csocket.recv(1024)
	if not response.startswith(b"250"):
		raise Exception("Auth Failed: ", response.decode())
	
def send_newnym(csocket):
	csocket.sendall(b"SIGNAL NEWNYM\r\n")
	response = csocket.recv(1024)
	if not response.startswith(b"250"):
		raise Exception("NEWNYM Failed: ", response.decode())

def send_term(csocket):
	csocket.sendall(b"SIGNAL TERM\r\n")
	response = csocket.recv(1024)
	if not response.startswith(b"250"):
		raise Exception("TERM Failed: ", response.decode())


	
      

def ipcheck():
	proxies = {
		"http": "socks5h://127.0.0.1:9050",
		"https": "socks5h://127.0.0.1:9050",
	}

	response = requests.get("http://httpbin.org/ip", proxies=proxies).json()
	address = response['origin']
	return address





if __name__ == "__main__":
	try:
		start_tor()
		time.sleep(10)
		csocket = connect_control()
		auth(csocket)
		# send_term(csocket)
		while True:
			send_newnym(csocket)
			print("Current IP: " + ipcheck())
			time.sleep(10)
	except KeyboardInterrupt:
		print("Goodbye!")
	