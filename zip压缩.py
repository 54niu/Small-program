'''
zip压缩文件
主要功能:1.可以对多个文件(可以是不同目录下的文件)进行压缩操作
        2.对文件进行解压操作，可以选择解压目录
        
思路     1. 将要压缩的文件路径存入一个列表里，并对列表进行去重操作
        2. 再从列表里提取路径进行压缩,调用tkinter.simpledialog选择压缩后的文件名
        3. 进行解压
'''



import tkinter
import zipfile
import tkinter.filedialog
import tkinter.messagebox
import tkinter.simpledialog
import os.path

class Niuzip:
    def __init__(self):
        self.filelists = []
        self.zwindows()

    # 界面布局
    def zwindows(self):
        app = tkinter.Tk()
        app.minsize(300, 400)
        app.resizable(False, False)  # 窗口大小不能改变
        app.title('小牛压缩')

        # 菜单
        def zuozhe():
            tkinter.messagebox.showinfo(title='作者', message='如果您在使用过程中遇到了问题，请联系作者\n'
                                                            '作者；牛少鹏\n邮箱：xxx@yy.com')
        def bangzhu():
            tkinter.messagebox.showinfo(title='帮助', message='1. 本压缩软件为测试版本\n'
                                                            '   只能压缩较小的文件\n'
                                                            '   暂不支持压缩文件夹功能\n'
                                                              '2. 敬请期待小牛压缩2.0')
        def banben():
            tkinter.messagebox.showinfo(title='版本', message='版本：1.0\n'
                                                            '版本名: Giroud')

        def shouce():
            tkinter.messagebox.showinfo(title='用户手册', message='1.点击选择文件按钮、选择想要压缩的文件\n'
                                                            '2.点击压缩文件按钮、本软件则会压缩选中的文件\n'
                                                            '3.点击解压按钮选择、想要解压的压缩包和解压后的路径\n'
                                                            '4.点击清空文件按钮、则会清除您已选择的文件')

        # 创建菜单
        menu = tkinter.Menu(app)

        menu.add_cascade(label='作者', command=zuozhe)
        app.config(menu=menu)

        menu.add_cascade(label='帮助', command=bangzhu)
        app.config(menu=menu)

        menu.add_cascade(label='版本', command=banben)
        app.config(menu=menu)

        menu.add_cascade(label='使用手册', command=shouce)
        app.config(menu=menu)


        # 按钮
        btn2 = tkinter.Button(app, text='选择文件', bg='Gainsboro', command=lambda: self.selectfiles())
        btn2.grid(row=0, column=0, padx=10, pady=10)

        btn3 = tkinter.Button(app, text='压缩文件', bg='Gainsboro', command=lambda: self.zfiles())
        btn3.grid(row=0, column=1, padx=10, pady=10)

        btn4 = tkinter.Button(app, text='解压文件', bg='Gainsboro', command=lambda: self.nozfile())
        btn4.grid(row=0, column=2, padx=10, pady=10)

        btn4 = tkinter.Button(app, text='清空文件', bg='Gainsboro', command=lambda: self.zipclear())
        btn4.grid(row=1, column=0, padx=10, pady=5, columnspan=3)

        self.files = tkinter.StringVar()
        self.files.set('              小牛压缩，年轻人的第一款压缩软件')

        label = tkinter.Label(app, textvariable=self.files, bg='Silver', width=45, height=20, justify='left', anchor='nw')
        label.grid(row=2, column=0, columnspan=3)
        app.mainloop()

    # 文件选择函数
    # tkinter.filedialog模块,可以创建文件打开和保存文件对话框。
    def selectfiles(self):

        filespath = tkinter.filedialog.askopenfilenames(title='请选择要压缩的文件')
        # 用askopenfilename的话，路径就竖着写了。
        self.filelists += list(filespath)  # 把每次选择的路径添加到filelists里

        # 列表去重
        zlist = list(set(self.filelists))
        print(zlist)

        # 显示出路径
        filestr = '\n'.join(zlist)  # 将路径写入label，一个路径一行
        self.files.set(filestr)

    # 压缩文件函数
    def zfiles(self):
        if len(self.filelists) != 0:  # 对路径列表进行判断，不为空才能往下进行操作
            compress = tkinter.filedialog.askdirectory(title='请选择文件压缩路径')
            if len(compress) != 0:

                # 创建文件名
                niu = tkinter.simpledialog.askstring(title='压缩文件名称', prompt='压缩包名称')

                if len(str(niu)) == 0:
                    basename = os.path.basename(compress) + '.zip'
                else:
                    basename = str(niu) + '.zip'
            else:

                tkinter.messagebox.showinfo('操作出错', ' 请选择要压缩到的路径')

                return None

            # 组合完整名称
            zippath = os.path.join(compress, basename)

            fzip = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)

            # 将文件压缩进来
            for path in self.filelists:
                # 检测文件是否存在
                if os.path.exists(path):
                    # 向压缩文件中写入文件
                    fzip.write(path, os.path.basename(path))
            fzip.close()
            tkinter.messagebox.showinfo('操作完成', '文件压缩成功，路径为：' + zippath)

            print(zippath)
        else:
            pass

    # 解压文件函数
    def nozfile(self):

        # 选择要解压的文件
        nozip = tkinter.filedialog.askopenfilename(title='请选择要解压的文件', filetypes=[('zip文件', '*.zip')])

        print(nozip)
        # 选择要解压到的路径

        if len(nozip) != 0:
            nopath = tkinter.filedialog.askdirectory(title='解压后的路径')

            if len(nopath) != 0:
                print(nopath)
                print('- '*10)

                # 解压
                nzip = zipfile.ZipFile(nozip, 'r', zipfile.ZIP_DEFLATED)
                nzip.extractall(nopath)
                nzip.close()
                tkinter.messagebox.showinfo('操作完成', '文件解压成功')
                return None
            else:
                tkinter.messagebox.showinfo('操作失败', '请选择解压文件')
                return None
        else:
            tkinter.messagebox.showinfo('操作失败1', '请选择解压文件')

    # 清空函数
    def zipclear(self):
        self.filelists.clear()
        self.files.set('              小牛压缩，年轻人的第一款压缩软件')



nz = Niuzip()