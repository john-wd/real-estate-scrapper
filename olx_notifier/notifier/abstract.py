from abc import ABCMeta


class BaseNotifier(metaclass=ABCMeta):
    def dispatch(message: str, **opts):
        raise NotImplementedError

    @classmethod
    def new(cls, *args, **kwargs):
        return cls(*args, **kwargs)
