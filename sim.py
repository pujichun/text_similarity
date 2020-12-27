from typing import List

import numpy as np


class CosSim(object):
    @staticmethod
    def corpora(l1: List[str], l2: List[str]) -> List[str]:
        s = set(l1)
        s.update(l2)
        return list(s)

    @staticmethod
    def vectorization(s: List[str], l: List[str]) -> List:
        vector = []
        for c in s:
            vector.append(l.count(c))
        return vector

    def sim(self, l1: List[str], l2: List[str]) -> float:
        s = self.corpora(l1=l1, l2=l2)
        vector1 = np.array(self.vectorization(s=s, l=l1))
        vector2 = np.array(self.vectorization(s=s, l=l2))
        dist = np.linalg.norm(vector1 - vector2)
        si = 1.0 / (1.0 + dist)
        return si


if __name__ == '__main__':
    print(CosSim().sim(["我", "在", "睡觉"], ["我", "在", "吃饭", "吃饭"]))
