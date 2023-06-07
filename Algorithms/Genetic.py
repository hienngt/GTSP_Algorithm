# coding: utf-8
import numpy as np
import random
from Algorithms import Algorithm
from timeit import default_timer as timer


class Genetic(Algorithm):
    def __init__(self, filename=None):
        super().__init__(filename)
        self.goodsType = list(self.goodsType)

    def set(self, population, crossRate, varyRate):
        """
        Parameters
        ----------
        population : int
        crossRate : float in (0,1)
        varyRate : float in (0,1)
        """
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
        if old_point >= self.points:
            print("Out of Index")
            exit(1)
        for goods in self.goodsType:
            if old_point in goods:
                return goods

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

        new_a = []
        new_b = []

        idx_a = [x for x in range(self.goods)]
        idx_b = idx_a.copy()

        aType = []
        bType = []
        for pointidx in range(len(a)):
            for goods in self.goodsType:
                if a[pointidx] in goods:
                    aType.append(self.goodsType.index(goods))
                    break

        for pointidx in range(len(b)):
            for goods in self.goodsType:
                if b[pointidx] in goods:
                    bType.append(self.goodsType.index(goods))
                    break

        a0 = a[:crossPoint]
        b0 = b[:crossPoint]

        for point in range(len(a0)):
            for goods in self.goodsType:
                if a0[point] in goods:
                    idx_b.append(bType[point])

        for point in range(len(b0)):
            for goods in self.goodsType:
                if b0[point] in goods:
                    idx_a.append(aType[point])

        for pointidx in range(len(aType)):
            if aType[pointidx] in idx_a:
                new_a.append(a[pointidx])

        for pointidx in range(len(bType)):
            if bType[pointidx] in idx_b:
                new_b.append(b[pointidx])

        new_a = new_a + b[crossPoint:]
        new_b = new_b + a[crossPoint:]

        return new_a, new_b

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

                # if len(opPoints) > 1:
                #     del opPoints[opPoints.index(vary_point)]

                tmp_individual.append(np.random.choice(opPoints))
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

    def check_same(self, lst, threshole=10):
        if len(lst) > threshole:
            return all(x == lst[-threshole] for x in lst[-threshole:])
        else:
            return False

    def fit(self, iteration, threshole=50):
        """
        Parameters
        ----------
        iteration : int
        """
        for i in range(iteration):
            cost = self._calculate_cost()
            self.result.append(min(cost))
            f = lambda x: 1 / x
            # newM = self.selection(cost, f)
            newM = self._vary(self.population)
            self.population = newM

            if self.check_same(self.result, threshole):
                print(f'number iteration: {i+1}')
                break


tic = timer()

g = Genetic('5gr21')
g.set(1000, 0, 1)
g.fit(2000)

print(g.result)

toc = timer()

print('cost:', toc - tic)
