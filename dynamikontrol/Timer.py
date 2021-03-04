import time
from datetime import datetime, timezone
import threading

class Timer(object):
    """General timer class.
    """
    __stop_thread = False

    def __init__(self):
        pass

    def callback_after(self, func, args=(), kwargs={}, after=0, interval=None):
        """Call the callback function after specific time.

        Args:
            func (function): Callback function.
            args (tuple, optional): args. Defaults to ``()``.
            kwargs (dict, optional): kwargs. Defaults to ``{}``.
            after (int, optional): Callback delay time in seconds. Defaults to ``0``.
            interval (int, optional): Callback interval time in seconds. Defaults to ``None``.
        """
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
        """Call the callback function at specific time.

        Args:
            func (function): Callback function.
            args (tuple, optional): args. Defaults to ``()``.
            kwargs (dict, optional): kwargs. Defaults to ``{}``.
            at (datetime str, optional): Callback time in datetime str. e.g) ``2021-03-04 21:57:30``. Defaults to ``None``.
            interval ([type], optional): Callback interval time in seconds. Defaults to ``None``.
        """
        after = datetime.strptime(at, '%Y-%m-%d %H:%M:%S').timestamp() - datetime.now().timestamp()

        if after < 0:
            return False

        self.callback_after(func=func, args=args, kwargs=kwargs, after=after, interval=interval)

    def stop(self):
        """Stop the timer.
        """
        self.__stop_thread = True
