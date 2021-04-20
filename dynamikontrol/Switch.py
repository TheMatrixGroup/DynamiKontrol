class Switch(object):
    """Switch submodule class.

    .. highlight:: python
    .. code-block:: python

        from dynamikontrol import Module
        import time

        module = Module()

        def callback(string, angle):
            print(string)
            module.motor.angle(angle)

        module.switch.press(callback, ('Switched to on', 85,))
        module.switch.release(callback, ('Switched to off', 0,))

        while True:
            time.sleep(1)

        module.disconnect()

    Args:
        module (object): Module object.
    """
    def __init__(self, module):
        self.m = module


    def on(self, func, args=(), kwargs={}, ch=0):
        """Define callback function when switch is set to ``on`` status.

        Args:
            func (function): Callback function.
            args (tuple, optional): args. Defaults to ``()``.
            kwargs (dict, optional): kwargs. Defaults to ``{}``.
            ch (int, optional): Switch channel number. Must be ``0`` or ``1``. Defaults to ``0``.
        """
        if ch not in [0, 1]:
            raise ValueError('Switch channel number must be one of 0 and 1.')

        self.m._add_switch_cb_func(func, args, kwargs, ch, 'on')


    def off(self, func, args=(), kwargs={}, ch=0):
        """Define callback function when switch is set to ``off`` status.

        Args:
            func (function): Callback function.
            args (tuple, optional): args. Defaults to ``()``.
            kwargs (dict, optional): kwargs. Defaults to ``{}``.
            ch (int, optional): Switch channel number. Must be ``0`` or ``1``. Defaults to ``0``.
        """
        if ch not in [0, 1]:
            raise ValueError('Switch channel number must be one of 0 and 1.')

        self.m._add_switch_cb_func(func, args, kwargs, ch, 'off')


    def press(self, *args, **kwargs):
        """Define callback function when switch is pressed. Exactly same as ``on`` method.
        """
        self.on(*args, **kwargs)


    def release(self, *args, **kwargs):
        """Define callback function when switch is released. Exactly same as ``off`` method.
        """
        self.off(*args, **kwargs)
