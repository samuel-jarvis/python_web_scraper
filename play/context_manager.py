import contextlib


class JarvisFile:
    def __init__(self, fileName, content):
        self.fileName = fileName

    def __enter__(self):
        self.file = open(self.fileName, 'w')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        return False


@contextlib.contextmanager
def jarvis_file(fileName, content):
    file = open(fileName, 'w')
    try:
        yield file
    finally:
        if file:
            file.close()
