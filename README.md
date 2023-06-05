# django-mails

django-mails is Django App to send simple or HTML template Emails by calling just hit of single function.

Quick Start
-----------
1. Add 'email_service' to your INSTALLED_APPS setting like this::
    ```
    INSTALLED_APPS = [
        ...
        'email_service',
        'ckeditor',
    ]
    ```
2. Run ``python manage.py migrate`` to create the django-mails models.
3. Set Email Settings in setting.py file
    ```
    EMAIL_FROM = ""
    EMAIL_BCC = ""
    EMAIL_HOST = ""
    EMAIL_PORT = ""
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False
    ```
4. Add Templates path to your TEMPLATES in setting.py
5. import method to send email ``from email_service.utils import send_custom_email``
6. set ``LOGO_IMAGE_NAME`` variable in setting.py file to add logo in email (Name should include subfolder inside static folder)

Description
-----------
```
send_custom_email(
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
)
```
* recipient : List of Receivers emails
* path : path to email html template under templates folder
* template : Object of Template Model if exists (Optional)
* template_prefix : html file name
* context : context to replace variable name in template
* subject : subject of email
* attachment: attach file to send email as attachement
* attachment_path : send string path of attachment,
* enable_logo : set true to enable logo in email


# Setup guideline

- build: Create the build and runtime images
```
    docker-compose build
```

- up: Start up the project
```
    docker-compose up
```
- To see services and their ports
```
    docker ps
```
- shell: Shell into the running Django container
```
    docker exec -it CONTAINER ID /bin/bash
```
- migrate: Changes you have made to your models
```
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
```
