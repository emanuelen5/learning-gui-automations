import time

class Timer:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.stop_time = time.time()
            print(f"{self.name} took {self.stop_time - self.start:.2f} seconds")
