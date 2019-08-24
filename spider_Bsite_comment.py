import requests
import traceback
import re
import pandas as pd
import json
import time


def get_html_text(url, headers, code='utf-8'):
    '''
    通过指定url链接获取html页面，编码方法默认为utf-8。有简单的错误处理，但不会提示。

    :param url: 指定url
    :param headers:头
    :param code: 默认为'utf-8'
    :return: 返回相应的html页面信息
    '''
    try:
        r = requests.get(url, headers, timeout=30)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        traceback.print_exc()
        print("获取html页面失败")
        return ""


def get_comment_info(oid, pn, headers):
    '''
    核心函数之一，爬取用户评论及相关数据并整理，使用DataFrame数据类型返回最终数据
    :param oid:视频id
    :param pn:评论页数
    :param headers:requests 头
    :return:
    '''
    start_url = 'https://api.bilibili.com/x/v2/reply?type=1&pn={}&oid=' + oid
    # 遍历爬取pn页评论
    dict_comment = {}
    k = 0
    for i in range(pn):
        if i != 0:
            try:
                # 爬取数据
                url = start_url.format(i)
                data_json = get_html_text(url, headers)
                # 爬取进度条
                print('\r当前进度：{:.2f}%'.format(i*100/pn), '[', '*'*int(i*50/pn),
                      '-' * int(50 - i * 50 / pn), ']', end='')
                # 整理数据
                data_list = json.loads(data_json)
                comment_dict = data_list["data"]["replies"]
                for j in range(0, 20):
                    dict_temp = {'mid': comment_dict[j]['mid'], 'uname': comment_dict[j]['member']['uname'],
                                 'sex': comment_dict[j]['member']['sex'], 'sign': comment_dict[j]['member']['sign'],
                                 'current_level': comment_dict[j]['member']['level_info']['current_level'],
                                 'vipType': comment_dict[j]['member']['vip']['vipType'],
                                 'vipDueDate': comment_dict[j]['member']['vip']['vipDueDate'],
                                 'ctime': comment_dict[j]['ctime'], 'rcount': comment_dict[j]['count'],
                                 'message': comment_dict[j]['content']['message'],
                                 'like': comment_dict[j]['like']}
                    # 修改时间戳 为 具体时间
                    timeTemp = dict_temp['ctime']
                    timeArray = time.localtime(timeTemp)
                    dict_temp['ctime'] = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    # 将数据存入主字典
                    dict_comment.update({k: dict_temp})
                    k = k + 1  # 为数据编号
            except:
                traceback.print_exc()
                continue

    # 爬取完成进度条
    print('\r当前进度：{:.2f}%'.format(100), '[', '*' * 50, ']', end='')

    # 将整理后的将数据放入DataFrame中
    user_comment_data = pd.DataFrame(dict_comment).T  # 转置一下
    # user_comment_data.index = range((i - 1) * 20 + 1, (i - 1) * 20 + len(user_comment_data) + 1)  # 为数据重新编号

    # data = pd.read_json(path, orient='index')
    return user_comment_data


def save_commment_to_json(datadf, data_name, path='./data/'):
    '''
    将数据datadf转为json文件后以data_name名称存储到path路径下

    :param datadf: 存储的文件（DataFrame）
    :param data_name:  数据名      ex: quanzhi_comment
    :param path: 文件存储的路径    ex : ./data/
    :return:
    '''
    # path = ./data/total_comment.json
    try:
        path = path+data_name+'.json'
        datadf_json = datadf.to_json(orient='index', force_ascii=False)
        with open(path, "w", encoding="utf-8") as file_data:
            file_data.write(datadf_json)
        return True
    except:
        traceback.print_exc()
        return False


def load_comment_from_json(data_name, path='./data/'):
    '''
    加载json评论数据，并且以DataFrame的数据结构返回
    :param data_name:
    :param path:
    :return:
    '''
    path = path+data_name+'.json'
    data = pd.read_json(path, orient='index')
    return data


def main():
    # url = 'https://www.bilibili.com/bangumi/play/ep107656/'       # 全职高手
    # url = 'https://www.bilibili.com/bangumi/play/ep277146/'       # 异常生物见闻录
    # url = 'https://www.bilibili.com/video/av13967569'
    # url = 'https://www.bilibili.com/bangumi/play/ss28296'           # 哈利波特
    url = 'https://www.bilibili.com/bangumi/play/ss12717/'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/68.0.3440.106 Safari/537.36',
    }
    start_html = get_html_text(url, headers)
    try:
        # 得到视频AV(oid)号
        oid = re.findall(r'av\d+|正片".{1,120}"aid":\d+', start_html)[0]
        oid = re.findall(r'av\d+|"aid":\d+', oid)[0]
        oid = re.findall(r'\d+', oid)[0]
        # 得到视频的Name
        AV_name = re.findall(r'<title>[\u4e00-\u9fa5|\d| |\w|·]+', start_html)[0][7:]
        # 得到视频评论总页数pn
        pn1_url = 'https://api.bilibili.com/x/v2/reply?type=1&pn=1&oid=' + oid
        pn1_html = get_html_text(pn1_url, headers)
        count = re.findall(r'20,"count":\d+', pn1_html)[0][11:]
        pn = float(count) / 20

        # 得到视频评论的DataFrame信息，并返回。
        user_comment_data = get_comment_info(oid, 10, headers)  # int(pn)
        save_commment_to_json(user_comment_data, AV_name)
    except:
        traceback.print_exc()
        print('爬取失败')


if __name__ == '__main__':
    main()
