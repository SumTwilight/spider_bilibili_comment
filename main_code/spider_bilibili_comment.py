import requests
import traceback
import re
import pandas as pd
import json
import time
import os
from os import path
from PyQt5.QtCore import QThread, pyqtSignal

FAILED_SPIDER = 0  # TODO 等待自己定义一个常量类
FAILED_SAVING = -1
OVERFLOW_ERROR = -2


class SpiderThread(QThread):
    finished_signal = pyqtSignal()
    log_signal = pyqtSignal(str)
    result_signal = pyqtSignal(dict)
    progressbar_signal = pyqtSignal(int, int)
    error_signal = pyqtSignal(int)

    # html info
    URL = ''
    oid = ''
    Av_name = ''
    spider_pn = 0
    count_pn = 0
    img = ''
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.99 Safari/537.36',
        'Referer': 'https://www.bilibili.com/video/av51259023'
    }

    def __init__(self):
        super(SpiderThread, self).__init__()

    def get_html_text(self, URL, code='utf-8'):
        """
        通过指定url链接获取html页面，编码方法默认为utf-8。有简单的错误处理，但不会提示。

        :param URL: 指定URL
        :param code: 默认为'utf-8'
        :return: 返回相应的html页面信息
        """
        try:
            r = requests.get(URL, headers=self.headers, timeout=30)
            r.raise_for_status()
            r.encoding = code
            return r.text
        except:
            traceback.print_exc()
            self.log_signal.emit("获取html页面失败")
            return FAILED_SPIDER

    def get_comment_info(self, oid, pn):
        """
        核心函数，爬取用户评论及相关数据并整理，使用DataFrame数据类型返回最终数据
        :param oid:视频id
        :param pn:评论页数
        :return:
        """
        start_url = 'https://api.bilibili.com/x/v2/reply?type=1&pn={}&oid=' + oid
        # 遍历爬取pn页评论
        dict_comment = {}
        k = 0
        for i in range(pn):
            if i != 0:
                try:
                    # 爬取数据
                    URL = start_url.format(i)
                    data_json = self.get_html_text(URL)
                    # 爬取进度条
                    # print('\r当前进度：{:.2f}%'.format(i * 100 / pn), '[', '*' * int(i * 50 / pn),
                    #       '-' * int(50 - i * 50 / pn), ']', end='')
                    # self.log_signal.emit('\r当前进度：{:.2f}%'.format(i * 100 / pn) + '[' + '*' * int(i * 50 / pn) +
                    #                      '-' * int(50 - i * 50 / pn) + ']')
                    self.progressbar_signal.emit(i, pn)
                    # 整理数据
                    data_dict = json.loads(data_json)
                    comment_dict = data_dict["data"]["replies"]
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
                        dict_temp['ctime'] = time.strftime("%Y-%m-%d %H:%M", timeArray)
                        self.result_signal.emit(dict_temp)  # 传送信号过去打印 TODO 不一定适合放在这里
                        dict_temp['ctime'] = time.strftime("%Y-%m-%d", timeArray)
                        dict_temp['ctime_time'] = time.strftime("%H:%M:%S", timeArray)
                        timeTemp = int(dict_temp['vipDueDate'] / 1000)
                        timeArray = time.localtime(timeTemp)
                        dict_temp['vipDueDate'] = time.strftime("%Y-%m-%d", timeArray)
                        # 将数据存入主字典
                        dict_comment.update({k: dict_temp})
                        k = k + 1  # 为数据编号
                except:
                    traceback.print_exc()
                    continue

        # 爬取完成进度条
        # print('\r当前进度：{:.2f}%'.format(100), '[', '*' * 50, ']')
        # self.log_signal.emit('\r当前进度：{:.2f}%'.format(100) + '[' + '*' * 50 + ']')
        self.progressbar_signal.emit(pn, pn)

        # 将整理后的将数据放入DataFrame中
        user_comment_data = pd.DataFrame(dict_comment).T  # 转置一下
        return user_comment_data

    def save_comment_to_json(self, datadf, data_name, img, data_path='./data/'):
        """
        1）将数据datadf转为json文件后以data_name为名称存储到data_path路径下
        2）从datadf中提取出评论信息以data_name为名称存储到'./data/comment_data/'路径下
        3）将对应的图片img以data_name为名称存储到'./data/image/'路径下
        :param datadf: 存储的文件（DataFrame）
        :param data_name:  数据名      ex: quanzhi_comment
        :param img:
        :param data_path: 文件存储的路径    ex : ./data/
        :return:
        """
        # path = ./data/total_comment.json
        self.log_signal.emit('爬取完成，保存数据中.....')
        try:
            # 写入完整json数据
            if not path.exists(data_path):
                os.makedirs(data_path)
            data_path = data_path + data_name + '.json'
            datadf_json = datadf.to_json(orient='index', force_ascii=False)
            with open(data_path, "w", encoding="utf-8") as file_data:
                file_data.write(datadf_json)
            self.log_signal.emit('评论用户数据已保存在：' + data_path)
        except:
            traceback.print_exc()
            self.log_signal.emit('json信息写入出错。')
            return FAILED_SAVING

        try:
            # 写入评论数据
            data_path = './data/comment_data/'
            if not path.exists(data_path):
                os.makedirs(data_path)
            data_path += data_name + '.txt'
            with open(data_path, "w", encoding="utf-8") as file_data:
                for i in datadf['message']:
                    file_data.write(i)
                    file_data.write('\n')
            self.log_signal.emit('评论数据已保存在：' + data_path)
        except:
            traceback.print_exc()
            self.log_signal.emit('评论数据写入出错。')
            return FAILED_SAVING

        try:
            # 保存图片信息       这部分暂时没用了
            img_path = './data/image/'
            if not path.exists(img_path):
                os.makedirs(img_path)
            img_path += data_name
            with open(img_path + '.jpg', 'wb') as f:
                f.write(img)
            self.log_signal.emit('视频图片已保存在：' + img_path + '.jpg')
            # 使用remove API 去掉图片的背景
            # response = requests.post(
            #     'https://api.remove.bg/v1.0/removebg',
            #     files={'image_file': open(img_path+'.jpg', 'rb')},
            #     data={'size': 'auto'},
            #     headers={'X-Api-Key': '52U8DP5PkSg6HhxmJzQcJbdf'},
            # )
            # if response.status_code == requests.codes.ok:
            #     with open(img_path+'.jpg', 'wb') as out:
            #         out.write(response.content)
            # else:
            #     print("Error:图片背景去除失败")
        except:
            traceback.print_exc()
            self.log_signal.emit('图片数据写入出错')
            return FAILED_SAVING
        return True

    @staticmethod
    def load_comment_from_json(data_name, data_path='./data/'):
        '''
        加载json评论数据，并且以DataFrame的数据结构返回
        :param data_name:
        :param data_path:
        :return:
        '''
        data_path = data_path + data_name + '.json'
        data = pd.read_json(data_path, orient='index', encoding='utf-8')
        return data

    @property
    def get_av_info(self):
        try:
            start_html = self.get_html_text(self.URL)
            # with open('./start.html', 'w', encoding='utf-8') as f:
            #     f.write(start_html)
        except:
            traceback.print_exc()
            self.log_signal.emit('100：初始页面爬取失败，请换一个视频链接')
            return FAILED_SPIDER
        try:
            # 得到视频AV(oid)号
            self.oid = re.findall(r'av\d+|正片".{1,120}"aid":\d+', start_html)[0]
            self.oid = re.findall(r'av\d+|"aid":\d+', self.oid)[0]
            self.oid = re.findall(r'\d+', self.oid)[0]
            self.log_signal.emit('视频id：' + self.oid)
            # 得到视频的Name
            self.Av_name = re.findall(r'<title>[\u4e00-\u9fa5|\d| |\w|·|，|【|】|,|\[|\]|!]+'
                                      r'|name="title" content=".+bilibili'
                                      , start_html)[0][:100]
            if self.Av_name[0:7] == '<title>':
                self.Av_name = self.Av_name[7:]
            else:
                self.Av_name = re.findall(r't=".+bilibili', self.Av_name)[0][3:-26]
            self.log_signal.emit('视频名称：' + self.Av_name)
            # 得到视频的图片
            self.img = re.findall(r'og:image".+g">', start_html)[0]
            self.img = re.findall(r'http.+g', self.img)[0]
            self.img = requests.get(self.img).content  # TODO 图片暂时还没用
            # 得到视频评论总页数pn
            pn1_url = 'https://api.bilibili.com/x/v2/reply?type=1&pn=1&oid=' + self.oid
            pn1_html = self.get_html_text(pn1_url)
            count = re.findall(r'20,"count":\d+', pn1_html)[0][11:]
            pn = int(float(count) / 20)
            self.count_pn = pn
            self.log_signal.emit('评论总页数：' + str(pn) + '\n请输入爬取页数：')
        except:
            traceback.print_exc()
            self.log_signal.emit('200：获取视频信息失败')
            return FAILED_SPIDER
        pass

    def main_spider(self):
        '''
        :return:
        '''
        try:
            if int(self.spider_pn) <= int(self.count_pn):
                user_comment_data = self.get_comment_info(self.oid, int(self.spider_pn))  # int(pn)
            else:
                error_signal.emit(1)  # 页数上溢
                return OVERFLOW_ERROR
        except:
            traceback.print_exc()
            self.log_signal.emit('300：获取评论数据失败')
            return FAILED_SPIDER

        try:
            self.save_comment_to_json(user_comment_data, self.Av_name, self.img)
        except:
            # traceback.print_exc()
            self.log_signal.emit('400：保存爬取数据失败')
            return FAILED_SAVING
        return True

    def run(self):
        flag = self.main_spider()

        if flag == FAILED_SPIDER:  # 在log中打印 爬虫失败
            self.log_signal.emit('状态码返回错误：爬虫失败')
        elif flag == FAILED_SAVING:  # 在log中打印 保存失败
            self.log_signal.emit('状态码返回错误：保存失败')
        elif flag == OVERFLOW_ERROR:
            pass
        else:
            self.finished_signal.emit()
            self.log_signal.emit('视频名称：' + str(self.Av_name) + '\n爬取成功')  # 在log中打印 爬虫成功


if __name__ == '__main__':
    pass
