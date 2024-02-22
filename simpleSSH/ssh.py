import socket
import threading

import paramiko


class SSH:
    def __init__(self, address: str, username: str, password: str):
        print(f"Connecting to server on IP {address}.")
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())

        try:
            self.client.connect(
                address, username=username, password=password, look_for_keys=False
            )
            self.transport = self.client.get_transport()
            self.shell = self.transport.open_session()
            self.shell.get_pty()
            self.shell.settimeout(5)
            self.shell.invoke_shell()
            self.strdata = ""
            self.fulldata = ""
            thread = threading.Thread(target=self.process)
            thread.daemon = True
            thread.start()
        except paramiko.AuthenticationException:
            print("Authentication failed. Please check your credentials.")

    def closeConnection(self):
        if self.client is not None:
            self.client.close()

    def sendShell(self, command: str):
        if self.shell:
            self.shell.send(command + "\n")
        else:
            print("Shell not opened.")

    def process(self):
        while True:
            try:
                alldata = self.shell.recv(1024)
                if not alldata:
                    break
                decoded_data = alldata.decode("utf-8")
                self.strdata = self.strdata + decoded_data
                self.fulldata = self.fulldata + decoded_data
                if self.shell.recv_ready():
                    self.strdata = self.print_lines(self.strdata)
            except (socket.timeout, EOFError):
                break

    def print_lines(self, data: str) -> str:
        last_line = data
        if "\n" in data:
            lines = data.splitlines()
            for line in lines[:-1]:
                print(f"{line}")
            last_line = lines[-1]
            if data.endswith("\n"):
                print(f"{last_line}")
                last_line = ""
        return last_line
