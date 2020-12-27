from typing import List

import pandas as pd


class XLSX(object):
    @staticmethod
    def save_excel(data: List) -> None:
        df = pd.DataFrame(data)
        df.to_excel("相似度结果.xlsx", index=False)
