from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import Post, PostCategory


@receiver(m2m_changed, sender=PostCategory)
def product_created(instance, action, **kwargs):
    if action != 'post_add':
        return

    emails = []
    for cat in instance.category.all():
        emails.extend(User.objects.filter(
            subscriber__category=cat
        ).values_list('email', flat=True))
    subject = f'Новая статья в категории {instance.category}'

    text_content = (
        f'Статья: {instance.header}\n'
        f'Ссылка на статью: http://127.0.0.1{instance.get_absolute_url()}'
    )
    html_content = (
        f'Статья: {instance.header}<br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на статью</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
