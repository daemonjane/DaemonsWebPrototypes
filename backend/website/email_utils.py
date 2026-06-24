from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_contact_auto_reply(contact_message):
    subject = "Thank you for contacting TechStore"
    context = {"message": contact_message}
    html_message = render_to_string("website/emails/contact_auto_reply.html", context)
    plain_message = render_to_string("website/emails/contact_auto_reply.txt", context)
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[contact_message.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_subscription_confirmation(subscription):
    subject = "Welcome to the TechStore newsletter"
    context = {"subscription": subscription}
    html_message = render_to_string("website/emails/subscription_confirmation.html", context)
    plain_message = render_to_string("website/emails/subscription_confirmation.txt", context)
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[subscription.email],
        html_message=html_message,
        fail_silently=False,
    )
