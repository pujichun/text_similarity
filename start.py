import itertools
import os
import sys
import tkinter as tk
from typing import Iterable, Iterator, List

import jieba.analyse

from create_window import Window
from processing import Process
from save_similarity import XLSX
from sim import CosSim
from traverse_folder import Traverse


class Controller(Window):
    def __init__(self) -> None:
        self.process = Process()
        self.sim = CosSim()
        self.traverse = Traverse()
        super().__init__()
        self.text = tk.Text(self.window, width=20, height=2)

    def select_mode(self) -> None:
        font = ('console', '11')
        but1 = tk.Button(self.window, text="比较选中的两个文件", bg="SkyBlue", command=self.select_two_file, font=font)
        but1.place(x=90, y=150, width=150, height=50)
        self.text.place(x=250, y=160)
        but2 = tk.Button(self.window, text="比较选中文件与选中文件夹下的所有文件", bg="SkyBlue", command=self.select_file_and_folder, font=font)
        but2.place(x=50, y=300, width=300, height=50)
        but3 = tk.Button(self.window, text="选中文件夹下两两比较", bg="SkyBlue", command=self.many_to_many, font=font)
        but3.place(x=100, y=450, width=200, height=50)


    def combination(self, items: Iterable) -> Iterator[tuple]:
        self.log.info("文件两两组合完成")
        return itertools.combinations(items, 2)

    def save_source(self, data: List[dict]) -> None:
        self.log.info("正在存储文件之间的相似度")
        XLSX.save_excel(data=data)
        self.log.info("存储文件之间的相似度存储完成")

    def many_to_many(self):
        self.log.info("选择的模式为选中文件夹下的文件两两比较")
        folder = self.select_folder()
        self.log.info("选择文件夹完成，遍历文件夹下的文件")
        file_list = list(self.traverse.traverse(folder))
        self.log.info("文件遍历完成")

        similarity_list = list()
        for i, j in self.combination(file_list):
            self.log.info(f"开始比较{i}和{j}的相似度")
            d = dict()
            similarity = self.pairwise_comparison(path1=i, path2=j)
            self.log.info(f"{i}和{j}的相似度比较完成，相似度为{similarity}")
            d["文件1"] = i
            d["文件2"] = j
            d["相似度"] = similarity
            similarity_list.append(d)
        self.save_source(data=similarity_list)

    def one_to_many(self, path1: str, path_iterator: Iterator[str]) -> List[dict]:
        similarity_list = list()
        for i in path_iterator:
            self.log.info(f"开始比较{path1}和{i}的相似度")
            d = {}
            similarity = self.pairwise_comparison(path1=path1, path2=i)
            self.log.info(f"{path1}和{i}的相似度比较完成，相似度为{similarity}")
            d["文件1"] = os.path.splitext(path1)[0] + os.path.splitext(path1)[1]
            d["文件2"] = os.path.splitext(i)[0] + os.path.splitext(i)[1]
            d["相似度"] = similarity
            similarity_list.append(d)
        self.save_source(data=similarity_list)

    def pairwise_comparison(self, path1: str, path2: str) -> float:
        """
        pairwise comparison
        """
        sentence1, sentence2 = self.process.process(log=self.log, path1=path1, path2=path2)
        mmax_sim = list()
        for i in sentence1:
            sim_list = list()
            for j in sentence2:
                s = self.sim.sim(i, j)
                sim_list.append(s)
            mmax_sim.append(max(sim_list))
        return (sum(mmax_sim) / len(mmax_sim))

    def select_two_file(self):
        self.text.delete('1.0', 'end')
        self.log.info("选择的模式为选中的两个文件对比")
        path1 = self.select_file()
        if path1 == "":
            self.log.error("未选择文件，即将退出程序")
            sys.exit()
        path2 = self.select_file()
        if path2 == "":
            self.log.error("未选择文件，即将退出程序")
            sys.exit()
        self.log.info(f"已选择{path2}")
        self.log.info(f"开始比较{path1}和{path1}的相似度")
        s = self.pairwise_comparison(path1=path1, path2=path2)
        self.log.info(f"{path1}和{path2}的相似度比较完成，相似度为{s}")
        self.text.insert("end", f"{s}")

    def select_file_and_folder(self):
        self.log.info("选择的模式为选中的文件对比文件夹下的所有文件")
        path1 = self.select_file()
        folder = self.select_folder()
        path_iterator = self.traverse.traverse(folder)
        self.one_to_many(path1=path1, path_iterator=path_iterator)


if __name__ == "__main__":
    jieba.analyse.set_stop_words("./stopwords.txt")
    Controller().show()
