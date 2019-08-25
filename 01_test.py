import pandas as pd
import json
import traceback
import matplotlib.pyplot as plt


def load_comment_from_json(data_name, path='./data/'):
    '''
    加载json评论数据，并且以DataFrame的数据结构返回
    :param data_name:
    :param path:
    :return:
    '''
    path = path+data_name+'.json'
    data = pd.read_json(path, orient='index', encoding='utf-8')
    return data


def gender_pie(datadf):
    labels = '男', '女', '保密'
    pass


def main():
    data_name = '全职高手 第一季'
    datadf = load_comment_from_json(data_name)
    print(datadf)
    data_dict = {'男': 0, '女': 0, '保密': 0}
    for i in datadf['sex'].values:
        data_dict[i] = data_dict[i] + 1
        



if __name__ == '__main__':
    main()
