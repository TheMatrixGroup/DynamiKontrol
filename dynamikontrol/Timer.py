import time
from datetime import datetime, timezone
import threading

class Timer(object):
    __stop_thread = False

    def __init__(self):
        pass

    def callback_after(self, func, args=(), kwargs={}, after=0, interval=None):
        self.__stop_thread = False
        if interval is None:
            self.__stop_thread = True

        def handler():
            time.sleep(after)
            func(*args, **kwargs)

            next_call = time.time()
            while True:
                if self.__stop_thread:
                    break

                next_call = next_call + interval
                time.sleep(max(next_call - time.time(), 0))
                func(*args, **kwargs)

        timer_thread = threading.Thread(target=handler)
        timer_thread.start()

    def callback_at(self, func, args=(), kwargs={}, at=None, interval=None):
        after = datetime.strptime(at, '%Y-%m-%d %H:%M:%S').timestamp() - datetime.now().timestamp()

        if after < 0:
            return False

        self.callback_after(func=func, args=args, kwargs=kwargs, after=after, interval=interval)

    def stop(self):
        self.__stop_thread = True

if __name__ == '__main__':
    t1 = Timer()
    t2 = Timer()

    def print_time(a, b):
        print(a, b, datetime.now())

    t1.callback_at(func=print_time, args=('AAAAAA',), kwargs={'b': 'bb'}, at='2021-02-19 17:16:30', interval=0.1)

    t1.callback_after(func=print_time, args=('t1',), kwargs={'b': 't11'}, after=0.1, interval=0.1)
    t2.callback_after(func=print_time, args=('t2',), kwargs={'b': 't22'}, after=3, interval=0.1)

    time.sleep(5)

    t1.stop()


