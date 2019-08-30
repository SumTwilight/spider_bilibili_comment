import os
import sys
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QTextBrowser, QTableWidget, QInputDialog, \
    QTableWidgetItem, QHeaderView, QProgressBar, QHBoxLayout, QVBoxLayout, QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal
import spider_bilibili_comment as spbili
import data_analysis as danalysis


class CrawIWindow(QWidget):
    # 添加控件
    def __init__(self):
        super(CrawIWindow, self).__init__()
        self.resize(800, 1000)
        self.setWindowTitle('b站视频评论爬取小工具')
        self.setWindowIcon(QIcon('./icon.png'))  # 设置窗口图标

        # 生成各个部件
        self.start_btn = QPushButton(self)
        self.stop_btn = QPushButton(self)
        self.open_save_dir_btn = QPushButton(self)
        self.set_av_link_btn = QPushButton(self)
        self.set_av_pn_btn = QPushButton(self)
        self.av_link_line = QLineEdit(self)
        self.av_pn_line = QLineEdit(self)
        self.table = QTableWidget(self)
        self.log_browser = QTextBrowser(self)
        self.progressbar = QProgressBar(self)

        # self.figure = plt.figure(facecolor='#FFD7C4')
        # self.canves = FigureCanvas(self.figure)

        # 数据分析按钮
        self.start_data_analysis_btn = QPushButton()
        self.gender_pie_btn = QPushButton()
        self.member_pie_btn = QPushButton()
        self.level_pie_btn = QPushButton()
        self.ctime_day_line_btn = QPushButton()
        self.ctime_hour_line_btn = QPushButton()
        self.wordcloud_btn = QPushButton()

        self.h_layout = QHBoxLayout()
        self.IO1_layout = QHBoxLayout()
        self.IO2_layout = QHBoxLayout()
        self.da_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.spider_thread = spbili.SpiderThread()  # 爬虫线程

        # 对各个部件进行初始化
        self.btn_init()
        self.data_btn_init()
        self.table_init()
        self.log_init()
        self.progressbar_init()
        self.layout_init()
        self.crawl_init()

    # 控件初始化
    def btn_init(self):
        # 爬虫按钮初始化
        self.start_btn.setText('开始爬取')
        self.stop_btn.setText('停止爬取')
        self.open_save_dir_btn.setText('打开data文件夹')
        self.set_av_link_btn.setText('输入待爬取视频链接后点击')
        self.set_av_pn_btn.setText('输入待爬取评论页数后点击')

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.open_save_dir_btn.setEnabled(True)
        self.set_av_link_btn.setEnabled(True)
        self.set_av_pn_btn.setEnabled(False)

        self.start_btn.clicked.connect(lambda: self.btn_slot(self.start_btn))
        self.stop_btn.clicked.connect(lambda: self.btn_slot(self.stop_btn))
        self.open_save_dir_btn.clicked.connect(lambda: self.btn_slot(self.open_save_dir_btn))
        self.set_av_link_btn.clicked.connect(lambda: self.btn_slot(self.set_av_link_btn))
        self.set_av_pn_btn.clicked.connect(lambda: self.btn_slot(self.set_av_pn_btn))

    def data_btn_init(self):
        # 数据分析按钮初始化
        self.start_data_analysis_btn.setText('点击加载分析数据')
        self.gender_pie_btn.setText('性别饼图')
        self.member_pie_btn.setText('会员分类饼图')
        self.level_pie_btn.setText('等级分布饼图')
        self.ctime_day_line_btn.setText('评论时间折线图（day）')
        self.ctime_hour_line_btn.setText('评论时间折线图（hour）')
        self.wordcloud_btn.setText('评论词云图')

        self.start_data_analysis_btn.setEnabled(False)
        self.gender_pie_btn.setEnabled(False)
        self.member_pie_btn.setEnabled(False)
        self.level_pie_btn.setEnabled(False)
        self.ctime_day_line_btn.setEnabled(False)
        self.ctime_hour_line_btn.setEnabled(False)
        self.wordcloud_btn.setEnabled(False)

        self.start_data_analysis_btn.clicked.connect(lambda: self.data_btn_slot(self.start_data_analysis_btn))
        self.gender_pie_btn.clicked.connect(lambda: self.data_btn_slot(self.gender_pie_btn))
        self.member_pie_btn.clicked.connect(lambda: self.data_btn_slot(self.member_pie_btn))
        self.level_pie_btn.clicked.connect(lambda: self.data_btn_slot(self.level_pie_btn))
        self.ctime_day_line_btn.clicked.connect(lambda: self.data_btn_slot(self.ctime_day_line_btn))
        self.ctime_hour_line_btn.clicked.connect(lambda: self.data_btn_slot(self.ctime_hour_line_btn))
        self.wordcloud_btn.clicked.connect(lambda: self.data_btn_slot(self.wordcloud_btn))

    def table_init(self):
        # 用户ID，用户名，用户等级，大会员，性别，评论时间，评论点赞数，评论内容
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['用户ID', '用户名', '用户等级', '大会员',
                                              '性别', '评论时间', '评论点赞数', '评论内容'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def log_init(self):
        new_log = '欢迎使用bilibili视频评论爬取软件\n请输入爬取视频链接'
        self.log_browser.append(new_log)

    def progressbar_init(self):
        self.progressbar.setRange(0, 100)
        self.progressbar.setValue(0)

    def layout_init(self):
        self.h_layout.addWidget(self.start_btn)
        self.h_layout.addWidget(self.stop_btn)
        self.h_layout.addWidget(self.open_save_dir_btn)

        self.IO1_layout.addWidget(self.set_av_link_btn)
        self.IO1_layout.addWidget(self.av_link_line)

        self.IO2_layout.addWidget(self.set_av_pn_btn)
        self.IO2_layout.addWidget(self.av_pn_line)

        self.da_layout.addWidget(self.gender_pie_btn)
        self.da_layout.addWidget(self.member_pie_btn)
        self.da_layout.addWidget(self.level_pie_btn)
        self.da_layout.addWidget(self.ctime_day_line_btn)
        self.da_layout.addWidget(self.ctime_hour_line_btn)
        self.da_layout.addWidget(self.wordcloud_btn)

        self.v_layout.addWidget(self.table)
        self.v_layout.addWidget(self.log_browser)
        self.v_layout.addWidget(self.progressbar)

        self.v_layout.addLayout(self.IO1_layout)
        self.v_layout.addLayout(self.IO2_layout)
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addWidget(self.start_data_analysis_btn)
        self.v_layout.addLayout(self.da_layout)
        # self.v_layout.addWidget(self.canves)

        self.setLayout(self.v_layout)

    def crawl_init(self):
        self.spider_thread.finished_signal.connect(self.finish_slot)  # 爬取完成信号
        self.spider_thread.log_signal.connect(self.set_log_slot)  # 日志打印信号
        self.spider_thread.result_signal.connect(self.set_table_slot)  # 用户评论信息打印信号
        self.spider_thread.progressbar_signal.connect(self.set_progressbar_slot)  # 进度条信号
        self.spider_thread.error_signal.connect(self.error_slot)  # 报错信号

    def finish_slot(self):
        self.set_av_link_btn.setEnabled(True)
        self.set_av_pn_btn.setEnabled(False)
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.open_save_dir_btn.setEnabled(True)
        self.start_data_analysis_btn.setEnabled(True)

    def set_log_slot(self, new_log):
        self.log_browser.append(new_log)

    def set_table_slot(self, dict_data):
        row = self.table.rowCount()  # 获取当前行数
        self.table.insertRow(row)  # 插入新的一行

        self.table.setItem(row, 0, QTableWidgetItem(str(dict_data['mid'])))
        self.table.setItem(row, 1, QTableWidgetItem(dict_data['uname']))
        self.table.setItem(row, 2, QTableWidgetItem(str(dict_data['current_level'])))
        dict_vip = {0: '普通会员', 1: '月大会员', 2: '年大会员'}
        self.table.setItem(row, 3, QTableWidgetItem(dict_vip[dict_data['vipType']]))
        self.table.setItem(row, 4, QTableWidgetItem(dict_data['sex']))
        self.table.setItem(row, 5, QTableWidgetItem(dict_data['ctime']))
        self.table.setItem(row, 6, QTableWidgetItem(str(dict_data['like'])))
        self.table.setItem(row, 7, QTableWidgetItem(dict_data['message']))  # TODO 格子太小，需要调整

    def set_progressbar_slot(self, i, pn):
        k = int((float(i) / pn) * 100)
        self.progressbar.setValue(k)

    def error_slot(self, error):
        # todo 补充其他error
        if error == 1:
            set_log_slot("爬取页数大于总页数，请重新输入")
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.open_save_dir_btn.setEnabled(False)
            self.set_av_link_btn.setEnabled(False)
            self.set_av_pn_btn.setEnabled(True)

    def btn_slot(self, btn):
        if btn == self.set_av_link_btn:
            self.log_browser.clear()  # 清除之前日志
            self.spider_thread.URL = self.av_link_line.text()
            self.spider_thread.get_av_info()  # 获取视频信息
            self.set_av_pn_btn.setEnabled(True)
            self.stop_btn.setEnabled(True)

            self.start_data_analysis_btn.setEnabled(False)
            self.gender_pie_btn.setEnabled(False)
            self.member_pie_btn.setEnabled(False)
            self.level_pie_btn.setEnabled(False)
            self.ctime_day_line_btn.setEnabled(False)
            self.ctime_hour_line_btn.setEnabled(False)
            self.wordcloud_btn.setEnabled(False)

        elif btn == self.set_av_pn_btn:
            self.spider_thread.spider_pn = self.av_pn_line.text()
            self.set_log_slot('将爬取前' + self.spider_thread.spider_pn + '页，请点击开始爬取！')
            self.start_btn.setEnabled(True)
        elif btn == self.start_btn:
            self.log_browser.append('<font color="red">开始爬取</font>')

            self.table.clearContents()  # 清空表格记录，并回到第一行
            self.table.setRowCount(0)

            self.set_av_link_btn.setEnabled(False)
            self.set_av_pn_btn.setEnabled(False)
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)

            self.spider_thread.start()  # 开始爬取进程
        elif btn == self.stop_btn:
            self.log_browser.append('<font color="red">停止爬取</font>')
            self.progressbar.setValue(0)
            self.set_av_link_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.start_btn.setEnabled(False)

            self.spider_thread.terminate()  # 停止爬取进程
        elif btn == self.open_save_dir_btn:
            os.system('explorer.exe /n,.\\data')

    def data_btn_slot(self, btn):
        # TODO
        if btn == self.start_data_analysis_btn:
            danalysis.load_data(self.spider_thread.Av_name)
            self.set_log_slot('读取数据成功')
            self.gender_pie_btn.setEnabled(True)
            self.member_pie_btn.setEnabled(True)
            self.level_pie_btn.setEnabled(True)
            self.ctime_day_line_btn.setEnabled(True)
            self.ctime_hour_line_btn.setEnabled(True)
            self.wordcloud_btn.setEnabled(True)

        elif btn == self.gender_pie_btn:
            danalysis.gender_pie(self.spider_thread.Av_name)
            self.set_log_slot("生成成功\n图片已保存在./data_analysis/" + self.spider_thread.Av_name +
                              "/Gender_pie_" + self.spider_thread.Av_name + ".jpg")

        elif btn == self.member_pie_btn:
            danalysis.member_pie(self.spider_thread.Av_name)
            self.set_log_slot("生成成功\n图片已保存在./data_analysis/" + self.spider_thread.Av_name +
                              "/Member_pie_" + self.spider_thread.Av_name + ".jpg")

        elif btn == self.level_pie_btn:
            danalysis.level_pie(self.spider_thread.Av_name)
            self.set_log_slot("生成成功\n图片已保存在./data_analysis/" + self.spider_thread.Av_name +
                              "/level_pie" + self.spider_thread.Av_name + ".jpg")

        elif btn == self.ctime_day_line_btn:
            danalysis.ctime_analysis_based_day(self.spider_thread.Av_name)
            self.set_log_slot("生成成功\n图片已保存在./data_analysis/" + self.spider_thread.Av_name +
                              "/CTime(day)_line_chart_" + self.spider_thread.Av_name + ".jpg")

        elif btn == self.ctime_hour_line_btn:
            danalysis.ctime_analysis_based_hour(self.spider_thread.Av_name)
            self.set_log_slot("生成成功\n图片已保存在./data_analysis/" + self.spider_thread.Av_name +
                              "/CTime(hour)_line_chart_" + self.spider_thread.Av_name + ".jpg")

        elif btn == self.wordcloud_btn:
            danalysis.wordcloud_comment(self.spider_thread.Av_name)
            self.set_log_slot("生成成功\n图片已保存在./data_analysis/" + self.spider_thread.Av_name +
                              "/wordcloud_" + self.spider_thread.Av_name + ".jpg")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CrawIWindow()
    window.show()
    sys.exit(app.exec())
