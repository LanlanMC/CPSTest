import time as t


class Timer:
    """Timer class used in CPS Test"""
    def __init__(self, delta=10):
        self.start = t.time()
        self.delta = delta
    
    def is_end(self):
        return self.get_time() >= self.delta
    
    def get_time(self):
        return t.time() - self.start
