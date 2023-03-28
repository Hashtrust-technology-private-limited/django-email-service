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

logger = logging.getLogger("emails")

email_variables = {
    "first_name": "",
    "challenge_name": "",
    "challenge_image": "",
    "weight_to_lose": "",
    "duration": "",
    "product_name": settings.PRODUCT_NAME,
    "support_email_address": settings.EMAIL_FROM,
}


def send_custom_email(
    recipient: List[str] | str,
    path: str | None = None,
    template: any = None,
    template_prefix: str | None = None,
    context: Dict = {},
    subject: str | None = None,
    body: str | None = None,
) -> None:
    from email_service.models import Email

    if (
        not recipient
        or not ((path and template_prefix) or subject)
        or not (path and template_prefix or body)
    ):
        return
    try:
        from_email = settings.EMAIL_FROM
        to = recipient if isinstance(recipient, list) else [recipient]
        bcc_email = settings.EMAIL_BCC

        if template:
            email_variables.update(context)

            email_subject = JinjaTemplate(template.subject).render(email_variables)
            html_content = JinjaTemplate(template.body).render(email_variables)

        else:
            subject_file = f"{path}/{template_prefix}_subject.txt"
            html_file = f"{path}/{template_prefix}.html"
            email_subject = render_to_string(subject_file).strip()
            html_content = render_to_string(body or html_file, context)

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
        print(msg)
        msg.attach_alternative(html_content, "text/html")
        sms_response = msg.send()
        print(sms_response)
    except Exception as ex:
        logger.exception(
            f"""Caught exception {ex} while sending email with params:
            path-{path} template-{template_prefix}, recipient-{recipient},
            context-{context}, subject-{subject}, body-{body}"""
        )
