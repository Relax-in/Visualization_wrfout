import sys
from PyQt5 import QtWidgets, QtCore
from ui_main import Ui_MainWindow  # ui python文件
from works import Worker_1
from ui_add import Ui_Dialog  # 导入 Ui_Dialog 类
from PyQt5.QtWidgets import QFileDialog





# 主线程
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.file_names_1 = []     # 文件1名字数组
        self.file_names_2 = []     # 文件2名字数组
        self.output_variables = []     # 输出变量数组
        self.directory = "."      # 文件输出路径
        
        # 绑定按钮(打开文件1)到open_file_1上
        self.action.triggered.connect(self.open_file_1)
        self.action_2.triggered.connect(self.open_file_2)
        self.pushButton.clicked.connect(self.start_progress)  # 启动或重启进度条 
        self.pushButton_2.clicked.connect(self.toggle_pause_resume)  # 暂停或恢复
        self.pushButton_3.clicked.connect(self.open_dialog)  # 打开弹出框
        
        self.action_3.triggered.connect(self.select_directory)  # 连接到选择文件夹的方法
        
        self.is_paused = False  # 用于记录当前是否暂停

        # 连接信号,确定输出变量
        self.checkBox.stateChanged.connect(lambda state: self.checkBox_changed('U', state))
        self.checkBox_2.stateChanged.connect(lambda state: self.checkBox_changed('V', state))
        self.checkBox_3.stateChanged.connect(lambda state: self.checkBox_changed('W', state))
        self.checkBox_4.stateChanged.connect(lambda state: self.checkBox_changed('P', state))
        self.checkBox_5.stateChanged.connect(lambda state: self.checkBox_changed('PH', state))
        self.checkBox_6.stateChanged.connect(lambda state: self.checkBox_changed('T', state))
        
        
    # 打开文件1
    def open_file_1(self):
        options = QtWidgets.QFileDialog.Options()
        self.file_names_1, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "打开文件", "", "All Files (*);;Text Files (*.txt)", options=options)
        if self.file_names_1:
            self.textBrowser.append("读取文件1的数据为：")
            self.textBrowser.append("===================")
            for file_name in self.file_names_1:
                self.textBrowser.append(file_name)
            self.textBrowser.append("===================\n")
            self.textBrowser_2.append("文件1的个数："+ f"{len(self.file_names_1)}")

    # 打开文件2
    def open_file_2(self):
        options = QtWidgets.QFileDialog.Options()
        self.file_names_2, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "打开文件", "", "All Files (*);;Text Files (*.txt)", options=options)
        if self.file_names_2:
            self.textBrowser.append("读取文件2的数据为：")
            self.textBrowser.append("===================")
            for file_name in self.file_names_2:
                self.textBrowser.append(file_name)
            self.textBrowser.append("===================\n")
            self.textBrowser_2.append("文件2的个数："+ f"{len(self.file_names_2)}")

    # 测试函数（不引入主代码中）
    def on_button_clicked_test(self):
        # 获取 QLineEdit 中的文本
        text1 = self.lineEdit.text()
        text2 = self.lineEdit_2.text()
        
        # 进行你需要的操作，例如打印或显示在其他地方
        print("LineEdit 1 内容:", text1)
        print("LineEdit 2 内容:", text2)
    
    # 启动进度条
    def start_progress(self):
        # 检查是否已有线程在运行
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.stop()  # 停止当前线程
            self.worker.quit()  # 退出线程
            self.worker.wait()  # 等待线程完全退出
        
        self.textBrowser_2.append("===================")


        # 重置进度条并启动新线程
        self.progressBar.setValue(0)
       
        if (self.lineEdit.text() != "" and self.lineEdit_2.text() != ""):
            self.worker = Worker_1(self.file_names_1, self.file_names_2, self.radioButton.isChecked(), 
                                self.radioButton_2.isChecked(), self.output_variables,
                                int(self.lineEdit.text()), int(self.lineEdit_2.text()),
                                self.directory)  # 创建新工作线程    
            
            self.worker.progress.connect(self.update_progress)  # 连接信号
            self.worker.str_signal.connect(self.update_signal)  # 连接信号
            self.worker.start()  # 启动新线程
        else:
            self.textBrowser.append("dx或dy未设置")
    

    # 暂停和恢复
    def toggle_pause_resume(self):
        if hasattr(self, 'worker') and self.worker.isRunning():
            if self.is_paused:
                self.worker.resume()  # 恢复线程
                self.is_paused = False
                self.pushButton_2.setText("暂停")  # 更新按钮文字
            else:
                self.worker.pause()  # 暂停线程
                self.is_paused = True
                self.pushButton_2.setText("恢复")  # 更新按钮文字

    # 更新进度条
    def update_progress(self, value):
        self.progressBar.setValue(value)  # 更新进度条的值

    # 测试代码
    def checkBox_changed(self, name, state):
        if state == QtCore.Qt.Checked:
            self.output_variables.append(name)
            self.textBrowser.append("变量" + name + "成功添加")
            # print(self.output_variables)    # 测试
        else:
            self.output_variables.remove(name)
            self.textBrowser.append("变量" + name + "成功去除")
            # print(self.output_variables)    # 测试

    # 在输出台输出性息
    def update_signal(self, value):
        self.textBrowser.append(value)


    def open_dialog(self):
        dialog = QtWidgets.QDialog(self)
        ui = Ui_Dialog()  # 创建 Ui_Dialog 实例
        ui.setupUi(dialog)  # 设置对话框的 UI

        if dialog.exec_() == QtWidgets.QDialog.Accepted:  # 检查对话框是否被接受
            value1, value2 = ui.get_values()  # 获取输入的值
            if value1 == "U" or value1 == "V" or value1 == "W" or value1 == "P" or value1 == "PH" or value1 == "T":
                self.textBrowser.append("添加变量为非自定义变量，添加失败！")
            elif value1 != "":
                self.output_variables.append(value1)
                self.textBrowser.append("变量" + value1 + "成功添加")
                
            if value2 == "U" or value2 == "V" or value2 == "W" or value2 == "P" or value2 == "PH" or value2 == "T":
                self.textBrowser.append("删除变量为非自定义变量，删除失败！")
            elif value2 != "":
                if value2 in self.output_variables:
                    self.output_variables.remove(value2)
                    self.textBrowser.append("变量" + value2 + "成功删除")
                else:
                    self.textBrowser.append("变量" + value2 + "不存在")
            
            print("输入的值1:", value1)
            print("输入的值2:", value2)
            # 这里可以将值用于其他处理
        # 在 ui_add.py更新后，要添加下面函数到ui_add.py
        # def get_values(self):
        #     return self.lineEdit.text(), self.lineEdit_2.text()

    def select_directory(self):
        options = QtWidgets.QFileDialog.Options()
        self.directory = QtWidgets.QFileDialog.getExistingDirectory(self, "选择文件夹", "", options=options)
        if self.directory:
            self.textBrowser.append(f"选择的文件夹路径:  {self.directory}")
            # 这里可以将 directory 用于后续操作


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
