import time
from socket import socket
from threading import Thread, Event


IP = "192.168.118.202"
PORT = 41

MESSAGES = [
    "39 00 13E0",
    "39 01 01 010101010101 49D0",
    "39 04 00 A30D",
    "39 08 00 A60D",
    "00 08 05 B603",
    "39 05 31 00 0929",
    "39 15 00 00 1D7C",
]


def with_limit(limit: int):
    """
    Выполняет функцию в другом треде в течение `limit` секунд.
    """

    def _wrapper(func):
        def _with_limit(*args, **kwargs):
            def _th_func():
                func(*args, **kwargs)
                event.set()

            event = Event()
            th = Thread(target=_th_func, daemon=True)
            th.start()
            time.sleep(limit)

            if event.is_set():
                return True
            else:
                th._is_stopped = True
                th._tstate_lock = None
                return False

        return _with_limit
    return _wrapper


@with_limit(1)
def read(sock):
    """
    Пытается считать 256 байт ответа и выводит их.
    """

    response = sock.recv(256)
    data = response.hex()
    data = data[:2] + " " + data[2:]

    print(f"raw    | {response}")
    print(f"answer | {data}")


def send(port=PORT):
    with socket() as sock:
        print(f"testing {IP} / {PORT}\n")
        sock.connect((IP, port))

        for (n, msg) in enumerate(MESSAGES):
            sock.send(bytes.fromhex(msg))
            print(f"{port} sent {n} >| {msg}")

            is_succ = read(sock)
            if not is_succ:
                print("<no awswer>")
            print()


if __name__ == '__main__':
    send()
