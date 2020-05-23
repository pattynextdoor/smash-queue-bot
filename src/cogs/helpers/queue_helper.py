class Queue:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.isOpen = True
        self.list = []
        self.cap = 10
    
    def add(self, name):
        if(self.__name_is_in_queue(name)):
            raise RuntimeError('Name is already in the queue.')
        
        if (len(self.list) == self.cap):
            raise RuntimeError('Could not add new player due to exceeding capacity.')
        
        self.list.append(name)

    def remove(self, name):
        if not self.__name_is_in_queue(name):
            raise RuntimeError('Specified name is not in the queue.')
        self.list.remove(name)

    def __name_is_in_queue(self, name):
        return name in self.list
