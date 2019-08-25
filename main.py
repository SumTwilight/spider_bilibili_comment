from spider_bilibili_comment import main_spider
from data_analysis import main_data_analysis


def main():
    # url = 'https://www.bilibili.com/bangumi/play/ep107656/'       # 全职高手
    url = 'https://www.bilibili.com/bangumi/play/ep277146/'       # 异常生物见闻录
    # url = 'https://www.bilibili.com/video/av13967569'
    # url = 'https://www.bilibili.com/bangumi/play/ss28296'  # 哈利波特
    # url = 'https://www.bilibili.com/bangumi/play/ss12717/'          # 扫毒
    AV_name = main_spider(url)
    # data_name = '哈利·波特与密室_电影_bilibili_哔哩哔哩'
    # data_name = '全职高手 第一季'
    main_data_analysis(AV_name)


if __name__ == '__main__':
    main()
