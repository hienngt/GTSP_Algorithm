# coding: utf-8
import numpy as np
import random
from Algorithms import Algorithm
from timeit import default_timer as timer


class Genetic(Algorithm):
    def __init__(self, filename=None, threshole=1000, crossRate=0, varyRate=1, population=1000):
        super().__init__(filename)
        self.goodsType = list(self.goodsType)
        self.threshole = threshole
        self.crossRate = crossRate
        self.varyRate = varyRate
        self.population = self._generate_population(population)

    def _generate_population(self, M):
        """
        Parameters
        ----------
        M: int
        Returns
        -------
        population: list of list of int
        """
        population = []
        for _ in range(M):
            sPoints = []
            for opGoods in self.goodsType:
                sPoints.append(np.random.choice(opGoods))
            np.random.shuffle(sPoints)
            population.append(sPoints)
        return population

    def findPoints(self, old_point):
        """
        Parameters
        ----------
        old_points: int
        Returns
        -------
        goods: list of int
        """
        for goods in self.goodsType:
            if old_point in goods:
                return goods

    def random_choice(self, old_point, opPoints, iterations=5):
        a = np.random.choice(opPoints)
        i = 0
        while a == old_point and i < iterations:
            a = np.random.choice(opPoints)
            i = i + 1
        return a

    def _calculate_single_population(self, population):
        singleCost = 0
        for i in range(self.goods):
            singleCost += self.graph[population[i], population[(i + 1) % self.goods]]
        return singleCost

    def _calculate_cost(self):
        """
        Returns
        -------
        cost : list of int
        """
        cost = []
        for sPoint in self.population:
            cost.append(self._calculate_single_population(sPoint))
        return cost

    def selection(self, cost, func):
        """
        Parameters
        ----------
        Returns
        -------
        newM : list of list
        """
        prob = []
        for i in cost:
            prob.append(func(i))

        sum_prob = sum(prob)
        for i in range(len(cost)):
            prob[i] = prob[i] / sum_prob

        idx = [x for x in range(len(cost))]

        newM = []
        for _ in range(len(cost)):
            newM.append(self.population[np.random.choice(idx, p=prob)])
        return newM

    def _merge(self, a, b, crossPoint):
        """
        Parameters:
        ----------
        a : list of int
        b : list of int
        crossPoint : int
        Returns:
        -------
        new_a : list of int
        new_b : list of int
        """
        if crossPoint > len(a) or crossPoint > len(b):
            print("Error！")
            exit(1)

        aType = []
        bType = []
        for pointidx in range(crossPoint):
            for goods in self.goodsType:
                if a[pointidx] in goods:
                    aType.append(self.goodsType.index(goods))
                    break

        for pointidx in range(crossPoint):
            for goods in self.goodsType:
                if b[pointidx] in goods:
                    bType.append(self.goodsType.index(goods))
                    break

        if set(aType) == set(bType):
            new_a = b[:crossPoint] + a[crossPoint:]
            new_b = a[:crossPoint] + b[crossPoint:]

            if a == new_b or b == new_a:
                return a, b

            cost_new_a = self._calculate_single_population(new_a)
            cost_new_b = self._calculate_single_population(new_b)

            cost_a = self._calculate_single_population(a)
            cost_b = self._calculate_single_population(b)

            lst = [[a, cost_a], [b, cost_b], [new_a, cost_new_a], [new_b, cost_new_b]]

            sorted_lst = sorted(lst, key=lambda x: x[1])

            return sorted_lst[0][0], sorted_lst[1][0]
        else:
            return a, b

    def _vary(self, M):
        """
         Parameters:
         ----------
         M : list of list of int
        Returns
        -------
        newM : list of list of int
        """

        varyM = []
        for individual in M:
            if self.varyRate > np.random.rand():
                tmp_individual = []
                vary_point = np.random.choice(individual)
                vary_point_idx = individual.index(vary_point)
                tmp_individual += individual[:vary_point_idx]
                opPoints = self.findPoints(vary_point)

                tmp_individual.append(self.random_choice(vary_point, opPoints))

                tmp_individual += individual[vary_point_idx + 1:]
                cost_old = self._calculate_single_population(individual)
                cost_new = self._calculate_single_population(tmp_individual)
                if cost_new < cost_old:
                    varyM.append(tmp_individual)
                else:
                    varyM.append(individual)
            else:
                varyM.append(individual)

        newM = []
        while varyM:
            a = random.choice(varyM)
            varyM.remove(a)
            if not varyM:
                newM.append(a)
                return newM
            b = random.choice(varyM)
            varyM.remove(b)
            if self.crossRate > np.random.rand():
                crossPoint = np.random.randint(1, self.goods)
                a1, b1 = self._merge(a, b, crossPoint)
                newM.append(a1)
                newM.append(b1)
            else:
                newM.append(a)
                newM.append(b)
        return newM

    def check_same(self, lst):
        if len(lst) > self.threshole:
            return all(x == lst[-self.threshole] for x in lst[-self.threshole:])
        else:
            return False

    def fit(self, iteration, value=None):
        """
        Parameters
        ----------
        iteration : int
        """
        check_value_time = 0
        for i in range(iteration):
            cost = self._calculate_cost()
            self.result.append(min(cost))
            f = lambda x: 1 / x
            # newM = self.selection(cost, f)
            newM = self._vary(self.population)
            self.population = newM

            t1 = timer()
            if value is not None:
                if min(self.result) == value:
                    return check_value_time, i
            t2 = timer()
            check_value_time = check_value_time + t2 - t1
            # if self.check_same(self.result):
            #     print(f'number iteration: {i + 1}')
            #     break
        return 100000000, iteration

g = Genetic('8ftv38', 800, 0.2, 1, 1000)
tic = timer()
a = g.fit(5000, 511)

# print(g.result)

toc = timer()

print('cost:', toc - tic)
