class PriorityQueue:
    def __init__(self, compare_index = 0):
        self.queue = []
        self.compare_index = compare_index
    def size(self):
        return len(self.queue)
    def put(self, element):
        iter = 0
        for item in self.queue:
            if item[self.compare_index] < element[self.compare_index]:
                self.queue.insert(iter, element)
                return
            iter+=1
        self.queue.append(element)
    def get(self):
        return self.queue.pop()

