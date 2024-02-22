import os
import time

from dotenv import load_dotenv

from ssh import SSH

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)


def main():
    sshUsername = ""
    sshPassword = ""
    sshServer = ""

    session = SSH(sshServer, sshUsername, sshPassword)

    commands = [
        "pwd"
    ]

    for cmd in commands:
        session.sendShell(cmd)
        print(session.fulldata)
        time.sleep(2)

    print(session.fulldata)

    session.closeConnection()


if __name__ == "__main__":
    main()
