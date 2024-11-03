from PyQt5 import QtCore
from work_fun import run_work_1, run_work_2

# 子线程
# class Worker_1(QtCore.QThread):
#     progress = QtCore.pyqtSignal(int)  # 定义进度信号

#     def run(self):
#         for i in range(500):
#             time.sleep(0.1)  # 模拟耗时操作
#             print(i)
#             self.progress.emit(i/5)  # 发送进度信号
            
            
class Worker_1(QtCore.QThread):
    progress = QtCore.pyqtSignal(int)  # 定义进度信号
    str_signal = QtCore.pyqtSignal(str)

    def __init__(self, file_1, file_2, radioButton, radioButton_2, output_variables, dx, dy, directory):
        super().__init__()
        self._is_running = True  # 控制线程运行
        self._is_paused = False  # 控制线程暂停
        self._mutex = QtCore.QMutex()  # 创建互斥锁
        self._wait_condition = QtCore.QWaitCondition()  # 创建条件变量
        self.file_1 = file_1     # 文件1名字数组
        self.file_2 = file_2     # 文件2名字数组
        self.radioButton = radioButton
        self.radioButton_2 = radioButton_2
        self.output_variables = output_variables  # 输出变量数组
        self.dx = dx
        self.dy = dy
        self.directory = directory    # 文件输出路径
        
    def run(self):
        self._is_running = True  # 重置运行标志
        

        if self.radioButton:
            self.str_signal.emit("正在执行单文件输出，请等待！")
            for i in range(len(self.file_1)):
                self._mutex.lock()
                while self._is_paused:  # 如果处于暂停状态，等待条件变量唤醒
                    self._wait_condition.wait(self._mutex)
                self._mutex.unlock()
                if not self._is_running:  # 检查是否需要停止
                    break
                
                # 核心程序
                out_str = run_work_1(self.file_1[i], self.output_variables, self.dx, self.dy, i, self.directory)  # 执行程序  output_variables 为输出变量数组
                if out_str == 1:
                    self.str_signal.emit("Done")
                self.progress.emit((i+1)*100/len(self.file_1))  # 发送进度信号
            self.str_signal.emit("输出完毕！")
            
        elif self.radioButton_2 and len(self.file_1) == len(self.file_2):
            self.str_signal.emit("正在执行做差文件输出")
            
            for i in range(len(self.file_1)):
                self._mutex.lock()
                while self._is_paused:  # 如果处于暂停状态，等待条件变量唤醒
                    self._wait_condition.wait(self._mutex)
                self._mutex.unlock()

                if not self._is_running:  # 检查是否需要停止
                    break
                
                # 核心程序
                out_str = run_work_2(self.file_1[i], self.file_2[i], self.output_variables, self.dx, self.dy, i, self.directory)  # 执行程序  output_variables 为输出变量数组

                if out_str == 1:
                    self.str_signal.emit("Done")
                else:
                    self.str_signal.emit("两组文件不匹配，跳过！")
                    
                self.progress.emit((i+1)*100/len(self.file_1))  # 发送进度信号
            self.str_signal.emit("输出完毕！")

        else:
            self.str_signal.emit("输出设置错误")
            print("输出设置错误")



    def stop(self):
        self._is_running = False  # 停止线程
        self.resume()  # 恢复线程以确保停止生效

    def pause(self):
        self._is_paused = True  # 设置暂停标志

    def resume(self):
        self._is_paused = False  # 取消暂停标志
        self._wait_condition.wakeAll()  # 唤醒等待的线程
