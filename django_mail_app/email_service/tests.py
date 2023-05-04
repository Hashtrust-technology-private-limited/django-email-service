from django.test import TestCase
from email_service.utils import send_custom_email
# Create your tests here.
class TestEmail(TestCase):

    def setUp(self) -> None:
        self.recipients = ['harsh@hashtrust.in']
        self.path = "users"
        self.template = None
        self.template_prefix = 'user_welcome'
        self.context = {"username":"Test User"}
        self.subject = "Welcome to Hashtrust"
        self.body = "Welcome to Hashtrust"

    def test_empty_recipients(self):
        response = send_custom_email(
            recipient= [],
            path = self.path,
            template = self.template,
            template_prefix = self.template_prefix,
            context = self.context,
            subject = self.subject,
            body = self.body
        )
        assert response == "Please provide at least one recipient."
    
    def test_empty_subject_or_templatepath(self):
        response = send_custom_email(
            recipient= self.recipients,
            path = None,
            template = self.template,
            template_prefix = None,
            context = self.context,
            subject = None,
            body = self.body
        )
        assert response == "Please provide either path to html template or text subject of email."
    
    def test_empty_body_or_templatepath(self):
        response = send_custom_email(
            recipient= self.recipients,
            path = None,
            template = self.template,
            template_prefix = None,
            context = self.context,
            subject = self.subject,
            body = None
        )
        assert response == "Please provide either path to html template or text body of email."
    
    def test_invalid_email_selection(self):
        response = send_custom_email(
            recipient= self.recipients,
            path = self.path,
            template = self.template,
            template_prefix = None,
            context = self.context,
            subject = self.subject,
            body = None
        )
        print(response)
        assert response == "You can either send templated email or simple email at a time, not both."

    def test_valid_email(self):
        response = send_custom_email(
            recipient= self.recipients,
            path = self.path,
            template = self.template,
            template_prefix = self.template_prefix,
            context = self.context,
            subject = None,
            body = None
        )
        assert response == "Email Sent Successfully."
