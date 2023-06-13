import pytest
from django.conf import settings
from django.core.files.base import ContentFile
from django.test import TestCase

from email_service.utils import send_custom_email
from tests.factories import TemplateFactory


# Create your tests here.
@pytest.mark.django_db
class TestEmail(TestCase):
    def setUp(self) -> None:
        self.recipients = ["testuser@gmail.com"]
        self.path = "users"
        self.template = TemplateFactory()
        self.template_prefix = "user_welcome"
        self.context = {"username": "Test User"}
        self.subject = "Welcome to Hashtrust"
        self.body = "Welcome to Hashtrust"
        self.files = [
            ContentFile(b"Hello World", name="file1.txt"),
            ContentFile(b"Hello Python", name="file2.txt"),
        ]

    def test_empty_recipients(self):
        response = send_custom_email(
            recipient=[],
            path=self.path,
            template_prefix=self.template_prefix,
            context=self.context,
            subject=self.subject,
            body=self.body,
        )
        assert response == "Please provide at least one recipient."

    def test_empty_subject_or_templatepath(self):
        response = send_custom_email(
            recipient=self.recipients,
            path=None,
            template_prefix=None,
            context=self.context,
            subject=None,
            body=self.body,
        )
        assert (
            response
            == "Please provide either path to html template or text subject of email."
        )

    def test_empty_body_or_templatepath(self):
        response = send_custom_email(
            recipient=self.recipients,
            path=None,
            template_prefix=None,
            context=self.context,
            subject=self.subject,
            body=None,
        )
        assert (
            response
            == "Please provide either path to html template or text body of email."
        )

    def test_invalid_template_file(self):
        template_prefix = "user_login"
        response = send_custom_email(
            recipient=self.recipients,
            path=self.path,
            template_prefix=template_prefix,
            context=self.context,
        )
        assert (
            response
            == f"Email template file or subject file not exists for prefix {template_prefix}"
        )

    def test_valid_simple_email(self):
        response = send_custom_email(
            recipient=self.recipients,
            subject="This is sample email",
            body="Hello world",
        )
        assert response == "Email Sent Successfully."

    def test_valid_html_email(self):
        response = send_custom_email(
            recipient=self.recipients,
            path=self.path,
            template_prefix=self.template_prefix,
            context=self.context,
        )
        assert response == "Email Sent Successfully."

    def test_valid_email_with_attachement(self):
        response = send_custom_email(
            recipient=self.recipients,
            path=self.path,
            template_prefix=self.template_prefix,
            context=self.context,
            attachments=self.files,
        )
        assert response == "Email Sent Successfully."

    def test_email_with_attachement_path(self):
        with open(f"{settings.MEDIA_ROOT}/sample_file.txt", "w") as file:
            file.write("Sample File")
        response = send_custom_email(
            recipient=self.recipients,
            path=self.path,
            template_prefix=self.template_prefix,
            context=self.context,
            attachment_path="media/sample_file.txt",
        )
        assert response == "Email Sent Successfully."

    def test_email_with_logo(self):
        response = send_custom_email(
            recipient=self.recipients,
            path=self.path,
            template_prefix=self.template_prefix,
            context=self.context,
            enable_logo=True,
        )
        assert response == "Email Sent Successfully."

    def test_email_with_template_model_content(self):
        response = send_custom_email(
            recipient=self.recipients,
            path=self.path,
            template=self.template,
            context=self.context,
            attachments=self.files,
        )
        assert response == "Email Sent Successfully."
