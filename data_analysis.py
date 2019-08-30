import pandas as pd
import json
import traceback
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from wordcloud import WordCloud
import os
from os import path
import jieba
from PIL import Image
import numpy as np


plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
datadf = pd.DataFrame()
text = ''


def load_comment_from_json(data_name, data_path='./data/'):
    """
    加载json评论数据，并且以DataFrame的数据结构返回
    :param data_path:
    :param data_name:
    :return:
    """
    try:
        # 获取用户+评论数据
        user_data_path = data_path + data_name + '.json'
        datadf = pd.read_json(user_data_path, orient='index', encoding='utf-8')
    except:
        # traceback.print_exc()
        print('加载用户评论数据失败')
        return 0
    data_path = './data_analysis/' + data_name + '/'
    if not path.exists(data_path):
            os.makedirs(data_path)
    return datadf


def load_comment_data(data_name, data_path='./data/'):
    try:
        # 获取评论数据
        comment_data_path = data_path + 'comment_data/' + data_name + '.txt'
        with open(comment_data_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except:
        print('加载评论数据失败')
        return 0, 0
    return text


def level_pie(data_name):
    """
        输出用户等级的饼图
        :param data_name:
        :param datadf:
        :return:
    """
    global datadf, text
    try:        
        data_dict = {'小于4级': 0, '4级': 0, '5级': 0, '6级': 0}
        for i in datadf['current_level']:
            if i < 4:
                data_dict['小于4级'] += 1
            elif i == 4:
                data_dict['4级'] += 1
            elif i == 5:
                data_dict['5级'] += 1
            elif i == 6:
                data_dict['6级'] += 1

        explode = (0, 0, 0, 0.03)
        plt.pie(data_dict.values(), explode=explode, labels=tuple(data_dict.keys()),
                autopct='%.1f%%', labeldistance=0.8, startangle=90,
                colors=('#22a2c3', '#eba0b3', '#83cbac', '#894276'))  # TODO 颜色
        plt.axis('equal')  # 让图像保持圆形
        plt.legend(loc="upper right", fontsize=13, bbox_to_anchor=(1.1, 1.05), borderaxespad=0.3)
        plt.title('Level Analysis')
        save_path = "./data_analysis/" + data_name + "/level_pie_" + data_name + ".jpg"
        plt.savefig(save_path, dpi=600)
        # save_path = os.getcwd() + save_path[1:]
        # os.startfile(save_path)
        plt.show()
    except:
        traceback.print_exc()


def member_pie(data_name):
    """
        输出会员构成的饼图
        :param data_name:
        :param datadf:
        :return:
    """
    global datadf, text
    try:
        data_dict = {'普通会员': 0, '月大会员': 0, '年大会员': 0}
        for i in datadf['vipType']:
            if i == 0:
                data_dict['普通会员'] += 1
            elif i == 1:
                data_dict['月大会员'] += 1
            elif i == 2:
                data_dict['年大会员'] += 1

        explode = (0, 0, 0.03)
        plt.pie(data_dict.values(), explode=explode, labels=tuple(data_dict.keys()),
                autopct='%.1f%%', labeldistance=0.8, startangle=90,
                colors=('#22a2c3', '#eba0b3', '#83cbac'))   # TODO 颜色
        plt.axis('equal')  # 让图像保持圆形
        plt.legend(loc="upper right", fontsize=13, bbox_to_anchor=(1.1, 1.05), borderaxespad=0.3)
        plt.title('Member Analysis')
        save_path = "./data_analysis/" + data_name + "/Member_pie_" + data_name + ".jpg"
        plt.savefig(save_path, dpi=600)
        # save_path = os.getcwd() + save_path[1:]
        # os.startfile(save_path)
        plt.show()
        print('会员分析饼图已保存：./data_analysis/' + data_name + '/Member_pie_' + data_name + '.jpg')
    except:
        traceback.print_exc()


def gender_pie(data_name):
    '''
    输出男女性别的饼图
    :param data_name:
    :param datadf:
    :return:
    '''
    global datadf, text
    try:
        data_dict = {'男': 0, '女': 0, '保密': 0}
        for i in datadf['sex'].values:
            data_dict[i] += 1
        explode = (0, 0, 0.03)
        plt.pie(data_dict.values(), explode=explode, labels=tuple(data_dict.keys()),
                autopct='%.1f%%', labeldistance=0.8, startangle=90,
                colors=('#22a2c3', '#eba0b3', '#83cbac'))
        # labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
        # autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
        # shadow，饼是否有阴影
        # startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
        # pctdistance，百分比的text离圆心的距离
        # patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本

        # 改变文本的大小
        # 方法是把每一个text遍历。调用set_size方法设置它的属性

        plt.axis('equal')  # 让图像保持圆形

        plt.legend(loc="upper right", fontsize=13, bbox_to_anchor=(1.1, 1.05), borderaxespad=0.3)
        # loc =  'upper right' 位于右上角
        # bbox_to_anchor=[0.5, 0.5] # 外边距 上边 右边
        # ncol=2 分两列
        # borderaxespad = 0.3图例的内边距

        plt.title('Gender Analysis')
        #  plt.savefig("./data_analysis/Gender_pie.jpg", dpi=600)
        save_path = "./data_analysis/" + data_name + "/Gender_pie_" + data_name + ".jpg"
        plt.savefig(save_path, dpi=600)
        # save_path = os.getcwd() + save_path[1:]
        # os.startfile(save_path)
        plt.show()
        print('性别分析饼图已保存：./data_analysis/' + data_name + '/Gender_pie_' + data_name + '.jpg')
    except:
        traceback.print_exc()


def ctime_analysis_based_day(data_name):
    '''
    输出以日为单位的评论数的折线图
    :param data_name:
    :return:
    '''
    global datadf, text
    try:
        data_dict = {}
        for i in datadf['ctime'].values:
            k = i[5:]
            if k in data_dict.keys():
                data_dict[k] += 1
            else:
                data_dict[k] = 1
        ax = plt.subplot(111)
        ax.plot(data_dict.keys(), data_dict.values())
        # TODO 修改曲线的颜色类型
        # 通过这四句话来控制 x，y轴的密度  ticker.MultipleLocater()给出的数字明确控制刻度线间距，允许自动限制确
        length = len(data_dict)
        # 设置 x 密度

        xtick_spacing = int(length/13) + 1
        ax.xaxis.set_major_locator(ticker.MultipleLocator(xtick_spacing))
        ytick_spacing = int(round(max(data_dict.values())/150)*10)+10
        if ytick_spacing < 11:
            ytick_spacing = 1
        ax.yaxis.set_major_locator(ticker.MultipleLocator(ytick_spacing))

        ax.set_title("Comment Time Analysis Based Day")
        save_path = "./data_analysis/" + data_name + "/CTime(day)_line_chart_" + data_name + ".jpg"
        plt.savefig(save_path, dpi=600)
        save_path = os.getcwd() + save_path[1:]
        # os.startfile(save_path)
        plt.show()
        print('评论时间(day)分析折线图已保存：./data_analysis/' + data_name + '/CTime(day)_line_chart_' + data_name + '.jpg')
    except:
        traceback.print_exc()


def ctime_analysis_based_hour(data_name):
    '''
    输出以小时为单位的评论数的折线图
    :param data_name:
    :param datadf:
    :return:
    '''
    global datadf, text
    try:
        data_dict = {'05': 0, '04': 0, '03': 0, '02': 0, '01': 0, '00': 0, '23': 0, '22': 0,
                     '21': 0, '20': 0, '19': 0, '18': 0, '17': 0, '16': 0, '15': 0, '14': 0,
                     '13': 0, '12': 0, '11': 0, '10': 0, '09': 0, '08': 0, '07': 0, '06': 0}
        for i in datadf['ctime_time'].values:
            k = i.astype(str)[11:13]
            if k in data_dict.keys():
                data_dict[k] += 1
            else:
                data_dict[k] = 1
        ax = plt.subplot(111)
        ax.plot(data_dict.keys(), data_dict.values())
        # TODO 修改曲线的颜色类型
        ax.set_title("Comment Time Analysis Based Hour")
        ytick_spacing = int(round(max(data_dict.values())/150)*10)+10
        ax.yaxis.set_major_locator(ticker.MultipleLocator(ytick_spacing))
        save_path = "./data_analysis/" + data_name + "/CTime(hour)_line_chart_" + data_name + ".jpg"
        plt.savefig(save_path, dpi=600)
        save_path = os.getcwd() + save_path[1:]
        # os.startfile(save_path)
        plt.show()
        print('评论时间(hour)分析折线图已保存：./data_analysis/' + data_name + '/CTime(hour)_line_chart_' + data_name + '.jpg')
    except:
        traceback.print_exc()


def stopword_cut(deal_text, stoplist):
    '''
    根据暂停词列表去掉原文本中的暂停词,返回处理后的text
    :param deal_text:
    :param stoplist:
    :return:
    '''
    result = []
    for i in jieba.cut(deal_text):
        if i not in stoplist and len(i) > 1:
            result.append(i)
    return result


def wordcloud_comment(data_name):
    '''
    评论数据 词云分析
    :param data_name:
    :param text
    :return:
    '''
    # 开始词云分析
    global datadf, text
    try:
        dict_path = './dict/worddict.txt'
        stopword_path = './dict/stopwords.txt'

        jieba.load_userdict(dict_path)      # 加载用户自定义字典
        with open(stopword_path, 'r', encoding='utf-8') as f:   # 加载用户自定义的暂停词
            stoptext = f.read()
        stoplist = stoptext.rsplit(sep="\n")
        text = stopword_cut(text, stoplist)         # 根据暂停词来去掉没用的数据
        text = ' '.join(text)   # 将list变为字符串
        # # 设置云图的遮蔽图片
        # mask_img_path = './data/image/' + data_name + '.png'
        # mask_img = np.array(Image.open(mask_img_path))
        word = WordCloud(font_path="C:\\Windows\\Fonts\\STFANGSO.ttf", max_words=200, min_font_size=7, scale=2,
                         background_color='white')
        word.generate(text)
        plt.imshow(word, interpolation='bilinear')
        plt.axis('off')  # 关闭坐标轴
        save_path = "./data_analysis/" + data_name + "/wordcloud_" + data_name + ".jpg"
        plt.savefig(save_path, dpi=600)
        save_path = os.getcwd() + save_path[1:]
        # os.startfile(save_path)
        plt.show()
        print("评论词云图已保存：./data_analysis/" + data_name + "/wordcloud_" + data_name + ".jpg")
    except:
        traceback.print_exc()


# GUI界面调用
def load_data(data_name):
    global datadf, text
    try:
        datadf = load_comment_from_json(data_name)
        text = load_comment_data(data_name)
    except:
        print('500：评论数据读取失败')
    pass


def main_data_analysis(data_name=''):
    '''
    数据分析主函数，
    :param data_name:
    :return:
    '''
    # 数据加载
    # data_name = '哈利·波特与密室_电影_bilibili_哔哩哔哩'
    # data_name = '全职高手 第一季'
    # data_name = '女高中生的虚度日常_番剧_bilibili_哔哩哔哩'
    # data_name = '某科学的超电磁炮S'
    global datadf, text
    try:
        datadf = load_comment_from_json(data_name)
        text = load_comment_data(data_name)
    except:
        print('500：评论数据读取失败')
    try:
        # 制作饼图
        gender_pie(data_name)
        member_pie(data_name)
        level_pie(data_name)

        # 制作折线图
        ctime_analysis_based_day(data_name)
        ctime_analysis_based_hour(data_name)

        # 评论词云分析
        wordcloud_comment(data_name)
    except:
        traceback.print_exc()
        print('600：数据分析失败')


if __name__ == '__main__':
    main_data_analysis('全职高手 第一季')
