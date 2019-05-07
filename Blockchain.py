# The Blockchain ~~~ MAGIC ~~~
import Block
import Data

class Blockchain:
    def __init__(self):
        self.root = Block.Block(Data.Data("0000", "0000", "Head", 0, "Head", "???"))
        self.head = self.root

    def add_block(self, data):
        new_block = Block.Block(data, self.head)
        self.head.next = new_block
        self.head = new_block

    def check_block(self):
        pass

    def get_head(self):
        return self.head.data
