import os
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QTextBrowser, QTableWidget, QInputDialog, \
                            QTableWidgetItem, QHeaderView, QProgressBar, QHBoxLayout, QVBoxLayout, QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal
import spider_bilibili_comment as spbili


class CrawIWindow(QWidget):
    # 添加控件
    def __init__(self):
        super(CrawIWindow, self).__init__()
        self.resize(800, 600)
        self.setWindowTitle('这里是标题')
        self.setWindowIcon(QIcon('./data/image/全职高手 第一季.jpg'))      # 设置窗口图标

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

        self.h_layout = QHBoxLayout()
        self.IO1_layout = QHBoxLayout()
        self.IO2_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.crawl_thread = spbili.CrawIThread()  # 爬虫线程

        # 对各个部件进行初始化
        self.btn_init()
        self.table_init()
        self.log_init()
        self.progressbar_init()
        self.layout_init()
        self.crawl_init()

    # 控件初始化
    def btn_init(self):
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

        self.v_layout.addWidget(self.table)
        self.v_layout.addWidget(self.log_browser)
        self.v_layout.addWidget(self.progressbar)

        self.v_layout.addLayout(self.IO1_layout)
        self.v_layout.addLayout(self.IO2_layout)
        self.v_layout.addLayout(self.h_layout)

        self.setLayout(self.v_layout)

    def crawl_init(self):
        self.crawl_thread.finished_signal.connect(self.finish_slot)     # 爬取完成信号
        self.crawl_thread.log_signal.connect(self.set_log_slot)     # 日志打印信号
        self.crawl_thread.result_signal.connect(self.set_table_slot)    # 用户评论信息打印信号
        self.crawl_thread.progressbar_signal.connect(self.set_progressbar_slot)   # 进度条信号
        self.crawl_thread.error_signal.connect(self.error_slot)     # 报错信号

    def finish_slot(self):
        self.set_av_link_btn.setEnabled(True)
        self.set_av_pn_btn.setEnabled(False)
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.open_save_dir_btn.setEnabled(True)

    def set_log_slot(self, new_log):
        self.log_browser.append(new_log)

    def set_table_slot(self, dict_data):
        row = self.table.rowCount()  # 获取当前行数
        self.table.insertRow(row)    # 插入新的一行

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
        k = int((float(i)/pn)*100)
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
            self.crawl_thread.URL = self.av_link_line.text()
            self.crawl_thread.get_av_info()  # 获取视频信息
            self.set_av_pn_btn.setEnabled(True)
            self.stop_btn.setEnabled(True)
        elif btn == self.set_av_pn_btn:
            self.crawl_thread.spider_pn = self.av_pn_line.text()
            self.set_log_slot('将爬取前'+self.crawl_thread.spider_pn+'页，请点击开始爬取！')
            self.start_btn.setEnabled(True)
        elif btn == self.start_btn:
            self.log_browser.append('<font color="red">开始爬取</font>')

            self.table.clearContents()  # 清空表格记录，并回到第一行
            self.table.setRowCount(0)

            self.set_av_link_btn.setEnabled(False)
            self.set_av_pn_btn.setEnabled(False)
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)

            self.crawl_thread.start()  # 开始爬取进程
        elif btn == self.stop_btn:
            self.log_browser.append('<font color="red">停止爬取</font>')
            self.set_av_link_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.start_btn.setEnabled(False)

            self.crawl_thread.terminate()   # 停止爬取进程
        elif btn == self.open_save_dir_btn:
            os.system('explorer.exe /n,.\\data')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CrawIWindow()
    window.show()
    sys.exit(app.exec())
