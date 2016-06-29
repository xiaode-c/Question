# coding:utf-8
import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


def send_email(from_addr, to_addr, subject, password):
    msg = MIMEText("欢迎加入QA，请前网网站验证你的账号",'html','utf-8')
    msg['From'] = _format_addr(u'<%s>' % from_addr)
    msg['To'] = _format_addr(u'<%s>' % to_addr)
    msg['Subject'] = Header(subject, 'utf-8').encode()

    smtp = smtplib.SMTP_SSL('smtp.163.com', 465)
    # smtp.starttls()
    smtp.set_debuglevel(1)
    smtp.ehlo("smtp.163.com")
    print from_addr,password
    smtp.login(from_addr, password)
    smtp.sendmail(from_addr, [to_addr], msg.as_string())
    smtp.quit()

if __name__ == "__main__":
    # 这里的密码是开启smtp服务时输入的客户端登录授权码，并不是邮箱密码
    send_email(u"18710890823@163.com",u"1178717119@qq.com","欢迎加入QA",u"gaodebao712")
