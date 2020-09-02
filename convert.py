from multiprocessing import Process, Queue
from config import Config
from db.oracle import Oracle

config = Config()
queue = Queue(int(config.RUNTIME_CONFIG.get("BUFFER")))


class DataHandler(object):

    def __init__(self, source, target):
        self.queue = Queue(config.TARGET_CONN.get("BUFFER"))
        self.source = source
        self.target = target


def producer():
    o = Oracle(**config.SOURCE_CONN)
    generator = o.generate_all_table_data()
    for row in generator:
        queue.put(row)


def consumer():
    while True:
        row = queue.get()
        if row:
            print(row)


if __name__ == '__main__':
    print('hello world')

    pro = Process(target=producer)
    con = Process(target=consumer)
    pro.start()
    con.start()
