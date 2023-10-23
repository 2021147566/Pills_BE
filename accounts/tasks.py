# users/tasks.py

from typing import List

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def test_task(a: int, b: int):
    print("test Celery task : ", a + b)
    return a + b

@shared_task
def send_verification_email(user_id, verification_url, recipient_email):
    subject = '이메일 확인 링크'
    message = f'이메일 확인을 완료하려면 다음 링크를 클릭하세요: {verification_url}'
    from_email = 'tkdcks7@gmail.com'
    
    send_mail(subject, message, from_email, [recipient_email])