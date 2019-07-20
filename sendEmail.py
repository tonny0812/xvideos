import smtplib
from email.mime.text import MIMEText

def SendEmail(text):
  
    fromAdd="kljxnnn@163.com"  #你的邮箱   发件地址
    toAdd = 'kljxn@qq.com'
    subject = 'xvideos爬虫出错'
    
    _pwd  = "163mail"  #授权码
    
    msg = MIMEText(text)
    msg["Subject"] = subject
    msg["From"]    = fromAdd
    msg["To"]      = toAdd
    try:
        s = smtplib.SMTP_SSL("smtp.163.com", 465)
        s.login(fromAdd, _pwd)
        s.sendmail(fromAdd, toAdd, msg.as_string())
        s.quit()
        print ("Send Email Success!")
    except smtplib.SMTPException:
        print('Send Email Falied!')
        
if __name__=='__main__':
    
    text = 'hhhhha'
    SendEmail(text)