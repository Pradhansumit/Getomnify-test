from django.urls import path

from api.views import HelloWorldView

urlpatterns = [
    path("hello-world/", HelloWorldView.as_view(), name="hello-world"),
]
