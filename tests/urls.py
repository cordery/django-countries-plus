import django
from django.views.generic import TemplateView

if django.VERSION[0] == 2:
    from django.conf.urls import url

    urlpatterns = [
        url(r'^$', TemplateView.as_view(template_name='test.html'))
    ]
else:
    from django.urls import path
    urlpatterns = [
        path(r'', TemplateView.as_view(template_name='test.html'))
    ]
