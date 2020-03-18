import socket


def search():
    """
    Retrieve program and database versions using clamd's ``VERSION``
    command.

    :return: JSON-structured response from clamd
    """
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect("/var/run/clamav/clamd.ctl")
    s.send(b"nVERSION\n")
    output = s.recv(4096)
    s.close()

    return {
        "output": output.decode("utf-8").strip(),
    }
