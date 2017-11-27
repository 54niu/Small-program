'''
palce布局方法

主要功能：1.ui仿照win10计算器，鼠标放在按钮上时变换颜色
        2.最上面的label显示第一个数和运算符，下面的label显示输入的过程
        3.对用户点击的运算符进行判断，如果用户连续输入多个运算符，只按照第一个运算符运算
        4.不能连续输入两个小数点或输入 1.2.3 之类的操作
        5.如果您想输入一个数的正负数，请先按数字再按正负号
        6.如果您连续点击多次运算符，则只有第一次点击会生效
        7.如果您要对负数进行开方，则结果为0 
        8.结果只保留五位小数
        9.如果您要求小数平方，则按下x²后按下=号键可以把结果只保留五位小数
        10.在您进行完一次带有等号的运算后，可以不清空屏幕上的数字直接开始下一次运算
              例如: 按下3+3=后屏幕显示6，可以不按清空键就进行4+4的运算
        11.在上一次运算完成后也可以直接按运算符对上一次运算的结果进行运算
        12.如果您依次输入3 + 3 * 2 则优先计算先输入的运算符，结果为12

'''

import tkinter
import math
import tkinter.messagebox



class Calc:
    def __init__(self):
        self.isys = False  # 判断按钮是否按下

        self.yslist = []  # 定义一个列表，用来存放要放入的字符
        self.toplabel = []  # 定义一个列表，用来存放最上面label要显示的内容

        self.initwindow()

    #  运算操作

    # 定义一个数字按钮操作
    def figrue(self, no):

        if self.isys == True:  # 按钮按下
            self.num.set(no)  # 向num传入按下的字符
            self.yslist.append(no)  # 在列表末尾添加按下的字符
            self.toplabel.append(no)
            print(self.yslist)
            self.isys = False
        else:
            oldno = self.num.get()
            if oldno == '0':  # 如果开始
                self.num.set(no)
                self.yslist.append(no)
                self.toplabel.append(no)
                print(self.yslist)
            else:
                self.num.set(self.num.get()+no)  # 在原先字符后继续添加字符
                self.yslist.append(no)
                self.toplabel.append(no)
                print(self.yslist)

    # 运算符按钮
    def pressys(self, ysflag):

        self.isys = True
        if len(self.yslist) != 0:  # 如果用户不点数字直接点运算符则pass，else则执行以下操作
            # 对运算符进行判断，防止用户连续多次点击运算符
            flags = ['*', '/', '-', '+', '%']
            if self.yslist[-1] not in flags:
                if ysflag == '*' or '/':  # 如果进行乘除法运算，则在列表开头和末尾添加括号()
                    self.yslist.insert(0, '(')
                    self.yslist.insert(len(self.yslist), ')')
                    self.yslist.append(ysflag)  # 向列表中添加运算符
                    self.toplabel.append(ysflag)  # 向上面的label的列表中添加运算符

                    asdf = len(self.toplabel)  # 上面的label只能显示运算符及运算符前面的数字
                    tlabel = self.toplabel[:asdf+1]
                    niu1 = ''
                    for i in tlabel:
                        niu1 += i
                    self.num1.set(niu1)   # 把 运算符添加到最上面的label里
                    print(self.yslist)
                else:
                    self.yslist.append(ysflag)  # 向列表中添加运算符
                    self.toplabel.append(ysflag)
                    print(self.yslist)
            else:
                pass
        elif self.num.get() != 0 and len(self.yslist) == 0:  # 显示的数字不为0，列表长度为0

            self.yslist.append(self.num.get())
            self.yslist.append(ysflag)

    # 获取运算结果
    def getresult(self):
        self.isys = True
        flags = ['*', '/', '-', '+', '%']
        if len(self.yslist) != 0 and self.yslist[-1] not in flags:

            self.toplabel.clear()  # 按下等号时清空上面label的列表

            if self.num.get() == '0' and len(self.yslist) != 0:  # 如果屏幕上的数字为0，而字符串长度不为0时
                self.num.set('除数不能为0')

            result = eval(''.join(self.yslist))  # eval运行
            if type(result) == float:   # 判断结果是不是一个浮点数，是的话只截取小数点后五位
                c = str(result)
                if len(c) - c.index('.') > 5:
                    b = '% 0.5f' % float(c)
                elif len(c) - c.index('.') == 2 and c[-1] == '0':  # 整数.0
                    b = int(result)
                else:
                    b = float(c)

                self.num.set(b)
                self.num1.set(b)
                self.yslist.clear()
                print(self.yslist)
            else:
                self.num.set(result)
                self.num1.set(result)
                self.yslist.clear()
                print('- '*10)
                print(self.yslist)
        else:
            pass

    # 删除操作
    def delnum(self):

        if len(self.yslist) != 0:  # 如果用户不点数字直接点运算符则pass，else则执行以下操作
            flags = ['*', '/', '-', '+', '%']
            if self.yslist[-1] not in flags:
                self.isys = True
                self.yslist.pop()   # 列表pop删除
                self.toplabel.pop()  # 同时末尾删除label
                print(self.yslist)
                n = ''              # 输出要显示的内容
                for i in self.yslist:
                    n += i
                self.num.set(str(n))
                # self.num1.set(str(n))
            else:
                pass
        else:
            pass

    # 清除操作
    def clearnum(self):

        self.isys = True
        self.yslist.clear()  # clear清除
        self.toplabel.clear()
        self.num.set(0)
        self.num1.set(0)

    # CE操作
    def cenum(self):
        self.yslist.clear()
        self.yslist.append(self.num1.get())
        print(self.yslist)

        self.num.set(0)

    # 开方操作
    def sqrtnum(self):
        self.isys = True

        aa = float(self.num.get())  # 获取屏幕上的值

        if aa > 0:  # 负数不能开方

            niunum = str(math.sqrt(aa))  # 截取小数点后三位
            if len(niunum) - niunum.index('.') == 2 and niunum[-1] == '0':
                n = niunum[:-2]  # 直接去除小数点和小数部分

                self.toplabel.clear()
                self.yslist.clear()
                self.num.set(n)  # 显示出结果
                self.num1.set(n)
            else:
                niun = '% 0.5f' % float(str(math.sqrt(aa)))  # 开方后只保留五位小数

                self.num.set(niun)
                self.num1.set(niun)
                self.toplabel.clear()
                self.yslist.clear()
        else:
            self.toplabel.clear()
            self.yslist.clear()
            self.num.set(0)
            self.num.set(0)

    # 平方
    def pownum(self):
        if len(self.yslist) != 0 or self.num.get() != '0':  # 判断列表长度是否为0，如果为0，则pass
            self.isys = True
            n = float(self.num.get())  # 获取屏幕上的值
            self.yslist.clear()
            self.toplabel.clear()

            self.yslist.append(str(math.pow(float(n), 2)))  # 把平方的结果添加到列表里
            self.toplabel.append(str(math.pow(float(n), 2)))
            print(self.yslist)
            self.num.set(math.pow(float(n), 2))  # 把平方的结果添加到label里
            self.num1.set(math.pow(float(n), 2))
            print(math.pow(float(n), 2))
        else:
            pass

    # 1/x 操作
    def peichunum(self):
        self.isys = True
        if len(self.yslist) != 0 or self.num.get() != '0':  # 如果用户不点数字直接点运算符则pass，else则执行以下操作
            n = float(self.num.get())  # 获取屏幕上的值

            niunum = '% 0.5f' % float(1/int(n))  # 截取小数点后五位
            self.yslist.clear()
            self.toplabel.clear()

            self.yslist.append(niunum)
            self.toplabel.append(niunum)

            self.num.set(niunum)
            self.num1.set(niunum)

        else:
            pass

    # 正负号
    def zhengfu(self):

        self.isys = True
        niunum = self.num.get()
        if float(niunum) < 0:
            self.num.set(abs(float(niunum)))
            self.num1.set(abs(float(niunum)))

        else:
            self.num.set(-(float(self.num.get())))  # 输入的数小于零
            self.num1.set(-(float(self.num.get())))  # 输入的数小于零

        self.yslist = self.yslist[:len(self.yslist)-len(self.num.get())+1]  # 对列表进行切片，去除输入的数字
        self.toplabel = self.yslist[:len(self.yslist)-len(self.num.get())+1]  # 对列表进行切片，去除输入的数字
        self.yslist.append(self.num.get())  # 再向列表添加显示的数字
        self.toplabel.append(self.num.get())  # 再向列表添加显示的数字

        print(self.yslist)

    # 小数点操作
    def dotsum(self):
        if '.' not in self.num.get():  # 看看显示的数字里有没有小数点
            if self.yslist[:-1] != '.':  # 判断最后一位是不是小数点，

                if self.num.get() == '0':  # 如果开始
                    self.num.set('0.')
                    self.yslist.append('0.')
                    self.toplabel.append('0.')
                    print(self.yslist)
                else:
                    self.num.set(self.num.get() + '.')  # 在原先字符后继续添加字符
                    self.yslist.append('.')  # 向列表添加显示的数字
                    self.toplabel.append('.')
                    print(self.yslist)

            else:
                pass
        else:
            pass

    # 界面函数
    def initwindow(self):
        app = tkinter.Tk()
        app.minsize(300, 420)
        app.resizable(False, False)  # 窗口大小不能改变
        app.title('小牛计算器')
        app.iconbitmap(bitmap='./pygame.ico')

        def zuozhe():
            tkinter.messagebox.showinfo(title='作者', message='如果您在使用过程中遇到了问题，请联系作者\n'
                                                            '作者；牛少鹏\n邮箱：xxx@yy.com')
        def bangzhu():
            tkinter.messagebox.showinfo(title='帮助', message='1.CE键： 只清空您在输入运算符之后输入的数字\n'
                                                            '2.C键：   清空您已输入的所有数字和运算符\n'
                                                            '3.del键： 从末尾依次删除您输入的数字\n'
                                                            '2.√键：   对您输入的数进行开方\n'
                                                             )
        def banben():
            tkinter.messagebox.showinfo(title='版本', message='版本：1.0\n'
                                                            '版本名: Arsenal')

        def shouce():
            tkinter.messagebox.showinfo(title='用户手册', message='用户手册：\n'
                                                            '1.如果您想输入一个数的正负数，请先按数字再按正负号\n'
                                                            '2.如果您连续点击多次运算符，则只有第一次点击会生效\n'
                                                            '3.如果您要对负数进行开方，则结果为0 \n'
                                                            '4.结果只保留五位小数\n'
                                                            '5.如果您要求小数平方，则按下x²后按下=号键可以把结果\n'
                                                              '  只保留五位小数\n'
                                                            '6.在您进行完一次带有等号的运算后，可以不清空屏幕上的数字\n'
                                                              '  直接开始下一次运算\n'
                                                              '  例如: 按下3+3=后屏幕显示6，可以不按清空键就进行4+4的运算\n'
                                                            '7.在上一次运算完成后也可以直接按运算符对上一次运算的结果进行运算\n'
                                                            '8.如果您依次输入3 + 3 * 2 则优先计算先输入的运算符，结果为12\n')

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

        # 结果框

        # 过程显示框
        self.num1 = tkinter.StringVar()
        self.num1.set(0)
        label = tkinter.Label(app, textvariable=self.num1, anchor='e', font=('楷体', 13), bg='white')
        label.place(x=0, y=0, width=300, height=50)

        # 结果显示框
        self.num = tkinter.StringVar()
        self.num.set(0)
        label = tkinter.Label(app, textvariable=self.num, anchor='e', font=('楷体', 25), bg='white')
        label.place(x=0, y=50, width=300, height=50)

        # 颜色变换函数
        def changebg(evt):
            evt.widget['bg'] = "Silver"  # 亮灰色

        def backbg(evt):
            evt.widget['bg'] = 'Gainsboro'  # 淡灰色#DCDCDC

        # 操作界面
        # 第一行
        btn1 = tkinter.Button(app, text='%', borderwidth=0, bg='Gainsboro', command=lambda: self.pressys('%'))
        btn1.place(x=0, y=100, width=75, height=50)
        btn1.bind('<Enter>', changebg)
        btn1.bind('<Leave>', backbg)

        btn2 = tkinter.Button(app, text='√', borderwidth=0, bg='Gainsboro', command=lambda: self.sqrtnum())
        btn2.place(x=75, y=100, width=75, height=50)
        btn2.bind('<Enter>', changebg)
        btn2.bind('<Leave>', backbg)

        btn3 = tkinter.Button(app, text='x²', borderwidth=0, bg='Gainsboro', command=lambda: self.pownum())
        btn3.place(x=150, y=100, width=75, height=50)
        btn3.bind('<Enter>', changebg)
        btn3.bind('<Leave>', backbg)

        btn4 = tkinter.Button(app, text='¹/x', borderwidth=0, bg='Gainsboro', command=lambda: self.peichunum())
        btn4.place(x=225, y=100, width=75, height=50)
        btn4.bind('<Enter>', changebg)
        btn4.bind('<Leave>', backbg)

        # 第二行
        btn5 = tkinter.Button(app, text='CE', borderwidth=0, bg='Gainsboro', command=lambda: self.cenum())
        btn5.place(x=0, y=150, width=75, height=50)
        btn5.bind('<Enter>', changebg)
        btn5.bind('<Leave>', backbg)

        btn6 = tkinter.Button(app, text='C', borderwidth=0, bg='Gainsboro', command=lambda: self.clearnum())
        btn6.place(x=75, y=150, width=75, height=50)
        btn6.bind('<Enter>', changebg)
        btn6.bind('<Leave>', backbg)

        btn7 = tkinter.Button(app, text='del', borderwidth=0, bg='Gainsboro', command=lambda: self.delnum())
        btn7.place(x=150, y=150, width=75, height=50)
        btn7.bind('<Enter>', changebg)
        btn7.bind('<Leave>', backbg)

        btn8 = tkinter.Button(app, text='÷', borderwidth=0, bg='Gainsboro', command=lambda: self.pressys('/'))
        btn8.place(x=225, y=150, width=75, height=50)
        btn8.bind('<Enter>', changebg)
        btn8.bind('<Leave>', backbg)

        # 第三行
        btn9 = tkinter.Button(app, text='7', borderwidth=0, bg='Gainsboro', command=lambda: self.figrue('7'))
        btn9.place(x=0, y=200, width=75, height=50)
        btn9.bind('<Enter>', changebg)
        btn9.bind('<Leave>', backbg)

        btn10 = tkinter.Button(app, text='8', borderwidth=0, bg='Gainsboro', command=lambda: self.figrue('8'))
        btn10.place(x=75, y=200, width=75, height=50)
        btn10.bind('<Enter>', changebg)
        btn10.bind('<Leave>', backbg)

        btn11 = tkinter.Button(app, text='9', borderwidth=0, bg='Gainsboro', command=lambda: self.figrue('9'))
        btn11.place(x=150, y=200, width=75, height=50)
        btn11.bind('<Enter>', changebg)
        btn11.bind('<Leave>', backbg)

        btn12 = tkinter.Button(app, text='×', borderwidth=0, bg='Gainsboro', command=lambda: self.pressys('*'))
        btn12.place(x=225, y=200, width=75, height=50)
        btn12.bind('<Enter>', changebg)
        btn12.bind('<Leave>', backbg)

        # 第四行
        btn13 = tkinter.Button(app, text='4', borderwidth=0, bg='Gainsboro', command=lambda: self.figrue('4'))
        btn13.place(x=0, y=250, width=75, height=50)
        btn13.bind('<Enter>', changebg)
        btn13.bind('<Leave>', backbg)

        btn14 = tkinter.Button(app, text='5', borderwidth=0, bg='Gainsboro', command=lambda: self.figrue('5'))
        btn14.place(x=75, y=250, width=75, height=50)
        btn14.bind('<Enter>', changebg)
        btn14.bind('<Leave>', backbg)

        btn15 = tkinter.Button(app, text='6', borderwidth=0, bg='Gainsboro', command=lambda: self.figrue('6'))
        btn15.place(x=150, y=250, width=75, height=50)
        btn15.bind('<Enter>', changebg)
        btn15.bind('<Leave>', backbg)

        btn16 = tkinter.Button(app, text='－', borderwidth=0, bg='Gainsboro', command=lambda: self.pressys('-'))
        btn16.place(x=225, y=250, width=75, height=50)
        btn16.bind('<Enter>', changebg)
        btn16.bind('<Leave>', backbg)

        # 第五行
        btn17 = tkinter.Button(app, text='1', borderwidth=0, bg='Gainsboro', command=lambda: self.figrue('1'))
        btn17.place(x=0, y=300, width=75, height=50)
        btn17.bind('<Enter>', changebg)
        btn17.bind('<Leave>', backbg)

        btn18 = tkinter.Button(app, text='2', borderwidth=0, bg='Gainsboro', command=lambda: self.figrue('2'))
        btn18.place(x=75, y=300, width=75, height=50)
        btn18.bind('<Enter>', changebg)
        btn18.bind('<Leave>', backbg)

        btn19 = tkinter.Button(app, text='3', borderwidth=0, bg='Gainsboro', command=lambda: self.figrue('3'))
        btn19.place(x=150, y=300, width=75, height=50)
        btn19.bind('<Enter>', changebg)
        btn19.bind('<Leave>', backbg)

        btn20 = tkinter.Button(app, text='＋', borderwidth=0, bg='Gainsboro', command=lambda: self.pressys('+'))
        btn20.place(x=225, y=300, width=75, height=50)
        btn20.bind('<Enter>', changebg)
        btn20.bind('<Leave>', backbg)

        # 第六行
        btn21 = tkinter.Button(app, text='±', borderwidth=0, bg='Gainsboro', command=lambda : self.zhengfu())
        btn21.place(x=0, y=350, width=75, height=50)
        btn21.bind('<Enter>', changebg)
        btn21.bind('<Leave>', backbg)

        btn22 = tkinter.Button(app, text='0', borderwidth=0, bg='Gainsboro', command=lambda: self.figrue('0'))
        btn22.place(x=75, y=350, width=75, height=50)
        btn22.bind('<Enter>', changebg)
        btn22.bind('<Leave>', backbg)

        btn23 = tkinter.Button(app, text='•', borderwidth=0, bg='Gainsboro', command=lambda: self.dotsum())
        btn23.place(x=150, y=350, width=75, height=50)
        btn23.bind('<Enter>', changebg)
        btn23.bind('<Leave>', backbg)

        btn24 = tkinter.Button(app, text='=', borderwidth=0, bg='Gainsboro', command=lambda: self.getresult())
        btn24.place(x=225, y=350, width=75, height=50)
        btn24.bind('<Enter>', changebg)
        btn24.bind('<Leave>', backbg)

        app.mainloop()

c = Calc()






