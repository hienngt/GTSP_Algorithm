import numpy as np
import argparse


def GenerateData(points, goods, filename=None):
    goodsIdx = np.random.choice(points, goods, replace=False)
    typeList = np.random.randint(goods, size=points)
    for i in range(goods):
        typeList[goodsIdx[i]] = i

    goodsType = []
    for i in range(goods):
        tmpList = []
        for j in range(points):
            if typeList[j] == i:
                tmpList.append(j)
        goodsType.append(tmpList)

    graph = np.random.randint(60, 100, size=(points, points))
    graph = np.tril(graph) + np.tril(graph, -1).T

    for i in range(points):
        graph[i][i] = 0

    if filename is None:
        np.save('TypeList_' + str(points) + '_' + str(goods) + '.npy', typeList)
        np.save('GoodsType_' + str(points) + '_' + str(goods) + '.npy', goodsType)
        np.save('Graph_' + str(points) + '.npy', graph)
    else:
        np.save(filename + '_TypeList.npy', typeList)
        np.save(filename + '_GoodsType.npy', goodsType)
        np.save(filename + '_Graph.npy', graph)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pointNumber")
    parser.add_argument("-g", "--goodNumber")
    parser.add_argument("-o", "--file")
    args = parser.parse_args()

    if args.goodNumber is None and args.pointNumber is not None:
        print("Input error！")
        exit(1)
    elif args.goodNumber is not None and args.pointNumber is None:
        print("Input error！")
        exit(1)
    elif args.goodNumber is None and args.pointNumber is None:
        defaultList = [(9, 5), (17, 11), (24, 15), (31, 16), (39, 25)]

        for example in defaultList:
            GenerateData(example[0], example[1], filename=args.file)
    else:
        if args.goodNumber > args.pointNumber:
            print("Input error！")
            exit(1)
        else:
            GenerateData(args.pointNumber, args.goodNumber, filename=args.file)


if __name__ == "__main__":
    main()
