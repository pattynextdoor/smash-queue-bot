class Queue:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.isOpen = True
        self.list = []
