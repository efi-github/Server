# the Block ~~~ MAGIC ~~~
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


class Block:
    def __init__(self, data, prev = None):
        self.data = data
        self.prev = prev
        self.next = None

    def set_next(self, next):
        self.next = next

