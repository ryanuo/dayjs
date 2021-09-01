#  -*-coding:utf8 -*-
import os, requests, json, threading, datetime, webbrowser
import tkinter.messagebox
from io import BytesIO
from tkinter import *  # 使用Tkinter前需要先导入
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter.ttk import Separator, Combobox

# 获取今日时间戳
today_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class TkinterWeb:
    def __init__(self):
        self.default_value_page = StringVar()
        self.default_value_page.set(day_n()[0])  # 设置初始化的天数
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
        pre_t = Button(window, text='上一页', foreground='#8b4513', font=('Cambria', 10), width=10, height=1,
                       command=lambda: thread_it(self.pnt('pre')))
        next_t = Button(window, text='下一页', foreground='#8b4513', font=('Cambria', 10), width=10, height=1,
                        command=lambda: thread_it(self.pnt('next')))
        # 题目总数统计
        self.tot = StringVar()
        self.tot.set(f'来自：前端每日知识3+1，本地题库对应天数：{day_n()[1]}天')
        total_all = Label(window, textvariable=self.tot, font=('Calibri', 9, 'bold'))
        total_all.place(x=400, y=450)
        sep = Separator(window, orient=HORIZONTAL)  # VERTICAL为竖的分割线
        sep.pack(padx=100, pady=100, fill=X)  # 我试了一下，去掉fill=X则分隔符不出现
        self.t1 = Entry(window, show=None, textvariable=self.default_value_page, bg='#D8BFD8', width=3)
        pre_t.place(x=600, y=13)
        next_t.place(x=600, y=53)
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
        self.theme = '#fff'
        thread_it(self.dynamic_tab)

    # 打开配置文件
    def open_file(self):
        paths = 'config'
        os.startfile(paths)

    # 将获取的数据写入到配置文件种
    def write_config(self, con, total):
        # status = tkinter.messagebox.askokcancel('确认操作', '确定要更新配置中心的appid和key？确认无误在更新')
        # if status:
        config_json = {
            "page": self.t1.get(),
            "total_titles": total,
            "tit_content": con,
        }
        with open('config/main_config.json', 'w+', encoding="utf-8") as f:
            f.write(json.dumps(config_json, indent=2, ensure_ascii=False))
            f.close()
        tkinter.messagebox.showinfo(title='提示', message='题目获取成功')
        return

    # 题目的获取
    def postTitle(self):
        try:
            with open('config/title.json', encoding='UTF-8') as f:
                str_f = f.read()
                tot = len(json.loads(str_f)["result"]) + 1
                str_m = f'来自：前端每日知识3+1，本地题库对应天数：{tot}天'
                res = json.loads(str_f)['result'][f'{self.t1.get()}_']
                self.tot.set(str_m)
                if len(res) < 4:
                    res['skill'] = {"title": "暂无题目", "issuesId": 0}
                thread_it(self.write_config(res, tot))
                thread_it(self.btnChange)  # 覆盖上一次生成的按钮链接
                f.close()
        except ValueError:
            tkinter.messagebox.showerror(title='提示', message='本地题库有误，请重置本地题库，点击左上角菜单')

    # 动态生成
    def dynamic_tab(self):
        f = open('config/main_config.json', encoding='utf-8')
        list_con = json.load(f)['tit_content']
        f.close()
        for index, item in enumerate(list_con):
            b = 'str' + str(index + 1)
            c = 's' + str(index + 1)
            d = 'l' + str(index + 1)
            tit_link = f'https://hub.fastgit.org/haizlin/fe-interview/issues/{list_con[item]["issuesId"]}'
            self.__dict__[d].set(tit_link)
            self.__dict__[b].set(item.upper())
            self.__dict__[c].set(list_con[item]['title'])
            hd_label = Label(window, textvariable=self.__dict__[b], font=('黑体', 13))
            rb_args_label = Message(window, textvariable=self.__dict__[c], font=('黑体', 13), foreground='#483D8B',
                                    width=700,
                                    anchor=W)
            self.open_config[index] = Button(window, text='点击访问', foreground='#8b4513',
                                             font=('Arial', 10, 'bold'),
                                             width=10, height=1,
                                             command=lambda f=self.__dict__[d].get(): thread_it(self.open_url(f)))
            hd_label.place(x=10, y=120 + index * 80)
            rb_args_label.place(x=10, y=160 + index * 80)
            self.open_config[index].place(x=100, y=120 + index * 80)

    # 动态改变按钮的值
    def btnChange(self):
        f = open('config/main_config.json', encoding='utf-8')
        list_con = json.load(f)['tit_content']
        for index, item in enumerate(list_con):
            b = 'str' + str(index + 1)
            c = 's' + str(index + 1)
            d = 'l' + str(index + 1)
            tit_link = f'https://hub.fastgit.org/haizlin/fe-interview/issues/{list_con[item]["issuesId"]}'
            self.__dict__[d].set(tit_link)
            self.__dict__[b].set(item.upper())
            self.__dict__[c].set(list_con[item]['title'])
            self.open_config[index] = Button(window, text='点击访问', foreground='#8B4513',
                                             font=('Arial', 10),
                                             width=10, height=1,
                                             command=lambda fl=self.__dict__[d].get(): thread_it(self.open_url(fl)))
            self.open_config[index].place(x=100, y=120 + index * 80)

    # 打开网页跳转
    def open_url(self, ul):
        if ul.split('/')[-1] == '0':
            tkinter.messagebox.showerror(title='提示', message='跳转地址为空')
        else:
            webbrowser.open(ul, new=0)

    # 创建菜单
    def menuList(self):
        f = tkinter.Menu(window)  # 创建根菜单
        window['menu'] = f  # 顶级菜单关联根窗体
        f1 = tkinter.Menu(f, tearoff=False)  # 创建子菜单
        f.add_cascade(label='菜单', menu=f1)  # 创建顶级菜单栏，并关联子菜单
        f1.add_command(label='博客', command=lambda: thread_it(self.open_url('https://m.mr90.top')))  # 子菜单栏
        f1.add_command(label='语雀',
                       command=lambda: thread_it(self.open_url('https://www.yuque.com/hr_iu/web/wg94gt')))  # 子菜单栏
        f1.add_command(label='关于', command=About)  # 新的窗口
        f1.add_command(label='交流群', command=Contact)  # 新的窗口
        # f1.add_command(label='交流群', command=lambda: thread_it(Contact))  # 新的窗口
        f1.add_command(label='建议反馈',
                       command=lambda: thread_it(self.open_url('https://hub.fastgit.org/Rr210/dayjs/issues')))  # 建议反馈
        f1.add_command(label='退出',
                       command=lambda: thread_it(self.layouts))  # 建议反馈
        f.add_cascade(label='更新',
                      command=lambda: thread_it(self.open_url('https://hub.fastgit.org/Rr210/dayjs/releases/')))
        f.add_cascade(label='重置题库', command=lambda: thread_it(getData))
        f.add_cascade(label='搜索', command=Search)

    # 上一页,下一页
    def pnt(self, params):
        if params == 'pre' and int(self.t1.get()) > 1:
            self.default_value_page.set(int(day_n()[0]) - 1)
        elif params == 'next':
            self.default_value_page.set(int(day_n()[0]) + 1)
        else:
            tkinter.messagebox.showerror(title='提示', message='天数不能大于题录总数，最小值为1')
            return False
        thread_it(self.postTitle)

    # 更新提示
    def supdate(self):
        title = ['功能待完善']

    # 退出
    def layouts(self):
        window.destroy()

    # # 主题自定义
    # def theme_custom(self,i):
    #     colors = {
    #         0: "#EFEBE7",
    #         1: "#F9CDDC",
    #         2: "#C578A4",
    #         3: "#9B7EB6",
    #         4: "#A8B680",
    #         5: "#F9DDD3",
    #         6: "#848786",
    #     }
    #     self.theme = colors[i]
    #     self.change_ele_bg(colors[self.theme % len(colors)])

    # def change_ele_bg(self, themecolor):
    #     gui_style = Style()
    #     gui_style.configure('My.TRadiobutton', background=themecolor)
    #     gui_style.configure('My.TFrame', background=themecolor)
    #     self.init_window_name['bg'] = themecolor  # 主窗口的背景色


# 获取题目到title.json文件中
def getData():
    result = tkinter.messagebox.askokcancel('确定 | 取消', '确认要重新加载本地题库，确认后耐心等待！！')
    if result:
        progressbarOne = tkinter.ttk.Progressbar(window, length=50, mode='determinate', orient=tkinter.HORIZONTAL)
        progressbarOne.place(x=10, y=10)
        progressbarOne['maximum'] = 100
        progressbarOne['value'] = 0
        progressbarOne.start()
        # tkinter.messagebox.showinfo(title='提示', message='正在获取，不要重复点击！！耐心等待，点击确认开始重置')
        res = requests.get('http://api.h-camel.com/api?mod=interview&ctr=issues&act=history').json()
        with open('config/title.json', 'w+', encoding='UTF-8') as f:
            f.write(json.dumps(res, ensure_ascii=False))
            f.close()
            progressbarOne['value'] = 100
            progressbarOne.stop()
            progressbarOne.destroy()
            tkinter.messagebox.showinfo(title='提示', message='最新题库已加载完成,点击确认。如需获取最新题库，点击菜单栏，重置题库')


# 天数获取
def day_n():
    fs = open('config/main_config.json', encoding='utf-8')
    p = json.load(fs)
    return [p['page'], p['total_titles']]


# 缓解软件卡顿
def thread_it(func, *args):
    # 创建线程
    t = threading.Thread(target=func, args=args)
    # 守护线程
    t.setDaemon(True)
    # 启动
    t.start()


# 设置打开的位置
def center_window(obj, width, height):
    # get screen width and height
    screen_width = obj.winfo_screenwidth()
    screen_height = obj.winfo_screenheight()
    # calculate position x and y coordinates
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    obj.geometry('%dx%d+%d+%d' % (width, height, x, y))


# 创建交流群窗口
class Contact:
    def __init__(self):
        self.tks = Toplevel()
        self.tks.title('前端小熊 交流群')
        # 设置窗口的长度和宽度
        self.tks.geometry('400x300')
        # 禁止用户调整窗口大小
        self.tks.resizable(False, False)
        thread_it(center_window(self.tks, 400, 300))
        default_hd = Label(self.tks, text='欢迎加入前端学习群,扫码加入', font=('Calibri', 15, 'bold'))
        default_hd.place(x=30, y=40)
        thread_it(pic_img(self.tks,
                          'https://gitee.com/rbozo/picgo_image/raw/master/image/0/6894948e26ffb1860f34f95ff270ae3%20.png',
                          120,
                          120, 50, 100))
        detail_data = Message(self.tks, text='QQ交流群\n群号：543171829\n简介：一群志同道合的前端学习者\n只要学不死，就往死里学', width=200)
        detail_data.place(x=180, y=120)
        self.tks.mainloop()


# 创建搜索模块
class Search:
    def __init__(self):
        self.tks = Toplevel()
        self.tks.title('前端小熊 搜索')
        # 设置窗口的长度和宽度
        self.tks.geometry('500x400')
        # 禁止用户调整窗口大小
        self.tks.resizable(False, False)
        thread_it(center_window(self.tks, 500, 400))
        v = StringVar()
        self.entry_text = Entry(self.tks, textvariable=v, width=52)
        next_t = Button(self.tks, text='点击搜索', foreground='#8b4513', font=('Cambria', 10), width=10, height=1,
                        command=lambda: thread_it(self.search_list))
        next_t.place(x=320,y=50)
        self.entry_text.place(x=50, y=20)
        comvalue = tkinter.StringVar()  # 窗体自带的文本，新建一个值
        self.comboxlist = ttk.Combobox(self.tks, textvariable=comvalue,width=50)  # 初始化
        self.comboxlist.place(x=50, y=100)
        self.tks.mainloop()

    def search_list(self):
        key = self.entry_text.get()
        res = requests.get(f'http://api.h-camel.com/api?mod=interview&ctr=issues&act=search&key={key}')
        if len(res.json()['result']['rows']) != 0:
            list_d = [item['title'] for(index,item) in enumerate(res.json()['result']['rows'])]
            self.comboxlist["values"] = list_d
            self.comboxlist.current(0)
        print(res.text)


# 创建关于窗口
class About:
    def __init__(self):
        self.a = Toplevel()
        self.a.title('前端小熊 关于页面')
        # 设置窗口的长度和宽度
        self.a.geometry('400x300')
        # 禁止用户调整窗口大小
        self.a.resizable(False, False)
        thread_it(center_window(self.a, 400, 300))
        thread_it(
            pic_img(self.a, 'https://gitee.com/rbozo/picgo_image/raw/master/image/0/%E7%86%8A%E7%8C%AB.png', 50, 50, 20,
                    20))
        Message(self.a, text='前端小熊', font=('Calibri', 14, 'bold'), width=200).place(x=80, y=30)
        Message(self.a, text='版本：v1.0.4\n作者：Harry', font=('Calibri', 13, 'bold'), width=200).place(x=20, y=100)
        r_gw = Message(self.a, text='官网：https://m.mr90.top', foreground='#0000ff', font=('Calibri', 13, 'bold'),
                       width=200)
        r_gw.place(x=20, y=150)


# 窗口对象 图片的地址 图片的宽度和高度 距离左侧的距离 距离顶部的距离
# 图片的创建
def pic_img(obj, url, w, h, x, y):
    i_img = requests.get(url)
    i_im = Image.open(BytesIO(i_img.content))
    i_im = i_im.resize((w, h))
    obj.img_res = ImageTk.PhotoImage(i_im)
    t = Label(obj, image=obj.img_res, width=w, height=h)
    t.place(x=x, y=y)


if __name__ == "__main__":
    # 题目文件
    window = Tk()
    # 设置window窗口标题
    window.title('前端小熊 v1.0.4 @Harry')
    # 设置窗口的长度和宽度
    window.geometry('720x500')
    # 禁止用户调整窗口大小
    window.resizable(False, False)
    center_window(window, 720, 500)
    # 定义页面右下角的公众号
    path = "https://gitee.com/rbozo/picgo_image/raw/master/image/0/gzh.png"
    res_img = requests.get(path)
    im = Image.open(BytesIO(res_img.content))
    im = im.resize((100, 100))
    img = ImageTk.PhotoImage(im)
    # 绘制窗口内容
    folder = os.path.exists('config/title.json')
    if not folder:
        thread_it(getData)  # 获取题目文件
    thread_it(TkinterWeb)
    window.mainloop()
