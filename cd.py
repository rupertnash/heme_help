from __future__ import print_function
from contextlib import contextmanager
import os

@contextmanager
def cd(path):
    orig_path = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(orig_path)


def test():
    cur_dir = os.getcwd()
    target = os.path.abspath(os.path.expanduser('~/..'))
    
    with cd(target):
        assert os.getcwd() == target

    assert os.getcwd() == cur_dir
    print("OK!")
    
if __name__ == "__main__":
    test()
    
