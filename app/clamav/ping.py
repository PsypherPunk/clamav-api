import socket


def search():
    """
    Check the server's state using clamd's ``PING`` command. It should
    reply with "PONG".

    :return: JSON-structured response from clamd
    """
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect("/var/run/clamav/clamd.ctl")
    s.send(b"nPING\n")
    output = s.recv(4096)
    s.close()

    return {
        "output": output.decode("utf-8").strip(),
    }
