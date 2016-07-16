import os
from functools import wraps


def lockfile_manager(lockfile):
    def _lockfile_manager(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            manager = LockfileManager(lockfile)
            if manager.lockfile_exists():
                raise RuntimeError('lockfile exists.')
            manager.create_lockfile()
            func(*args, **kwargs)
            manager.delete_lockfile()
        return wrapper
    return _lockfile_manager


class LockfileManager:

    def __init__(self, lockfile):
        self.lockfile = lockfile

    def create_lockfile(self):
        with open(self.lockfile, 'w'):
            pass

    def delete_lockfile(self):
        return os.remove(self.lockfile)

    def lockfile_exists(self):
        return os.path.exists(self.lockfile)