#!/usr/bin/python
# -*- coding: UTF-8 -*-



def readConfiguration(path):
    """通过json配置文件, 获得配置信息.

    """
    f = open(path, 'r')
    data = f.readline()
    print(data)
    


# def _save_tsi2tempfile_(filename, data):
#     """后面程序的数据交换通过这个文件
#     """
#     with open(filename, 'w') as f:
#         # print('Type:', type(data))
#         f.write(str(data))


def main():
    readConfiguration('')

if __name__ == "__main__":
    main()

