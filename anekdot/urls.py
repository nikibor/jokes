from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

from joke import urls as joke_urls

schema_view = get_swagger_view(title='Jokes API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jokes/', include(joke_urls)),
    path('doc/', schema_view),
]
