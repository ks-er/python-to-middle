import threading
import uuid
from abc import abstractstaticmethod
from multiprocessing import Process, Queue, Manager
from time import sleep

class Composer:

    def __init__(self):
        self.result = None
        manager = Manager()
        dict = manager.dict()
        print(dict)
        self.back = Back(dict)
        self.front = Front(dict)

    def start(self):
        self.back.start()
        self.front.start()

    def stop(self):
        self.back.stop()
        self.front.stop()

    def get_front(self):
        return self.front

class Worker:

    def __init__(self, dict):
        self.worker = None
        self.dict = dict
        self.queue = Queue()

    def start(self):
        self.worker = Process(target=self._run, args=(self.dict, self.queue,))
        self.worker.start()

    def stop(self):
        self.worker.terminate()
        self.worker.join()

    @abstractstaticmethod
    def _run(manager, queue):
        pass

class Back(Worker):

    @staticmethod
    def _run(manager, queue):
        commands = {
            'sum': sum,
            'max': max,
            'min': min,
        }

        if (manager.items() is not None):
            while True:
                for id_, data in manager.items():

                    if not isinstance(data, tuple):
                        continue

                    cmd, *nums = data
                    command = commands.get(cmd)
                    if command:
                        manager[id_] = command(*nums)
                    else:
                        manager[id_] = None


class Front (Worker):

    def call_command(self, cmd, *args):
        id_ = str(uuid.uuid4())
        self.queue.put((id_, cmd, *args),)
        sleep(1)

        return id_

    def get_result(self, id_):
        return self.dict.pop(id_)

    @staticmethod
    def _run(manager, queue):

        def calculate(msg, mngr):
            id_, cmd, *nums = msg
            mngr[id_] = (cmd, *nums)

        while True:
            message = queue.get()
            if message:
                thread = threading.Thread(target=calculate, args=(message, manager))
                thread.start()
                thread.join()
