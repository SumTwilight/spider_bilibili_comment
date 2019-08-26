import traceback
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QTextBrowser, QTableWidget, \
                            QTableWidgetItem, QHeaderView, QProgressBar, QHBoxLayout, QVBoxLayout


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
        self.save_combobox = QComboBox(self)
        self.table = QTableWidget(self)
        self.log_browser = QTextBrowser(self)
        self.progressbar = QProgressBar(self)

        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        # 对各个部件进行初始化
        self.btn_init()
        self.combobox_init()
        self.table_init()
        self.progressbar_init()
        self.layout_init()

    # 设置控件
    def btn_init(self):
        self.start_btn.setText('开始爬取')
        self.stop_btn.setText('停止爬取')
        self.stop_btn.setEnabled(False)

        self.start_btn.clicked.connect(lambda: self.btn_slot(self.start_btn))
        self.stop_btn.clicked.connect(lambda: self.btn_slot(self.stop_btn))

    def combobox_init(self):
        save_list = ['另存到', '方式1', '方式2', '方式3']
        self.save_combobox.addItems(save_list)
        self.save_combobox.setEnabled(False)

    def table_init(self):
        # 用户ID，用户名，用户等级，大会员，性别，评论时间，评论点赞数，评论内容
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['用户ID', '用户名', '用户等级', '大会员',
                                              '性别', '评论时间', '评论点赞数', '评论内容'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def progressbar_init(self):
        self.progressbar.setRange(0, 100)  # TODO  这个进度条不行
        self.progressbar.setValue(0)

    def layout_init(self):
        self.h_layout.addWidget(self.start_btn)
        self.h_layout.addWidget(self.stop_btn)
        self.h_layout.addWidget(self.save_combobox)
        self.v_layout.addWidget(self.table)
        self.v_layout.addWidget(self.log_browser)
        self.v_layout.addWidget(self.progressbar)
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)

    def btn_slot(self, btn):
        if btn == self.start_btn:
            self.log_browser.clear()
            self.log_browser.append('<font color="red">开始爬取</font>')
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.save_combobox.setEnabled(False)
        else:
            self.log_browser.append('<font color="red">停止爬取</font>')
            self.stop_btn.setEnabled(False)
            self.start_btn.setEnabled(True)
            self.save_combobox.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CrawIWindow()
    window.show()
    sys.exit(app.exec())
