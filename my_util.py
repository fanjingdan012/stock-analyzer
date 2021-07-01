import os

def get_abs_path():
    dir=os.path.abspath(__file__)
    abs_dir = dir.replace('\\', '/')
    root_dir = abs_dir[:abs_dir.rfind("/")]
    return root_dir
get_abs_path()