import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
# from django.urls import reverse

from blog.serializers import PostSerializer
# from blog.models import Posts


def test_image(name="media/posts/1.png", size=(250, 250)):
    with open(name, mode="rb") as content:
        return SimpleUploadedFile(name, content=content.read())


@pytest.fixture
def post_create_serializer(request, category_factory):
    image = test_image()
    data = {
        "complete_data": (
            True, {
                "title": "Garry Poter",
                "image": image,
                "description": "asdad",
                "category": {"title": "Iqtisod"},
                "tags": [{"title": "Qui eligendi eum voluptatem ut libero nisi et ut dolore quis cupidatat amet velit reprehenderit"}],
                "author": {"username": "xe"}
            }
        )
    }
    return data[request.param]


def test_db_access(django_db_blocker):
    with django_db_blocker.unblock():
        assert True


@pytest.mark.django_db
@pytest.mark.parametrize("post_create_serializer", ['complete_data'], indirect=True)
def test_post_create_serializer(post_create_serializer):
    validity, data = post_create_serializer
    serializer = PostSerializer(data=data)
    assert serializer.is_valid() == validity
