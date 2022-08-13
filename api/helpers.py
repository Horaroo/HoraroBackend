from django.core.mail import send_mail, EmailMessage


def send_message_to_mail(to_email):
    m = EmailMessage(
        subject='Subject',
        from_email='abulaysovv@mail.ru',
        to=[to_email],
    )
    m.send()
