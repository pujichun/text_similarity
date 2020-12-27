import os
from typing import Iterator


class Traverse(object):

    @staticmethod
    def traverse(base_path) -> Iterator[str]:
        for root, _, fs in os.walk(base_path):
            for f in fs:
                if f.endswith('docx') or f.endswith('pdf') or f.endswith('txt'):
                    fullname = os.path.join(root, f)
                    yield fullname


if __name__ == "__main__":
    paths = Traverse().traverse(r"C:/Users/pujic/Desktop/新建文件夹")
    for path in paths:
        print(path)
