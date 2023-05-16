import logging
import os
from typing import Dict, List

import html2text
from jinja2 import Template as JinjaTemplate

# from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from email.mime.image import MIMEImage
logger = logging.getLogger("emails")


def send_custom_email(
    recipient: List[str] | str,
    path: str | None = None,
    template: any = None,
    template_prefix: str | None = None,
    context: Dict = {},
    subject: str | None = None,
    body: str | None = None,
    attachment: any = None,
    attachment_path : str | None = None,
    enable_logo : bool = False
) -> None:
    from email_service.models import Email

    if not recipient or len(recipient) == 0:
        logger.error(
            "Please provide at least one recipient."
        )
        return "Please provide at least one recipient."
    if (path or template_prefix) and (subject or body):
        return "You can either send templated email or simple email at a time, not both."
    if not ((path and template_prefix) or subject):
        logger.error(
            "Please provide either path to html template or text subject of email."
        )
        return "Please provide either path to html template or text subject of email."

    if not ((path and template_prefix) or body):
        logger.error(
            "Please provide either path to html template or text body of email."
        )
        return "Please provide either path to html template or text body of email."

    try:
        from_email = settings.EMAIL_FROM
        to = recipient if isinstance(recipient, list) else [recipient]
        bcc_email = settings.EMAIL_BCC

        if template:
            email_subject = JinjaTemplate(template.subject).render(context)
            html_content = JinjaTemplate(template.body).render(context)

        else:
            subject_file = f"{path}/{template_prefix}_subject.txt" if path else f"{template_prefix}_subject.txt"
            html_file = f"{path}/{template_prefix}.html" if path else f"{template_prefix}.html"
            email_subject = render_to_string(subject_file).strip() if template_prefix and path else subject
            html_content = render_to_string(html_file, context) if template_prefix and path else body

        Email.objects.create(
            subject=email_subject,
            body=html_content,
            recipients=recipient,
            from_user=from_email,
            template=template,
        )
        text_content = html2text.HTML2Text().handle(html_content)
        msg = EmailMultiAlternatives(
            subject or email_subject, text_content, from_email, to, bcc=[bcc_email]
        )
        msg.attach_alternative(html_content, "text/html")

        if attachment_path:
            msg.attach_file(f"{settings.BASE_DIR}/{attachment_path}")

        if attachment:
            msg.attach_file(f"{settings.BASE_DIR}/{attachment.url}")
        
        if enable_logo:
            msg.content_subtype = 'html'
            msg.mixed_subtype = 'related'
            image_path = os.path.join(settings.BASE_DIR, f'static/{settings.LOGO_IMAGE_NAME}')
            with open(image_path, 'rb') as banner_image:
                banner_image = MIMEImage(banner_image.read())
                banner_image.add_header('Content-ID', f'<{settings.LOGO_IMAGE_NAME}>')
                msg.attach(banner_image)
        msg.send()
        return "Email Sent Successfully."
    except Exception as ex:
        logger.exception(
            f"""Caught exception {ex} while sending email with params:
            path-{path} template-{template_prefix}, recipient-{recipient},
            context-{context}, subject-{subject}, body-{body}"""
        )
