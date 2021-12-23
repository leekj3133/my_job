from django.urls import path

from . import views
from jobapp.views import hello_job

app_name = "jobapp"

urlpatterns = [
    path('', hello_job, name="hello_job"),
]