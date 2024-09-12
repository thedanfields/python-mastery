from typing import Any


class Descriptor:
    def __init__(self, name: str):
        self.name = name

    def __get__(self, instance: object, cls: type):
        print("%s:__get__" % self.name)

    def __set__(self, instance: object, value: Any):
        print("%s:__set__ %s" % (self.name, value))

    def __delete__(self, instance: object):
        print("%s:__delete__" % self.name)
