import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import logging

logging.basicConfig(level=logging.DEBUG)
from spyne import Application, rpc, ServiceBase, \
    Integer, Unicode
from spyne import Iterable
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication





class send_email():
    def __init__(self):
        self.username = *****#此处为你自己申请的阿里云邮箱地址
        self.password = *****#此处为你自己设定的密码
        self.rcptlist = []
        self.receivers = []
        self.msg = None

    def create_email(self, header, text,sender):
        msg = MIMEMultipart('mixed')
        msg = MIMEMultipart('mixed')
        # self.receivers = ','.join(tolists)
        msg['Subject'] = header
        msg['From'] = Header(sender, 'utf-8')
        msg['To'] = self.receivers
        alternative = MIMEMultipart('alternative')
        textplain = MIMEText('纯文本部分', _subtype='plain', _charset='UTF-8')
        alternative.attach(textplain)
        # 构建 multipart/alternative 的 text/html 部分
        texthtml = MIMEText(text, _subtype='html', _charset='UTF-8')
        alternative.attach(texthtml)
        # 将 alternative 加入 mixed 的内部
        msg.attach(alternative)
        return msg

    def validateEmailAddress(self,url):
        pat = r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$'
        matched = re.match(pat, url)
        if matched:
            return 'Y'
        else:
            return 'N'

    # @rpc(Unicode, Unicode, Unicode, _returns=Iterable(Unicode))
    def sendEmailBatch(self, tolists, header, text,sender):
        a = 0
        wrong_addrs = "#"
        for i in tolists:
            if self.validateEmailAddress(i) == 'N':
                print('第' + str(int(tolists.index(i)) + 1) + '个邮件地址格式错误，请检查邮件地址')
                a += 1
                wrong_addrs = wrong_addrs + i
                wrong_addrs = wrong_addrs + "#"
        if a == len(tolists):
            print('所有邮件格式地址错误，请检查邮件地址')
            return 'N', '所有邮件格式地址错误，请检查邮件地址'
        self.receivers = ','.join(tolists)
        self.msg = self.create_email(header, text,sender)
        try:
            client = smtplib.SMTP()
            # python 2.7以上版本，若需要使用SSL，可以这样创建client
            # client = smtplib.SMTP_SSL()
            client.connect('smtpdm.aliyun.com')
            client.login(self.username, self.password)
            # 发件人和认证地址必须一致
            client.sendmail(self.username, tolists, self.msg.as_string())
            client.quit()
            print('邮件发送成功！')
            return wrong_addrs
        except smtplib.SMTPRecipientsRefused:
            print('邮件发送失败，收件人被拒绝')
            return "a"
        except smtplib.SMTPAuthenticationError:
            print('邮件发送失败，认证错误')
            return "b"
        except smtplib.SMTPSenderRefused:
            print('邮件发送失败，发件人被拒绝')
            return "c"
        except smtplib.SMTPException as e:
            print('邮件发送失败, ', e.message)
            return e.message


class send(ServiceBase):

    @rpc(Integer, _returns=Integer)
    def test(self, a):
        k = send_email.bbb(self,a)
        return k

    @rpc(Unicode, Unicode, Unicode,Unicode, _returns=Iterable(Unicode))
    def send(self,url, header, text,sender):
        to_url=url.split(',')
        b=send_email()
        t=send_email.sendEmailBatch(b,to_url,header,text,sender)
        return t


application = Application([send],
                          tns='spyne.examples.hello',
                          in_protocol=HttpRpc(validator='soft'),
                          out_protocol=JsonDocument()
                          )
if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.
    from wsgiref.simple_server import make_server

    # logging.info("listening to http://127.0.0.1:8000")
    logging.info("http://localhost:8000/send?url=3309628599@qq.com,1227993492@qq.com&header=ttt&text=bbb&sender=father")
    # logging.info("listening to http://localhost:8000/test?a=10")
    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()

# if __name__ == '__main__':
#     email = send_email()
#     tolists = ['1227993492@qq.com']
#     header = '123'
#     text = 'aaa'
#     email.sendEmail(tolists, header, text)
