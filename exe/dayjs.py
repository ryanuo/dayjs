#  -*-coding:utf8 -*-
import os, requests, json, threading, datetime, webbrowser
import tkinter.font as tf
import tkinter.messagebox
from io import BytesIO
from tkinter import *  # 使用Tkinter前需要先导入
from PIL import ImageTk, Image
from tkinter.ttk import Separator

# 获取今日时间戳
today_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class TkinterWeb:
    def __init__(self):
        default_value_page = StringVar()
        default_value_page.set(dayN())  # 设置初始化的天数
        self.menuList()
        default_d = Label(window, text='天')
        rb_page_label = Label(window, text='设置天数:')
        default_today_time = Label(window, text='今日时间：' + today_time, font=('Arial', 16))
        # 打开配置文件
        open_config = Button(window, text='打开配置文件', foreground='red', font=('Arial', 10), width=10, height=1,
                             command=lambda: thread_it(self.open_file))
        # 点击查询
        post_title = Button(window, text='获取题目', foreground='red', font=('黑体', 10), width=10, height=1,
                            command=lambda: thread_it(self.postTitle))
        sep = Separator(window, orient=HORIZONTAL)  # VERTICAL为竖的分割线
        sep.pack(padx=100, pady=100, fill=X)  # 我试了一下，去掉fill=X则分隔符不出现
        self.t1 = Entry(window, show=None, textvariable=default_value_page, bg='#D8BFD8', width=3)
        default_today_time.place(x=200, y=13)
        rb_page_label.place(x=310, y=53)
        open_config.place(x=200, y=50)  # 打开配置
        post_title.place(x=420, y=50)  # 查询
        self.t1.place(x=370, y=53)
        default_d.place(x=392, y=53)
        img_label = Label(window, image=img, width=100, height=100)
        img_label.place(x=600, y=270)
        # 设置动态变量
        self.str1 = StringVar()
        self.str2 = StringVar()
        self.str3 = StringVar()
        self.str4 = StringVar()
        self.s1 = StringVar()
        self.s2 = StringVar()
        self.s3 = StringVar()
        self.s4 = StringVar()
        self.l1 = StringVar()
        self.l2 = StringVar()
        self.l3 = StringVar()
        self.l4 = StringVar()
        self.open_config = [0, 0, 0, 0]  # 动态按钮
        thread_it(self.dynamic_tab())

    # 打开配置文件
    def open_file(self):
        path = 'config'
        os.startfile(path)

    # 将获取的数据写入到配置文件种
    def write_config(self, con):
        # status = tkinter.messagebox.askokcancel('确认操作', '确定要更新配置中心的appid和key？确认无误在更新')
        # if status:
        config_json = {
            "page": self.t1.get(),
            "tit_content": con
        }
        with open('config/config.json', 'w+', encoding="utf-8") as f:
            f.write(json.dumps(config_json, ensure_ascii=False))
            f.close()
        tkinter.messagebox.showinfo(title='提示', message='今日题目获取成功')
        return

    # 题目的获取
    def postTitle(self):
        with open('config/title.json', encoding='UTF-8') as f:
            res = json.loads(f.read())['result'][f'{self.t1.get()}_']
            if len(res) == 4:
                self.backTitle(res, 'html', 'css', 'js', 'skill')
            else:
                self.backTitle(res, 'html', 'css', 'js')
            f.close()

    # 链接分析
    def backTitle(self, dataList, *args):
        result = []
        dayn = self.t1.get()
        for index, item in enumerate(args):
            title = f'{item.upper()}题目:-' + dataList[item]['title']
            if int(dayn) <= 11:
                tit_link = f'http://www.h-camel.com/show/{(int(dayn) - 1) * len(args) + index + 1}.html'
            elif int(dayn) >= 35:
                tit_link = f'http://www.h-camel.com/show/{35 + (int(dayn) - 12) * len(args) + index + 1}.html'
            else:
                print(33 + (int(dayn) - 12) * len(args) + index + 1)
                tit_link = f'http://www.h-camel.com/show/{33 + (int(dayn) - 12) * len(args) + index + 1}.html'
            result.append({"title": title, "tit_link": tit_link})
        if len(result) < 4:
            result.append({"title": "SKILL:-暂无题目", "tit_link": ''})
        self.write_config(result)
        thread_it(self.dynamic_column(result))
        thread_it(self.btnChange())
        return result

    # 动态生成
    def dynamic_tab(self):
        f = open('config/config.json', encoding='utf-8')
        for index, item in enumerate(json.load(f)['tit_content']):
            b = 'str' + str(index + 1)
            c = 's' + str(index + 1)
            d = 'l' + str(index + 1)
            self.__dict__[d].set(item['tit_link'])
            self.__dict__[b].set(item['title'].split(':-')[0])
            self.__dict__[c].set(item['title'].split(':-')[1])
            hd_label = Label(window, textvariable=self.__dict__[b], font=('黑体', 13))
            rb_args_label = Message(window, textvariable=self.__dict__[c], font=('黑体', 13), foreground='#483D8B',
                                    width=700,
                                    anchor=W)
            self.open_config[index] = Button(window, text='点击访问', foreground='#778899',
                                             font=('Arial', 10),
                                             width=10, height=1,
                                             command=lambda f=self.__dict__[d].get(): thread_it(self.open_url(f)))
            hd_label.place(x=10, y=120 + index * 80)
            rb_args_label.place(x=10, y=160 + index * 80)
            self.open_config[index].place(x=100, y=120 + index * 80)
            # 动态生成展示栏

    # 动态改变按钮的值
    def btnChange(self):
        f = open('config/config.json', encoding='utf-8')
        for index, item in enumerate(json.load(f)['tit_content']):
            d = 'l' + str(index + 1)
            self.__dict__[d].set(item['tit_link'])
            self.open_config[index] = Button(window, text='点击访问', foreground='#8B4513',
                                             font=('Arial', 10),
                                             width=10, height=1,
                                             command=lambda f=self.__dict__[d].get(): thread_it(self.open_url(f)))
            self.open_config[index].place(x=100, y=120 + index * 80)
    def dynamic_column(self, res):
        for index, item in enumerate(res):
            b = 'str' + str(index + 1)
            c = 's' + str(index + 1)
            self.__dict__[b].set(item['title'].split(':-')[0])
            self.__dict__[c].set(item['title'].split(':-')[1])

    # 打开网页跳转
    def open_url(self, ul):
        webbrowser.open(ul, new=0)

    # 创建菜单
    def menuList(self):
        f = tkinter.Menu(window)  # 创建根菜单
        window['menu'] = f  # 顶级菜单关联根窗体
        f1 = tkinter.Menu(f, tearoff=False)  # 创建子菜单
        f1.add_command(label='打开', command=lambda: thread_it(self.open_url('https://m.mr90.top')))  # 子菜单栏
        f.add_cascade(label='博客', menu=f1)  # 创建顶级菜单栏，并关联子菜单
        f.add_cascade(label='关于')
        f.add_cascade(label='更新', command=lambda: thread_it(self.open_url('https://github.com/Rr210/dayjs/releases/')))

    # 更新提示
    def sUpdate(self):
        title = ['功能待完善']

    # 页面的刷新
    def refresh_data(self):
        window.destroy()


# 获取题目到title.json文件中
def getData():
    res = requests.get('http://api.h-camel.com/api?mod=interview&ctr=issues&act=history').json()
    with open('config/title.json', 'w+', encoding='UTF-8') as f:
        f.write(json.dumps(res, ensure_ascii=False))
        f.close()


# 天数获取
def dayN():
    fs = open('config/config.json', encoding='utf-8')
    # json.load()参数是文件对象
    return json.load(fs)['page']  # 定义全局变量 天数


# 缓解软件卡顿
def thread_it(func, *args):
    # 创建线程
    t = threading.Thread(target=func, args=args)
    # 守护线程
    t.setDaemon(True)
    # 启动
    t.start()


# 设置打开的位置
def center_window(width=720, height=500):
    # get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    # calculate position x and y coordinates
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))


if __name__ == "__main__":
    # 题目文件
    window = Tk()
    # 设置window窗口标题
    window.title('前端每日记v1.0 @Harry')
    # 设置窗口的长度和宽度
    window.geometry('720x500')
    # 禁止用户调整窗口大小
    window.resizable(False, False)
    center_window(720, 500)
    path = "https://gitee.com/rbozo/picgo_image/raw/master/image/0/gzh.png"
    res_img = requests.get(path)
    im = Image.open(BytesIO(res_img.content))
    im = im.resize((100, 100))
    img = ImageTk.PhotoImage(im)
    # 绘制窗口内容
    folder = os.path.exists('config/title.json')
    if not folder:
        getData()  # 获取题目文件
    thread_it(TkinterWeb)
    window.mainloop()
