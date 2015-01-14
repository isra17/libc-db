import os

class ChDir:
    """Context manager for changing the current working directory"""
    def __init__(self, new_dir):
        self.new_dir = new_dir

    def __enter__(self):
        self.old_dir = os.getcwd()
        os.chdir(self.new_dir)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.old_dir)

