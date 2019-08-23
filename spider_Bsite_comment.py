import requests
from bs4 import BeautifulSoup
import traceback
import re
import pandas as pd
import json


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
        return ""


def get_comment_info(oid, pn, headers):
    '''

    :param oid:
    :param pn:
    :param headers:
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
                # TODO  爬取进度条

                # 整理数据
                # TODO   爬取  评论点赞数  修改时间为时间轴
                data_list = json.loads(data_json)
                comment_dict = data_list["data"]["replies"]
                for j in range(0, 20):
                    dict_temp = {'mid': comment_dict[j]['mid'], 'uname': comment_dict[j]['member']['uname'],
                                 'sex': comment_dict[j]['member']['sex'], 'sign': comment_dict[j]['member']['sign'],
                                 'current_level': comment_dict[j]['member']['level_info']['current_level'],
                                 'vipType': comment_dict[j]['member']['vip']['vipType'],
                                 'vipDueDate': comment_dict[j]['member']['vip']['vipDueDate'],
                                 'ctime': comment_dict[j]['ctime'], 'rcount': comment_dict[j]['count'],
                                 'message': comment_dict[j]['content']['message']}
                    dict_comment.update({k: dict_temp})
                    k = k + 1
            except:
                traceback.print_exc()
                continue

    # 将整理后的将数据放入DataFrame中
    user_comment_data = pd.DataFrame(dict_comment).T  # 转置一下
    # user_comment_data.index = range((i - 1) * 20 + 1, (i - 1) * 20 + len(user_comment_data) + 1)  # 为数据重新编号

    # 将数据重新转为json后存储
    comment_data_json = user_comment_data.to_json(orient='index')
    with open('./data/total_comment.json', "w", encoding="utf-8") as file_data:
        file_data.write('\n')
        file_data.write(comment_data_json)

    return user_comment_data


def main():
    url = 'https://www.bilibili.com/bangumi/play/ep107656/'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/68.0.3440.106 Safari/537.36',
    }
    # 得到视频AV(oid)号
    start_html = get_html_text(url, headers)
    oid = re.findall(r'av\d+', start_html)[0][2:]

    # 得到视频评论总页数pn
    pn1_url = 'https://api.bilibili.com/x/v2/reply?type=1&pn=1&oid=' + oid
    pn1_html = get_html_text(pn1_url, headers)
    count = re.findall(r'20,"count":\d+', pn1_html)[0][11:]
    pn = float(count) / 20

    # 得到视频评论的json信息，并返回。
    user_comment_data = get_comment_info(oid, 5, headers)  # int(pn)
    a = user_comment_data


if __name__ == '__main__':
    main()
