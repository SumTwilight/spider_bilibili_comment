import pandas as pd
import json
import traceback
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def load_comment_from_json(data_name, path='./data/'):
    '''
    加载json评论数据，并且以DataFrame的数据结构返回
    :param data_name:
    :param path:
    :return:
    '''
    path = path + data_name + '.json'
    data = pd.read_json(path, orient='index', encoding='utf-8')
    return data


def level_pie(datadf):
    '''
        输出用户等级的饼图
        :param datadf:
        :return:
    '''
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
            autopct='%.1f%%', labeldistance=0.8, shadow=True, startangle=90,
            colors=('#22a2c3', '#eba0b3', '#83cbac', '#894276'))  # TODO 颜色
    plt.axis('equal')  # 让图像保持圆形
    plt.legend(loc="upper right", fontsize=13, bbox_to_anchor=(1.1, 1.05), borderaxespad=0.3)
    plt.title('Level Analysis')
    plt.savefig("./data_analysis/level_pie.jpg", dpi=600)
    plt.show()


def member_pie(datadf):
    '''
        输出会员构成的饼图
        :param datadf:
        :return:
    '''
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
            autopct='%.1f%%', labeldistance=0.8, shadow=True, startangle=90,
            colors=('#22a2c3', '#eba0b3', '#83cbac'))   # TODO 颜色
    plt.axis('equal')  # 让图像保持圆形
    plt.legend(loc="upper right", fontsize=13, bbox_to_anchor=(1.1, 1.05), borderaxespad=0.3)
    plt.title('Member Analysis')
    plt.savefig("./data_analysis/Member_pie.jpg", dpi=600)
    plt.show()


def gender_pie(datadf):
    '''
    输出男女性别的饼图
    :param datadf:
    :return:
    '''
    data_dict = {'男': 0, '女': 0, '保密': 0}
    for i in datadf['sex'].values:
        data_dict[i] += 1
    explode = (0, 0, 0.03)
    plt.pie(data_dict.values(), explode=explode, labels=tuple(data_dict.keys()),
            autopct='%.1f%%', labeldistance=0.8, shadow=True, startangle=90,
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
    plt.savefig("./data_analysis/Gender_pie.jpg", dpi=600)
    plt.show()


def ctime_analysis_based_day(datadf):
    '''
    输出以日为单位的评论数的折线图
    :param datadf:
    :return:
    '''
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
    ytick_spacing = int(round(max(data_dict.values())/150)*10)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(ytick_spacing))

    ax.set_title("Comment Time Analysis Based Day")
    plt.show()


def ctime_analysis_based_hour(datadf):
    '''
    输出以小时为单位的评论数的折线图
    :param datadf:
    :return:
    '''
    data_dict = {'00': 0, '23': 0, '22': 0, '21': 0, '20': 0, '19': 0, '18': 0, '17': 0, '16': 0, '15': 0, '14': 0,
                 '13': 0, '12': 0, '11': 0, '10': 0, '09': 0, '08': 0, '07': 0, '06': 0, '05': 0, '04': 0, '03': 0,
                 '02': 0, '01': 0}
    for i in datadf['ctime_time'].values:
        k = i.astype(str)[11:13]
        if k in data_dict.keys():
            data_dict[k] += 1
        else:
            data_dict[k] = 1
    ax = plt.subplot(111)
    ax.plot(data_dict.keys(), data_dict.values())
    # TODO 修改曲线的颜色类型
    ax.set_title("Comment Time Analysis Based Time")
    ytick_spacing = 100
    ax.yaxis.set_major_locator(ticker.MultipleLocator(ytick_spacing))
    plt.show()


def main():
    # data_name = '哈利·波特与密室_电影_bilibili_哔哩哔哩'
    data_name = '全职高手 第一季'
    datadf = load_comment_from_json(data_name)

    gender_pie(datadf)
    member_pie(datadf)
    level_pie(datadf)
    ctime_analysis_based_day(datadf)
    ctime_analysis_based_hour(datadf)


if __name__ == '__main__':
    main()
