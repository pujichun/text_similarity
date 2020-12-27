import re
from typing import List

import jieba
import jieba.analyse

import jieba.analyse


class Splitter(object):
    """
    split content and sentence
    """

    @staticmethod
    def split_content(text: str) -> List[str]:
        sentence = re.split("[,.!?，。！？]", text)
        while "" in sentence or "\n" in sentence:
            try:
                sentence.remove("")
            except:
                sentence.remove("\n")
        return sentence

    @staticmethod
    def split_sentence(sentence: str) -> List[str]:
        jieba.analyse.set_stop_words("./stopwords.txt")
        word_list = list(jieba.cut(sentence=sentence, cut_all=False))
        keywords = jieba.analyse.extract_tags("|".join(word_list), topK=200, withWeight=False)
        return keywords

    def split(self, content) -> List[List[str]]:
        sentence = self.split_content(content)
        word_list = []
        for item in sentence:
            w = self.split_sentence(item)
            word_list.append(w)
        return word_list


if __name__ == "__main__":
    s = Splitter().split("函数得到的是仅当前路径下的文件名，不包括子目录中的文件，所有需要使用递归的方法得到全部文件名。")
    print(s)
