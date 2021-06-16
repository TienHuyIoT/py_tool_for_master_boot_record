import os


def force_make(dir_):
    if not os.path.exists(dir_) and dir_ != '':
        os.makedirs(dir_)


def get_abspath(base, path):
    if os.path.isabs(path):
        return path
    else:
        return os.path.normpath(os.path.join(base, path))
