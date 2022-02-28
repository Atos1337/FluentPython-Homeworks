import codecs
import datetime
import multiprocessing
import sys
import time
from multiprocessing import Process
from threading import Thread


def A(q, child_conn):
    try:
        while True:
            s = q.get()
            child_conn.send(s.lower())
            time.sleep(5)
    except ValueError:
        pass
    finally:
        child_conn.close()


def B(child_conn, parent_conn):
    try:
        while True:
            s = parent_conn.recv()
            child_conn.send(codecs.encode(s, 'rot13'))
    except EOFError:
        pass
    finally:
        child_conn.close()


def send_messages(q):
    for line in sys.stdin:
        print(f"In message: {line} in {datetime.datetime.now()}")
        q.put(line)
    q.close()


def get_messages(parent_conn):
    try:
        global stop
        while not stop:
            s = parent_conn.recv()
            print(f"Out message: {s} in {datetime.datetime.now()}")
    except EOFError:
        pass


if __name__ == "__main__":
    sys.stdout = open("artifacts/hard-log.txt", 'w')
    q = multiprocessing.Queue()
    parent_conn_B, child_conn_A = multiprocessing.Pipe()
    parent_conn_main, child_conn_B = multiprocessing.Pipe()

    process_a = Process(target=A, args=(q, child_conn_A,))
    process_b = Process(target=B, args=(child_conn_B, parent_conn_B,))

    process_a.start()
    process_b.start()

    stop = False

    thread_send = Thread(target=send_messages, args=(q,))
    thread_get = Thread(target=get_messages, args=(parent_conn_main,), daemon=True)

    thread_send.start()
    thread_get.start()

    thread_send.join()
    process_a.kill()
    process_b.kill()
    sys.stdout.close()
