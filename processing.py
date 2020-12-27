from typing import List, Tuple

import log
import read_source
from split import Splitter


class Process(object):

    def __init__(self) -> None:
        self.splitter = Splitter()

    def process(self, log, path1: str, path2: str) -> Tuple[List]:
        log.info("开始分割文章")
        content1, content2 = read_source.read(path1), read_source.read(path2)
        sentence1, sentence2 = self.splitter.split(content1), self.splitter.split(content2)
        log.info("分割文章完成")
        return sentence1, sentence2
