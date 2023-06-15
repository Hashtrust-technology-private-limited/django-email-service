import random

import factory
import factory.fuzzy

from email_service.models import Template


class TemplateFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    subject = factory.fuzzy.FuzzyText(length=50)
    body = factory.fuzzy.FuzzyText(length=50)
    template_type = random.choice([0, 1, 2, 3, 4, 5, 6])

    class Meta:
        model = Template
