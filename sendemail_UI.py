import tkinter
from tkinter import *
import requests
from tkinter import messagebox


def validateEmailAddress(url):
    pat = r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$'
    matched = re.match(pat, url)
    if matched:
        return 'Y'
    else:
        return 'N'


class send_email_UI:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("600x500")
        self.root.title("邮件发送程序")

        self.label1 = Label(self.root, text="请输入收件人邮箱地址：（多个收件人请以，分隔）")
        self.label1.pack()

        self.text1 = Text(self.root, height=3, width=70)
        self.text1.pack()

        self.label4 = Label(self.root, text="请输入你的名称：")
        self.label4.pack()

        self.text4 = Text(self.root, height=3, width=70)
        self.text4.pack()

        self.label2 = Label(self.root, text="请输入邮件标题信息：")
        self.label2.pack()

        self.text2 = Text(self.root, height=10, width=70)
        self.text2.pack()

        self.label3 = Label(self.root, text="请输入邮件文本信息：")
        self.label3.pack()

        self.text3 = Text(self.root, height=10, width=70)
        self.text3.pack()

        self.button1 = Button(self.root, text="发送邮件",command=self.send_email)
        self.button1.pack()

        self.root.mainloop()

    def send_email(self):
        urls = self.text1.get("0.0",END)
        urls=urls.split(",")
        header = self.text2.get("0.0",END)
        text = self.text3.get("0.0",END)
        sender=self.text4.get("0.0",END)
        '''
        识别所输入的网址中的错误网址     
        此处我测试了将网址全部传到webservice后台进行处理，但处理结果会是将错误网址进行分为单个数字进行返回值，
        和我预期想得到的位置不一样，所以我在此处进行了一个网址判别过程   
        '''
        u=[]
        wrong=[]
        for i in urls:
            if validateEmailAddress(i)=="Y":
                u.append(i)
            elif validateEmailAddress(i)=="N":
                wrong.append(str(int(urls.index(i)) + 1))
        if wrong is not None:
            w='第 '
            for i in wrong:
                w=w+i+" "
            messagebox.showwarning('警告', w + '个邮箱地址有错误！')
        url="http://localhost:8000/send?url="
        for i in urls:
            url=u+i+","
        url=url+"&header="+header+"&text="+text+"&sender="+sender

        a = requests.get(url)
        if str(a.content)[4]=="#":
            tkinter.messagebox.showinfo('提示','邮件发送成功!')
        elif str(a.content)[4]=="a":
            tkinter.messagebox.showerror('错误', '邮件发送失败，收件人已拒绝!')
        elif str(a.content)[4]=="b":
            tkinter.messagebox.showerror('错误', '邮件发送失败，认证错误!')
        elif str(a.content)[4]=="c":
            tkinter.messagebox.showerror('错误', '邮件发送失败，发件人被拒绝!')
        else:
            tkinter.messagebox.showerror('错误', str(a.content))



if __name__ == '__main__':
    a = send_email_UI()
