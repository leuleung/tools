#!/usr/bin/python
# -*- coding: UTF-8 -*-


def readConfiguration(path):
    """通过json配置文件, 获得配置信息.

    """
    info = []
    channle = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    f = open(path, 'r')
    data = f.readlines()
    for i in range(len(data)):
        if len(data[i].split()) == 64:
            info.append(data[i].split())
            # print(data[i].split())
            pass
        else:
            # print(data[i])
            pass

    for lines in range(len(info)):
        channle_index = 0  # 16个通道序列号
        for i in range(0, 63, 4):
            # print("Hello is", info[lines][0])
            for index in range(4):
                # print(info[lines][i+index])
                channle[channle_index].append(info[lines][i+index])
            channle_index = channle_index + 1
        pass

    channle_str = str(channle).replace("\'", "")
    # print(channle_str)
    channle_str = channle_str.replace("[", "")
    channle_str = channle_str.replace("], ", "\n")
    fp = open('hello.csv', 'w')
    fp.writelines(str(channle_str))


def main():
    readConfiguration('./data.txt')


if __name__ == "__main__":
    main()
