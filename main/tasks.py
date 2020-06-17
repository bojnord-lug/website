from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from LUG.settings import EMAIL_HOST_USER
# from main.models import NewsLetter

@shared_task
def event_send_email(id, event):
    result = send_mail(
        subject = event,
        message = " \n  http://127.0.0.1:8000/event?id={}بجنورد لاگ قراره که یه ایونت برگزار کنه . اگه می خوای بدونی چه خبره بیا به این لینک".format(id),
        from_email= EMAIL_HOST_USER,
        recipient_list = ['mahmoodabdali79@gmail.com'],
        fail_silently=False,
        )



@shared_task
def post_send_email(id, title):
    result = send_mail(
        subject = title,
        message = " بجنورد لاگ یه پست در مورد {0} گذاشته . برای اینکه بیشتر در موردش بدونی , بیا به این لینک \n http://127.0.0.1:9000/post?id={1} ".format(title, id),
        from_email= EMAIL_HOST_USER,
        recipient_list = ['ridod79996@tywmp.com',],
        fail_silently=False,
        )
