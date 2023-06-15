# coding: utf-8
import re

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

PATH_DIR = BASE_DIR / 'data/GTSP_asymmetric/edge_weight_section'


class Algorithm():
    def __init__(self, filename=None):
        self.filename = filename
        numbers = re.findall(r'\d+', self.filename)  # file like 4gr17.gtsp -> group = 4, city = 17

        self.points = int(numbers[1])
        self.goods = int(numbers[0])
        self.result = []

        self.graph = np.load(PATH_DIR / f'{filename}_Graph_{self.points}_{self.goods}.npy', allow_pickle=True)
        self.goodsType = np.load(PATH_DIR  / f'{filename}_GoodsType_{self.points}_{self.goods}.npy',
                                 allow_pickle=True)
        self.typeList = np.load(PATH_DIR / f'{filename}_TypeList_{self.points}_{self.goods}.npy',
                                allow_pickle=True)

    def fit(self, iteration):
        pass

    def show_result(self):
        sns.set(style="white", palette="muted")
        x = [i + 1 for i in range(len(self.result))]
        y = self.result

        plt.plot(x, y)
        plt.show()
