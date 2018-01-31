# -*- coding: utf-8 -*-
from random import randint
from django.core.mail import send_mail

from MOOC.settings import DEFAULT_FROM_EMAIL
from users.models import EmailVerifyRecord
def random_str(randomlength=8):
    str = ''
    chars ='AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890'
    length = len(chars)-1
    for i in range(randomlength):
        str += chars[randint(0,length)]
    return str


def send_register_email(email,send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    email_title = ''
    email_body = ''
    if send_type == 'register':
        email_title = u'MOOC注册激活链接'
        email_body = u'请点击下边的链接激活你的账号：http://127.0.0.1:8000/active/{0}'.format(code)
        send_status =  send_mail(email_title,email_body,DEFAULT_FROM_EMAIL,[email])
        if send_status:
            print u'邮件发送成功！'

    elif send_type =='forget':
        email_title = u'MOOC密码重置密码重置'
        email_body = u'请点击下边的链接重置你的密码：http://127.0.0.1:8000/reset/{0}'.format(code)
        send_status =  send_mail(email_title,email_body,DEFAULT_FROM_EMAIL,[email])
        if send_status:
            print u'邮件发送成功！'