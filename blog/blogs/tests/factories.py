import factory
from blog.models import Category
from faker import Faker

fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    title = fake.bothify(text="????????")
