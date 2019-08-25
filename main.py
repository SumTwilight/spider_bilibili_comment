from spider_bilibili_comment import main_spider
from data_analysis import main_data_analysis


def main():
    # url = 'https://www.bilibili.com/bangumi/play/ep107656/'       # 全职高手
    # url = 'https://www.bilibili.com/bangumi/play/ep277146/'       # 异常生物见闻录
    # url = 'https://www.bilibili.com/video/av13967569'
    # url = 'https://www.bilibili.com/bangumi/play/ss28296'  # 哈利波特
    # url = 'https://www.bilibili.com/bangumi/play/ss12717/'          # 扫毒
    # url = 'https://www.bilibili.com/video/av63897667'
    # url ='https://www.bilibili.com/video/av28547786'
    # url = 'https://www.bilibili.com/bangumi/play/ss5978'      # 博人传  爬取失败，没有avid
    # url = 'https://www.bilibili.com/bangumi/play/ss28016'     # 女高中生的虚度日常_番剧_bilibili_哔哩哔哩
    # url = 'https://www.bilibili.com/bangumi/play/ep71958'       # 某科学的超电磁炮
    url = input('请输入bilibili视频链接，例如：https://www.bilibili.com/bangumi/play/ep71958')
    try:
        AV_name = main_spider(url)
        if AV_name == '爬取失败':
            raise Exception
        # data_name = '哈利·波特与密室_电影_bilibili_哔哩哔哩'
        # data_name = '全职高手 第一季'
        main_data_analysis(AV_name)
    except:
        print('运行失败')


if __name__ == '__main__':
    main()
