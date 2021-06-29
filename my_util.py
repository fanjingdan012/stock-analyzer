def get_abs_path(dir):
    abs_dir = dir.replace('\\', '/')
    root_dir = abs_dir[:abs_dir.rfind("/")]
    return root_dir