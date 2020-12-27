import sys
import tkinter as tk
from tkinter import filedialog

import log


class Window(object):
    def __init__(self) -> None:
        """
        create window and get file or folder 
        """
        self.log = log.get_logger()
        self.window = tk.Tk()
        self.window.title("文本相似度比较程序")

    def config(self) -> None:
        """
        window config
        """
        self.window.config(bg="LavenderBlush")
        width = 400
        height = 600
        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        self.window.geometry(alignstr)

    def select_mode(self) -> None:
        """
        create button for select mode
        """
        but1 = tk.Button(self.window, text="比较选中的两个文件", command=self.select_two_file, font=('console', '11'))
        but1.place(x=125, y=150, width=150, height=50)
        but2 = tk.Button(self.window, text="比较选中文件与选中文件夹下的所有文件", command=self.select_file_and_folder,
                         font=('console', '11'))
        but2.place(x=50, y=300, width=300, height=50)
        but3 = tk.Button(self.window, text="选中文件夹下两两比较", command=self.select_folder, font=('console', '11'))
        but3.place(x=100, y=450, width=200, height=50)

    def select_two_file(self):
        """
        select tow file mode
        """
        f1 = self.select_file()
        if f1 == "":
            sys.exit()
        f2 = self.select_file()
        if f2 == "":
            sys.exit()

    def select_file_and_folder(self):
        """
        select a file and a folder mode
        """
        self.select_file()
        self.select_folder()

    def select_file(self):
        self.log.info(f"正在选择文件")
        path = filedialog.askopenfilename(title="请选择文件",
                                          filetypes=[("word文档", "*.docx"), ("pdf文件", "*.pdf"), ("txt文件", "*.txt")])
        self.log.info(f"已选择{path}")
        return path

    def select_folder(self) -> str:
        """
        select folder and for two mode
        """
        self.log.info("正在选择文件")
        folder = filedialog.askdirectory(title="请选择文件夹")
        if folder == "":
            self.log.error("没有选择文件夹，即将退出！")
            sys.exit()
        self.log.info(f"已选取{folder}文件夹")
        return folder

    def show(self):
        """
        show window
        """
        self.config()
        self.select_mode()
        self.window.mainloop()


if __name__ == "__main__":
    window = Window()
    window.show()
