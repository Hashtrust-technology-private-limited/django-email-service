import pytest
from django.core.files.base import ContentFile
from django.test import TestCase

from email_service.utils import send_custom_email


# Create your tests here.
class TestEmail(TestCase):
    @pytest.mark.django_db
    def setUp(self) -> None:
        self.recipients = ["testuser@gmail.com"]
        self.path = "users"
        self.template = None
        self.template_prefix = "user_welcome"
        self.context = {"username": "Test User"}
        self.subject = "Welcome to Hashtrust"
        self.body = "Welcome to Hashtrust"

    def test_empty_recipients(self):
        response = send_custom_email(
            recipient=[],
            path=self.path,
            template=self.template,
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
            template=self.template,
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
            template=self.template,
            template_prefix=None,
            context=self.context,
            subject=self.subject,
            body=None,
        )
        assert (
            response
            == "Please provide either path to html template or text body of email."
        )

    def test_invalid_email_selection(self):
        response = send_custom_email(
            recipient=self.recipients,
            path=self.path,
            template=self.template,
            template_prefix=None,
            context=self.context,
            subject=self.subject,
            body=None,
        )
        assert (
            response
            == "You can either send templated email or simple email at a time, not both."
        )

    def test_valid_email(self):
        files = [
            ContentFile(b"Hello World", name="file1.txt"),
            ContentFile(b"Hello Python", name="file2.txt"),
        ]
        response = send_custom_email(
            recipient=self.recipients,
            path=self.path,
            template=self.template,
            template_prefix=self.template_prefix,
            context=self.context,
            attachments=files,
            subject=None,
            body=None,
        )
        assert response == "Email Sent Successfully."
